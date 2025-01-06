"""SSL certificate management for CLIDB."""
import subprocess
import os
import socket
from pathlib import Path
from typing import Optional, List, Tuple
import docker
import time

class SSLManager:
    def __init__(self):
        self.docker_client = docker.from_env()

    def verify_domain(self, domain: str) -> Tuple[bool, str]:
        """Verify domain points to current server."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            server_ip = s.getsockname()[0]
            s.close()

            domain_ip = socket.gethostbyname(domain)
            if domain_ip == server_ip:
                return True, "Domain verification successful"
            return False, f"Domain {domain} points to {domain_ip}, but server IP is {server_ip}"
        except Exception as e:
            return False, f"Domain verification failed: {str(e)}"

    def setup_nginx(self) -> Tuple[bool, str]:
        """Install and configure Nginx."""
        try:
            # Install Nginx
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "nginx"], check=True)

            # Stop any running Nginx
            subprocess.run(["systemctl", "stop", "nginx"], check=False)

            nginx_root = Path("/etc/nginx")
            for d in ["sites-available", "sites-enabled"]:
                dir_path = nginx_root / d
                if dir_path.exists():
                    for f in dir_path.iterdir():
                        f.unlink()
                else:
                    dir_path.mkdir(parents=True)

            nginx_conf = """
            user www-data;
            worker_processes auto;
            pid /run/nginx.pid;

            events {
                worker_connections 768;
            }

            http {
                sendfile on;
                tcp_nopush on;
                types_hash_max_size 2048;
                server_names_hash_bucket_size 64;

                include /etc/nginx/mime.types;
                default_type application/octet-stream;

                access_log /var/log/nginx/access.log;
                error_log /var/log/nginx/error.log;

                include /etc/nginx/conf.d/*.conf;
                include /etc/nginx/sites-enabled/*;
            }
            """
            (nginx_root / "nginx.conf").write_text(nginx_conf)

            default_conf = """
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 404;
}
"""
            (nginx_root / "sites-available/default").write_text(default_conf)
            default_link = nginx_root / "sites-enabled/default"
            if default_link.exists():
                default_link.unlink()
            default_link.symlink_to(nginx_root / "sites-available/default")

            result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)
            if result.returncode != 0:
                return False, f"Invalid Nginx config: {result.stderr}"

            subprocess.run(["systemctl", "start", "nginx"], check=True)
            time.sleep(2)  # Give Nginx time to start

            return True, "Nginx configured successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to setup Nginx: {e.stderr if e.stderr else str(e)}"
        except Exception as e:
            return False, f"Failed to setup Nginx: {str(e)}"

    def setup_certbot(self) -> Tuple[bool, str]:
        """Install and configure Certbot."""
        try:
            subprocess.run(["apt-get", "install", "-y", "certbot", "python3-certbot-nginx"], check=True)
            return True, "Certbot installed successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to install Certbot: {e.stderr if e.stderr else str(e)}"
        except Exception as e:
            return False, f"Failed to install Certbot: {str(e)}"

    def configure_site(self, domain: str, port: int) -> Tuple[bool, str]:
        """Configure Nginx site for domain."""
        try:
            config = f"""
server {{
    listen 80;
    listen [::]:80;
    server_name {domain};

    location / {{
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
            sites_available = Path("/etc/nginx/sites-available")
            sites_enabled = Path("/etc/nginx/sites-enabled")

            # Write config
            config_file = sites_available / domain
            config_file.write_text(config)

            # Create symlink
            link_file = sites_enabled / domain
            if link_file.exists():
                link_file.unlink()
            link_file.symlink_to(config_file)

            # Test config
            result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)
            if result.returncode != 0:
                return False, f"Invalid site config: {result.stderr}"

            # Reload Nginx
            subprocess.run(["systemctl", "reload", "nginx"], check=True)
            return True, "Site configured successfully"
        except Exception as e:
            return False, f"Failed to configure site: {str(e)}"

    def setup_ssl(self, domain: str, email: str, db_type: str, port: int, container_name: str) -> Tuple[bool, str]:
        """Setup SSL for a database."""
        try:
            # Verify domain
            success, message = self.verify_domain(domain)
            if not success:
                return False, message

            # Setup Nginx
            success, message = self.setup_nginx()
            if not success:
                return False, message

            # Setup Certbot
            success, message = self.setup_certbot()
            if not success:
                return False, message

            # Configure site
            success, message = self.configure_site(domain, port)
            if not success:
                return False, message

            # Run Certbot
            cmd = [
                "certbot", "--nginx",
                "-d", domain,
                "--email", email,
                "--agree-tos",
                "--non-interactive",
                "--redirect"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False, f"Certbot failed: {result.stderr}"

            # Configure PostgreSQL SSL if needed
            if db_type == 'postgres':
                try:
                    container = self.docker_client.containers.get(container_name)
                    cert_path = f"/etc/letsencrypt/live/{domain}"
                    
                    # Create SSL directory in container
                    container.exec_run("mkdir -p /var/lib/postgresql/ssl")
                    
                    # Copy certificates
                    with open(f"{cert_path}/fullchain.pem", 'rb') as f:
                        container.put_archive("/var/lib/postgresql/ssl", f.read())
                    with open(f"{cert_path}/privkey.pem", 'rb') as f:
                        container.put_archive("/var/lib/postgresql/ssl", f.read())
                    
                    # Configure PostgreSQL
                    container.exec_run("chown -R postgres:postgres /var/lib/postgresql/ssl")
                    container.exec_run("chmod 600 /var/lib/postgresql/ssl/privkey.pem")
                    
                    # Add SSL configuration
                    ssl_conf = """
ssl = on
ssl_cert_file = '/var/lib/postgresql/ssl/fullchain.pem'
ssl_key_file = '/var/lib/postgresql/ssl/privkey.pem'
"""
                    container.exec_run(f'bash -c "echo \'{ssl_conf}\' >> /var/lib/postgresql/data/postgresql.conf"')
                    
                    # Restart container
                    container.restart()
                except Exception as e:
                    return False, f"Failed to configure PostgreSQL SSL: {str(e)}"

            return True, "SSL setup completed successfully"
        except Exception as e:
            return False, f"SSL setup failed: {str(e)}"

    def remove_ssl(self, domain: str) -> Tuple[bool, str]:
        """Remove SSL configuration."""
        try:
            # Remove Certbot configuration
            subprocess.run(["certbot", "delete", "--cert-name", domain, "--non-interactive"], check=False)

            # Remove Nginx configuration
            for path in [f"/etc/nginx/sites-available/{domain}", f"/etc/nginx/sites-enabled/{domain}"]:
                if os.path.exists(path):
                    os.unlink(path)

            # Reload Nginx
            subprocess.run(["systemctl", "reload", "nginx"], check=True)
            return True, "SSL removed successfully"
        except Exception as e:
            return False, f"Failed to remove SSL: {str(e)}"

ssl_manager = SSLManager() 
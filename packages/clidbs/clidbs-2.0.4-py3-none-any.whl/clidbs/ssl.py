"""SSL certificate management for CLIDB."""
import subprocess
import os
import socket
from pathlib import Path
from typing import Optional, List, Tuple
import docker
import shutil

def check_port_in_use(port: int) -> Tuple[bool, Optional[str], Optional[List[int]]]:
    """Check if a port is in use and what's using it."""
    try:
        # Try to get process using port 80
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Try to extract PIDs
            pids = []
            for line in result.stdout.splitlines()[1:]:  # Skip header
                parts = line.split()
                if len(parts) > 1:
                    try:
                        pids.append(int(parts[1]))
                    except ValueError:
                        pass
            return True, result.stdout, pids
        return False, None, None
    except:
        # If lsof isn't available, try netstat
        try:
            result = subprocess.run(
                ["netstat", "-tulpn"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, result.stdout, None
        except:
            pass
        return False, None, None

class SSLManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "clidb" / "ssl"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.nginx_dir = self.config_dir / "nginx"
        self.nginx_dir.mkdir(exist_ok=True)
        self.docker_client = docker.from_env()

    def find_containers_using_port(self, port: int) -> List[docker.models.containers.Container]:
        """Find Docker containers using a specific port."""
        containers = []
        for container in self.docker_client.containers.list():
            ports = container.attrs['NetworkSettings']['Ports']
            for container_port, host_bindings in ports.items():
                if host_bindings:
                    for binding in host_bindings:
                        if binding['HostPort'] == str(port):
                            containers.append(container)
        return containers

    def stop_containers_using_port(self, port: int) -> Tuple[bool, str]:
        """Stop Docker containers using a specific port."""
        try:
            containers = self.find_containers_using_port(port)
            if not containers:
                return True, "No containers using port 80"

            for container in containers:
                container.stop()
                print(f"Stopped container {container.name} using port {port}")
            
            return True, f"Stopped {len(containers)} containers using port {port}"
        except Exception as e:
            return False, f"Failed to stop containers: {str(e)}"

    def setup_postgres_ssl(self, container_name: str) -> Tuple[bool, str]:
        """Configure PostgreSQL container for SSL support."""
        try:
            # Create SSL directory in container
            container = self.docker_client.containers.get(container_name)
            
            # Copy SSL certificate and key to container
            cert_path = "/etc/letsencrypt/live"
            domains = os.listdir(cert_path)
            if not domains:
                return False, "No SSL certificates found"
            
            domain = domains[0]  # Use first domain's certificates
            
            # Create a temporary directory for PostgreSQL SSL files
            ssl_dir = self.config_dir / "postgres_ssl"
            ssl_dir.mkdir(exist_ok=True)
            
            # Copy and rename SSL files
            shutil.copy(f"{cert_path}/{domain}/fullchain.pem", str(ssl_dir / "server.crt"))
            shutil.copy(f"{cert_path}/{domain}/privkey.pem", str(ssl_dir / "server.key"))
            
            # Set correct permissions
            os.chmod(str(ssl_dir / "server.key"), 0o600)
            os.chmod(str(ssl_dir / "server.crt"), 0o644)
            
            # Create postgresql.conf additions
            ssl_conf = """
ssl = on
ssl_cert_file = '/var/lib/postgresql/ssl/server.crt'
ssl_key_file = '/var/lib/postgresql/ssl/server.key'
"""
            (ssl_dir / "ssl.conf").write_text(ssl_conf)
            
            # Copy files to container
            container.exec_run("mkdir -p /var/lib/postgresql/ssl")
            for file in ["server.crt", "server.key", "ssl.conf"]:
                with open(str(ssl_dir / file), 'rb') as f:
                    container.put_archive("/var/lib/postgresql/ssl", f.read())
            
            # Update PostgreSQL configuration
            container.exec_run("chown -R postgres:postgres /var/lib/postgresql/ssl")
            container.exec_run("chmod 600 /var/lib/postgresql/ssl/server.key")
            container.exec_run("cat /var/lib/postgresql/ssl/ssl.conf >> /var/lib/postgresql/data/postgresql.conf")
            
            # Restart container to apply changes
            container.restart()
            
            return True, "PostgreSQL SSL configuration updated successfully"
            
        except Exception as e:
            return False, f"Failed to configure PostgreSQL SSL: {str(e)}"

    def verify_domain(self, domain: str) -> Tuple[bool, str]:
        """Verify domain points to current server."""
        try:
            # Get server's public IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            server_ip = s.getsockname()[0]
            s.close()

            # Get domain's IP
            domain_ip = socket.gethostbyname(domain)

            if domain_ip == server_ip:
                return True, "Domain verification successful"
            else:
                return False, f"Domain {domain} points to {domain_ip}, but server IP is {server_ip}"
        except Exception as e:
            return False, f"Domain verification failed: {str(e)}"

    def check_certbot(self) -> bool:
        """Check if certbot is installed."""
        try:
            subprocess.run(["certbot", "--version"], 
                         capture_output=True, 
                         check=True)
            return True
        except:
            return False

    def stop_nginx(self):
        """Stop nginx if it's running."""
        try:
            subprocess.run(["systemctl", "stop", "nginx"], check=True)
        except:
            pass

    def check_and_fix_nginx(self) -> Tuple[bool, str]:
        """Check Nginx status and try to fix any issues."""
        try:
            # Check if port 80 is in use
            in_use, details, pids = check_port_in_use(80)
            if in_use:
                # Check for Docker containers using port 80
                success, message = self.stop_containers_using_port(80)
                if not success:
                    return False, message
                
                # Try to stop nginx
                self.stop_nginx()
                
                # Check again
                in_use, details, pids = check_port_in_use(80)
                if in_use:
                    return False, f"Port 80 is still in use by another process:\n{details}"

            # Try to start nginx
            result = subprocess.run(
                ["systemctl", "start", "nginx"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Get more detailed error
                status = subprocess.run(
                    ["systemctl", "status", "nginx"],
                    capture_output=True,
                    text=True
                )
                return False, f"Failed to start Nginx:\n{status.stdout}\n{status.stderr}"

            return True, "Nginx started successfully"
        except Exception as e:
            return False, f"Error checking Nginx: {str(e)}"

    def install_certbot(self) -> Tuple[bool, str]:
        """Install certbot if not present."""
        try:
            # Try to detect package manager
            if os.path.exists("/usr/bin/apt"):
                # Run apt-get update first
                update_cmd = ["apt-get", "update"]
                subprocess.run(update_cmd, check=True)
                
                # Then install certbot
                install_cmd = ["apt-get", "install", "-y", "certbot", "python3-certbot-nginx", "nginx"]
                subprocess.run(install_cmd, check=True)
                
            elif os.path.exists("/usr/bin/dnf"):
                install_cmd = ["dnf", "install", "-y", "certbot", "python3-certbot-nginx", "nginx"]
                subprocess.run(install_cmd, check=True)
                
            elif os.path.exists("/usr/bin/yum"):
                install_cmd = ["yum", "install", "-y", "certbot", "python3-certbot-nginx", "nginx"]
                subprocess.run(install_cmd, check=True)
                
            else:
                return False, "Could not detect package manager"

            # Check and fix nginx
            success, message = self.check_and_fix_nginx()
            if not success:
                return False, message

            return True, "Certbot and Nginx installed successfully"
            
        except subprocess.CalledProcessError as e:
            return False, f"Package installation failed: {str(e)}"
        except Exception as e:
            return False, f"Failed to install certbot: {str(e)}"

    def generate_nginx_config(self, domain: str, db_type: str, port: int) -> str:
        """Generate Nginx configuration for database."""
        config = f"""
server {{
    listen 80;
    server_name {domain};

    location / {{
        proxy_pass http://localhost:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
        config_path = Path("/etc/nginx/sites-available") / domain
        config_path.write_text(config)
        
        # Create symlink in sites-enabled
        enabled_path = Path("/etc/nginx/sites-enabled") / domain
        if enabled_path.exists():
            enabled_path.unlink()
        enabled_path.symlink_to(config_path)
        
        # Test and reload nginx
        subprocess.run(["nginx", "-t"], check=True)
        subprocess.run(["systemctl", "reload", "nginx"], check=True)
        
        return str(config_path)

    def setup_ssl(self, domain: str, email: str, db_type: str, port: int, container_name: str) -> Tuple[bool, str]:
        """Setup SSL for a database."""
        try:
            # Verify domain first
            domain_ok, msg = self.verify_domain(domain)
            if not domain_ok:
                return False, msg

            # Check/install certbot
            if not self.check_certbot():
                success, msg = self.install_certbot()
                if not success:
                    return False, msg

            # Check nginx status
            success, message = self.check_and_fix_nginx()
            if not success:
                return False, message

            # Generate nginx config
            nginx_conf = self.generate_nginx_config(domain, db_type, port)

            # Run certbot
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
                success, message = self.setup_postgres_ssl(container_name)
                if not success:
                    return False, message

            return True, "SSL certificate installed successfully"

        except Exception as e:
            return False, f"SSL setup failed: {str(e)}"

    def remove_ssl(self, domain: str) -> Tuple[bool, str]:
        """Remove SSL certificate and nginx config."""
        try:
            # Remove nginx config
            config_path = Path("/etc/nginx/sites-available") / domain
            enabled_path = Path("/etc/nginx/sites-enabled") / domain
            
            if config_path.exists():
                config_path.unlink()
            if enabled_path.exists():
                enabled_path.unlink()

            # Remove certificate
            cmd = ["certbot", "delete", "--cert-name", domain, "--non-interactive"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Reload nginx
            subprocess.run(["systemctl", "reload", "nginx"], check=True)
            
            if result.returncode == 0:
                return True, "SSL certificate removed successfully"
            else:
                return False, f"Failed to remove certificate: {result.stderr}"

        except Exception as e:
            return False, f"Failed to remove SSL: {str(e)}"

# Initialize SSL manager as singleton
ssl_manager = SSLManager() 
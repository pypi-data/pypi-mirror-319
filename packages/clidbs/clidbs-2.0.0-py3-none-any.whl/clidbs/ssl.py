"""SSL certificate management for CLIDB."""
import subprocess
import os
from pathlib import Path
from typing import Optional, List, Tuple
import socket
from .style import print_warning, print_error, print_success

class SSLManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "clidb" / "ssl"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.nginx_dir = self.config_dir / "nginx"
        self.nginx_dir.mkdir(exist_ok=True)

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

    def install_certbot(self) -> bool:
        """Install certbot if not present."""
        try:
            # Try to detect package manager
            if os.path.exists("/usr/bin/apt"):
                cmd = "apt-get update && apt-get install -y certbot python3-certbot-nginx"
            elif os.path.exists("/usr/bin/dnf"):
                cmd = "dnf install -y certbot python3-certbot-nginx"
            elif os.path.exists("/usr/bin/yum"):
                cmd = "yum install -y certbot python3-certbot-nginx"
            else:
                return False, "Could not detect package manager"

            subprocess.run(cmd.split(), check=True)
            return True, "Certbot installed successfully"
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
        config_path = self.nginx_dir / f"{domain}.conf"
        config_path.write_text(config)
        return str(config_path)

    def setup_ssl(self, domain: str, email: str, db_type: str, port: int) -> Tuple[bool, str]:
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
            
            if result.returncode == 0:
                return True, "SSL certificate installed successfully"
            else:
                return False, f"Certbot failed: {result.stderr}"

        except Exception as e:
            return False, f"SSL setup failed: {str(e)}"

    def remove_ssl(self, domain: str) -> Tuple[bool, str]:
        """Remove SSL certificate and nginx config."""
        try:
            # Remove nginx config
            config_path = self.nginx_dir / f"{domain}.conf"
            if config_path.exists():
                config_path.unlink()

            # Remove certificate
            cmd = ["certbot", "delete", "--cert-name", domain]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "SSL certificate removed successfully"
            else:
                return False, f"Failed to remove certificate: {result.stderr}"

        except Exception as e:
            return False, f"Failed to remove SSL: {str(e)}"

# Initialize SSL manager as singleton
ssl_manager = SSLManager() 
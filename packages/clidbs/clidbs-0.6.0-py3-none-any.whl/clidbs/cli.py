import click
import docker
import os
import secrets
import string
import socket
from typing import Optional, List
from .notifications import send_discord_notification
from .config import Config
from .databases import (
    get_database_config, 
    list_supported_databases, 
    DATABASES, 
    DatabaseCredentials,
    credentials_manager
)

def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_container_name(db_type: str, db_name: str) -> str:
    """Convert db_name to full container name."""
    return f"clidb-{db_type}-{db_name}"

def find_container(client: docker.DockerClient, db_name: str) -> Optional[docker.models.containers.Container]:
    """Find a container by database name."""
    containers = client.containers.list(all=True)
    for container in containers:
        # Split container name into parts
        parts = container.name.split('-')
        # Check if it's our container (starts with clidb- and ends with db_name)
        if len(parts) >= 3 and parts[0] == "clidb" and '-'.join(parts[2:]) == db_name:
            return container
    return None

def get_db_info(container_name: str) -> tuple:
    """Extract db_name and type from container name."""
    parts = container_name.split('-')
    if len(parts) >= 3 and parts[0] == "clidb":
        db_type = parts[1]
        db_name = '-'.join(parts[2:])
        return db_name, db_type
    return None, None

def get_host_ip() -> str:
    """Get the host's public IP address."""
    # First try to get the IP from environment variable
    if os.getenv("CLIDB_HOST_IP"):
        return os.getenv("CLIDB_HOST_IP")
    
    try:
        # Try to get the host's IP by creating a dummy connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def get_connection_string(db_type: str, host: str, port: int, user: str, password: str, db_name: str) -> str:
    """Generate a connection string based on database type."""
    if db_type == 'postgres':
        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    elif db_type == 'mysql' or db_type == 'mariadb':
        return f"mysql://{user}:{password}@{host}:{port}/{db_name}"
    elif db_type == 'mongo':
        return f"mongodb://{user}:{password}@{host}:{port}/{db_name}"
    elif db_type == 'redis':
        return f"redis://:{password}@{host}:{port}"
    elif db_type == 'neo4j':
        return f"neo4j://{user}:{password}@{host}:{port}"
    return ""

def get_cli_command(db_type: str, host: str, port: int, user: str, password: str, db_name: str) -> str:
    """Generate CLI command based on database type."""
    if db_type == 'postgres':
        return f"psql -h {host} -p {port} -U {user} -d {db_name}  # Password: {password}"
    elif db_type == 'mysql' or db_type == 'mariadb':
        return f"mysql -h {host} -P {port} -u {user} -p{password} {db_name}"
    elif db_type == 'mongo':
        return f"mongosh {host}:{port}/{db_name} -u {user} -p {password}"
    elif db_type == 'redis':
        return f"redis-cli -h {host} -p {port} -a {password}"
    elif db_type == 'neo4j':
        return f"cypher-shell -a {host}:{port} -u {user} -p {password}"
    return ""

@click.group()
def main():
    """Simple database management for your VPS."""
    pass

@main.command()
@click.argument('db_name')
@click.option('--type', 'db_type', type=click.Choice(list(DATABASES.keys())), default='postgres', help='Database type')
@click.option('--version', help='Database version')
@click.option('--access', type=click.Choice(['public', 'private']), default='public', help='Access type')
@click.option('--user', help='Database user to create')
@click.option('--port', type=int, help='Port to expose the database on')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def create(db_name: str, db_type: str, version: Optional[str], access: str, user: str, 
          port: Optional[int], discord_webhook: Optional[str]):
    """Create a new database.
    
    Example: clidb create mydb --type postgres --version 16
    """
    try:
        client = docker.from_env()
        
        # Get database configuration
        db_config = get_database_config(db_type, version)
        
        # Use db_name as user if not specified
        if not user:
            user = db_name
            
        # Use default port if not specified
        if not port:
            port = db_config.default_port
        
        # Generate secure password
        password = generate_password()
        
        # Prepare environment variables
        environment = db_config.get_env_vars(db_name, user, password)
        
        # Configure ports
        ports = {f'{db_config.default_port}/tcp': port}
        
        # Configure network mode based on access type
        network_mode = 'bridge' if access == 'public' else 'host'
        
        # Prepare container configuration
        container_config = {
            'image': db_config.image,
            'name': get_container_name(db_type, db_name),
            'environment': environment,
            'ports': ports,
            'network_mode': network_mode,
            'detach': True
        }
        
        # Add optional configurations
        if db_config.volumes:
            container_config['volumes'] = db_config.volumes
        if db_config.command:
            container_config['command'] = db_config.command
        
        # Create and start container
        container = client.containers.run(**container_config)
        
        # Get the appropriate host
        host = get_host_ip() if access == 'public' else 'localhost'
        
        # Store credentials
        creds = DatabaseCredentials(
            db_type=db_type,
            version=version,
            user=user,
            password=password,
            port=port,
            host=host,
            access=access,
            name=db_name
        )
        credentials_manager.store_credentials(creds)
        
        # Generate connection details
        conn_string = get_connection_string(db_type, host, port, user, password, db_name)
        cli_command = get_cli_command(db_type, host, port, user, password, db_name)
        
        success_message = f"""
Database '{db_name}' created successfully!
Type: {db_config.name}
Version: {version or 'latest'}
Access: {access.upper()}
Host: {host}
Port: {port}
User: {user}
Password: {password}

Connection String (copy/paste ready):
{conn_string}

CLI Command:
{cli_command}

Tip: Use 'clidb info {db_name}' to see these details again.
"""
        click.echo(success_message)
        
        if discord_webhook:
            # Don't send sensitive info to Discord
            safe_message = f"""Database '{db_name}' ({db_config.name} {version or 'latest'}) created successfully!
Type: {db_config.name}
Host: {host}
Port: {port}"""
            send_discord_notification(
                webhook_url=discord_webhook,
                message=safe_message
            )
            
    except Exception as e:
        error_message = f"Failed to create database: {str(e)}"
        click.echo(error_message, err=True)
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=f"Error creating database '{db_name}': {str(e)}"
            )

@main.command()
@click.argument('db_name')
def info(db_name: str):
    """Show connection information for a database.
    
    Example: clidb info mydb
    """
    try:
        # Get credentials
        creds = credentials_manager.get_credentials(db_name)
        if not creds:
            raise Exception(f"No stored information found for database '{db_name}'")
        
        # Get database configuration
        db_config = get_database_config(creds.db_type, creds.version)
        
        # Generate connection details
        conn_string = get_connection_string(
            creds.db_type, creds.host, creds.port, 
            creds.user, creds.password, creds.name
        )
        cli_command = get_cli_command(
            creds.db_type, creds.host, creds.port, 
            creds.user, creds.password, creds.name
        )
        
        info_message = f"""
Database Information for '{db_name}':
Type: {db_config.name}
Version: {creds.version or 'latest'}
Access: {creds.access.upper()}
Host: {creds.host}
Port: {creds.port}
User: {creds.user}
Password: {creds.password}

Connection String (copy/paste ready):
{conn_string}

CLI Command:
{cli_command}
"""
        click.echo(info_message)
            
    except Exception as e:
        error_message = f"Failed to get database info: {str(e)}"
        click.echo(error_message, err=True)

@main.command()
@click.argument('db_name')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def stop(db_name: str, discord_webhook: Optional[str]):
    """Stop a database.
    
    Example: clidb stop mydb
    """
    try:
        client = docker.from_env()
        container = find_container(client, db_name)
        
        if not container:
            raise Exception(f"Database '{db_name}' not found")
        
        container.stop()
        success_message = f"Database '{db_name}' stopped successfully"
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=success_message
            )
    except Exception as e:
        error_message = f"Failed to stop database: {str(e)}"
        click.echo(error_message, err=True)
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=error_message
            )

@main.command()
@click.argument('db_name')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def start(db_name: str, discord_webhook: Optional[str]):
    """Start a stopped database.
    
    Example: clidb start mydb
    """
    try:
        client = docker.from_env()
        container = find_container(client, db_name)
        
        if not container:
            raise Exception(f"Database '{db_name}' not found")
        
        container.start()
        success_message = f"Database '{db_name}' started successfully"
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=success_message
            )
    except Exception as e:
        error_message = f"Failed to start database: {str(e)}"
        click.echo(error_message, err=True)
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=error_message
            )

@main.command()
@click.argument('db_name')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def remove(db_name: str, discord_webhook: Optional[str]):
    """Remove a database completely.
    
    Example: clidb remove mydb
    """
    try:
        client = docker.from_env()
        container = find_container(client, db_name)
        
        if not container:
            raise Exception(f"Database '{db_name}' not found")
        
        container.remove(force=True)
        
        # Remove stored credentials
        credentials_manager.remove_credentials(db_name)
        
        success_message = f"Database '{db_name}' removed successfully"
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=success_message
            )
    except Exception as e:
        error_message = f"Failed to remove database: {str(e)}"
        click.echo(error_message, err=True)
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=error_message
            )

@main.command()
def list():
    """List all databases.
    
    Example: clidb list
    """
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        
        # Filter our containers
        our_containers = []
        for container in containers:
            db_name, db_type = get_db_info(container.name)
            if db_name and db_type:
                our_containers.append((db_name, db_type, container.status))
        
        if not our_containers:
            click.echo("No databases found")
            return
            
        click.echo("\nDatabases:")
        click.echo("-" * 50)
        for db_name, db_type, status in sorted(our_containers):
            click.echo(f"Name: {db_name:<20} Type: {db_type:<10} Status: {status}")
        click.echo("-" * 50)
            
    except Exception as e:
        error_message = f"Failed to list databases: {str(e)}"
        click.echo(error_message, err=True)

@main.command(name='supported')
def list_supported():
    """List supported database types and versions.
    
    Example: clidb supported
    """
    click.echo("\nSupported Databases:")
    click.echo("-" * 50)
    click.echo(list_supported_databases())

if __name__ == '__main__':
    main() 
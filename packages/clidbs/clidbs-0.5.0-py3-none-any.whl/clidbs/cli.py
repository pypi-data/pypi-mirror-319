import click
import docker
import os
import secrets
import string
from typing import Optional
from .notifications import send_discord_notification
from .config import Config
from .databases import get_database_config, list_supported_databases, DATABASES

def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_container_name(db_type: str, db_name: str) -> str:
    """Convert db_name to full container name."""
    return f"clidb-{db_type}-{db_name}"

def get_db_name_from_container(container_name: str) -> str:
    """Extract db_name from container name."""
    parts = container_name.split('-')
    if len(parts) >= 3 and parts[0] == "clidb":
        return '-'.join(parts[2:])
    return container_name

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
        
        success_message = f"""
Database '{db_name}' created successfully!
Type: {db_config.name}
Version: {version or 'latest'}
User: {user}
Password: {password}
Port: {port}
Container: {db_name}

Connect using: """

        if db_type == 'postgres':
            success_message += f"psql -h localhost -p {port} -U {user} -d {db_name}"
        elif db_type == 'mysql' or db_type == 'mariadb':
            success_message += f"mysql -h localhost -P {port} -u {user} -p {db_name}"
        elif db_type == 'mongo':
            success_message += f"mongosh mongodb://{user}:PASSWORD@localhost:{port}/{db_name}"
        elif db_type == 'redis':
            success_message += f"redis-cli -h localhost -p {port} -a PASSWORD"
        
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=f"Database '{db_name}' ({db_config.name} {version or 'latest'}) created successfully!"
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
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def stop(db_name: str, discord_webhook: Optional[str]):
    """Stop a database.
    
    Example: clidb stop mydb
    """
    try:
        client = docker.from_env()
        # Try to find the container by name pattern
        containers = client.containers.list(all=True, filters={"name": f"clidb-*-{db_name}"})
        if not containers:
            raise Exception(f"Database '{db_name}' not found")
        
        container = containers[0]
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
        # Try to find the container by name pattern
        containers = client.containers.list(all=True, filters={"name": f"clidb-*-{db_name}"})
        if not containers:
            raise Exception(f"Database '{db_name}' not found")
        
        container = containers[0]
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
        # Try to find the container by name pattern
        containers = client.containers.list(all=True, filters={"name": f"clidb-*-{db_name}"})
        if not containers:
            raise Exception(f"Database '{db_name}' not found")
        
        container = containers[0]
        container.remove(force=True)
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
        containers = client.containers.list(all=True, filters={"name": "clidb-"})
        
        if not containers:
            click.echo("No databases found")
            return
            
        click.echo("\nDatabases:")
        click.echo("-" * 50)
        for container in containers:
            db_name = get_db_name_from_container(container.name)
            db_type = container.name.split('-')[1]
            status = container.status
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
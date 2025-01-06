import click
import docker
import os
import secrets
import string
from typing import Optional
from .notifications import send_discord_notification
from .config import Config

def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_container_name(db_name: str) -> str:
    """Convert db_name to full container name."""
    return f"clidb-postgres-{db_name}"

def get_db_name_from_container(container_name: str) -> str:
    """Extract db_name from container name."""
    if container_name.startswith("clidb-postgres-"):
        return container_name[len("clidb-postgres-"):]
    return container_name

@click.group()
def main():
    """Simple database management for your VPS."""
    pass

@main.command()
@click.argument('db_name')
@click.option('--type', 'db_type', type=click.Choice(['postgres']), default='postgres', help='Database type')
@click.option('--access', type=click.Choice(['public', 'private']), default='public', help='Access type')
@click.option('--user', help='Database user to create')
@click.option('--port', default=5432, help='Port to expose the database on')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def create(db_name: str, db_type: str, access: str, user: str, port: int, 
          discord_webhook: Optional[str]):
    """Create a new database.
    
    Example: clidb create mydb --user admin --port 5432
    """
    try:
        client = docker.from_env()
        
        # Use db_name as user if not specified
        if not user:
            user = db_name
        
        # Generate secure password
        password = generate_password()
        
        # Prepare environment variables
        environment = [
            f"POSTGRES_DB={db_name}",
            f"POSTGRES_USER={user}",
            f"POSTGRES_PASSWORD={password}"
        ]
        
        # Configure ports
        ports = {f'5432/tcp': port}
        
        # Configure network mode based on access type
        network_mode = 'bridge' if access == 'public' else 'host'
        
        # Create and start container
        container = client.containers.run(
            'postgres:latest',
            name=get_container_name(db_name),
            environment=environment,
            ports=ports,
            network_mode=network_mode,
            detach=True
        )
        
        success_message = f"""
Database '{db_name}' created successfully!
Type: PostgreSQL
User: {user}
Password: {password}
Port: {port}
Container: {db_name}

Connect using: psql -h localhost -p {port} -U {user} -d {db_name}
"""
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=f"Database '{db_name}' created successfully!"
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
        container = client.containers.get(get_container_name(db_name))
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
        container = client.containers.get(get_container_name(db_name))
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
        container = client.containers.get(get_container_name(db_name))
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
        containers = client.containers.list(all=True, filters={"name": "clidb-postgres-"})
        
        if not containers:
            click.echo("No databases found")
            return
            
        click.echo("\nDatabases:")
        click.echo("-" * 50)
        for container in containers:
            db_name = get_db_name_from_container(container.name)
            status = container.status
            click.echo(f"Name: {db_name:<20} Status: {status}")
        click.echo("-" * 50)
            
    except Exception as e:
        error_message = f"Failed to list databases: {str(e)}"
        click.echo(error_message, err=True)

if __name__ == '__main__':
    main() 
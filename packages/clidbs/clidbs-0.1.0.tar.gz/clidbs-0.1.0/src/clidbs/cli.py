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

@click.group()
def main():
    """CLI tool for managing databases on VPS systems."""
    pass

@main.command()
@click.argument('db_type', type=click.Choice(['postgres']))
@click.argument('access_type', type=click.Choice(['public', 'private']))
@click.option('--db-name', default='defaultdb', help='Name of the database to create')
@click.option('--user', default='dbuser', help='Database user to create')
@click.option('--port', default=5432, help='Port to expose the database on')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def create(db_type: str, access_type: str, db_name: str, user: str, port: int, 
          discord_webhook: Optional[str]):
    """Create a new database instance."""
    try:
        client = docker.from_env()
        
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
        network_mode = 'bridge' if access_type == 'public' else 'host'
        
        # Create and start container
        container = client.containers.run(
            'postgres:latest',
            name=f'clidb-postgres-{db_name}',
            environment=environment,
            ports=ports,
            network_mode=network_mode,
            detach=True
        )
        
        success_message = f"""
Database created successfully!
Type: PostgreSQL
Name: {db_name}
User: {user}
Password: {password}
Port: {port}
Container ID: {container.id[:12]}
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
@click.argument('container_name')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def stop(container_name: str, discord_webhook: Optional[str]):
    """Stop a running database container."""
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        container.stop()
        success_message = f"Container {container_name} stopped successfully"
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=success_message
            )
    except Exception as e:
        error_message = f"Failed to stop container: {str(e)}"
        click.echo(error_message, err=True)
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=error_message
            )

@main.command()
@click.argument('container_name')
@click.option('--discord-webhook', help='Discord webhook URL for notifications')
def start(container_name: str, discord_webhook: Optional[str]):
    """Start a stopped database container."""
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        container.start()
        success_message = f"Container {container_name} started successfully"
        click.echo(success_message)
        
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=success_message
            )
    except Exception as e:
        error_message = f"Failed to start container: {str(e)}"
        click.echo(error_message, err=True)
        if discord_webhook:
            send_discord_notification(
                webhook_url=discord_webhook,
                message=error_message
            )

if __name__ == '__main__':
    main() 
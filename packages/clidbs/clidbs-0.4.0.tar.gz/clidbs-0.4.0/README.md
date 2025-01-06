# CLIDB - Simple Database Management CLI

A command-line tool for managing databases (currently PostgreSQL) on VPS systems using Docker containers.

## Prerequisites

- Python 3.8 or higher
- Docker installed and running
- pip (Python package installer)

## Installation

```bash
pip install clidbs
```

## Usage

### Create a new PostgreSQL database

```bash
# Create a public PostgreSQL database
clidb create postgres public --db-name mydb --user myuser --port 5432

# Create a private PostgreSQL database
clidb create postgres private --db-name mydb --user myuser
```

### Stop a database container

```bash
clidb stop clidb-postgres-mydb
```

### Start a database container

```bash
clidb start clidb-postgres-mydb
```

### Discord Notifications

To enable Discord notifications, you can either:

1. Set the webhook URL when running commands:
```bash
clidb create postgres public --discord-webhook "YOUR_WEBHOOK_URL"
```

2. Set it as an environment variable:
```bash
export CLIDB_DISCORD_WEBHOOK="YOUR_WEBHOOK_URL"
```

## Configuration

The CLI can be configured using environment variables:

- `CLIDB_DISCORD_WEBHOOK`: Discord webhook URL for notifications
- `CLIDB_DEFAULT_DB`: Default database type (defaults to "postgres")
- `CLIDB_DEFAULT_PORT`: Default port (defaults to 5432)

## Security

- Passwords are automatically generated and displayed only once at creation
- Private mode uses host networking for better security
- Public mode exposes ports for remote access

## License

MIT License 
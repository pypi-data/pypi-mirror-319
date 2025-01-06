"""Database configurations and templates for CLIDB."""
from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import os
import stat
from pathlib import Path

@dataclass
class DatabaseCredentials:
    """Stored credentials for a database."""
    db_type: str
    version: Optional[str]
    user: str
    password: str
    port: int
    host: str
    access: str
    name: str

    def to_dict(self) -> dict:
        return {
            "db_type": self.db_type,
            "version": self.version,
            "user": self.user,
            "password": self.password,
            "port": self.port,
            "host": self.host,
            "access": self.access,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DatabaseCredentials':
        return cls(**data)

class CredentialsManager:
    """Manage database credentials with secure file permissions."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "clidb"
        self.creds_file = self.config_dir / "credentials.json"
        self._ensure_secure_directory()
        self._load_credentials()

    def _ensure_secure_directory(self):
        """Ensure config directory exists with secure permissions."""
        # Create directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Set directory permissions to 700 (rwx------)
        # Only owner can read, write, or access the directory
        self.config_dir.chmod(0o700)

    def _secure_file(self, path: Path):
        """Set secure permissions on a file."""
        # Set file permissions to 600 (rw-------)
        # Only owner can read and write the file
        path.chmod(0o600)

    def _load_credentials(self):
        """Load credentials from file with secure permissions."""
        if self.creds_file.exists():
            # Ensure file has secure permissions before reading
            self._secure_file(self.creds_file)
            with self.creds_file.open('r') as f:
                self.credentials = {
                    name: DatabaseCredentials.from_dict(data)
                    for name, data in json.load(f).items()
                }
        else:
            self.credentials = {}

    def _save_credentials(self):
        """Save credentials to file with secure permissions."""
        # Write to a temporary file first
        temp_file = self.creds_file.with_suffix('.tmp')
        with temp_file.open('w') as f:
            json.dump({
                name: creds.to_dict()
                for name, creds in self.credentials.items()
            }, f, indent=2)
        
        # Secure the temporary file
        self._secure_file(temp_file)
        
        # Atomically replace the old file
        temp_file.replace(self.creds_file)
        
        # Ensure final file has correct permissions
        self._secure_file(self.creds_file)

    def store_credentials(self, creds: DatabaseCredentials):
        """Store credentials for a database."""
        self.credentials[creds.name] = creds
        self._save_credentials()

    def get_credentials(self, db_name: str) -> Optional[DatabaseCredentials]:
        """Get credentials for a database."""
        return self.credentials.get(db_name)

    def remove_credentials(self, db_name: str):
        """Remove credentials for a database."""
        if db_name in self.credentials:
            del self.credentials[db_name]
            self._save_credentials()

@dataclass
class DatabaseConfig:
    """Configuration for a database type."""
    name: str
    image: str
    default_port: int
    environment_prefix: str
    volumes: Optional[List[str]] = None
    command: Optional[str] = None
    default_version: str = "latest"
    supported_versions: List[str] = None
    description: str = ""

    def get_env_vars(self, db_name: str, user: str, password: str) -> List[str]:
        """Get environment variables for this database type."""
        if self.environment_prefix == "POSTGRES":
            return [
                f"POSTGRES_DB={db_name}",
                f"POSTGRES_USER={user}",
                f"POSTGRES_PASSWORD={password}"
            ]
        elif self.environment_prefix == "MYSQL":
            return [
                f"MYSQL_DATABASE={db_name}",
                f"MYSQL_USER={user}",
                f"MYSQL_PASSWORD={password}",
                "MYSQL_RANDOM_ROOT_PASSWORD=yes"
            ]
        elif self.environment_prefix == "MONGO":
            return [
                f"MONGO_INITDB_DATABASE={db_name}",
                f"MONGO_INITDB_ROOT_USERNAME={user}",
                f"MONGO_INITDB_ROOT_PASSWORD={password}"
            ]
        elif self.environment_prefix == "CLICKHOUSE":
            return [
                f"CLICKHOUSE_DB={db_name}",
                f"CLICKHOUSE_USER={user}",
                f"CLICKHOUSE_PASSWORD={password}",
                "CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1"
            ]
        return []

# Database configurations
DATABASES: Dict[str, DatabaseConfig] = {
    "postgres": DatabaseConfig(
        name="PostgreSQL",
        image="postgres",
        default_port=5432,
        environment_prefix="POSTGRES",
        supported_versions=["16", "15", "14", "13", "12", "11"],
        description="Advanced open source relational database"
    ),
    
    "mysql": DatabaseConfig(
        name="MySQL",
        image="mysql",
        default_port=3306,
        environment_prefix="MYSQL",
        supported_versions=["8.0", "5.7"],
        description="Popular open source relational database"
    ),
    
    "mariadb": DatabaseConfig(
        name="MariaDB",
        image="mariadb",
        default_port=3306,
        environment_prefix="MYSQL",
        supported_versions=["11.2", "11.1", "11.0", "10.11", "10.10"],
        description="Community-developed fork of MySQL"
    ),
    
    "redis": DatabaseConfig(
        name="Redis",
        image="redis",
        default_port=6379,
        environment_prefix="REDIS",
        command="redis-server --requirepass ${REDIS_PASSWORD}",
        supported_versions=["7.2", "7.0", "6.2"],
        description="In-memory data structure store"
    ),
    
    "keydb": DatabaseConfig(
        name="KeyDB",
        image="eqalpha/keydb",
        default_port=6379,
        environment_prefix="REDIS",
        command="keydb-server --requirepass ${REDIS_PASSWORD}",
        supported_versions=["6.3", "6.2", "6.1"],
        description="Multithreaded fork of Redis with better performance"
    ),
    
    "clickhouse": DatabaseConfig(
        name="ClickHouse",
        image="clickhouse/clickhouse-server",
        default_port=8123,
        environment_prefix="CLICKHOUSE",
        volumes=["/var/lib/clickhouse"],
        supported_versions=["23.12", "23.11", "23.10", "23.9"],
        description="Column-oriented database for real-time analytics"
    ),
    
    "mongo": DatabaseConfig(
        name="MongoDB",
        image="mongo",
        default_port=27017,
        environment_prefix="MONGO",
        supported_versions=["7.0", "6.0", "5.0"],
        description="NoSQL document database"
    ),
    
    "neo4j": DatabaseConfig(
        name="Neo4j",
        image="neo4j",
        default_port=7687,
        environment_prefix="NEO4J",
        volumes=["/data"],
        supported_versions=["5", "4.4"],
        description="Graph database management system"
    )
}

def get_database_config(db_type: str, version: Optional[str] = None) -> DatabaseConfig:
    """Get database configuration by type and version."""
    if db_type not in DATABASES:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    config = DATABASES[db_type]
    
    if version:
        if version not in config.supported_versions:
            raise ValueError(
                f"Unsupported version {version} for {db_type}. "
                f"Supported versions: {', '.join(config.supported_versions)}"
            )
        return DatabaseConfig(
            **{**config.__dict__, "image": f"{config.image}:{version}"}
        )
    
    return config

def list_supported_databases() -> str:
    """Get a formatted string of supported databases and versions."""
    output = []
    for db_type, config in DATABASES.items():
        versions = ", ".join(config.supported_versions) if config.supported_versions else "latest"
        output.append(f"{config.name} ({db_type}):")
        output.append(f"  Description: {config.description}")
        output.append(f"  Versions: {versions}")
        output.append(f"  Default port: {config.default_port}")
        output.append("")
    
    return "\n".join(output) 

# Initialize the credentials manager as a singleton
credentials_manager = CredentialsManager() 
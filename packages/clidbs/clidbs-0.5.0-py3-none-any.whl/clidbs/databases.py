"""Database configurations and templates for CLIDB."""
from dataclasses import dataclass
from typing import Dict, List, Optional

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
        supported_versions=["11.0", "10.11", "10.10"],
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
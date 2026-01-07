import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all models here so that Base has them registered
from app.models import chromosome, gene, statistic, centromere
from app.db.session import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# Skip logging configuration if running under pytest, as it handles its own logging setup
if os.getenv("PYTEST_RUNNING") != "true" and config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
    url = os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///../genome_guides.db") # Direct read from env
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    """
    configuration = config.get_section(config.config_ini_section)
    db_url = os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///../genome_guides.db") # Direct read from env
    configuration["sqlalchemy.url"] = db_url

    # Debug print to see where Alembic is looking for scripts
    # This might require importing script from alembic.script
    from alembic.script import ScriptDirectory
    script = ScriptDirectory.from_config(config)
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

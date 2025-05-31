from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

from db.models import Base, engine  # <-- твой engine и Base

# Alembic config object
config = context.config

# Вставим URL из твоего engine
config.set_main_option("sqlalchemy.url", str(engine.url))

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Мета-данные моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

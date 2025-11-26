# file: src/app/db/migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.db.base import Base
from app.core.config.settings import settings

# IMPORTACIÓN OBLIGATORIA DE TODOS LOS MODELOS
# Sin estos imports, Alembic NO detecta las tablas
import app.models.cash_account
import app.models.cash_movement
import app.models.customer
import app.models.line_purchase_note
import app.models.line_sales_note
import app.models.product
import app.models.purchase_note
import app.models.sales_note
import app.models.stock_location
import app.models.stock_movement
import app.models.stock_product_location
import app.models.supplier
import app.models.user

# Alembic config
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Override URL from settings
db_url = settings.DATABASE_URL
config.set_main_option("sqlalchemy.url", db_url)


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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

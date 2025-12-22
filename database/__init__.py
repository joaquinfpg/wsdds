from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

db = SQLAlchemy()


def ensure_user_role_column(engine):
    if not engine:
        return
    inspector = inspect(engine)
    if 'users' not in inspector.get_table_names():
        return
    columns = {col['name'] for col in inspector.get_columns('users')}
    if 'role' in columns:
        return
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE users ADD COLUMN role VARCHAR(50) NOT NULL DEFAULT 'User'")
        )

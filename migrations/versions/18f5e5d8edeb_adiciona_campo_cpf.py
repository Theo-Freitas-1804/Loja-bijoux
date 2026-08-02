"""Adiciona campo cpf

Revision ID: 18f5e5d8edeb
Revises: e937cb787dfb
Create Date: 2026-07-25 23:17:10.891521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18f5e5d8edeb'
down_revision = 'e937cb787dfb'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a coluna CPF aos clientes
    with op.batch_alter_table('Clientes', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'cpf',
                sa.String(length=14),
                nullable=True
            )
        )


def downgrade():
    # Remove a coluna CPF
    with op.batch_alter_table('Clientes', schema=None) as batch_op:
        batch_op.drop_column('cpf')
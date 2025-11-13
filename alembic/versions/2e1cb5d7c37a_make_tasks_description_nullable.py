from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2e1cb5d7c37a"
down_revision = "f5a1111c32f7"   # ← MUST match previous file's revision
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "tasks",
        "description",
        existing_type=sa.Text(),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "tasks",
        "description",
        existing_type=sa.Text(),
        nullable=False,
    )

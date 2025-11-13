from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "f5a1111c32f7"      # ← MUST match the filename prefix
down_revision = "30e1492dffa2"  # ← previous migration
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "tasks",
        sa.Column("closed_at", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_column("tasks", "closed_at")

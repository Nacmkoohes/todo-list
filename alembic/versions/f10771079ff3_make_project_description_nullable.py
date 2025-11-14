from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "abcd1234efgh"      # همونی باشه که بالای فایل هست
down_revision = "2e1cb5d7c37a" # head قبلی
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "projects",
        "description",
        existing_type=sa.Text(),  # اگر تو مایگریشن اولیه String بود، می‌تونی String بذاری
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "projects",
        "description",
        existing_type=sa.Text(),
        nullable=False,
    )

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<REV_ID>'      # ← همان که Alembic ساخته
down_revision = '<PREV_ID>' # ← همان قبلی
branch_labels = None
depends_on = None

def upgrade():
    # nullable=True
    op.alter_column(
        'tasks',
        'description',
        existing_type=sa.String(length=1000),
        nullable=True
    )

def downgrade():
    # برگرداندن به NOT NULL (برای سازگاری مجبوریم default بگذاریم)
    op.alter_column(
        'tasks',
        'description',
        existing_type=sa.String(length=1000),
        nullable=False,
        server_default=''
    )


"""empty message

Revision ID: 120ee2333afe
Revises: f9d3104b97bf
Create Date: 2021-01-08 14:29:22.329272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120ee2333afe'
down_revision = 'f9d3104b97bf'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.sql.text(
        """
        CREATE OR REPLACE FUNCTION adjust_count()
        RETURNS TRIGGER AS
        $$
           DECLARE
           BEGIN
           IF TG_OP = 'INSERT' THEN
              EXECUTE 'UPDATE stats set count=count +1 where label = ''' || TG_ARGV[0] || '''';
              RETURN NEW;
           ELSIF TG_OP = 'DELETE' THEN
              EXECUTE 'UPDATE stats set count=count -1 where label = ''' || TG_ARGV[0] || '''';
              RETURN OLD;
           END IF;
           END;
        $$
        LANGUAGE 'plpgsql';

        CREATE TRIGGER activities_count BEFORE INSERT OR DELETE ON activity
          FOR EACH ROW EXECUTE PROCEDURE adjust_count('activities');

        CREATE TRIGGER transactions_count BEFORE INSERT OR DELETE ON transaction
          FOR EACH ROW EXECUTE PROCEDURE adjust_count('transactions');

        CREATE TRIGGER budgets_count BEFORE INSERT OR DELETE ON budget
          FOR EACH ROW EXECUTE PROCEDURE adjust_count('budgets');

        COMMIT;
        """))


def downgrade():
    pass

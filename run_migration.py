import os
import sys
from sqlalchemy import create_engine

def run_sql_file(db_url: str, path: str) -> None:
    if not os.path.exists(path):
        print(f"[v0] SQL file not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    engine = create_engine(db_url, pool_pre_ping=True)
    print(f"[v0] Connecting to: {db_url}")
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    print(f"[v0] Executing {len(statements)} SQL statements from {path}...")
    try:
        with engine.begin() as conn:
            for i, stmt in enumerate(statements, 1):
                print(f"[v0] Running statement {i}/{len(statements)}...")
                conn.exec_driver_sql(stmt)
        print("[v0] Migration completed successfully.")
    except Exception as e:
        print(f"[v0] Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("[v0] DATABASE_URL is not set. Example: mysql+pymysql://root:root@127.0.0.1:3306/insurance_app")
        sys.exit(1)

    path = sys.argv[1] if len(sys.argv) > 1 else "scripts/sql/20251011_add_assessment_json_columns.sql"
    run_sql_file(db_url, path)

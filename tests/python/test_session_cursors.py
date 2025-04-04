import psycopg2
from psycopg2.extras import NamedTupleCursor

conn_args = dict(
    host="localhost",
    user="example_user_3",
    password="test",
    dbname="example_db",
    port=6433,
    cursor_factory=NamedTupleCursor,
    sslmode="disable",
)

declare_cursor_statement = (
    "declare cursor_name no scroll cursor with hold for select 1;"
)
select_cursor_statement = "select * from pg_cursors;"

# connect to a session pool and declare a cursor
with psycopg2.connect(**conn_args) as conn, conn.cursor() as cur:
    cur.execute(declare_cursor_statement)
    cur.execute(select_cursor_statement)
    res = cur.fetchall()

    assert len(res) == 1

    record = res[0]
    assert hasattr(record, "statement") and record.statement == declare_cursor_statement

# re-connect and ensure the cursor is not there
with psycopg2.connect(**conn_args) as conn, conn.cursor() as cur:
    cur.execute(select_cursor_statement)
    res = cur.fetchall()

    assert len(res) == 0


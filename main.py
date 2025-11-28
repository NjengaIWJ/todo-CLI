import click
import sqlite3


def db_conn():
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_conn()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )
    conn.close()


@click.group()
def cli():
    """Simple TODO CLI"""
    db_conn()


@cli.command(name="add")
@click.argument("item")
def add_todo(item: str) -> None:
    """Add a new todo item."""
    conn = db_conn()

    with conn:
        conn.execute("INSERT INTO todos (item) VALUES (?)", (item,))
    conn.close()


@cli.command(name="get")
def get_todos():
    """List all todo items."""
    conn = db_conn()

    cursor = conn.execute("SELECT id, item, done FROM todos ORDER BY id")
    rows = cursor.fetchall()

    if not rows:
        click.echo("No todos found.")
    else:
        for row in rows:
            click.echo(
                f"{row['id']}: {row['item']} - {'Done' if row['done'] else 'Not Done'}"
            )


@cli.command(name="delete")
@click.argument("id", type=int)
def remove_todos(id: int) -> None:
    """Delete a todo by its index."""

    conn = db_conn()

    with conn:
        cur = conn.execute("DELETE FROM todos WHERE id = ?", (id,))

        if cur.rowcount:
            click.echo(f"Deleted todo with id {id}")
        else:
            click.echo(f"Todo with id {id} does not exist in database")

    conn.close()


if __name__ == "__main__":
    init_db()
    cli()

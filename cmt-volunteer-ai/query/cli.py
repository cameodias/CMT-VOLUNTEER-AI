import sqlite3
from rich.table import Table
from rich.console import Console

conn = sqlite3.connect("volunteer_data.db")
c = conn.cursor()

name_input = input("Enter name (optional): ").strip().lower()

query = """
SELECT m.name, p.persona, p.confidence, m.join_date
FROM members m
JOIN personas p ON m.id = p.member_id
WHERE LOWER(m.name) LIKE ?
ORDER BY p.confidence DESC, m.join_date DESC
"""

rows = c.execute(query, (f"%{name_input}%",)).fetchall()

table = Table(title="Potential Mentors")

table.add_column("Name")
table.add_column("Persona")
table.add_column("Confidence")
table.add_column("Join Date")

for r in rows:
    table.add_row(*map(str, r))

Console().print(table)

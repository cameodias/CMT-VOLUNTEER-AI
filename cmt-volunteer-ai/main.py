from etl.loader import load_csv
from etl.validator import validate_row
from etl.normalizer import normalize_name, normalize_date
from etl.logger import log_error
from brain.enrich import enrich_bio
from db.models import get_connection
from datetime import datetime

# Load CSV (your actual structure)
df = load_csv("data/members_raw.csv")

print("CSV loaded")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

conn = get_connection()
cur = conn.cursor()

for idx, row in df.iterrows():
    valid, error = validate_row(row)
    if not valid:
        log_error(idx, error)
        continue

    try:
        name = normalize_name(row.get("members"))
        bio = row.get("bio or comment") or ""
        join_date = normalize_date(row.get("last active"))
        city = "Unknown"  # Not available in CSV
    except Exception as e:
        log_error(idx, f"Normalization error: {e}")
        continue

    # Insert member
    cur.execute("""
        INSERT INTO members (name, city, join_date, bio, processed_at, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        city,
        join_date,
        bio,
        datetime.utcnow().isoformat(),
        "processed"
    ))

    member_id = cur.lastrowid

    # AI enrichment (safe + fallback)
    enrichment = enrich_bio(bio)

    # Insert skills
    for skill in enrichment.get("skills", []):
        cur.execute(
            "INSERT INTO skills (member_id, skill) VALUES (?, ?)",
            (member_id, skill)
        )

    # Insert persona (ALWAYS)
    cur.execute("""
        INSERT INTO personas (member_id, persona, confidence, version)
        VALUES (?, ?, ?, ?)
    """, (
        member_id,
        enrichment.get("persona", "Needs Guidance"),
        enrichment.get("confidence", 0.3),
        1
    ))

conn.commit()
conn.close()

print("Pipeline executed successfully.")

import logging

logging.basicConfig(
    filename="etl_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(record_id, error):
    logging.error(f"Record {record_id}: {error}")

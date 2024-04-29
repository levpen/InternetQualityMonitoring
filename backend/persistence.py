"""Storage module."""
import sqlite3
from datetime import datetime


class MetricsRepository:
    """Repository for saving and retrieving metrics."""

    def __init__(self: object, db_path: str) -> None:
        """MetricsRepository constructor."""
        self.db_path = db_path

    def __enter__(self: object) -> object:
        """Open database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (ID       INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                  datetime DATETIME NOT NULL,
                  loss     NUMERIC  NOT NULL,
                  latency  NUMERIC  NOT NULL,
                  http     TEXT     NOT NULL 
                    CHECK (http == 'open' or http == 'filtered' or http == 'closed'),
                  https    TEXT     NOT NULL 
                    CHECK (https == 'open' or https == 'filtered' or https == 'closed'),
                  imap     TEXT     NOT NULL 
                    CHECK (imap == 'open' or imap == 'filtered' or imap == 'closed'),
                  smtp     TEXT     NOT NULL 
                    CHECK (smtp == 'open' or smtp == 'filtered' or smtp == 'closed'),
                  ssh      TEXT     NOT NULL 
                    CHECK (ssh == 'open' or ssh == 'filtered' or ssh == 'closed'),
                  dns      TEXT     NOT NULL 
                    CHECK (dns == 'open' or dns == 'filtered' or dns == 'closed'));''')
        self.conn.commit()
        return self

    def save_record(self: object, record: dict) -> None:
        """Add new record to metrics."""
        acc = dict(record['accessibility'])
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.conn.execute('''INSERT INTO metrics 
                            (datetime, loss, latency, http, https, imap, smtp, ssh, dns)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (
                              current_datetime,
                              record['loss'],
                              record['latency'],
                              acc['HTTP'],
                              acc['HTTPS'],
                              acc['IMAP'],
                              acc['SMTP'],
                              acc['SSH'],
                              acc['DNS']
                          ))
        self.conn.commit()

    def __exit__(self: object, *args: [any]) -> object:
        """Close connection."""
        self.conn.close()

# Example usage:
# if __name__ == "__main__":
#     db_path = "metrics.db"
#     with MetricsRepository(db_path) as metrics_repo:
#         record = {
#             "loss": 0.0,
#             "latency": 801.2,
#             "accessibility": [
#                 ('HTTP', 'open'),
#                 ('HTTPS', 'filtered'),
#                 ('IMAP', 'filtered'),
#                 ('SMTP', 'filtered'),
#                 ('SSH', 'open'),
#                 ('DNS', 'open')
#             ]
#         }
#         metrics_repo.save_record(record)

# if __name__ == "__main__":
#     conn = sqlite3.connect('metrics.db')
#     c = conn.execute('''SELECT * FROM metrics''')
#     for row in c:
#         print(row)

"""Storage module."""
import sqlite3
from datetime import datetime
from typing import Self


class MetricsRepository:
    """Repository for saving and retrieving metrics."""

    def __init__(self: Self, db_path: str) -> None:
        """MetricsRepository constructor."""
        self.db_path = db_path

    def __enter__(self: Self) -> Self:
        """Open database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS hosts
                 (host TEXT PRIMARY KEY NOT NULL);''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (ID       INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                  host     TEXT     NOT NULL,
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

    def save_record(self: Self, host: str,  record: dict) -> None:
        """Add new record to metrics."""
        acc = dict(record['accessibility'])
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # pragma: no mutate
        self.conn.execute('''INSERT INTO metrics 
                            (host, datetime, loss, latency, 
                                http, https, imap, smtp, ssh, dns)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (
                              host,
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

    def add_host(self: Self, host: str) -> None:
        """Add new host to metrics."""
        self.conn.execute('''INSERT INTO hosts (host)
                                 VALUES (?)''',
                          (host,))
        self.conn.commit()

    def get_hosts_cursor(self: Self) -> sqlite3.Cursor:
        """Get cursor to access hosts."""
        return self.conn.execute('''SELECT * FROM hosts''')

    def get_hosts(self: Self) -> list:
        """Fetch all hosts from database."""
        return self.get_hosts_cursor().fetchall()

    def get_metrics_cursor(self: Self, hour_offset: int) -> sqlite3.Cursor:
        """Get cursor to access metrics with days offset."""
        return self.conn.execute(
            '''SELECT * FROM metrics 
                   WHERE datetime > DATETIME("now", ?) 
                   ORDER BY datetime''',
            ("-" + str(hour_offset) + " hour",))

    def get_metrics(self: Self, hour_offset: int) -> list:
        """Fetch all metrics from database."""
        return self.get_metrics_cursor(hour_offset).fetchall()

    def __exit__(self: Self, *args: [any]) -> None:
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
# conn = sqlite3.connect('metrics.db')
# c = conn.execute('''SELECT * FROM metrics''')
# for row in c:
#     print(row)

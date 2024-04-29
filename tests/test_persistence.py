import os
from datetime import datetime

import pytest

from backend.persistence import MetricsRepository


# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def in_memory_db():
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    delete_file("metrics.db")
    return "metrics.db"


# Test cases for MetricsRepository class
def test_save_record(in_memory_db):
    with MetricsRepository(in_memory_db) as metrics_repo:
        record = {
            "loss": 0.0,
            "latency": 801.2,
            "accessibility": {
                'HTTP': 'open',
                'HTTPS': 'filtered',
                'IMAP': 'filtered',
                'SMTP': 'filtered',
                'SSH': 'open',
                'DNS': 'open'
            }
        }
        metrics_repo.save_record('example.com', record)
        cursor = metrics_repo.conn.execute('''SELECT * FROM metrics''')
        result = cursor.fetchone()
        assert result[1] == 'example.com'
        assert result[3] == 0.0
        assert result[4] == 801.2
        assert result[5] == 'open'
        assert result[6] == 'filtered'
        assert result[7] == 'filtered'
        assert result[8] == 'filtered'
        assert result[9] == 'open'
        assert result[10] == 'open'


def test_add_host(in_memory_db):
    with MetricsRepository(in_memory_db) as metrics_repo:
        metrics_repo.add_host('example.com')
        cursor = metrics_repo.conn.execute('''SELECT * FROM hosts''')
        result = cursor.fetchone()
        assert result[0] == 'example.com'


def test_get_hosts(in_memory_db):
    with MetricsRepository(in_memory_db) as metrics_repo:
        metrics_repo.add_host('example.com')
        hosts = metrics_repo.get_hosts()
        assert len(hosts) == 1
        assert hosts[0][0] == 'example.com'


def test_get_metrics(in_memory_db):
    with MetricsRepository(in_memory_db) as metrics_repo:
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        metrics_repo.conn.execute('''INSERT INTO metrics 
                            (host, datetime, loss, latency, 
                                http, https, imap, smtp, ssh, dns)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                  (
                                      'example.com',
                                      current_datetime,
                                      0.0,
                                      801.2,
                                      'open',
                                      'filtered',
                                      'filtered',
                                      'filtered',
                                      'open',
                                      'open'
                                  ))
        metrics = metrics_repo.get_metrics(1)
        assert len(metrics) == 1
        assert metrics[0][1] == 'example.com'
        assert metrics[0][3] == 0.0
        assert metrics[0][4] == 801.2
        assert metrics[0][5] == 'open'
        assert metrics[0][6] == 'filtered'
        assert metrics[0][7] == 'filtered'
        assert metrics[0][8] == 'filtered'
        assert metrics[0][9] == 'open'
        assert metrics[0][10] == 'open'


def test_delete_host(in_memory_db):
    with MetricsRepository(in_memory_db) as metrics_repo:
        # Add a host to the database
        metrics_repo.add_host('example.com')

        # Verify that the host was added successfully
        cursor = metrics_repo.conn.execute('''SELECT * FROM hosts''')
        assert cursor.fetchone()[0] == 'example.com'

        # Delete the host
        metrics_repo.delete_host('example.com')

        # Verify that the host was deleted
        cursor = metrics_repo.conn.execute('''SELECT * FROM hosts''')
        assert cursor.fetchone() is None

"""Module to test main.py."""
from unittest.mock import patch
from backend.main import collect_and_append_data


@patch('backend.collect_data')
def test_collect_and_append_data(mock_collect_data: {}) -> None:
    """Do test collect_and_append_data() function."""
    host = "example.com"
    record = {
        'accessibility': [('HTTP', 'open'),
                          ('HTTPS', 'open'),
                          ('IMAP', 'filtered'),
                          ('SMTP', 'filtered'),
                          ('SSH', 'filtered'),
                          ('DNS', 'filtered')],
        'latency': 0.0,
        'loss': 0.0
    }
    mock_collect_data.return_value = record

    records = []
    collect_and_append_data(host, records)

    assert len(records) == 1
    assert records[0]["accessibility"] == record["accessibility"]




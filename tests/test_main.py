from unittest.mock import patch, MagicMock
import pytest
from backend.main import *


@patch('backend.collect_data')
def test_collect_and_append_data(mock_collect_data):
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

    assert records == [record]




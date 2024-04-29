"""Tests for collect_data.py."""
from backend.collect_data import collect_data,get_loss_and_latency,get_accessibility

def test_collect_data() -> None:
    """Do call of stable service to test."""
    host = "ya.ru" # Assume super stable
    expected_result = {
        "loss": 0.0,
        "latency": 0.0,
        "accessibility": [
            ("HTTP", "open"), 
            ("HTTPS", "open"),
            ("IMAP", "filtered"),
            ("SMTP", "filtered"),
            ("SSH", "filtered"),
            ("DNS", "filtered")
        ]
    }
    result = collect_data(host)
    for ex_status, status in zip(expected_result["accessibility"],
                        result["accessibility"], strict=False):
        assert ex_status == status
    
def test_get_acc() -> None:
    """Do call services to test."""
    assert get_accessibility("ya.ru", 80) == "open"
    assert get_accessibility("ya.ru", 43) == "filtered"
    assert get_accessibility("ru.ya", 80) == "unreachable"
    

def test_ping() -> None:
    """Do ping services to test."""
    assert get_loss_and_latency("ya.ru", 1)[0] == 100.0
    assert get_loss_and_latency("ya.ru", 1)[1] >= 0.0
    assert get_loss_and_latency("ru.ya", 1)[0] == 100.0
    


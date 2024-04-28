Example:
```py
from collect_data import collect_data

print('ya.ru')
print(collect_data('ya.ru'))
print('77.88.8.8')
print(collect_data('77.88.8.8'))
```
Output:
```text
~/D/I/backend (main)> python3 test.py
ya.ru
{'loss': 0.0, 'latency': 800.8, 'accessibility': [('HTTP', 'open'), ('HTTPS', 'open'), ('IMAP', 'filtered'), ('SMTP', 'filtered'), ('SSH', 'filtered'), ('DNS', 'filtered')]}
77.88.8.8
{'loss': 0.0, 'latency': 801.0, 'accessibility': [('HTTP', 'filtered'), ('HTTPS', 'open'), ('IMAP', 'filtered'), ('SMTP', 'filtered'), ('SSH', 'filtered'), ('DNS', 'open')]}
```

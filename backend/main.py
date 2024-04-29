"""Daemon that collect data from hosts."""
from persistence import MetricsRepository
from collect_data import collect_data
from threading import Thread

DB_PATH = "metrics.db"

def collect_and_append_data(host: str, records: []) -> None:
    """Do to run in thread."""
    record = collect_data(host, 1)
    records.append(record)

if __name__ == "__main__":
    while True:
        hosts = ["ya.ru"] # MetricsRepository.get_hosts() TODO
        records = []
        threads = []
        for host in hosts:
            thread = Thread(target=collect_and_append_data, args=(host, records))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        with MetricsRepository(DB_PATH) as metrics_repo:
            for record in records:
                metrics_repo.save_record(record)



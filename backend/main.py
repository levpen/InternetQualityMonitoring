"""Daemon that collect data from hosts."""
from persistence import MetricsRepository
from collect_data import collect_data
from time import sleep
from threading import Thread

DB_PATH = "metrics.db"

def collect_and_append_data(host: str, records: []) -> None:
    """Do to run in thread."""
    record = collect_data(host, 1)
    records.append(record)

if __name__ == "__main__":
    while True:
        with MetricsRepository(DB_PATH) as metrics_repo:
            hosts = metrics_repo.get_hosts()
            records = []
            threads = []
            for host in hosts:
                thread = Thread(target=collect_and_append_data, args=(host, records))
                threads.append(thread)
                thread.start()
            
            sleep(1)
            for thread in threads:
                thread.join()
            print(records)
            
            for host, record in zip(hosts, records):
                print(record)
                metrics_repo.save_record(host, record)



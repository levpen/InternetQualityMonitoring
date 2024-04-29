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
    
    with MetricsRepository(DB_PATH) as metrics_repo:
        while True:
            hosts = ['.'.join(item) for item in metrics_repo.get_hosts()]
            records = []
            threads = []
            for host in hosts:
                thread = Thread(target=collect_and_append_data, args=(host, records))
                threads.append(thread)
                thread.start()
            
            sleep(1)
            for thread in threads:
                thread.join()
            
            for host, record in zip(hosts, records, strict=False):
                metrics_repo.save_record(host, record)
            

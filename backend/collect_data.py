"""Module for collecting data."""
from subprocess import Popen, PIPE

PORTS = {
    "HTTP": 80,
    "HTTPS": 443,
    "IMAP": 143,
    "SMTP": 25,
    "SSH": 22,
    "DNS": 53
}    

def get_loss_and_latency(host: str, n_packet: int = 5) -> (float, float):
    """Do getting packet loss and latency of resource, using ICMP port via ping."""
    process = Popen(['/bin/sh', '-c', f'ping -c {n_packet} {host}'], stdout=PIPE)
    stdout, _ = process.communicate()
    packetloss = float(next(x for x in stdout.decode('utf-8').split('\n') 
                        if x.find('packet loss') != -1).split('%')[0].split(' ')[-1])
    latency = float(stdout.decode('utf-8').split('\n')[-3].split(' ')[-1][:-2])/n_packet

    return (packetloss, latency)


def get_accessibility(host: str, port: int) -> str:
    """Do checks of accessibility of given resource via nmap util."""
    process = Popen(['/bin/sh', '-c', f'nmap -p {port} {host}'], stdout=PIPE)
    stdout, _ = process.communicate()
    acc = stdout.decode('utf-8').split('\n')[-4].split(' ')[1]

    return acc


def collect_data(host: str, n_packet: int = 5) -> {str: object}:
    """Do aggregate data of given resource."""
    pl, lat = get_loss_and_latency(host, n_packet)
    acc = [(name, get_accessibility(host, port)) for name, port in PORTS.items()]
    return {
        "loss": pl,
        "latency": lat,
        "accessibility": acc
    }

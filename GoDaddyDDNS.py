import argparse
import sys
import logging
import json
from urllib.request import urlopen, Request
from godaddypy import Client, Account
from time import sleep

PUBLIC_IP_REPLIER = "http://ipv4.icanhazip.com" 

def main(logger):
    parser = argparse.ArgumentParser(description="Automatically updating GoDaddy's DNS records.")
    parser.add_argument("config", type=str, help="Config file that includes the key, secret, hostname and ttl.")
    parser.add_argument("sleep", type=int, default=60*10, help="Time between each IP address change check (default is 10 minutes)")
    args = parser.parse_args()

    parameters = parse_json_file(args.config)
    key = parameters["key"]
    secret = parameters["secret"]
    ttl = parameters["ttl"]
    name, domain_name = split_hostname(parameters["hostname"])

    logger.info("Starting Dynamic-DNS for {}".format(parameters["hostname"]))

    account = Account(api_key=key, api_secret=secret)
    client = Client(account)

    last_ip_address = get_last_ip(client, name, domain_name)
    logger.info("Last IP address was set to {}".format(last_ip_address))
    try:
        while True:
            ip_address = get_current_ip()
            if ip_address != last_ip_address:
                logger.info("IP address has changed to {}".format(ip_address))
                last_ip_address = ip_address
                if client.update_record(domain_name, {"ttl": ttl, "data": ip_address}, name=name, record_type="A"):
                    logger.info("Updated the record successfully.")
                else:
                    raise Exception("Failed to update the record!")
            sleep(args.sleep)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt has been raised.")

def split_hostname(hostname):
    hostnames = hostname.split(".")
    return hostname[0], ".".join(hostnames[1:])

def get_last_ip(client, name, domain_name):
    return client.get_records(domain_name, record_type="A", name=name)[0]["data"]

def get_current_ip():
    with urlopen(PUBLIC_IP_REPLIER) as response:
        response_content = response.read()
    return response_content.strip().decode("ascii")

def init_logger():
    logger = logging.getLogger()
    logger.setLevel("INFO")
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def parse_json_file(config_path):
    with open(config_path) as config_file:
        config_content = json.load(config_file)
    return config_content

if "__main__" == __name__:
    logger = init_logger()
    main(logger)

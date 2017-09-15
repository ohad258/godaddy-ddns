Introduction
------------
Since some of the internet providers are giving dynamic IP address, there is a need for a program to track the dynamic IP address and
update the DNS records in the domain supplier. This script will check for changes periodically and update the record if necessary.

Dependencies
------------
This script was tested only on Python 3.6
 - GoDaddyPy (`pip install godaddypy`)

Usage
-----
.. code-block:: python
usage: GoDaddyDDNS.py [-h] config sleep

positional arguments:
  config      Config file that includes the key, secret, hostname and ttl.
  sleep       Time between each IP address change check (default is 10 minutes)

optional arguments:
  -h, --help  show this help message and exit
..

The config file is a json built up like that:
```json
{
    "key": "XXX",
    "secret": "XXX",
    "hostname": "@.domain.example",
    "ttl": 3600
}
```

You can obtain the key and the secret key by creating a production key at https://developer.godaddy.com/keys

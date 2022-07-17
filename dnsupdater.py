import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

cf_headers = {
    'X-Auth-Email': os.getenv("CF_EMAIL"),
    'X-Auth-Key': os.getenv("CLOUDFLARE_API"),
    'Content-Type': 'application/json',
}

params = {
    'type': 'A',
    'match': 'all',
}

cf_url = 'https://api.cloudflare.com/client/v4/'
cf_zone = os.getenv("CF_ZONE")

# response = requests.get('https://api.cloudflare.com/client/v4/user', headers=cf_headers)

def get_ip() -> str:
    r = requests.get('https://api.myip.com')
    jr = json.loads(r.content)
    return jr['ip']

def get_zone_records(zone:str):
    r = requests.get(cf_url + 'zones/' + zone + '/dns_records', headers=cf_headers)
    jr = json.loads(r.content)
    return jr

def need_updates(dns:str, ip:str) -> bool:
    return False if dns == ip else True


def main():
    # check ip address
    # compare to dns entry
    # update dns entry for all
    ip = get_ip()
    dns_records = get_zone_records(cf_zone)
    for rec in dns_records['result']:
        if need_updates(rec['content'], ip):
            # update record function
            pass
        else:
            # log non-productive run
            print('DNS is already pointing here.')


main()
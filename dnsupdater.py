import os
import requests
import json
from logger import Logger
from dotenv import load_dotenv

load_dotenv()
logger = Logger()

cf_headers = {
    'X-Auth-Email': os.getenv("CF_EMAIL"),
    'X-Auth-Key': os.getenv("CLOUDFLARE_API"),
    'Content-Type': 'application/json',
}
cf_url = 'https://api.cloudflare.com/client/v4/'
cf_zone = os.getenv("CF_ZONE")

def get_ip() -> str:
    r = requests.get('https://api.myip.com')
    jresponse = json.loads(r.content)
    return jresponse['ip']

def get_zone_records(zone:str):
    r = requests.get(cf_url + 'zones/' + zone + '/dns_records', headers=cf_headers)
    jresponse = json.loads(r.content)
    return jresponse

def need_updates(dns:str, ip:str) -> bool:
    return False if dns == ip else True

def put_updates(name:str, content:str, id:str, zone:str):
    json_data = {
    'type': 'A',
    'name': name,
    'content': content,
    'ttl': 1,
    }
    r = requests.put(cf_url + 'zones/' + zone + '/dns_recors', headers=cf_headers[:1], json=json_data)
    jresponse = json.loads(r.content)
    return jresponse


def main():
    ip = get_ip()
    dns_records = get_zone_records(cf_zone)
    for rec in dns_records['result']:
        if need_updates(rec['content'], ip):
            # update record function
            r = put_updates(rec['name'], rec['content'], rec['id'], cf_zone)
            logger.log(f'{rec["name"]} updated with ip: {rec["content"]}', json.dumps(r))
            # log update
            pass
        else:
            # log non-productive run
            logger.log(f'{rec["name"]} does not need to be updated.')


main()
import requests
import json
import sys
import os

query = str(sys.argv[1])
token = os.environ["MONICA_TOKEN"]

if not token:
    raise Exception("MONICA_TOKEN environment variable not defined")

response = requests.get(
    'https://app.monicahq.com/api/contacts',
    params={"query": query, "limit": 10},
    headers={
        "Authorization": f'Bearer {token}',
        "Accept": "application/json",
    }
)

response.raise_for_status()

matches = response.json()["data"]

# https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
values = [
    {
        'uid': contact["id"],
        'title': f'{contact["first_name"]} {contact["last_name"]}',
        'subtitle': f'Open {contact["first_name"]} {contact["last_name"]} in MonicaHQ',
        'autocomplete': f'{contact["first_name"]} {contact["last_name"]}',
        'arg': f'https://app.monicahq.com/people/{contact["hash_id"]}',
        # Would need to cache the images locally and then provide path to Alfred
        # https://www.alfredforum.com/topic/3873-script-filter-icon-from-url/
        # 'icon': {
        #    "path": contact["information"]["avatar"]["url"],
        # }
    }
    for contact in matches
]

sys.stdout.write(json.dumps({'items': values}))

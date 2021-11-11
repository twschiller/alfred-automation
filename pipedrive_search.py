import requests
import json
import sys
import os

query = str(sys.argv[1])
token = os.environ["PIPEDRIVE_TOKEN"]
company_domain = os.environ["PIPEDRIVE_DOMAIN"]

if not token:
    raise Exception("PIPEDRIVE_TOKEN environment variable not defined")

if not company_domain:
    raise Exception("PIPEDRIVE_DOMAIN environment variable not defined")

if len(query) < 2:
    # Minimum 2 characters required for itemSearch
    sys.stdout.write(json.dumps({'items': []}))

else:
    response = requests.get(
        # https://developers.pipedrive.com/docs/api/v1/ItemSearch
        f'https://{company_domain}.pipedrive.com/api/v1/itemSearch',
        # https://pipedrive.readme.io/docs/core-api-concepts-about-pipedrive-api
        params={"term": query, "item_types": "deal,person,organization,lead", "limit": 10, "api_token": token},
        headers={
            "Accept": "application/json",
        }
    )

    response.raise_for_status()

    matches = response.json()["data"]["items"]


    def select_value(result):
        item = result["item"]
        resource = item["type"]
        title = item["title"] if resource == "deal" else item["name"]

        return {
            'uid': f'{resource}-{item["id"]}',
            'title': title,
            'subtitle': f'Open {title} {resource} in Pipedrive',
            'autocomplete': title,
            'arg': f'https://{company_domain}.pipedrive.com/{resource}/{item["id"]}',
        }


    # https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    values = [select_value(item) for item in matches]

    sys.stdout.write(json.dumps({'items': values}))

from fastapi import FastAPI, HTTPException
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import concurrent.futures

app = FastAPI()

def task(id):
    json_data = {
        'variables': {
            'id': id,
        },
        'query': 'query ($id: String!) {\n  corporate(id: $id) {\n    id\n    name\n    description\n    logo_url\n    hq_city\n    hq_country\n    website_url\n    linkedin_url\n    twitter_url\n    startup_partners_count\n    startup_partners {\n      master_startup_id\n      company_name\n      logo_url: logo\n      city\n      website\n      country\n      theme_gd\n      __typename\n    }\n    startup_themes\n    startup_friendly_badge\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://ranking.glassdollar.com/graphql', json=json_data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Request failed with status code {response.status_code}: {response.text}")

@app.get("/get_results")
def get_results():
    global processing_completed
    if not processing_completed:
        return {"message": "Come back later"}
    else:
        return unique_companies

@app.on_event("startup")
def startup_event():
    # Original code for fetching top-ranked corporates
    json_data = {
        'operationName': 'TopRankedCorporates',
        'variables': {},
        'query': 'query TopRankedCorporates {\n  topRankedCorporates {\n    id\n    name\n    logo_url\n    industry\n    hq_city\n    startup_partners {\n      company_name\n      logo_url: logo\n      __typename\n    }\n    startup_friendly_badge\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://ranking.glassdollar.com/graphql', json=json_data)

    if response.status_code == 200:
        parsed_json = response.json()
        ids = [item["id"] for item in parsed_json["data"]["topRankedCorporates"]]
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Request failed with status code {response.status_code}: {response.text}")

    global unique_companies
    unique_companies = []

    def background_task(task_id):
        result = task(task_id)
        for company in result['data']['corporate']['startup_partners']:
            if all(item['company_name'] != company['company_name'] for item in unique_companies):
                unique_companies.append(company)

    global processing_completed
    with ThreadPoolExecutor() as executor:
        # Submit tasks and get future objects
        futures = [executor.submit(background_task, task_id) for task_id in ids]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

    processing_completed = True
    print("Background tasks completed.")

# Initialize the variable
processing_completed = False



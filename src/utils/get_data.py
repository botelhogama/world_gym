import requests
import pandas as pd
import json
import os
import time
import random


class GetClientData:
    def __init__(self, endpoint="/api/v1/members", take_number=50, unidade='planaltina'):
        self.base_url = "https://evo-integracao.w12app.com.br/"
        self.user = "worldgym"
        if unidade == "itapoa":
            self.password = "44D6E01E-6DFF-4E0F-A787-73F0036496F1"
            self.unidade = unidade
        elif unidade == "planaltina":
            self.password = "D1BC64B6-4EE7-4E16-974E-BD37F2F3DC2E"
            self.unidade = unidade

        self.endpoint = endpoint
        self.params = {
            "take": take_number,
            "skip": 0,
            "onlyPersonal": False,
            "showActivityData": True
        }
        self.data = [ ]

    def make_api_request(self):
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(self.base_url + self.endpoint,
                                        auth=(self.user, self.password),
                                        params=self.params,
                                        timeout=120)  # Increased timeout to 120 seconds
                response.raise_for_status()

                # Debugging Point: Print the status code
                print(f"Status Code: {response.status_code}")

                current_data = response.json()
                self.data.extend(current_data)

                # Debugging Point: Print the number of records fetched so far
                print(f"Total Records So Far: {len(self.data)}")

                if len(current_data) < self.params[ "take" ]:
                    break
                self.params[ "skip" ] += self.params[ "take" ]
                print(f"Retrieved {self.params[ 'skip' ]} records so far")

                # Sleep for a random duration to avoid hitting rate limits
                time.sleep(random.uniform(5, 10.0))

            except requests.exceptions.ReadTimeout:
                retries += 1
                print(f"Request timed out. Attempt {retries} of {max_retries}.")
                time.sleep(random.uniform(5, 10.0))

            except requests.exceptions.RequestException as e:
                print("Error:", e)
                break

    def retrieve_data(self, use_cache=True):
        cache_file_path = f"C:/Users/Pichau/PycharmProjects/worldgym/data/{self.endpoint.replace('/', '_')}_cache.json"

        if use_cache and os.path.exists(cache_file_path):
            with open(cache_file_path, "r") as file:
                self.data = json.load(file)

            # Update the skip parameter to skip already fetched records
            self.params[ "skip" ] = len(self.data)
            print(f"Data loaded from cache for endpoint: {self.endpoint}")
            print(f"Starting data retrieval from record number: {self.params[ 'skip' ] + 1}")

        # Fetch the data from the API, starting from the record after the cached data
        self.make_api_request()
        print(f"Total records retrieved (including cached): {len(self.data)}")

        # Cache the updated data set
        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
        with open(cache_file_path, "w") as file:
            json.dump(self.data, file)
        print("Data cached.")

        df = pd.DataFrame(self.data)
        return df

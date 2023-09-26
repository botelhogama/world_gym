import requests
import pandas as pd
import json
import os

class GetClientData:
    def __init__(self, endpoint="/api/v1/members", take_number=25):
        self.base_url = "https://evo-integracao.w12app.com.br/"
        self.user = "worldgym"
        self.password = "44D6E01E-6DFF-4E0F-A787-73F0036496F1"
        self.endpoint = endpoint
        self.params = {
            "take": take_number,
            "skip": 0,
            "onlyPersonal": False,
            "showActivityData": True
        }
        self.data = []

    def make_api_request(self):
        try:
            while True:
                response = requests.get(self.base_url + self.endpoint, auth=(self.user, self.password), params=self.params)
                response.raise_for_status()

                # Debugging Point: Print the status code
                print(f"Status Code: {response.status_code}")

                current_data = response.json()
                self.data.extend(current_data)

                # Debugging Point: Print the number of records fetched so far
                print(f"Total Records So Far: {len(self.data)}")

                if len(current_data) < self.params["take"]:
                    break
                self.params["skip"] += self.params["take"]
                print(f"Retrieved {self.params['skip']} records so far")

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def retrieve_data(self, use_cache=True):
        cache_file_path = f"C:/Users/Pichau/PycharmProjects/worldgym/data/{self.endpoint.replace('/','_')}_cache.json"

        if use_cache and os.path.exists(cache_file_path):
            with open(cache_file_path, "r") as file:
                self.data = json.load(file)
            print(f"Data loaded from cache for endpoint: {self.endpoint}")
        else:
            self.make_api_request()
            print(f"Total records retrieved: {len(self.data)}")
            os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
            with open(cache_file_path, "w") as file:
                json.dump(self.data, file)
            print("Data cached.")

        df = pd.DataFrame(self.data)
        return df



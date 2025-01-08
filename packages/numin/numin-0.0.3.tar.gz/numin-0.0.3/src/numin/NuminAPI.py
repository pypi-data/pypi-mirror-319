import pandas as pd
import requests
from io import StringIO
import os
import base64
import io 

# Class Definition

class NuminAPI():
    def __init__(self, api_key: str = None):
        """
        Initializes the NuminAPI instance.

        Parameters:
        - api_key (str, optional): The API key for authenticating requests.
        """
        
        self.api_key = api_key
        
        # Published Anvil app's URL
        # https://familiar-subtle-comment.anvil.app
        # self.base_url = "https://beneficial-absolute-depth.anvil.app/_/api" # TEST
        # self.base_url = "https://familiar-subtle-comment.anvil.app/_/api" # Numin BUILD
        self.base_url = "https://numin-tournament.anvil.app/_/api" # Numin PROD

    def get_data(self, data_type: str):
        """
        Fetches the specified type of data (e.g., 'training' or 'round') from the server 
        and returns it as a DataFrame.

        Parameters:
        - data_type (str): The type of data to fetch. Must be 'training' or 'round'.

        Returns:
        - pd.DataFrame: Data from the CSV file.
        """
        if data_type not in ["training", "round"]:
            return {"error": "Invalid data_type. Must be 'training' or 'round'."}

        url = f"{self.base_url}/download_data"
        response = requests.post(url, json={"type": data_type})  # Send type as JSON payload

        if response.status_code == 200:
            if data_type == "round":
                # The endpoint returns the file content; we'll treat response.text as CSV.
                return pd.read_csv(StringIO(response.text))
            elif data_type == "training":
                # Treat the response as a ZIP file and return it as a file-like object
                return io.BytesIO(response.content)
        else:
            return {"error": f"Failed to fetch {data_type} data: {response.text}"}

    def submit_predictions(self, file_path: str):
        """
        Submits predictions to the server by uploading a CSV file.
        Requires API key authentication.

        Parameters:
        - file_path (str): Path to the CSV file with columns ["id", "predictions", "round_no"].

        Returns:
        - dict: JSON response from the server.
        """
        if not self.api_key:
            return {"error": "API key is required to submit predictions."}

        if not os.path.exists(file_path):
            return {"error": f"No such file: '{file_path}'"}

        # Check if required columns are present
        required_columns = ["id", "predictions", "round_no"]
        df = pd.read_csv(file_path, nrows=1)
        if not all(column in df.columns for column in required_columns):
            return {"error": f"CSV file must contain columns: {required_columns}"}

        url = f"{self.base_url}/upload_predictions"
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "text/csv")}
            data = {"api_key": self.api_key}
            
            file_content = base64.b64encode(f.read()).decode('utf-8')

            # Create JSON payload
            payload = {
                "api_key": self.api_key,
                "file_name": os.path.basename(file_path),
                "file_content": file_content,
                "content_type": "text/csv"
            }
                        
            response = requests.post(url, json=payload)

        # return response.text
        try:
            response_data = response.json()  # Parse JSON response
        except ValueError:
            print(f"Raw server response: {response.text}")  # Debugging
            return {"error": f"Server returned non-JSON response: {response.text}"}

        if response.status_code == 200:
            if response_data.get("status") == "success":
                return response_data
            else:
                return {"error": f"Failed to submit predictions: {response_data.get('message', 'Unknown error')}"}
        else:
            return {"error": f"Failed to submit predictions: {response.text}"}

    def get_current_round(self):
        """
        Fetches the current round number from the server.

        Returns:
        - str: The current round number.
        """
        
        url = f"{self.base_url}/get_current_round"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("message")
            else:
                return {"error": f"Failed to get current round: {data.get('message')}"}
        else:
            return {"error": f"Failed to get current round: {response.text}"}
      
    # TODO: Complete the following functions
    def log_predictions(self):
        pass

    def clean_predlog(self):
        pass

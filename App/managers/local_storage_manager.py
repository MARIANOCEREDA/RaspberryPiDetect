import os 
import yaml
import datetime
import json

class LocalStorageManager:

    def __init__(self, package_data:dict) -> None:

        CONFIG_FILE = os.path.dirname(__file__) + "../config/config.yaml"

        with open(CONFIG_FILE) as f:
            self.config = yaml.safe_load(f)
        
        self.package_data = package_data
        self.folder_name = f'{self.config["local_storage_folder"]}/{datetime.date.today()}'
        self.file_name = f"{self.package_data.n_package}.json"
        self.file_path = self.folder_name + f"/{self.file_name}"

    def _write_file_with_data(self):

        with open(self.file_path, "w") as f:
                json.dump(self.package_data, f)


    def store_data(self, package_data:dict):

        # Check if the folder already exists
        if not os.path.exists(self.folder_name):

            os.makedirs(self.folder_name)

            self._write_file_with_data()

            return { "success": True }
            
        else:
            
            self._write_file_with_data()

            return { "success": True }




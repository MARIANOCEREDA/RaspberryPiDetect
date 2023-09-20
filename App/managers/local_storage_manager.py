import os 
import yaml
import datetime
import json
from App.config.logger_config import get_logger

logger = get_logger("PackageDetectAPIRequests")

class LocalStorageManager:

    def __init__(self, config:dict, package_data:dict) -> None:

        self.config = config
        
        self.package_data = package_data
        
        self.folder_name =  os.path.join(f'{self.config["local_storage_folder"]}', str(datetime.date.today()))
        n_package = self.package_data["packageNumber"]
        self.file_name = f"{n_package}.json"
        self.file_path = os.path.join(self.folder_name, self.file_name)

    def _write_file_with_data(self):

        with open(self.file_path, "w") as f:
                json.dump(self.package_data, f)


    def store_data(self) -> None:

        # Check if the folder already exists
        if not os.path.exists(self.folder_name):

            os.makedirs(self.folder_name)

            self._write_file_with_data()

            return { "success": True }
            
        else:
            
            self._write_file_with_data()

            return { "success": True }




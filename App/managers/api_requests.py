import requests
import json
from App.config.logger_config import get_logger
from PyQt5.QtCore import QThread, pyqtSignal

logger = get_logger("PackageDetectAPIRequests")

class PackageDetectAPIRequests(QThread):

    finished = pyqtSignal(dict, dict)

    def __init__(self, config_server_data, parent=None) -> None:
        super().__init__(parent)
        ip = config_server_data["ip"]
        port = config_server_data["port"]
        self.url = f"http://{ip}:{port}/api/v1/package"
        self.package_data = {}

    def request_package(self):

        try:
            response = requests.get(self.url)

            # Verificamos si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:

                logger.info(response.json())
                logger.info("Solicitud GET exitosa")

                return { "success":True }
            
            else:
                
                logger.error(f"Error en la solicitud GET. Código de estado: {response.status_code}")

                return { "success":False }

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud GET: {str(e)}")
    
    def set_package_data(self, data) -> None:
        self.package_data = data

    def run(self):

        # Convierte los datos a formato JSON
        json_data = json.dumps(self.package_data)

        # Define las cabeceras de la solicitud para indicar que se envía JSON
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Realiza la solicitud POST con los datos en el cuerpo
            response = requests.post(self.url, data=json_data, headers=headers, timeout=10)
            
            # Verifica si la solicitud fue exitosa (código de estado 200 o 201, dependiendo de la API)
            if response.status_code in [200, 201]:

                logger.info("Solicitud POST exitosa")

                result = { "success":True, "response":response.text}
            
                self.finished.emit(result, self.package_data)
            
            else:

                logger.error(f"Error en la solicitud POST. Código de estado: {response.status_code}")

                result = { "success":False, "code":response.status_code }
                
                logger.info(response)

                self.finished.emit(result, self.package_data)

        except requests.exceptions.RequestException as e:

            logger.error(f"Error en la solicitud POST: {str(e)}")

            result = { "success":False, "code":"Bad Request"}

            self.finished.emit(result, self.package_data)

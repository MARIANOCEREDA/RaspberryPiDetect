import requests
import json

class PackageDetectAPIRequests:

    def __init__(self, package_data) -> None:
        self.url = "http://20.125.138.87:3000/api/v1/package"
        self.package_data = package_data

    def request_package(self):

        try:
            response = requests.get(self.url)
            # Verificamos si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:

                print(response.json())

                print("Solicitud GET exitosa")

                return { "success":True }
            
            else:
                
                print(f"Error en la solicitud GET. Código de estado: {response.status_code}")

                return { "success":False }

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud GET: {str(e)}")

    def post_package(self):


        # Convierte los datos a formato JSON
        json_data = json.dumps(self.package_data)

        # Define las cabeceras de la solicitud para indicar que se envía JSON
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Realiza la solicitud POST con los datos en el cuerpo
            response = requests.post(self.url, data=json_data, headers=headers)
            
            # Verifica si la solicitud fue exitosa (código de estado 200 o 201, dependiendo de la API)
            if response.status_code in [200, 201]:

                print("Solicitud POST exitosa")
                print("Mensaje de respuesta:")

                return { "success":True, "response":response.text}
            else:

                print(f"Error en la solicitud POST. Código de estado: {response.status_code}")

                return { "success":False, "code":response.status_code }

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud POST: {str(e)}")

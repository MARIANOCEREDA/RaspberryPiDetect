import requests
import json

def request_package():
    url = "http://20.125.138.87:3000/api/v1/package"

    try:
        response = requests.get(url)
        # Verificamos si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            print(response.json())
            print("Solicitud GET exitosa")
            # Puedes imprimir la respuesta si lo deseas
            # print(response.text)
        else:
            print(f"Error en la solicitud GET. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud GET: {str(e)}")

def post_package():

    url = "http://20.125.138.87:3000/api/v1/package"

    # Datos que deseas enviar en el cuerpo de la solicitud como JSON
    data = {
        "packageNumber": 290,
        "sticksAmount": 286,
        "stickType": "medio poste",
        "averageDiameter": 10.71
    }

    # Convierte los datos a formato JSON
    json_data = json.dumps(data)

    # Define las cabeceras de la solicitud para indicar que se envía JSON
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Realiza la solicitud POST con los datos en el cuerpo
        response = requests.post(url, data=json_data, headers=headers)
        
        # Verifica si la solicitud fue exitosa (código de estado 200 o 201, dependiendo de la API)
        if response.status_code in [200, 201]:
            print("Solicitud POST exitosa")
            print("Mensaje de respuesta:")
            print(response.text)
        else:
            print(f"Error en la solicitud POST. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud POST: {str(e)}")


if __name__ == "__main__":

    request_package()
    post_package()
import os
import numpy as np
import cv2

FILTERED_IMAGE_NAME = "image_main_with_boxes.jpg"

def read_results_from_txt(file_path):

    data_list = []

    # Open the file in read mode
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                # Split the line into a list of strings using spaces as separators
                line_data = line.strip().split()
                data_list.append(line_data)

    # Convert the list of lists to a NumPy array
    return np.array(data_list).astype(float)


def get_main_package(packages:np.array) -> np.array:

    main_package = np.empty((1, 4))
    if len(packages) > 1:

        areas = np.array([ p[3] * p[4] for p in packages])
        max_area_index = np.argmax(areas)
        main_package = packages[max_area_index]
    
    else:
        main_package = packages[0]
    return main_package

            
def filter_sticks_within_package(sticks:np.array, package:np.array) -> np.array:

    _, x, y, w, h = package
    x_max = x + w / 2
    x_min = x - w / 2
    y_max = y + h / 2
    y_min = y - h / 2

    filtered_sticks = []

    for stick in sticks:
        _, x_s, y_s, w_s, h_s = stick

        # Verifica si el centro del stick está dentro del área del paquete
        if x_min < x_s < x_max and y_min < y_s < y_max:
            filtered_sticks.append(stick)

    return np.array(filtered_sticks)
def draw_package_and_sticks(image_path:str, main_package_dims, sticks_within_package:int, config_data:dict) -> str:

    # Load image
    image1 = cv2.imread(image_path)
    img_size,_,_=image1.shape

    white_image = np.zeros((img_size, img_size, 3), dtype=np.uint8)
    alpha = 50

    # Dibujar el recuadro del paquete principal en verde
    _, x, y, w, h = main_package_dims * img_size

    #cv2.rectangle(image1, (int(x - w / 2), int(y + h / 2)), (int(x + w / 2), int(y - h / 2)), (0, 255, 0), 2)
    cv2.circle(image1, (int(x), int(y)), int(((w+h)/4)), (0, 255, 0), 2)

    # Draw rectangles 
    for stick in sticks_within_package:
        _, x_s, y_s, w_s, h_s = stick * img_size
        cv2.circle(white_image, (int(x_s), int(y_s)), int((w_s+h_s)/4), (0, 255, 255), -1)
        cv2.circle(image1, (int(x_s), int(y_s)), int((w_s+h_s)/4), (0, 255, 255), 2)
    
    result = cv2.addWeighted(image1, 1 - (alpha / 255.0), white_image, (alpha / 255.0), 0)
    
    # Store image 
    output_path = os.path.join(os.path.dirname(_file_) + "/../", config_data["images"]["results"] + "/" + FILTERED_IMAGE_NAME)

    cv2.imwrite(output_path, result)

    return output_path



def cut_image(image_path, config_data):
    image_cut = cv2.imread(image_path)
    output_path = os.path.join(os.path.dirname(__file__),config_data["images"]["results"])

    # Obtener las dimensiones de la imagen y centro
    h, w, _ = image_cut.shape 
    x_c = w//2
    y_c = h//2
    pixels_overlap = 50

    # Cortar la imagen en cuatro partes
    top_left = image_cut[0:x_c + pixels_overlap, 0:y_c + pixels_overlap]
    top_right = image_cut[x_c - pixels_overlap:w, y_c - pixels_overlap:h]
    bottom_left = image_cut[y_c:h, 0:x_c]
    bottom_right = image_cut[y_c:h, x_c:w]

    #Agrandamos las imagenes a 640
    top_left = cv2.resize(top_left, (w, h))
    top_right = cv2.resize(top_right, (w, h))
    bottom_left = cv2.resize(bottom_left, (w, h))
    bottom_right = cv2.resize(bottom_right, (w, h))

    # Guardar las imágenes cortadas
    cv2.imwrite(os.path.join(os.path.dirname(__file__),config_data["images"]["results"],'top_left.jpeg'), top_left)
    cv2.imwrite(os.path.join(os.path.dirname(__file__),config_data["images"]["results"],'top_right.jpeg'), top_right)
    cv2.imwrite(os.path.join(os.path.dirname(__file__),config_data["images"]["results"],'bottom_left.jpeg'), bottom_left)
    cv2.imwrite(os.path.join(os.path.dirname(__file__),config_data["images"]["results"],'bottom_right.jpeg'), bottom_right)



def calculate_sticks_diameter(package_diameter:float, img_size:int, main_package_size:np.array, sticks_within_package:int) -> float:

    _, x_d, y_d, w_d, h_d = main_package_size * img_size

    diam_mainpackage_pixel= (w_d+h_d) / 2 #tomamos el diametro en pixeles como el promedio entra la altura y ancho

    rel_pixeles_cm = diam_mainpackage_pixel / package_diameter

    diam_sticks=[]

    for stick in sticks_within_package:

        _, x_s, y_s, w_s, h_s=stick*img_size

        diam_stick_pixel=(w_s+h_s)/2

        diam_stick_cm = diam_stick_pixel / rel_pixeles_cm

        diam_sticks.append(diam_stick_cm)

    return(diam_sticks)


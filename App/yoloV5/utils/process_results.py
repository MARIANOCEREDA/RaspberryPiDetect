import os
import numpy as np
import cv2

FILTERED_IMAGE_NAME = "image_main_with_boxes.jpeg"

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

    return (filtered_sticks)
def draw_package_and_sticks(image_path:str, sticks_within_package:int, config_data:dict) -> str:

    # Load image
    image1 = cv2.imread(image_path)
    img_size_h,img_size_w,_=image1.shape
    white_image = np.zeros((img_size_h, img_size_w, 3), dtype=np.uint8)
    alpha = 50
    # Dibujar el recuadro del paquete principal en verde
    #_, x, _, w, _ = main_package_dims * img_size_w
    #_, _, y, _, h = main_package_dims * img_size_h

    #r=max(int(w)/2,int(h)/2)

    #cv2.rectangle(image1, (int(x - w / 2), int(y + h / 2)), (int(x + w / 2), int(y - h / 2)), (0, 255, 0), 2)
    #cv2.circle(image1, (int(x), int(y)), int(r), (0, 255, 0), 2)

    # Draw circles 
    for stick in sticks_within_package:
        _, x_s, _, w_s, _ = stick * img_size_w
        _, _, y_s, _, h_s = stick * img_size_h
        cv2.circle(white_image, (int(x_s), int(y_s)), int((w_s+h_s)/4), (0, 255, 255), -1)
        cv2.circle(image1, (int(x_s), int(y_s)), int((w_s+h_s)/4), (0, 255, 255), 2)
    
    result = cv2.addWeighted(image1, 1 - (alpha / 255.0), white_image, (alpha / 255.0), 0)
    
    # Store image 
    output_path = os.path.join(os.path.dirname(__file__) + "/../", config_data["images"]["results"] + "/" + FILTERED_IMAGE_NAME)
    cv2.imwrite(output_path, result)

    return output_path


def calculate_sticks_diameter(distance_to_package:float, image_path:str, sticks_within_package:int, camera) -> float:

    print(distance_to_package)

    # Calcula la relación entre cm reales y cm en la imagen para el objeto de referencia 
    rel_cm_cm_w = camera["w_obj_real_cm"] / camera["w_obj_ref_cm"] 
    rel_cm_cm_h = camera["h_obj_real_cm"] / camera["h_obj_ref_cm"]

    rel_cm_cm_w = distance_to_package * rel_cm_cm_w / int(camera["distance_cm"])
    rel_cm_cm_h = distance_to_package * rel_cm_cm_h / int(camera["distance_cm"])

    # Calcula la relación entre píxeles y centímetros en la imagen para el objeto de referencia
    rel_cm_px_w = camera["w_obj_ref_cm"]/ camera["w_obj_ref_px"] 
    rel_cm_px_h = camera["h_obj_ref_cm"] / camera["h_obj_ref_px"] 

    # Escalado para la distancia real.
    rel_cm_px_w = distance_to_package * rel_cm_px_w / int(camera["distance_cm"])
    rel_cm_px_h = distance_to_package * rel_cm_px_h / int(camera["distance_cm"])

    image1 = cv2.imread(image_path)
    img_size_h,img_size_w,_=image1.shape

    # _, x_d, _, w_d, _ = main_package_size * img_size_w
    # _, _, y_d, _, h_d = main_package_size * img_size_h


    # diam_mainpackage_pixel= (w_d+h_d) / 2 #tomamos el diametro en pixeles como el promedio entra la altura y ancho

    # rel_pixeles_cm = diam_mainpackage_pixel / package_diameter

    diam_sticks=[]

    for stick in sticks_within_package:
        
        _, x_s, _, w_s, _ = stick * img_size_w #tomamos el ancho y alto de cada palo detectado en pixeles
        _, _, y_s, _, h_s = stick * img_size_h

        # Calcula el tamaño real del objeto de interés en centímetros
        w_s_cm = w_s * rel_cm_px_w
        h_s_cm = h_s * rel_cm_px_h

        w_cm_real= w_s_cm * rel_cm_cm_w
        h_cm_real= h_s_cm * rel_cm_cm_h

        diam_stick_cm=(w_cm_real+h_cm_real)/2
        diam_sticks.append(diam_stick_cm)

    prom_diameters = sum(diam_sticks)/len(diam_sticks)
    index_delete=[]
    print(prom_diameters)
    #Para eliminar los palos que estan detras del fardo principal.
    for i in range(len(diam_sticks)):
        if diam_sticks[i]<prom_diameters*0.6:
            index_delete.append(i)

    for index in reversed(index_delete):
        del diam_sticks[index]
        del sticks_within_package[index]


    return (diam_sticks,sticks_within_package)


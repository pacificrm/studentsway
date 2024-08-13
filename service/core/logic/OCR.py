# import json
# import cv2
import numpy as np
# import service.main as s
# import time
import easyocr
from PIL import Image

# Load images
image_path_1 = '/home/agustus/8thSem/IDs/studentid_7.png'
# image_path_2 = '/home/agustus/8thSem/IDs/studentid_4.png'

reader = easyocr.Reader(['en'])

def extract_text_from_image(image):
    # image = Image.open(image)
    # image = np.array(image)
    # if isinstance(image, np.ndarray):
    #     image = Image.fromarray(image)
    # image = image.resize((1024, 1024))
    text_lines = reader.readtext(image)
    print(text_lines)
    info = {
        "School Name": None,
        "Student Name": None,
        "Father's Name": None,
        "Class": None,
        "Address": None
    }
    
    for i, line in enumerate(text_lines):
        if "School" in line[-2] and info["School Name"] is None:
            info["School Name"] = line[-2]
        elif "Name" in line[-2] and info["Student Name"] is None:
            if i + 1 < len(text_lines):
                info["Student Name"] = text_lines[i + 1][-2]
        elif "Class" in line[-2] and info["Class"] is None:
            if i + 1 < len(text_lines):
                info["Class"] = text_lines[i + 1][-2]
        elif ("Address" in line[-2] or "Add." in line[-2]or "Add_" in line[-2])  and info["Address"] is None:
            if i + 1 < len(text_lines):
                info["Address"] = text_lines[i + 1][-2]
        elif ("Father" in line[-2] or "F Name" in line[-2] or "F / Name" in line[-2] or "S/D of Mr" in line[-2]) and info["Father's Name"] is None:
            if i + 1 < len(text_lines):
                info["Father's Name"] = text_lines[i + 1][-2]


    for key in info:
        if info[key] is None:
            info[key] = ""

    return info


# info_1 = extract_text_from_image( image_path_1)

# print("\nConsolidated Information from Image 1:")
# for key, value in info_1.items():
#     print(f"{key}: {value}")


# def skindisease_detector(img_array):
#     # Load skin diseases from the JSON file
#     with open('service/core/logic/skindisease.json', 'r') as file:
#         skin_diseases = json.load(file)['skin_diseases']
    
#     # Model inference
#     time_init = time.time()
#     test_image = cv2.resize(img_array, (256, 256))
#     im = np.float32(test_image)
#     img_array = np.expand_dims(im, axis=0)

#     onn_pred = s.m_q.run(['dense'], {"input_1": img_array})

#     time_elapsed = time.time() - time_init
#     disease_index = np.argmax(onn_pred[0][0])
#     disease_info = skin_diseases[disease_index]

   

#     return {
#         "disease": disease_info['name'],
#         "overview": disease_info['overview'],
#         "symptoms": disease_info['symptoms'],
#         "causes": disease_info['causes'],
#         "treatments": disease_info['treatments'],
#         "probability": float(onn_pred[0][0][disease_index]),
#         "time": str(time_elapsed)
#     }
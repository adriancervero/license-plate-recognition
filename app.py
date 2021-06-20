import streamlit as st
import os
from PIL import Image
import random
import easyocr

from detect import detect

IMAGE_FOLDER = 'dataset/val/images'
DETECTIONS_FOLDER = 'runs/detect/exp'
CROP_FOLDER = 'runs/detect/exp/crops/license'
test_image = 'dataset/val/images/Cars10.png'




def pick_random_image():
    image_list = os.listdir(IMAGE_FOLDER)
    idx = random.randint(0, len(image_list)-1)
    rand_image = image_list[idx]
    
    return str(os.path.join(IMAGE_FOLDER, rand_image))

def read_plate(image_path):
    reader = easyocr.Reader(['en'])
    ocr_result = reader.readtext(image_path)
    result = ' '.join([item[1] for item in ocr_result])
    
    return result


#### SIDEBAR #########################

st.sidebar.write('Upload an image...')

uploaded_file = st.sidebar.file_uploader('', 
                                        type=['png', 'jpg', 'jpeg'],
                                        accept_multiple_files=False)
st.sidebar.write('Or click this button to pick a random image from repository')
random_image_bt = st.sidebar.button('Random Image')

confidence_threshold = st.sidebar.slider('Confidence threshold:',0.0, 1.0, 0.5, 0.01)

######### Main APP ##############
# Title
st.title('License plate recognition')
# subtitle
st.text('I applied transfer learning to a Yolov5 net and retrained it\nto detect car license plates. Then I performed character recognition\nusing EasyOCR.')
st.text('Author: Adrián Cerveró')
st.text('GitHub: https://github.com/adriancervero/license-plate-recognition')


   
with open('image_path.txt', 'r') as f:
    image_path = f.readline()

#image_st = st.empty()
detect_bt = st.button('Detect')
if detect_bt:
    detect(source=image_path,
            weights='trained/best.pt',
            save_crop=True,
            name='exp',
            exist_ok=True,
            conf_thres=float(confidence_threshold))

    file_name = image_path.split('/')[-1]
    detection_file = os.path.join(DETECTIONS_FOLDER, file_name)
    image_path = detection_file
    
    #image = Image.open(image_path)
    #st.image(image)
else:
    if random_image_bt:
        image_path = pick_random_image()
        with open('image_path.txt', 'w') as f:
            f.write(image_path)
    

    elif uploaded_file is not None:
        image_path = 'tempImage.png'
        with open(image_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        with open('image_path.txt', 'w') as f:
            f.write(image_path)

col1, col2 = st.beta_columns(2)

# Display Images
image = Image.open(image_path)
col1.image(image, use_column_width=True)

if detect_bt:
    ## display crop image with the plate
    file_name = image_path.split('/')[-1].split('.')[0] + '.jpg'
    crop_image_path = os.path.join(CROP_FOLDER, file_name)
    crop_image = Image.open(crop_image_path)
    col2.image(crop_image, use_column_width=True)

    # display plate content
    plate_text = read_plate(crop_image_path)

    col2.text('Text recognized:')
    if plate_text == '':
        col2.text('None')
    else:
        display_text = f'<p style="font-family:Monospace; color:Black; font-size: 20px;">{plate_text}</p>'
        col2.markdown(display_text, unsafe_allow_html=True)

    # clean crop images folder
    for file_name in os.listdir(CROP_FOLDER):
        if file_name.endswith('.jpg'):
            file_path = os.path.join(CROP_FOLDER, file_name)
            os.remove(file_path)



    

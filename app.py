import streamlit as st
import os
from PIL import Image
import random

from detect import detect

IMAGE_FOLDER = 'dataset/val/images'
DETECTIONS_FOLDER = 'runs/detect/exp'
test_image = 'dataset/val/images/Cars10.png'



def pick_random_image():
    image_list = os.listdir(IMAGE_FOLDER)
    idx = random.randint(0, len(image_list)-1)
    rand_image = image_list[idx]
    
    return str(os.path.join(IMAGE_FOLDER, rand_image))


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

   
with open('image_path.txt', 'r') as f:
    image_path = f.readline()






if st.button('Detect'):
    detect(source=image_path,
            weights='trained/best.pt',
            save_crop=True,
            name='exp',
            exist_ok=True)

    file_name = image_path.split('/')[-1]
    image_path = os.path.join(DETECTIONS_FOLDER, file_name)
    image = Image.open(image_path)
    st.image(image)
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

    # Display Image
    image = Image.open(image_path)
    st.image(image)

    

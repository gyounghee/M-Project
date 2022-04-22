import cv2, os, shutil, math
import numpy as np

from PIL import Image
from re import X

# tensorflow
from tensorflow.keras.models import load_model 
# Pytorch
import torch
from torchvision import transforms


####### 모델 keras CNN - 말티즈, 비글, 치와와    
def img_predict_keras(dog_breed, selected_model, decode_img, img_name):
    model_path = 'dog_models'
    old_path = f'Image_check'
    new_path = f'Image/{dog_breed}'

    shutil.move(f'{old_path}/{img_name}', f'{new_path}/{img_name}')

    model = load_model(f'{model_path}/{selected_model}')

    kernel = np.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]]) # 커널 생성

    # 이미지를 선명하게
    image_sharp = cv2.filter2D(decode_img, -1, kernel)
    # scaling
    image_sharp = image_sharp / 255
    # dsize
    dst = cv2.resize(image_sharp, dsize=(299, 299))

    test = (np.expand_dims(dst, 0))

    predict_prob = model.predict(test)

    accuracy = int( 100 - ( round(predict_prob[0][0],2) * 100 ) ) 
    # print( round(predict_prob[0][0],2) * 100 )

    if round(predict_prob[0][0],2) > 0.5 :
        result = {'result':'정상', 'accuracy' : accuracy, 'text': "당신의 강아지는 정상입니다" }
        return result
    else :
        result = {'result':'비만', 'accuracy' : accuracy, 'text': "당신의 강아지는 비만입니다" }
        return result  


# # predict.py 안에서 TEST  
# import base64, io, cv2
# import numpy as np
# from PIL import Image
# def stringToRGB(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     dataBytesIO = io.BytesIO(imgdata)
#     image = Image.open(dataBytesIO)
#     return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# img_path = 'Image_check/one.jpg'
# img_name = 'one.jpg'

# with open(img_path, 'rb') as img:
#     base64_str = base64.b64encode(img.read())

# print( img_predict_keras('Maltese','maltese_3.1.h5',stringToRGB(base64_str), img_name) )



###### 모델이 Pytorch - 리트리버, 웰시코기, 닥스훈트
def trim(image):
    h, w = image.shape[0], image.shape[1]
    # The center of a image
    X, Y = int(w/2), int(h/2)

    if w > h :    # 폭 > 높이 : 가로 방향
        img_trim = image[ : ,  X-int(h/2) : X+int(h/2)  ]
    elif w < h :  # 폭 < 높이 : 세로 방향
        img_trim = image[  Y-int(w/2) : Y+int(w/2)  , : ]
    else :        # 폭 = 높이 : 정방형
        img_trim = image
    
    return img_trim 


def img_predict_torch(dog_breed, selected_model, decode_img, img_name):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # device 객체

    model_path = 'dog_models'

    old_path = f'Image_check'
    new_path = f'Image/{dog_breed}'

    shutil.move(f'{old_path}/{img_name}', f'{new_path}/{img_name}')

    # 모델 업로드 
    model = torch.load(f'{model_path}/{selected_model}', map_location='cpu')
    
    kernel = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])

    if dog_breed == 'Retriever' : 
        image_sharp = cv2.filter2D(decode_img, -1, kernel)  ## 이미지 선명하게
        image_tmp = image_sharp

    elif dog_breed == 'Dachshund':
        trim_img = trim(decode_img)
        image_yuv = cv2.cvtColor(trim_img, cv2.COLOR_BGR2YUV)
        image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])  ## yuv 적용
        image_sharp = cv2.filter2D(image_yuv, -1, kernel)  ## 이미지 선명하게
        image_tmp = image_sharp

    elif dog_breed == 'Welsh Corgi':
        image_sharp = cv2.filter2D(decode_img, -1, kernel)  ## 이미지 선명하게
        sobelx = cv2.Sobel(image_sharp, cv2.CV_8U, 1, 0, ksize=3)  
        image_tmp = sobelx

    cv2.imwrite(f'{new_path}/gh{img_name}', image_tmp)

    ## test 전처리 
    transforms_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    class_names = ['비만', '정상']

    ## 이미지 업로드 
    image = Image.open(f'{new_path}/gh{img_name}')
    image = transforms_test(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
    
    ## 전처리 된 이미지 파일 삭제
    os.remove(f'{new_path}/gh{img_name}')

    ## 비만일 확률
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    accuracy = int(round(probabilities[0].item() * 100, 0))

    print(f'비만율 : {probabilities[0].item()}')

    if class_names[preds[0]] == '정상':
        result = {'result':'정상', 'accuracy' : accuracy, 'text': "당신의 강아지는 정상입니다" }
        return result
    else :
        result = {'result':'비만', 'accuracy' : accuracy, 'text': "당신의 강아지는 비만입니다" }
        return result


# ## predict.py 안에서 TEST2  
# import base64, io, cv2
# import numpy as np
# from PIL import Image

# def stringToRGB(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     dataBytesIO = io.BytesIO(imgdata)
#     image = Image.open(dataBytesIO)
#     return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# img_path = 'Image_check/three.jpg'
# img_name = 'three.jpg'

# with open(img_path, 'rb') as img:
#     base64_str = base64.b64encode(img.read())

# testresult = img_predict_torch('Retriever','ret_set5_B_9_1.pth',stringToRGB(base64_str), img_name) 
# print(testresult['text'])
# print(testresult['accuracy'])



####### 정상 / 비만 예측 전 개(성견)인지 확인
def dog_check(decode_img, img_name):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # model = torch.load('dog_models/precondition_set1_B20_E49.pth', map_location='cpu')
    model = torch.load('dog_models/precondition_set1_B20_E49.pth', map_location='cpu')

    img_path = 'Image_check'

    cv2.imwrite(f'{img_path}/{img_name}', decode_img)

    transforms_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    class_names = ['cat', 'dog', 'human']
    
    image = Image.open(f'{img_path}/{img_name}')
    image = transforms_test(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        
    if class_names[preds[0]] == 'dog':
        return True
    else : 
        return False


# # predict.py 안에서 TEST  
# import base64, io, cv2
# import numpy as np
# from PIL import Image
# def stringToRGB(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     dataBytesIO = io.BytesIO(imgdata)
#     image = Image.open(dataBytesIO)
#     return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# img_path = 'three.jpg'
# img_name = 'cat.jpg'

# with open(img_path, 'rb') as img:
#     base64_str = base64.b64encode(img.read())

# print(dog_check(stringToRGB(base64_str), img_name))
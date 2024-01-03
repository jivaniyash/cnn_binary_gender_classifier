from fastapi import APIRouter, Path, Depends, HTTPException
from app.models import ImageURLIn, ClassificationResult

from tensorflow as keras
# import matplotlib.pyplot as plt
from keras import models
from keras.preprocessing import image
# import cv2
import wget

router = APIRouter(
    include_in_schema=True,
)

#test
@router.get("/ping/{ping_message}")
def home(ping_message):
    return {'ping_message':ping_message}


print('...........Started.............')
pipeline = models.load_model('image-classifier-f-m.keras')

@router.post("/classify/", response_model=ClassificationResult)
def predict_image(data: ImageURLIn):
    img_url = data.img_url
    # return ClassificationResult(img_url=img_url)
    # file_name = 'image.jpg'
    try:
        # print('Downloading ...')

        img = wget.download(img_url)
        # print('\n Download Complete')
    except Exception as e:
        # print(e)
        # raise HTTPException(status_code=403, detail=f'Error downloading image. Please check the url - {img} :####: {img_url}')
        return e

    # img = cv2.imread(file_name)

    # plt.imshow(img)

    # img_np = cv2.resize(img, (64,64))

    img_np = image.img_to_array(image.load_img(img, target_size=(64,64)))
    test_img = img_np.reshape((1,64,64,3))

    try:
        y = pipeline(test_img/64, training=False)
        out = y.numpy()[0][0]
        output = round(out)
    except:
        # print('Issue with output prediction')
        return
        
    if output == 0:
        prob = 1-out # probability of predicting output
        img_class = "Female"
    elif output == 1:
        prob = out
        img_class = "Male"
    else:
        # print('there is some problem - output:- ', str(output))
        return

    return ClassificationResult(img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob)
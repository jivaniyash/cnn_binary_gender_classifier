from fastapi import APIRouter, Response, Query, status
from app.models import ImageURLIn, ClassificationResult
from app.services import gender_classification_pipeline, digit_classification_pipeline
from app.mongodb import insert_one_doc, find_doc, check_mongo_connection
import json
from datetime import datetime

router = APIRouter(
    include_in_schema=True,
)

@router.get("/ping/")
def custom_ping_message(ping_message: str = Query(description="Add your custom message to check if its returning the same message")):
    return {'ping_message':ping_message}

@router.get("/ping_mongo/", description="Try it out to check if mongodb is connected")
def ping_mongo():

    ping_message = check_mongo_connection()
    
    return ping_message

@router.get("/results/")
def retreive_prediction(model: str = Query(description="Model name", enum=["gender-classifier", "digit_classifier"]),
                        img_url: str = Query(description="URL of the image")):
    ''' 
    Get the classification results of the given image url from mongoDB collection
    '''
    ping_message = check_mongo_connection()

    if ping_message == {'ok': 0.0}:
        return {"status":"mongo connection error"}
    
    doc_status, doc = find_doc(model=model, img_url=img_url)
    if doc_status:
        doc.pop("_id") # remove _id column
        return doc
    else:
        return {"status":"Doc not found"}

@router.post("/classify/gender/")
def classify_gender(data: ImageURLIn, response:Response):
    model = 'gender-classifier'
    img_url = data.img_url # fetch img_url from client request

    # find if doc is inserted in the collections
    doc = retreive_prediction(model=model, img_url=img_url)

    if doc not in  [{"status":"Doc not found"}, {"status":"mongo connection error"}]: # if doc is found in mongodb 
        return doc
    
    # if doc is not found
    img_class, prob = gender_classification_pipeline(img_url=img_url) # run pipeline

    # set doc status
    doc_status = "Failed to Add Record: mongo-connection error"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if doc == {"status":"mongo connection error"}:
        return ClassificationResult(timestamp=timestamp,
                                img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob,
                                doc_status=doc_status,
                                model=model)
    
    if img_class in ["Male", "Female"]:
        try:
            document = insert_one_doc(img_url, img_class, prob, model=model)
            timestamp = document['timestamp']
            doc_status = 'inserted'
            response.status_code = status.HTTP_201_CREATED
        except:
            pass

    return ClassificationResult(timestamp=timestamp,
                                img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob,
                                doc_status=doc_status,
                                model=model)

@router.post("/classify/digit/")
def classify_digit(data: ImageURLIn, response:Response):
    model = 'digit-classifier'
    img_url = data.img_url # fetch img_url from client request

    # find if doc is inserted in the collections
    doc = retreive_prediction(model=model, img_url=img_url)

    if doc not in  [{"status":"Doc not found"}, {"status":"mongo connection error"}]: # if doc is found in mongodb 
        return doc
    
    # if doc is not found
    img_class, prob = digit_classification_pipeline(img_url=img_url) # run pipeline

    # set doc status
    doc_status = "Failed to Add Record: mongo-connection error"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if doc == {"status":"mongo connection error"}:
        return ClassificationResult(timestamp=timestamp,
                                img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob,
                                doc_status=doc_status,
                                model=model)
    
    if int(img_class) in range(10):
        try:
            document = insert_one_doc(img_url, img_class, prob, model=model)
            timestamp = document['timestamp']
            doc_status = 'inserted'
            response.status_code = status.HTTP_201_CREATED
        except:
            pass

    return ClassificationResult(timestamp=timestamp,
                                img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob,
                                doc_status=doc_status,
                                model=model)
from fastapi import APIRouter, Response, Query, status
from app.models import ImageURLIn, ClassificationResult
from app.services import run_pipeline
from app.mongodb import insert_one_doc, find_doc
import json
from datetime import datetime

router = APIRouter(
    include_in_schema=True,
)

#test
@router.get("/ping/{ping_message}")
def home(ping_message):
    return {'ping_message':ping_message}

@router.get("/classify/")
def retreive_prediction(img_url: str = Query()):

    doc_status, doc = find_doc(img_url=img_url)
    if doc_status:
        doc.pop("_id") # remove _id column
        return doc
    else:
        return {'status':'Doc not found'}

@router.post("/classify/")
def classify_image(data: ImageURLIn, response:Response):

    img_url = data.img_url # fetch img_url from client request

    # find if doc is inserted in the collections
    doc = retreive_prediction(img_url)

    if doc != {'status':'Doc not found'}: # if doc is found in mongodb 
        return doc
    
    # if doc is not found
    img_class, prob = run_pipeline(img_url=img_url) # run pipeline

    # set doc status
    doc_status = "Failed to Add Record: INVALID OUTPUT"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if img_class in ["Male", "Female"]:
        try:
            document = insert_one_doc(img_url, img_class, prob)
            timestamp = document['timestamp']
            doc_status = 'inserted'
            response.status_code = status.HTTP_201_CREATED
        except:
            pass

    return ClassificationResult(timestamp=timestamp,
                                img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob,
                                doc_status=doc_status)
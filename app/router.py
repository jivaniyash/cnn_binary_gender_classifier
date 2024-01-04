from fastapi import APIRouter, Response, status
from app.models import ImageURLIn, ClassificationResult
from app.services import run_pipeline
from app.mongodb import insert_one_doc

router = APIRouter(
    include_in_schema=True,
)

#test
@router.get("/ping/{ping_message}")
def home(ping_message):
    return {'ping_message':ping_message}

@router.post("/classify/", response_model=ClassificationResult, status_code=status.HTTP_200_OK)
def classify_image(data: ImageURLIn, response:Response):

    img_url = data.img_url # fetch img_url from client request

    img_class, prob = run_pipeline(img_url=img_url) # run pipeline

    # set doc status
    doc_status = "Failed to Add Record: INVALID OUTPUT"

    if img_class in ["Male", "Female"]:
        doc = insert_one_doc(img_url, img_class, prob)
        doc_status = 'inserted' if doc else 'failed to insert doc'
        if doc_status == 'inserted': # if doc is inserted in MongoDB, change repsone status code
            response.status_code = status.HTTP_201_CREATED

    return ClassificationResult(img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob,
                                doc_status=doc_status)
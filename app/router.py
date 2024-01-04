from fastapi import APIRouter, Path, Depends, HTTPException
from app.models import ImageURLIn, ClassificationResult
from services import run_pipeline

router = APIRouter(
    include_in_schema=True,
)

#test
@router.get("/ping/{ping_message}")
def home(ping_message):
    return {'ping_message':ping_message}

@router.post("/classify/", response_model=ClassificationResult)
def classify_image(data: ImageURLIn):

    img_url = data.img_url # fetch img_url from client request

    img_class, prob = run_pipeline(img_url=img_url)

    return ClassificationResult(img_url=img_url,
                                img_class=img_class,
                                img_pred_prob=prob)
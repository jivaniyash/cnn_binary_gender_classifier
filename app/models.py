from pydantic import BaseModel

class ImageURLIn(BaseModel):
    img_url: str
    
class ClassificationResult(BaseModel):
    timestamp: str
    img_url: str
    img_class: str
    img_pred_prob: float
    doc_status: str
    model: str
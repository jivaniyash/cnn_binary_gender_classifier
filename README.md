# IMAGE PREDICTION USING CNN

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)

## Overview
This Project is used to predict gender - male/female & hand-written digit in an image. There are 2 models - 
- Gender Model has 6-layered architecture. Model is trained using 4-CNN, 2-Dense-Fully connected layer.
- Digit Classifier Model has 3-layered architecture - trained using [https://www.tensorflow.org/datasets/catalog/mnist](MNIST) dataset

If you want to run project using Gradio, follow the steps - https://github.com/jivaniyash/image_classifier_app/tree/gradio or can open huggingface - https://huggingface.co/spaces/jivaniyash/demo-image-classifier

If you want to run project, it is currently depolyed using gcloud run - https://tensorflow-kq4trppvsa-uc.a.run.app/

Instructions for deploying in GCP - [gcloud.md](https://github.com/jivaniyash/image_classifier_app/blob/main/gcloud.md)

## Getting Started

### Prerequisities

- git
- docker
- docker-compose

### Installation

1. Clone the Repository
    ```bash
    git clone https://github.com/jivaniyash/image_classifier_app.git
    ```

2. Navigate to project directory
    ```bash
    cd image_classifier_app
    ```
## Usage

To build Docker Image and predict gender from image
```bash
docker compose up --build
```

This command will build docker image and run uvicorn app at `http://0.0.0.0:8080`. If you face any issue with port, run `http://localhost:8080` in your browser. It will open OpenAPI web Swagger UI, you can use `/classify/gender/` and `/classify/digit` API endpoint to test the model.

Please make sure that the image link you provide for prediction is working and downloadable.

- [https://github.com/jivaniyash/cnn_binary_gender_classifier/blob/main/models/gender-classifier.keras](gender-classifier.keras)` file contians gender-classifier model weights & params which is used to predict the gender. 
- [https://github.com/jivaniyash/cnn_binary_gender_classifier/blob/main/models/digit-classifier.keras](digit-classifier.keras) file contians digit-classifier model weights & params which is used to recognize and classify digit (0-10). 
---

- [https://github.com/jivaniyash/cnn_binary_gender_classifier/blob/main/colab-notebook/Gender_Classifier.ipynb](Gender_Classifier.ipynb) - juptyer notebook contains steps for training the gender-classifier model.

- [https://github.com/jivaniyash/cnn_binary_gender_classifier/blob/main/colab-notebook/Digit_Classifier.ipynb](Digit_Classifier.ipynb)  - juptyer notebook contains steps for training the digit-classifier model.
 
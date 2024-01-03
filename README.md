# GENDER PREDICTION USING CNN

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)

## Overview
This Project is used to predict gender - male/female in an image. Model has 6-layered architecture. Model is trained using 4-CNN, 2-Dense-Fully connected layer. 

## Getting Started

### Prerequisities

- git
- docker
- docker-compose

### Installation

1. Clone the Repository
    ```bash
    git clone https://github.com/jivaniyash/cnn_binary_gender_classifier.git
    ```

2. Navigate to project directory
    ```bash
    cd cnn_binary_gender_classifier
    ```
## Usage

To build Docker Image and predict gender from image
```bash
docker compose up --build
```

This command will build docker image and run uvicorn app at `http://0.0.0.0:8080`. If you face any issue with port, run `http://localhost:8080` in your browser. It will open OpenAPI web Swagger UI, you can use `/classify/` API endpoint to test the image.

Please make sure that the image link you provide for prediction is working and downloadable.

[https://github.com/jivaniyash/cnn_binary_gender_classifier/blob/main/image-classifier-f-m.keras](image-classifier-f-m.keras)` file contians model weights & params which is used to predict the gender.

[https://github.com/jivaniyash/cnn_binary_gender_classifier/blob/main/colab-notebook/Image_Classifier_gender.ipynb](colab-notebook/Image_Classifier_gender.ipynb) - juptyer notebook contains steps for training the model. 

 
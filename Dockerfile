FROM tensorflow/tensorflow:latest

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR  /app

COPY . /app

RUN pip install -r requirements.txt

# set env variable indide container to aviod TF errors
ENV TF_ENABLE_ONEDNN_OPTS=0 
EXPOSE 8080

# Run tests with coverage reporting -- Unhide next line to run test-cases
# CMD ["pytest", "--cov=app", "--cov-report=term-missing", "-s"] 

# Run app
CMD ["python", "-c", "from app.main import start; start()"]
import gradio as gr
from tensorflow import keras
from keras import models
from keras.preprocessing import image



title = "Image Classifier"

description = '''This Project is used to predict gender - male/female & hand-written digit in an image. There are 2 models - 
- Gender Model has 6-layered architecture. Model is trained using 4-CNN, 2-Dense-Fully connected layer Dataset - https://www.kaggle.com/datasets/gpiosenka/gender-classification-from-an-image. Notebook link - https://github.com/jivaniyash/image_classifier_app/blob/main/colab-notebook/Gender_Classifier.ipynb
- Digit Classifier Model has 3-layered architecture - trained using dataset - https://www.tensorflow.org/datasets/catalog/mnist. Notebook Link - https://github.com/jivaniyash/image_classifier_app/blob/main/colab-notebook/Digit_Classifier.ipynb
'''

article="<p style='text-align: center'><a href='https://github.com/jivaniyash/image_classifier_app' target='_blank'>Link to Git Repository</a <p> There are 2 different classification tasks merged over single endpoint function. This practice should not be adpoted in real use -case scenarios. Try creating different endpoint for each classification. This project is just for learning purposes.</p>"


def image_classifier(model_name, img):
    
    if model_name == "Gender Classifier":
        img_np = image.img_to_array(image.load_img(img, target_size=(64,64)))
        test_img = img_np.reshape((1, 64, 64, 3))

        pipeline = models.load_model('./models/gender-classifier.keras')
    
        y = pipeline(test_img/255., training=False)  # output prob between 0 to 1 , 0 indicates female & 1 indicates male
        prob = y.numpy()[0][0]
        predictions = [prob,1-prob]
        
        labels = ["Male", "Female"]

        return {labels[i]:float(predictions[i]) for i in range(len(labels))}
        

    if model_name == "Digit Classifier":
        img_np = image.img_to_array(image.load_img(img, target_size=(28,28)).convert('L'))
        test_img = img_np.reshape((1,28,28,1))

        pipeline = models.load_model('./models/digit-classifier.keras')

        y = pipeline(test_img/255., training=False)  # output list of 10 tensors
 
        labels = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

        return {labels[i]:float(y[0][i]) for i in range(len(labels))}


demo = gr.Interface(fn=image_classifier, 
                    inputs=[gr.Dropdown(["Gender Classifier","Digit Classifier"], label="Select Model to predict", info="models"),
                            gr.Image(type='filepath')],
                    outputs=gr.Label(num_top_classes=2),
                    title=title,
                    description=description,
                    article=article,
                    examples=[["Gender Classifier","./images/gender/male01.jpg"],
                            ["Gender Classifier","./images/gender/female01.jpg"],
                            ["Digit Classifier", "./images/digit/1.png"],
                            ["Digit Classifier", "./images/digit/3.png"]])

demo.launch(share=False, debug=True)
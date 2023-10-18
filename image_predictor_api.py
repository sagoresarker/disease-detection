from fastapi import FastAPI, HTTPException, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import psycopg2
from PIL import Image

app = FastAPI()

model = tf.keras.models.load_model("model_dis.hdf5")
class_names = ['Bean_angular_leaf_spot', 'Bean_bean_rust', 'Rice_Bacterial leaf blight', 'Rice_Brown_Spot', 'Rice_Healthy', 'Rice_Hispa', 'Rice_Leaf smut', 'Rice_Leaf_Blast', 'Wheat_Brown_Rust', 'Wheat_Healthy', 'Wheat_Yellow_Rust']

def save_prediction_to_database(prediction, confidence):
    conn = psycopg2.connect(
        host="localhost",
        database="imagepredictor",
        user="sagore",
        password="sagore"
    )

    cur = conn.cursor()

    cur.execute("INSERT INTO predictions (prediction, confidence) VALUES (%s, %s)", (prediction, confidence))

    conn.commit()

    cur.close()
    conn.close()


data_dict = {
    'Bean Angular Leaf Spot': [
        {
            'Pesticide': 'azoxystrobin',
            'Quantity': '1.5 ml',
            'Area': '100 square feet',
            'Volume': '0.15 mL/L'
        },
        {
            'Pesticide': 'propiconazole',
            'Quantity': '2.0 ml',
            'Area': '100 square feet',
            'Volume': '0.20 mL/L'
        },{
            'Pesticide': 'flutriafol',
            'Quantity': '2.25 ml',
            'Area': '100 square feet',
            'Volume': '0.23 mL/L'
        },{
            'Pesticide': 'trifloxystrobin + pyraclostrobin',
            'Quantity': '1.25ml',
            'Area': '100 square feet',
            'Volume': '0.15 mL/L'
        },
    ],

    'Bean Rust': [
        {
            'Pesticide': 'azoxystrobin',
            'Quantity': '1.25ml',
            'Area': '100 square feet',
            'Volume': '30 mL/L'
        },
        {
            'Pesticide': 'propiconazole',
            'Quantity': '1.50ml',
            'Area': '100 square feet',
            'Volume': '45 mL/L'
        },
        {
            'Pesticide': 'flutriafol',
            'Quantity': '1.75ml',
            'Area': '100 square feet',
            'Volume': '50 mL/L'
        },
        {
            'Pesticide': 'trifloxystrobin + pyraclostrobin',
            'Quantity': '1.25ml',
            'Area': '100 square feet',
            'Volume': '30 mL/L'
        },
        {
            'Pesticide': 'azoxystrobin + trifloxystrobin',
            'Quantity': '1.25ml',
            'Area': '100 square feet',
            'Volume': '30 mL/L'
        },
    ],
    'Tomato Bacterial Spot': [
        {
            'Pesticide': 'Copper hydroxide',
            'Quantity': '44.35 ml',
            'Area': '100 square feet',
            'Volume': '39-59 mL/L'
        }, {
            'Pesticide': 'Serenade ASO',
            'Quantity': '14.75 ml',
            'Area': '100 square feet',
            'Volume': '11.8 mL/L'
        }, {
            'Pesticide': 'Copper, sulfur, and neem oil',
            'Quantity': '29.57 ml',
            'Area': '100 square feet',
            'Volume': '29.57 mL/L'
        },
    ],
    'Tomato Early Blight': [
        {
            'Pesticide': 'Serenade ASO',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '5.3-10.6 ml/L'
        },  {
            'Pesticide': 'Copper hydroxide',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '10.6-21.2 ml/L'
        }, {
            'Pesticide': 'Mancozeb',
            'Quantity': '29.57-44.36 ml',
            'Area': '100 square feet',
            'Volume': '10.6-15.9 ml/L'
        },
    ],
    'Tomato Late Blight': [{
            'Pesticide': 'Serenade ASO',
            'Quantity': '44.36-88.72 ml',
            'Area': '100 square feet',
            'Volume': '12.5-25 ml/L'
        },  {
            'Pesticide': 'Copper hydroxide\t',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '40-80 ml/L'
        }, {
            'Pesticide': 'Mancozeb',
            'Quantity': '29.57-44.36 ml',
            'Area': '100 square feet',
            'Volume': '40-60 ml/L'
        }, {
            'Pesticide': 'trifloxystrobin + pyraclostrobin',
            'Quantity': '36.96-73.93 ml',
            'Area': '100 square feet',
            'Volume': '30ml/L'
        },
    ],
    'Tomato Leaf Mold': [{
            'Pesticide': 'Serenade ASO',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '28.4 ml/L'
        },  {
            'Pesticide': 'Mancozeb',
            'Quantity': '29.57-44.36 ml',
            'Area': '100 square feet',
            'Volume': '81.5 ml/L'
        }, {
            'Pesticide': 'Copper hydroxide',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '57.9 ml/L'
        },
    ],
    'Tomato Septoria Leaf Spot': [{
            'Pesticide': 'azoxystrobin',
            'Quantity': '36.96 ml',
            'Area': '100 square feet',
            'Volume': '15 mL/L'
        }, {
            'Pesticide': 'propiconazole',
            'Quantity': '44.36 ml',
            'Area': '100 square feet',
            'Volume': '20 mL/L'
        }, {
            'Pesticide': 'flutriafol',
            'Quantity': '51.75 ml',
            'Area': '100 square feet',
            'Volume': '27.5 mL/L'
        }, {
            'Pesticide': 'Copper hydroxide',
            'Quantity': '59.14 ml',
            'Area': '100 square feet',
            'Volume': '57.9 ml/L'
        },
    ],
    'Tomato Spider Mites': [{
            'Pesticide': 'bifenthrin',
            'Quantity': '29.57-36.96 ml',
            'Area': '100 square feet',
            'Volume': '14-21 ml/L'
        }, {
            'Pesticide': 'permethrin',
            'Quantity': '7.40-14.78 ml',
            'Area': '100 square feet',
            'Volume': '14.8-29.6 ml/L'
        }, {
            'Pesticide': 'spinosad',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '14 ml/L'
        }, {
            'Pesticide': 'insecticidal soap',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '29.6 ml/L'
        }, {
            'Pesticide': 'spinosad',
            'Quantity': '29.57 ml',
            'Area': '100 square feet',
            'Volume': '14 ml/L'
        },],
    'Tomato Target Spot': [{
            'Pesticide': 'Serenade ASO',
            'Quantity': '7.40-59.14 ml',
            'Area': '100 square feet',
            'Volume': '10.9-21.8 ml/L'
        }, {
            'Pesticide': 'Copper hydroxide',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '21.8-43.6 ml/L'
        }, {
            'Pesticide': 'Mancozeb',
            'Quantity': '29.57-44.36 ml',
            'Area': '100 square feet',
            'Volume': '21.8-32.7 ml/L'
        },
    ],
    'Tomato Mosaic Virus': [{
            'Pesticide': 'Serenade ASO',
            'Quantity': '14.78 ml',
            'Area': '100 square feet',
            'Volume': '7-14 ml/L'
        },  {
            'Pesticide': 'Azadirachtin',
            'Quantity': '29.57 ml',
            'Area': '100 square feet',
            'Volume': '3.5-7 ml/L'
        }, {
            'Pesticide': 'mancozeb',
            'Quantity': '44.36 ml',
            'Area': '100 square feet',
            'Volume': '14-21 ml/L'
        },
    ],
    'Tomato Yellow Leaf Curl Virus': [{
            'Pesticide': 'Serenade ASO',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '7-14 ml/L'
        },  {
            'Pesticide': 'Copper hydroxide',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '57.9 ml/L'
        }, {
            'Pesticide': 'mancozeb',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '14-21 ml/L'
        },
    ],
    'Two-Spotted Spider Mite': [{
            'Pesticide': 'Spinosad',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '7 ml/L'
        },  {
            'Pesticide': 'abamectin',
            'Quantity': '29.57-59.14 ml',
            'Area': '100 square feet',
            'Volume': '7 ml/L'
        }, {
            'Pesticide': 'permethrin',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '14 ml/L'
        }, {
            'Pesticide': 'Azadirachtin',
            'Quantity': '14.78-29.57 ml',
            'Area': '100 square feet',
            'Volume': '20 ml/L'
        }],
}



@app.post("/predict")
async def predict(file: UploadFile):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        image = image.convert("RGB")
        resized_image = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        img_array = np.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)

        # Save the prediction to the database
        #save_prediction_to_database(predicted_class, confidence)

        words = predicted_class.split('_')

        predicted_class = ' '.join(word.capitalize() for word in words)

        if predicted_class in data_dict:
            class_data = data_dict[predicted_class]
        else:
            class_data = {}

        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "class_data":class_data,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

        return {"prediction": predicted_class, "confidence": confidence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

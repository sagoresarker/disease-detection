from fastapi import FastAPI, HTTPException, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import psycopg2
from PIL import Image
import requests
import json
import data_saver
import os


app = FastAPI()

model = tf.keras.models.load_model("model_dis.hdf5")
class_names = [
    "Bean_angular_leaf_spot",
    "Bean_bean_rust",
    "Rice_Bacterial leaf blight",
    "Rice_Brown_Spot",
    "Rice_Healthy",
    "Rice_Hispa",
    "Rice_Leaf smut",
    "Rice_Leaf_Blast",
    "Wheat_Brown_Rust",
    "Wheat_Healthy",
    "Wheat_Yellow_Rust",
]


def save_prediction_to_database(prediction, confidence):
    conn = psycopg2.connect(
        host="localhost", database="imagepredictor", user="sagore", password="sagore"
    )

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO predictions (prediction, confidence) VALUES (%s, %s)",
        (prediction, confidence),
    )

    conn.commit()

    cur.close()
    conn.close()


@app.post("/predict")
async def predict(file: UploadFile):
    """
    This endpoint is for direct image upload to server. And it will return a
    saved file name of the image output.
    The generated file will be stored in the root directory inside 'data' directory.
    """
    try:
        image = Image.open(io.BytesIO(await file.read()))

        image = image.convert("RGB")
        resized_image = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        img_array = np.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)

        words = predicted_class.split("_")

        predicted_class = " ".join(word.capitalize() for word in words)


        result_data = {
            "prediction": predicted_class,
        }

        filename = data_saver.save_data(result_data)

        return {
            "filename": filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/image-url={image_url:path}")
async def predict_image_url(image_url: str):
    """
    This endpoint is for uploading an image using an image URL to the server and
    returning a saved file name of the image output.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()


        image = Image.open(io.BytesIO(response.content))

        image = image.convert("RGB")
        resized_image = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        img_array = np.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)

        words = predicted_class.split("_")
        predicted_class = " ".join(word.capitalize() for word in words)


        result_data = {
            "prediction": predicted_class,
        }

        filename = data_saver.save_data(result_data)

        return {
            "filename": filename,
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch image from URL: {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


DATA_DIRECTORY = "/app/data"


@app.get("/data/filename={filename:path}")
async def get_data(filename: str):
    """
    Get a JSON file from the "data" directory based on the hashed filename.
    The file is fetch from 'data' directory located in the root folder.
    """
    file_path = os.path.join(DATA_DIRECTORY, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r") as file:
        data = file.read()

    return {"data": data}

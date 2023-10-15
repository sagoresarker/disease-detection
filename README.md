Run the following command to build the Docker image:

   ```bash
   docker build -t image-predictor .
   ```

Once the image is built, you can run a container using the following command:

   ```bash
   docker run -p 8000:8000 image-predictor
   ```


Run wihout Docker

   ```bash
   uvicorn image_predictor_api:app --host 0.0.0.0 --port 8000
   ```



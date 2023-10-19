# Final List
## Endpoints
    1. Direct image upload(POST)
        => /predict
    2. Use image url to upload image (POST)
        => /predict/image-url='https://example.com'
    3. Request data for pre-analysed image (GET)
        => /data/image-id

## Database:
    Postgresql
        1. Store processed data in text or json file

## Keypoints
    Set image id based on meta data of that image.
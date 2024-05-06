# Image Service

## Instructions
1. Checkout this repository locally
1. Update the `docker-compose.yml` with `API_KEY` environment value . This will be used in the request for authentication.
2. Build and run the docker container using the docker-compose
   ```
   docker compose up --build
   ```
   This will bring up two containers, one is the image_service and other is the jupyter-lab to test the apis
3. Find the jupyter url from the logs that were displayed from the last command. You should be able to find one of the following form
   ```
   http://127.0.0.1:8888/lab?token=914252ac1ad30e1209df....
   ```
   click on the link or paste it in the browser to run the api tests from jupyter notebook
4. In the jupyter notebook tab, there will be notebook in the name of `image_server_playbook.ipynb` . Follow the instruction to test the image service apis.
5. You should also be able to see the openapi docs at http://localhost:8001/docs

## APIs

### Pre-req
All the api endpoints except `/api/images` (which is a static file serving endpoint), requires a `x-api-key` in the request headers with valid api key (the one that was set as env value during the docker up).

### Generate Upload Link
```
POST /api/generate-upload-link
Headers: x-api-key=<valid-api>
{
    "expiry": 60
}
```
This api takes in `expiry` as integer (in seconds) and gives back `upload_id` in json response
```
{
    "upload_id": "2643772f-5cbd-4b72-bdfa-9a10c72c6fec"
}
```

### Upload Images
```
POST /api/upload-images/{upload-id}
Headers: x-api-key=<valid-api>
Files: image_files=@foo-1.jpg image_files=@foo-2.jpg
```
The url this api is constructed with the `upload_id` from the generated upload link api. This api takes multiple image files posted to it as `multipart/form-data` to `image_files` variable and returns a dict of `filename` to `image_id` mapping
```
{
    "foo-1.jpg" : "134811388d45f26f3889497c34284d418fb4278a4a49dc5e10ee7ae32a1f0af9",
    "foo-2.jpg" : "99c9de8712749b15ae7662333f04c07e747a1497fd7fcd3b80c0b9682035b184"
}
```

Note: 
If the same image is uploaded, internally it wont update any data but will still return the same id as the first upload.

### Images 
```
GET /api/images/{image_id}
```
This api is internally a static endpoint. The `image_id` in the api path should be valid one from upload images api response.
Note: This api doesn't require the api key in the header

### Stats
```
GET /api/stats
Header: x-api-key=<valid-api>
```
This api gets the stats based on the image metadata and image uploads information. 
```
{'Image Upload Frequency Per Day (last 30 days)': {'2024-05-06': 3},
 'Most Popular Image Format': 'JPEG',
 'Top 10 Popular Camera Models': ['Google - Pixel 6a', 'SONY - ILCE-7M2']}
 ```
Note: It only supports the above three mentioned in the example output.
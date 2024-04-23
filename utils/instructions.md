# Instructions to set up multimodal (i.e. image) references
## Split PDF, create images, and uplaod to GCS
The script `upload_pdf_images_to_gcs.py` will
- Split a PDF into single pages
- Upload each page as a separate .png file to GCS
## Create image embeddings
The script `image_embeddings.py` will
- create a multimodal embedding for each image
- save all embeddings in `indexData.json`, together with the corresponding filenames
## Create Vector Search Index
- First, create the configuration for the index as in `index_metadata.json` (see also https://cloud.google.com/vertex-ai/docs/vector-search/configuring-indexes)
- Then create the index via CLI
```
gcloud ai indexes create \
  --metadata-file=index_metadata.json \
  --display-name=MultiModal-Embeddings \
  --project=heikohotz-genai-sa \
  --region=us-central1
  ```
## Create Index Endpoint
This can be done in the console via the `Deploy` button
## Image search
If the user requests an image reference with their query, the steps are as follows:
- Create query embeddings
- Identify the nearest neighbour (i.e. the image that most closely resembles the query) using Vector Search
- Extract the image filename
- Download the corresponding image from GCS
- Display in UI
The image search is done in `imagesearch.py`
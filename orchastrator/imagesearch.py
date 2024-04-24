from vertexai.vision_models import MultiModalEmbeddingModel
from google.cloud import storage, aiplatform_v1


def get_query_embedding(query: str):
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    embeddings = model.get_embeddings(contextual_text=query)
    return embeddings.text_embedding


def get_gcs_location_for_query(query: str):
    # Generate query embedding
    query_embedding = get_query_embedding(query)

    # Set variables for the current deployed index
    API_ENDPOINT = "413178169.us-central1-83304708959.vdb.vertexai.goog"
    INDEX_ENDPOINT = (
        "projects/83304708959/locations/us-central1/indexEndpoints/8822925503972245504"
    )
    DEPLOYED_INDEX_ID = "dbg_image_search_1713623191588"

    # Configure Vector Search client
    client_options = {"api_endpoint": API_ENDPOINT}
    vector_search_client = aiplatform_v1.MatchServiceClient(
        client_options=client_options
    )

    # Build FindNeighborsRequest object
    datapoint = aiplatform_v1.IndexDatapoint(feature_vector=query_embedding)
    query = aiplatform_v1.FindNeighborsRequest.Query(
        datapoint=datapoint, neighbor_count=10
    )
    request = aiplatform_v1.FindNeighborsRequest(
        index_endpoint=INDEX_ENDPOINT,
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query],
        return_full_datapoint=True,
    )
    
    gcs_path = ""

    try:
        # Execute the request
        response = vector_search_client.find_neighbors(request)

        # Extract the filename from the response (only first result is used here)
        filename = response.nearest_neighbors[0].neighbors[0].datapoint.datapoint_id
        filename = filename.split("'")[1]

        gcs_path = f"gs://dbg-images-heikohotz-genai/images/{filename}"
    except:
        print("No image found")

    return gcs_path

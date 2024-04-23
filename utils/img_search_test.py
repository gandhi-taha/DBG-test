from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
)

from google.cloud import storage

# from google.cloud import aiplatform
# from google.cloud import aiplatform_v1beta1


# # Generate an embedding for the user query (assuming an image query for this example)
def get_query_embedding(query: str):
    # Use the same function as before to generate the embedding for the query text
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")

    embeddings = model.get_embeddings(
        contextual_text=query,
    )
    return embeddings.text_embedding


# def find_closest_image(client, query_embedding, index_endpoint, deployed_index_id):
#     request = aiplatform.gapic.FindNeighborsRequest(
#         index_endpoint=index_endpoint,
#         deployed_index_id=deployed_index_id,
#         queries=[{"datapoint": {"feature_vector": query_embedding}}],
#     )
#     response = client.find_neighbors(request)
#     return response


query = "What was DBG's track record on growth 2017 - 2023?"
query_embedding = get_query_embedding(query)
# print(query_embedding)

# exit(0)
# index_endpoint = (
#     "projects/83304708959/locations/us-central1/indexEndpoints/8822925503972245504"
# )
# deployed_index_id = "dbg_image_search_1713623191588"


# client = aiplatform.gapic.MatchServiceClient(
#     client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
# )

# # query_embedding.text_embeddingresponse = find_closest_image(
# #     client, query_embedding.text_embedding, index_endpoint, deployed_index_id
# # )

# # converted_query_to_embedding = client.get_embedding(text=search_term)

# request = aiplatform_v1beta1.FindNeighborsRequest(
#     index_endpoint=index_endpoint,  # "projects/serious-hall-371508/locations/asia-southeast1/indexEndpoints/3656641422448132096",
#     deployed_index_id=deployed_index_id,  # "js_index_id_unique",
# )

# # text_embedding = [v for v in query_embedding]

# dp1 = aiplatform_v1beta1.IndexDatapoint(
#     datapoint_id="0", feature_vector=query_embedding.text_embedding
# )
# # pass the embedding to do matching
# query = aiplatform_v1beta1.FindNeighborsRequest.Query(
#     datapoint=dp1,
# )
# # request.queries.append(query)
# response = client.find_neighbors(request)
# print(response)
# i = 0


from google.cloud import aiplatform_v1

# Set variables for the current deployed index.
API_ENDPOINT = "413178169.us-central1-83304708959.vdb.vertexai.goog"
INDEX_ENDPOINT = (
    "projects/83304708959/locations/us-central1/indexEndpoints/8822925503972245504"
)
DEPLOYED_INDEX_ID = "dbg_image_search_1713623191588"

# Configure Vector Search client
client_options = {"api_endpoint": API_ENDPOINT}
vector_search_client = aiplatform_v1.MatchServiceClient(
    client_options=client_options,
)

# Build FindNeighborsRequest object
datapoint = aiplatform_v1.IndexDatapoint(feature_vector=query_embedding)

query = aiplatform_v1.FindNeighborsRequest.Query(
    datapoint=datapoint,
    # The number of nearest neighbors to be retrieved
    neighbor_count=10,
)
request = aiplatform_v1.FindNeighborsRequest(
    index_endpoint=INDEX_ENDPOINT,
    deployed_index_id=DEPLOYED_INDEX_ID,
    # Request can have multiple queries
    queries=[query],
    return_full_datapoint=True,
)

# Execute the request
response = vector_search_client.find_neighbors(request)

# Handle the response
# print(response)

filename = response.nearest_neighbors[0].neighbors[0].datapoint.datapoint_id
storage_client = storage.Client()
bucket = storage_client.get_bucket("dbg-images-heikohotz-genai")
path = filename.split("'")[1]
# print(path)
gcs_path = f"images/{path}"
# print(gcs_path)
# img_bytes = bucket.blob(gcs_path).download_as_bytes()

# print(img_bytes)

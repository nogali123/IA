#    embeddings = BedrockEmbeddings(
#        credentials_profile_name="default", region_name="us-east-1"
#    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
#    return embeddings

from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="Mistral")
    return embeddings
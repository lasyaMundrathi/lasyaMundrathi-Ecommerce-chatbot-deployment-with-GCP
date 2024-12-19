from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os
from data_converter import dataconverter

# Load environment variables
load_dotenv()

# Initialize Google Generative AI Embeddings
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize Pinecone client
pc = Pinecone(api_key="pcsk_6BWo5h_HM4amcvFhnGjKbtAUhZqk87ZEwQdAksmbeH4oPuHD1CNQ26sK4hcPC8w481yMK2")

# Define Pinecone index name
index_name = "e-bot"  # Ensure this matches your existing index name

def ingestdata(status):
    # Retrieve the list of existing indexes
    existing_indexes = [index['name'] for index in pc.list_indexes()]

    # Check if the index exists; if not, create it
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )

    # Connect to the Pinecone index
    index = pc.Index(index_name)

    # Create Pinecone vector store
    vstore = PineconeVectorStore(index_name=index_name, embedding=embedding)

    # Add documents if not already stored
    if status is None:
        docs = dataconverter()  # Ensure this returns a list of Document objects
        inserted_ids = vstore.add_documents(docs)
    else:
        return vstore, None

    return vstore, inserted_ids

if __name__ == "__main__":
    # Ingest data into Pinecone vector store
    vstore, inserted_ids = ingestdata(None)

    if inserted_ids:
        print(f"\nInserted {len(inserted_ids)} documents.")

    # Perform a similarity search
    query = "can you tell me the low budget sound basshead."
    results = vstore.similarity_search(query)

    print(f"\nQuery: {query}")
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")

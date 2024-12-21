# lasyaMundrathi-Ecommerce-chatbot-deployment-with-GCP
### Overview:

This project is an end-to-end deployment of an AI-powered chatbot tailored for e-commerce platforms. The chatbot leverages Retrieval-Augmented Generation (RAG) pipelines to provide product recommendations and customer support, combining data from product reviews and embeddings stored in Pinecone.

The project uses Google Cloud Platform (GCP) services for deployment, including:
- **Artifact Registry** for Docker image storage.
- **Cloud Run** for serverless application deployment.
- **GitHub Actions** for CI/CD automation.
---

### File Structure:
```bash
.github/workflows/
  └── google-cloudrun-docker2.yml      # CI/CD pipeline configuration

ecommercebot/
  ├── Dockerfile                       # Docker configuration
  ├── app.py                           # Streamlit app for chatbot interface
  ├── data_converter.py                # Converts and prepares data for Pinecone
  ├── ingestpinecone.py                # Handles data ingestion into Pinecone
  ├── requirements.txt                 # Python dependencies
  ├── retrieval_generation.py          # Implements RAG pipeline
  └── setup.py                         # Package setup configuration
```
# Architecture
![ecommercebotGCP](https://github.com/user-attachments/assets/8a622bfc-1123-4f61-b785-dc444fb4378f)

## Key Layers:
- **CI/CD Deployment Pipeline:** Automates code build, image creation, and deployment to Cloud Run.
- **Data Ingestion Layer:** Prepares and uploads product review data into Pinecone for storage and retrieval.
- **Retrieval Augmented Generation:** Processes queries and retrieves context from Pinecone before generating responses.
- **User Interface Layer**: Provides a chatbot interface using Streamlit.
---
### Demonstration
https://github.com/user-attachments/assets/aafbfcd8-a12d-4bbf-88a5-4aed824e4ea9

### Deployment Steps
- **Clone the Repository**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```
- **Set Up the CI/CD Pipeline**
Ensure the ```.github/workflows/google-cloudrun-docker2.yml``` file is configured correctly.
- **Build and Push Docker Image**
The pipeline automatically builds and pushes the Docker image to GCP Artifact Registry upon a git push.
- **Deploy to Cloud Run**
The pipeline deploys the service to Cloud Run. Verify deployment:
```bash
gcloud run services describe <service-name> --region=<region>
```
- **Launch the Chatbot**
Access the deployed Streamlit chatbot via the URL provided by Cloud Run.
---
### Prerequisites
- Python 3.10
- langchain==0.3.9 
- langchain-google-genai==2.0.6
- langchain-pinecone==0.2.0
- pypdf== 5.1.0
- python-dotenv
-pinecone-client[grpc]==5.0.1
- streamlit
---

### Setup Instructions
**Google Cloud Platform Setup**:
   - Enable the following APIs:
     - Cloud Run
     - Artifact Registry
     - IAM Credentials API
   - Create a **Workload Identity Provider** for GitHub.
   - Grant the following roles to the service account:
     - `Artifact Registry Writer`
     - `Cloud Run Admin`
     - `IAM Service Account User`
   
### Troubleshooting
- Verify Authentication and Permissions:
  - Use this to confirm the active authenticated accounts and validate access
    ```gcloud auth list```
- Debug Cloud Run Deployment Issues:
  -Check the deployment status and logs for a specific service
  ```gcloud run services describe githubaction --region=us-central1```
### Usage
- **Data Ingestion:**
  - data_converter.py: Converts product data into LangChain Document objects.
  - ingestpinecone.py: Uploads these documents into Pinecone for similarity searches.
- **Chatbot Interface:**
  Accessible through Streamlit.
  Enter queries like:
  "What are the features of the OnePlus Bullets Wireless Z?"
  "Is BoAt Rockerz 235v2 worth buying?"
- **RAG Pipeline:**
  Combines product embeddings and generative AI to provide detailed responses.
---

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from ingestpinecone import ingestdata
import os

# Retrieve secrets from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE =  """ You are an expert ecommerce bot specializing in product recommendations and customer support. You have access to product titles and corresponding customer reviews. Use this data to provide detailed, accurate, and helpful responses to user queries.

        Key Instructions:
        Analyze both the product title and customer reviews to deliver context-aware recommendations.
        Focus on extracting key features, pros, cons, and product-specific details from reviews.
        Ensure responses are well-informed, relevant to the product, and customer-centric.
        If multiple reviews are available, synthesize the most relevant details.
        Avoid straying from the provided product context.
        Example Query:

        User: "Tell me about the sound quality of BoAt Rockerz 235v2."
        Expected Response: "The BoAt Rockerz 235v2 features exceptional sound clarity, strong bass, and a powerful audio experience, as highlighted by multiple user reviews."
        Reminder: Always ground responses in the product title and reviews to maintain accuracy and relevance.
        User: "Does BoAt Rockerz 500 have fast charging?"
        Fallback Response: "I couldn't find reviews for the BoAt Rockerz 500, but the BoAt Rockerz 235v2 offers fast charging with 20 minutes of charge providing up to 4 hours of playback. Would you like to hear more about it?"
    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)
    
    # Initialize the ChatGoogleGenerativeAI with the correct parameter
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

    def chain(question):
        # Retrieve relevant documents
        context_docs = retriever.invoke(question)
        context = " ".join([doc.page_content for doc in context_docs])

        # If no context is found, provide a default response
        if not context:
            return "I'm sorry, I couldn't find any information related to your question."

        # Generate the prompt with the retrieved context
        formatted_prompt = prompt.format(context=context, question=question)

        # Generate the answer using the language model
        answer = llm.invoke(formatted_prompt)

        # Parse the output
        parsed_answer = StrOutputParser().parse(answer)

        # If the model fails to generate a response, provide a default message
        if not parsed_answer:
            return "I'm sorry, I couldn't generate an answer to your question at this time."

        # Return only the content from the parsed answer
        return parsed_answer.content if hasattr(parsed_answer, 'content') else parsed_answer

    return chain

if __name__ == '__main__':
    vstore, inserted_ids = ingestdata(None)
    chain = generation(vstore)

    question = "Can you tell me about the OnePlus Bullets Wireless Z Bluetooth Headset?"
    print(chain(question))

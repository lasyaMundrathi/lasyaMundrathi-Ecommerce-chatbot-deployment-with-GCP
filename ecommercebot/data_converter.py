import os
import pandas as pd
from langchain_core.documents import Document

def dataconverter():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "flipkart_product_review.csv")
    
    # Check if the file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"The CSV file does not exist at {csv_path}")
    
    # Read the CSV file
    product_data = pd.read_csv(csv_path)
    
    data = product_data[["product_title", "review"]]
    
    product_list = []
    
    # Iterate over the rows of the DataFrame
    for index, row in data.iterrows():
        obj = {
            'product_name': row['product_title'],
            'review': row['review']
        }
        product_list.append(obj)
    
    docs = []
    for entry in product_list:
        metadata = {"product_name": entry['product_name']}
        doc = Document(page_content=entry['review'], metadata=metadata)
        docs.append(doc)
    
    return docs

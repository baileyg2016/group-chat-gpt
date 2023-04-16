import math
import os
import re
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pinecone
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
from langchain.chains import (RetrievalQAWithSourcesChain,
                              VectorDBQAWithSourcesChain)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from tqdm.auto import tqdm
from langchain.vectorstores import Milvus

# *** Chunk size: key parameter *** 
chunks = 1500
splits_new = [ ]
metadatas_new = [ ]

# Read the csv file
messages = pd.read_csv("chats/group-chat-updated.csv", sep=',')

# Convert the Message Date column to datetime format
messages["Date"] = pd.to_datetime(messages["Message Date"])

# Group the dataframe by Message Date (date only)
groupedMessages = messages.groupby(messages["Date"].dt.date)

members = messages["Sender Name"].unique()

for date, group in groupedMessages:

    text = group["Text"].astype(str).apply(lambda x: x.strip())

    times = list(group["Date"].dt.time)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunks, 
                                                chunk_overlap=50)
    splits = text_splitter.split_text(text)

    # Metadata 
    N = len(splits) 
    bins = np.linspace(0, len(times)-1, N, dtype=int)
    sampled_times = [times[i] for i in bins]
    
    # Here we can add "link", "title", etc that can be fetched in the app 
    metadatas=[{"source": t.strftime("%Y-%m-%d %H:%M:%S"), "id": t.strftime("%Y-%m-%d"), "time": t.strftime("%H:%M:%S")} for t in sampled_times]

    # Append to output 
    splits_new.append(splits)
    metadatas_new.append(metadatas)

splits_all = []
for sublist in splits_new:
    splits_all.extend(sublist)

metadatas_all = []
for sublist in metadatas_new:
    metadatas_all.extend(sublist)



# pinecone instance took too long to create
# Pinecone
# pinecone.init(
#     api_key=os.environ.get('PINECONE_API_KEY'),  
#     environment="northamerica-northeast1-gcp")

# # Update - 
# index_name = "neighborhood-gpt-test"
# embeddings = OpenAIEmbeddings()
# cone = Pinecone.from_existing_index(index_name=index_name,embedding=embeddings)

chunk_size = 100
last_chunk = 0
num_chunks = math.ceil(len(splits_all) / chunk_size)
for i in range(last_chunk,num_chunks):
    
    print(i)
    start_time = time.time()
    start_idx = i * chunk_size
    end_idx = min(start_idx + chunk_size, len(splits_all))
    
    # Extract the current chunk
    current_splits = splits_all[start_idx:end_idx]
    current_metadatas = metadatas_all[start_idx:end_idx]
    
    # Add the current chunk to the vector database
    # print(current_splits)
    # print(current_metadatas)
    print(current_splits)
    print(current_metadatas)
    print()
    # cone.add_texts(texts = current_splits, metadatas=current_metadatas)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print("--------")


# ideas:
# - go through each days
# - go through each persons





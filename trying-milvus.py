import math
import os
import re
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from langchain.chains import (RetrievalQAWithSourcesChain,
                              VectorDBQAWithSourcesChain)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from tqdm.auto import tqdm
from langchain.document_loaders import DataFrameLoader

messages = pd.read_csv("chats/group-chat-updated.csv", sep=',')

# Convert the Message Date column to datetime format
# messages["Date"] = pd.to_datetime(messages["Message Date"]) # this is causing an error
messages["Content"] = messages["Sender Name"].str.cat(messages["Text"], sep=": ")
messages.fillna("blank", inplace=True)
messages.columns = messages.columns.str.replace(' ', '_')

loader = DataFrameLoader(messages, page_content_column="Content")

documents = loader.load()

embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

vector_db = Milvus.from_documents(
    documents,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
)

def run_retrievalQA_sources_chain(llm, query, docstore):

    start_time = time.time()
    chain = RetrievalQAWithSourcesChain.from_chain_type(llm,chain_type="stuff",retriever=docstore.as_retriever(k=3))
    a = chain({"question": query},return_only_outputs=True)
    print(a["answer"])
    print(a["sources"])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print("--------")

def run_vectorDBQA_sources_chain(llm, query, docstore, k):

    start_time = time.time()
    chain = VectorDBQAWithSourcesChain.from_chain_type(llm,chain_type="stuff", vectorstore=docstore,k=k)
    a = chain({"question": query},return_only_outputs=True)
    print(a["answer"])
    print(a["sources"])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print("--------")

llm = OpenAIChat(temperature=0)
q = "Who talks the most in the group chat?"
run_vectorDBQA_sources_chain(llm, q, vector_db, 4)
import time

import pandas as pd
from pandas import DataFrame
from langchain.chains import (RetrievalQAWithSourcesChain,
                              VectorDBQAWithSourcesChain)
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI

# messages = pd.read_csv("chats/group-chat-updated.csv", sep=',')

# Convert the Message Date column to datetime format
# messages["Date"] = pd.to_datetime(messages["Message Date"]) # this is causing an error
# messages["Content"] = messages["Sender Name"].str.cat(messages["Text"], sep=": ")
# # need to add source for the vector db
# messages["source"] = messages["Sender Name"].str.cat(messages["Message Date"], sep=": ")
# messages.fillna("blank", inplace=True)
# messages.columns = messages.columns.str.replace(' ', '_')

def concatenate_rows(row: dict) -> str:
    """Combine message information in a readable format ready to be used."""
    sender = row["Sender Name"]
    text = row["Text"]
    date = row["Message Date"]
    return f"{sender} on {date}: {text}\n\n"

# lang chain simulated loader for now
def load_messages(path="chats/group-chat-updated.csv"):
    messages: DataFrame = pd.read_csv(path, sep=',')
    df_filtered = messages[messages['Text'].apply(lambda x: isinstance(x, str))]
    # print(messages.)
    # df_filtered = messages[
    #         (messages.apply(lambda x: type(x) == str))
    #     ]

    df_filtered = df_filtered[["Message Date", "Text", "Sender Name"]]

    # messages["Content"] = messages["Sender Name"].str.cat(messages["Text"], sep=": ")
    # messages["source"] = messages["Sender Name"].str.cat(messages["Message Date"], sep=": ")
    # messages.fillna("blank", inplace=True)
    # messages.columns = messages.columns.str.replace(' ', '_')

    text = df_filtered.apply(concatenate_rows, axis=1).str.cat(sep="")
    metadata = {"source": str(path)}
    return [Document(page_content=text, metadata=metadata)]

# need to figure out how to load in all of the data
# half = len(messages) // 2
# secondHalf = messages[half:]

# loader = DataFrameLoader(secondHalf, page_content_column="Content")

documents = load_messages()

embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

vector_db = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
)

def run_retrievalQA_sources_chain(llm, query, docstore):

    start_time = time.time()
    chain = RetrievalQAWithSourcesChain.from_chain_type(llm,chain_type="stuff",retriever=docstore.as_retriever(k=10))
    a = chain({"question": query},return_only_outputs=True)
    print(a["answer"])
    print(a["sources"])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print("--------")
    return a["answer"]

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

while True:


    q = input("Ask Neighborhood GPT anything: ")
    a = run_retrievalQA_sources_chain(llm, q, vector_db)
    print()
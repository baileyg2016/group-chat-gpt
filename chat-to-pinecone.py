import pandas as pd
import pinecone
import nltk
from gensim.models import Word2Vec

# Initialize the Pinecone client
pinecone.init(api_key="your-api-key")

# Create a new index
index_name = "neighborhood-gpt"
dimension = 128
pinecone.create_index(index_name=index_name, dimension=dimension)

# Load the data into a Pandas DataFrame
data = pd.read_csv("my-data.csv")

# Preprocess the text data
nltk.download("stopwords")
stop_words = nltk.corpus.stopwords.words("english")
data["clean_text"] = data["Text"].apply(lambda x: " ".join([word.lower() for word in x.split() if word.lower() not in stop_words]))

# Train a Word2Vec model on the preprocessed text data
corpus = [doc.split() for doc in data["clean_text"].tolist()]
model = Word2Vec(corpus, size=dimension, min_count=1)

# Encode the text data as numerical vectors
vectors = []
for doc in corpus:
    vector = []
    for word in doc:
        if word in model.wv.vocab:
            vector.append(model.wv[word])
    if len(vector) == 0:
        vector = [0] * dimension
    else:
        vector = sum(vector) / len(vector)
    vectors.append(vector)

# Convert the vectors to Pinecone format
ids = data["Sender"].tolist()
pinecone_data = []
for i, vector in enumerate(vectors):
    pinecone_data.append(pinecone.VectorData(id=ids[i], data=vector))

# Insert the data into the index
pinecone.insert(index_name=index_name, data=pinecone_data)

# Shutdown the Pinecone client
pinecone.deinit()

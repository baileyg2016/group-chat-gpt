import pandas as pd
import langchain
from langchain.llms import OpenAI
from langchain.cache import InMemoryCache

# what am i going to need:
# [] feed the data into the llm
# [] 
# [] create some type of memory

langchain.llm_cache = InMemoryCache()

llm = OpenAI(model_name='text-davinci-002')



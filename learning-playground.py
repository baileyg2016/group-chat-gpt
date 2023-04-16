from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate

template = """The following is a text group chat between 12 college best friends.
The AI is going to learn about each one of the friends and their interactions between
each other. The AI will then be able to predict what each friend would say in a given
context or parts of current conversation.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], 
    template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=OpenAI(), 
    prompt=prompt, 
    verbose=True, 
    memory=memory,
)

llm_chain.predict(human_input="Hi there my friend")
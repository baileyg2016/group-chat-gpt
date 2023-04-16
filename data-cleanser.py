import pandas as pd

chat = pd.read_csv('chats/group-chat.csv')

print(chat.columns)
print(chat.head(10))
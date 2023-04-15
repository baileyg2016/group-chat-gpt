import pandas as pd
import contacts

members = {
    "": "Bailey Spell",
}

chat = pd.read_csv('group-chat.csv')

chat['Sender Name'] = chat['Sender Name'].fillna('Bailey Spell')

subset = chat.loc[:, ['Sender Name', 'Text']]
print(subset.head(10))
print(len(subset))

subset.to_csv('group-chat-subset.csv', index=False, encoding='utf-8')
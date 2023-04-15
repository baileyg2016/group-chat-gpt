# connection code
import sqlite3
import pandas as pd
import numpy as np

# substitute username with your username
conn = sqlite3.connect('/Users/baileyspell/Desktop/chat.db')
# connect to the database
cur = conn.cursor()
# get the names of the tables in the database
cur.execute(" select name from sqlite_master where type = 'table' ")

# for name in cur.fetchall():
#     print(name)
messages = pd.read_sql_query("select * from message limit 10", conn)

messages.head(10).to_csv('./messages.csv', index = False, encoding='utf-8')

# get the handles to apple-id mapping table
handles = pd.read_sql_query("select * from handle", conn)

# handles.head(10).to_csv('./handles.csv', index = False, encoding='utf-8')

# and join to the messages, on handle_id
messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)
handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)
merge_level_1 = temp = pd.merge(messages[['text', 'handle_id', 'date','is_sent', 'message_id']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')

# get the chat to message mapping
chat_message_joins = pd.read_sql_query("select * from chat_message_join", conn)

# and join back to the merge_level_1 table
df_messages = pd.merge(merge_level_1, chat_message_joins[['chat_id', 'message_id']], on = 'message_id', how='left')
print(len(df_messages))
print(df_messages.head(10))
print(df_messages["chat_id"].unique())
# df_messages.to_csv('./df_messages.csv', index = False, encoding='utf-8')

# how to use that in the SQL query
# messages = pd.read_sql_query("select *, datetime(message.date + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date_uct from message", conn)
# print(messages)

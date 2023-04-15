import sqlite3
import pandas as pd

# Replace the path below with the actual path to your chat.db file
path_to_chat_db = '/Users/baileyspell/Desktop/chat.db'

# Connect to the SQLite database
conn = sqlite3.connect(path_to_chat_db)

# Get group chat handles (identifiers) and their metadata
group_chat_query = '''
SELECT chat.chat_identifier, chat.guid, handle.id
FROM chat
JOIN chat_handle_join ON chat.ROWID = chat_handle_join.chat_id
JOIN handle ON chat_handle_join.handle_id = handle.ROWID
WHERE chat.chat_identifier LIKE "chat%"
'''
group_chats = pd.read_sql_query(group_chat_query, conn)

print(group_chats)

# Replace <group_chat_identifier> with the actual chat_identifier of the group you want to extract
# group_chat_identifier = "<group_chat_identifier>"

# # Get the specific group chat messages
# group_messages_query = f'''
# SELECT message.text, message.date, handle.id
# FROM message
# JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
# JOIN chat ON chat_message_join.chat_id = chat.ROWID
# JOIN handle ON message.handle_id = handle.ROWID
# WHERE chat.chat_identifier = "{group_chat_identifier}"
# ORDER BY message.date
# '''
# group_messages = pd.read_sql_query(group_messages_query, conn)

# # Print the group messages
# print(group_messages)

# Close the database connection
conn.close()

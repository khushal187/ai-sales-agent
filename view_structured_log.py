#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install streamlit


# In[6]:


import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("hiring_data.db")

# Read the data from the 'structured_data' table
df = pd.read_sql("SELECT * FROM structured_data", conn)

# Display the first 10 rows
df.head(10)

# Close the connection
conn.close()


# In[8]:


conn = sqlite3.connect("hiring_data.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(structured_data);")
columns = cursor.fetchall()
for col in columns:
    print(col)
conn.close()


# In[13]:


#RUN THIS TO VIEW STRUCTURED LOGS
import sqlite3
import pandas as pd

# Connect and load everything
conn = sqlite3.connect("hiring_data.db")

# View table names
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in DB:")
print(tables)

# Read data from the structured_data table
df = pd.read_sql("SELECT * FROM structured_data", conn)
print("\nFirst 5 rows of 'structured_data':")
display(df.head())

# Show column details
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(structured_data);")
print("\nColumns in 'structured_data':")
for col in cursor.fetchall():
    print(col)

# Close connection
conn.close()


# In[ ]:





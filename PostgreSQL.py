import streamlit as st
import psycopg2
import pandas as pd

# Connect to PostgreSQL database
@st.cache_resource
def get_pg_connection():
    conn = psycopg2.connect(
        host='localhost',       # Or your DB host
        database='mydatabase',
        user='myuser',
        password='mypassword'
    )
    return conn

conn = get_pg_connection()
cursor = conn.cursor()

# Create table (optional)
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
)
''')
conn.commit()

# UI: Add new customer
st.header("Add Customer (PostgreSQL)")
name = st.text_input("Customer Name")
email = st.text_input("Customer Email")

if st.button("Add Customer"):
    cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    st.success("Customer added to PostgreSQL!")

# UI: View all customers
st.header("Customer List")
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=['ID', 'Name', 'Email'])
st.dataframe(df)

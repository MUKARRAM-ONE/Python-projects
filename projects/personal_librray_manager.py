import streamlit as st
import pandas as pd
import os

FILE = "library.csv"

# Initialize CSV
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Title", "Author", "Year", "Genre"])
    df.to_csv(FILE, index=False)

def load_data():
    return pd.read_csv(FILE)

def save_data(df):
    df.to_csv(FILE, index=False)

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add Book", "View Library", "Search", "Delete Book"])

# Add Book
if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Year", step=1, format="%d")
    genre = st.text_input("Genre")

    if st.button("Add Book"):
        if title and author:
            new_book = pd.DataFrame([[title, author, year, genre]], columns=["Title", "Author", "Year", "Genre"])
            df = load_data()
            df = pd.concat([df, new_book], ignore_index=True)
            save_data(df)
            st.success("Book added!")
        else:
            st.warning("Title and Author are required.")

# View Library
elif menu == "View Library":
    st.header("📖 Your Library")
    df = load_data()
    st.dataframe(df)

# Search Book
elif menu == "Search":
    st.header("🔍 Search Books")
    query = st.text_input("Enter title or author keyword").lower()
    if query:
        df = load_data()
        results = df[df.apply(lambda row: query in row["Title"].lower() or query in row["Author"].lower(), axis=1)]
        if not results.empty:
            st.dataframe(results)
        else:
            st.info("No matches found.")

# Delete Book
elif menu == "Delete Book":
    st.header("🗑️ Delete a Book")
    df = load_data()
    book_to_delete = st.selectbox("Select a book to delete", df["Title"])
    if st.button("Delete"):
        df = df[df["Title"] != book_to_delete]
        save_data(df)
        st.success(f"'{book_to_delete}' deleted.")

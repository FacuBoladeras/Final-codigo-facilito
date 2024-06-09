import streamlit as st
import requests

# Define the base URL of your FastAPI app
BASE_URL = "http://127.0.0.1:8000"

st.title("Library Management System")

# Function to get books from the API
def get_books():
    try:
        response = requests.get(f"{BASE_URL}/books/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching books: {e}")
        return []

# Function to get a single book by ID
def get_book(book_id):
    try:
        response = requests.get(f"{BASE_URL}/book/{book_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching book with ID {book_id}: {e}")
        return None

# Function to create a new book
def create_book(book_data):
    try:
        response = requests.post(f"{BASE_URL}/books/", json=book_data)
        response.raise_for_status()
        st.success("Book created successfully")
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating book: {e}")

# Main menu
menu = st.sidebar.selectbox("Menu", ["View Books", "Add Book", "View Book by ID"])

if menu == "View Books":
    st.header("Books List")
    books = get_books()
    for book in books:
        st.subheader(f"{book['title']} by {book['author']}")
        st.write(f"Genre: {book['genre']}")
        st.write(f"Year: {book['year']}")

elif menu == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Year", min_value=1000, max_value=9999, step=1)

    if st.button("Add Book"):
        book_data = {
            "title": title,
            "author": author,
            "genre": genre,
            "year": year
        }
        create_book(book_data)

elif menu == "View Book by ID":
    st.header("View Book by ID")
    book_id = st.number_input("Book ID", min_value=1, step=1)
    if st.button("Fetch Book"):
        book = get_book(book_id)
        if book:
            st.subheader(f"{book['title']} by {book['author']}")
            st.write(f"Genre: {book['genre']}")
            st.write(f"Year: {book['year']}")

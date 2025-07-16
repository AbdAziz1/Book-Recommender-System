import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import zipfile


MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
ZIP_PATH = os.path.join(os.path.dirname(__file__), "model.zip")

# Automatically extract zip if the folder doesn't exist,
if not os.path.exists(MODEL_DIR):
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(MODEL_DIR)

with open(os.path.join(MODEL_DIR, "popular.pkl"), "rb") as f:
    popular_df = pickle.load(f)

with open(os.path.join(MODEL_DIR, "pt.pkl"), "rb") as f:
    pt = pickle.load(f)

with open(os.path.join(MODEL_DIR, "books.pkl"), "rb") as f:
    books = pickle.load(f)

with open(os.path.join(MODEL_DIR, "similarity_scores.pkl"), "rb") as f:
    similarity_scores = pickle.load(f)


# Load pre-trained data
#popular_df = pickle.load(open(r'E:\My Work\DataScience Projects\Book Recommender System\model\popular.pkl', 'rb'))
#pt = pickle.load(open(r'E:\My Work\DataScience Projects\Book Recommender System\model\pt.pkl', 'rb'))
#books = pickle.load(open(r'E:\My Work\DataScience Projects\Book Recommender System\model\books.pkl', 'rb'))
#similarity_scores = pickle.load(open(r'E:\My Work\DataScience Projects\Book Recommender System\model\similarity_scores.pkl', 'rb'))

# Title and header
st.title("📚 Book Recommender System")
st.markdown("## Discover your next favorite book!")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Top 50 Books", "Recommend Books"])

if page == "Top 50 Books":
    # Display Top 50 Books
    st.markdown("### Top 50 Books")
    st.write("Here are some of the most popular books you might like:")

    # Use Streamlit columns for better layout
    num_columns = 4
    for i in range(0, len(popular_df), num_columns):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            if i + j < len(popular_df):
                with cols[j]:
                    st.image(popular_df.iloc[i + j]['Image-URL-M'], use_column_width=True)
                    st.markdown(f"**{popular_df.iloc[i + j]['Book-Title']}**")
                    st.write(f"Author: {popular_df.iloc[i + j]['Book-Author']}")
                    st.write(f"Votes: {popular_df.iloc[i + j]['num_ratings']}")
                    st.write(f"Rating: {popular_df.iloc[i + j]['avg_rating']}")
                    st.write("---")

elif page == "Recommend Books":
    # Recommend Books
    st.markdown("### Recommend Books")
    st.write("Enter the name of a book you like, and we'll recommend similar books.")

    user_input = st.text_input("Enter a book name:")
    if st.button("Recommend"):
        if user_input in pt.index:
            try:
                index = np.where(pt.index == user_input)[0][0]
                similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

                st.markdown("#### Here are some books you might like:")
                num_columns_rec = 3
                rec_cols = st.columns(num_columns_rec)
                for i, item in enumerate(similar_items):
                    temp_df = books[books['Book-Title'] == pt.index[item[0]]].drop_duplicates('Book-Title')
                    book_title = temp_df['Book-Title'].values[0]
                    book_author = temp_df['Book-Author'].values[0]
                    book_image = temp_df['Image-URL-M'].values[0]

                    with rec_cols[i % num_columns_rec]:
                        st.image(book_image, use_column_width=True)
                        st.markdown(f"**{book_title}**")
                        st.write(f"Author: {book_author}")
                        st.write("---")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Book not found in the database")

# Additional styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #00a65a;
            color: white;
            font-size: 18px;
            padding: 10px;
        }
        .stTextInput>div>div>input {
            font-size: 18px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

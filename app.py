import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="ReadMate AI Recommender", page_icon="📚", layout="wide")

# --- Load books ---
@st.cache_data
def load_books():
    return pd.read_csv("books.csv")

books_df = load_books()

# --- Header ---
st.markdown(
    "<h1 style='text-align:center;color:#6c63ff;font-family:Arial Black;'>📚 ReadMate AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;font-size:18px;color:#333;'>AI-Powered Book Recommendations By Runner And Keywords</p>",
    unsafe_allow_html=True,
)

# --- Library / Book Collection Section ---
with st.expander("📖 Library / Book Collection"):
    st.markdown("<h3 style='color:#6c63ff;'>Library Books</h3>", unsafe_allow_html=True)
    st.dataframe(books_df[["Id","Title","Author","Year","Runner","Keywords"]], use_container_width=True)

# --- Search & Recommendation ---
search = st.text_input("Enter a Book Title or Author to get Recommendations:")

def recommend_books(search_term):
    search_term = search_term.strip().lower()
    matched = books_df[
        books_df["Title"].str.lower().str.contains(search_term) |
        books_df["Author"].str.lower().str.contains(search_term)
    ]
    if matched.empty:
        return pd.DataFrame(columns=books_df.columns)
    
    book = matched.iloc[0]
    genre = book["Runner"]
    keywords = set(book["Keywords"].split(";"))
    
    # AI-style recommendations: same runner + shared keywords
    recs = books_df[books_df["Runner"] == genre]
    recs = recs[recs["Id"] != book["Id"]]  # exclude the searched book
    recs["Shared_Keywords"] = recs["Keywords"].apply(lambda x: len(keywords.intersection(set(x.split(";")))))
    recs = recs[recs["Shared_Keywords"] > 0]
    recs = recs.sort_values(by="Shared_Keywords", ascending=False)
    
    return recs.drop(columns="Shared_Keywords")

if search:
    recommendations = recommend_books(search)
    if recommendations.empty:
        st.warning("No recommendations found for this book.")
    else:
        st.markdown("<h3 style='color:#ff6f61;'>Recommended Books For You</h3>", unsafe_allow_html=True)
        st.dataframe(recommendations[["Id","Title","Author","Year","Runner","Keywords"]], use_container_width=True)

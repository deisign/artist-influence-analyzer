import requests
import streamlit as st
from bs4 import BeautifulSoup

# Base URL for SecondHandSongs API
BASE_URL = "https://secondhandsongs.com/search"

# Function to search for artists
def search_artists(common_name, page=1, page_size=10):
    url = f"{BASE_URL}/artist"
    params = {
        "commonName": common_name,
        "page": page,
        "pageSize": page_size,
    }
    headers = {"Accept": "application/json"}
    st.text(f"Request URL: {url}")
    st.text(f"Request Params: {params}")
    
    response = requests.get(url, params=params, headers=headers)
    st.text(f"Response Status Code: {response.status_code}")
    
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.reason}")
        st.text(response.text)
        return {"error": f"Error {response.status_code}: {response.reason}"}
    
    if not response.content:
        st.warning("The server returned an empty response.")
        return {"error": "Empty response from server"}
    
    try:
        return response.json()
    except ValueError:
        st.error("The response could not be parsed as JSON.")
        st.text(response.text)  # Shows raw server response for debugging
        soup = BeautifulSoup(response.text, "html.parser")
        st.write("HTML Response (Parsed):", soup.prettify())
        return {"error": "Invalid JSON response"}

# Streamlit application
st.title("SecondHandSongs API Explorer")

# Sidebar for search type
search_type = st.sidebar.selectbox("Search Type", ["Artist"])

# Artist search
if search_type == "Artist":
    st.header("Search for Artists")
    common_name = st.text_input("Enter artist's name:")
    page = st.number_input("Page", min_value=1, value=1)
    page_size = st.number_input("Results per page", min_value=1, max_value=100, value=10)

    if st.button("Search Artists"):
        if common_name:
            results = search_artists(common_name, page, page_size)
            if "error" in results:
                st.error(results["error"])
            else:
                st.write("Results:", results)
        else:
            st.warning("Please enter an artist's name.")

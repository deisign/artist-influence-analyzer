import requests
import streamlit as st
import pandas as pd

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
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.reason}")
        return None
    
    try:
        return response.json()
    except ValueError:
        st.error("The response could not be parsed as JSON.")
        st.text(response.text)  # Debug: Show raw response if JSON parsing fails
        return None

# Function to parse and display artist results
def display_artist_results(data):
    if "resultPage" not in data or not data["resultPage"]:
        st.warning("No results found.")
        return

    # Extract relevant fields into a DataFrame
    results = [
        {
            "Name": item["commonName"],
            "Type": item["entitySubType"],
            "Profile Link": item["uri"],
        }
        for item in data["resultPage"]
    ]
    df = pd.DataFrame(results)
    
    # Display as a table
    st.write("### Results")
    st.dataframe(df)
    st.markdown("### Links")
    for _, row in df.iterrows():
        st.markdown(f"- [{row['Name']}]({row['Profile Link']})")

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
            if results:
                display_artist_results(results)
            else:
                st.error("No data returned from API.")
        else:
            st.warning("Please enter an artist's name.")

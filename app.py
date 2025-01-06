import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Function to fetch covers (primary method)
def fetch_covers(artist_uri):
    url = f"{artist_uri}/covers"
    headers = {"Accept": "application/json"}
    
    st.text(f"Fetching covers from: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 500:
        st.warning("The server encountered an internal error (500). Covers may not be available.")
        return None
    if response.status_code != 200:
        st.error(f"Error fetching covers: {response.status_code}")
        st.text(response.text)
        return None

    try:
        return response.json()
    except ValueError:
        st.error("The response could not be parsed as JSON.")
        st.text(response.text)
        return None

# Function to fetch performances (alternative for covers)
def search_performances(performer, page=1, page_size=10):
    url = f"{BASE_URL}/performance"
    params = {
        "performer": performer,
        "page": page,
        "pageSize": page_size,
    }
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, params=params, headers=headers)
    st.text(f"Fetching performances from: {response.url}")
    
    if response.status_code != 200:
        st.error(f"Error fetching performances: {response.status_code}")
        st.text(response.text)
        return None

    try:
        return response.json()
    except ValueError:
        st.error("The response could not be parsed as JSON.")
        st.text(response.text)
        return None

# Function to display artist results
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
    st.write("### Artist Results")
    st.dataframe(df)

    # Add clickable links
    st.markdown("### Artist Links")
    for _, row in df.iterrows():
        st.markdown(f"- [{row['Name']}]({row['Profile Link']})")

    # Select artist for covers
    selected_artist = st.selectbox("Select an artist to view covers or performances", df["Name"])
    artist_uri = df[df["Name"] == selected_artist]["Profile Link"].values[0]
    
    if artist_uri:
        covers_data = fetch_covers(artist_uri)
        if covers_data:
            display_covers(covers_data)
        else:
            st.warning("No covers found. Attempting to fetch performances.")
            performances_data = search_performances(selected_artist)
            if performances_data:
                display_performances(performances_data)

# Function to display covers
def display_covers(data):
    if "resultPage" not in data or not data["resultPage"]:
        st.warning("No covers found for this artist.")
        return
    
    st.write("### Covers")
    covers = [
        {
            "Title": item["commonName"],
            "Performer": item.get("performer", {}).get("commonName", "Unknown"),
            "Year": item.get("date", "Unknown"),
        }
        for item in data["resultPage"]
    ]
    df_covers = pd.DataFrame(covers)
    st.dataframe(df_covers)

    # Plot covers by year
    if "Year" in df_covers and not df_covers["Year"].isnull().all():
        df_covers["Year"] = pd.to_numeric(df_covers["Year"], errors="coerce")
        df_covers = df_covers.dropna(subset=["Year"])
        year_counts = df_covers["Year"].value_counts().sort_index()

        st.write("### Covers Over Time")
        plt.figure(figsize=(10, 6))
        plt.bar(year_counts.index, year_counts.values, color="blue")
        plt.xlabel("Year")
        plt.ylabel("Number of Covers")
        plt.title("Covers Over Time")
        st.pyplot(plt)

# Function to display performances (alternative for covers)
def display_performances(data):
    if "resultPage" not in data or not data["resultPage"]:
        st.warning("No performances found for this artist.")
        return
    
    st.write("### Performances")
    performances = [
        {
            "Title": item["commonName"],
            "Performer": item.get("performer", {}).get("commonName", "Unknown"),
            "Year": item.get("date", "Unknown"),
        }
        for item in data["resultPage"]
    ]
    df_performances = pd.DataFrame(performances)
    st.dataframe(df_performances)

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

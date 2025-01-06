import requests
import streamlit as st

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
    st.text(f"Request URL: {url}")
    st.text(f"Request Params: {params}")
    
    response = requests.get(url, params=params)
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
        st.text(response.text)
        return {"error": "Invalid JSON response"}

# Function to search for performances
def search_performances(title, performer=None, date=None, page=1, page_size=10):
    url = f"{BASE_URL}/performance"
    params = {
        "title": title,
        "performer": performer,
        "date": date,
        "page": page,
        "pageSize": page_size,
    }
    st.text(f"Request URL: {url}")
    st.text(f"Request Params: {params}")
    
    response = requests.get(url, params=params)
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
        st.text(response.text)
        return {"error": "Invalid JSON response"}

# Function to search for works
def search_works(title, credits=None, page=1, page_size=10):
    url = f"{BASE_URL}/work"
    params = {
        "title": title,
        "credits": credits,
        "page": page,
        "pageSize": page_size,
    }
    st.text(f"Request URL: {url}")
    st.text(f"Request Params: {params}")
    
    response = requests.get(url, params=params)
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
        st.text(response.text)
        return {"error": "Invalid JSON response"}

# Streamlit application
st.title("SecondHandSongs API Explorer")

# Sidebar for search type
search_type = st.sidebar.selectbox("Search Type", ["Artist", "Performance", "Work"])

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
                st.write(results)
        else:
            st.warning("Please enter an artist's name.")

# Performance search
if search_type == "Performance":
    st.header("Search for Performances")
    title = st.text_input("Enter performance title:")
    performer = st.text_input("Enter performer name (optional):")
    date = st.text_input("Enter date (optional, format YYYY-MM-DD):")
    page = st.number_input("Page", min_value=1, value=1)
    page_size = st.number_input("Results per page", min_value=1, max_value=100, value=10)

    if st.button("Search Performances"):
        if title:
            results = search_performances(title, performer, date, page, page_size)
            if "error" in results:
                st.error(results["error"])
            else:
                st.write(results)
        else:
            st.warning("Please enter a performance title.")

# Work search
if search_type == "Work":
    st.header("Search for Works")
    title = st.text_input("Enter work title:")
    credits = st.text_input("Enter credits (optional):")
    page = st.number_input("Page", min_value=1, value=1)
    page_size = st.number_input("Results per page", min_value=1, max_value=100, value=10)

    if st.button("Search Works"):
        if title:
            results = search_works(title, credits, page, page_size)
            if "error" in results:
                st.error(results["error"])
            else:
                st.write(results)
        else:
            st.warning("Please enter a work title.")

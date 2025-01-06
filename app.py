import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import streamlit as st

# Base URL for the API
BASE_URL = 'https://api.secondhandsongs.com/v1'

# Function to fetch artist data
def get_artist(artist_id):
    response = requests.get(f"{BASE_URL}/artist/{artist_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch artist data: {response.status_code}")
        return None

# Function to fetch covers data
def get_covers(artist_id):
    response = requests.get(f"{BASE_URL}/artist/{artist_id}/covers")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch covers data: {response.status_code}")
        return None

# Function to process covers data
def process_covers(data):
    artists = [cover['original_artist']['name'] for cover in data['data']]
    genres = [cover.get('genre', 'Unknown') for cover in data['data']]
    years = [cover['release_date'][:4] for cover in data['data'] if 'release_date' in cover]

    artist_influence = Counter(artists)
    genre_distribution = Counter(genres)
    year_distribution = Counter(years)
    
    return artist_influence, genre_distribution, year_distribution

# Function to draw influence graph
def draw_influence_graph(artist_influence):
    G = nx.DiGraph()
    for artist, count in artist_influence.items():
        G.add_edge(artist, 'Target Artist', weight=count)

    pos = nx.spring_layout(G)
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', width=weights, font_size=10)
    plt.title("Artist Influence Graph", fontsize=14)
    st.pyplot(plt)

# Streamlit app
st.title("Artist Influence Analyzer")
st.sidebar.header("Input Parameters")

# Input: Artist ID
artist_id = st.sidebar.text_input("Enter Artist ID", "11578")

# Analyze Button
if st.sidebar.button("Analyze"):
    st.subheader("Artist Information")
    
    # Fetch artist data
    artist_data = get_artist(artist_id)
    if artist_data:
        st.write(f"**Artist Name:** {artist_data['name']}")
        st.write(f"**Type:** {artist_data.get('type', 'Unknown')}")
    
    # Fetch covers data
    covers_data = get_covers(artist_id)
    if covers_data:
        st.write(f"**Total Covers Found:** {len(covers_data['data'])}")
        
        # Process covers data
        artist_influence, genre_distribution, year_distribution = process_covers(covers_data)

        # Display top influential artists
        st.subheader("Top Influential Artists")
        top_artists = pd.DataFrame(artist_influence.items(), columns=["Artist", "Covers"]).sort_values(by="Covers", ascending=False)
        st.dataframe(top_artists)

        # Display genre distribution
        st.subheader("Genre Distribution")
        genre_chart = pd.DataFrame(genre_distribution.items(), columns=["Genre", "Count"]).set_index("Genre")
        st.bar_chart(genre_chart)

        # Display covers over time
        st.subheader("Covers Over Time")
        year_chart = pd.DataFrame(year_distribution.items(), columns=["Year", "Count"]).set_index("Year").sort_index()
        st.line_chart(year_chart)

        # Draw influence graph
        st.subheader("Influence Graph")
        draw_influence_graph(artist_influence)

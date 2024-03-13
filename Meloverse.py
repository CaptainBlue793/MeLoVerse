"""Music Recommendation System"""

# Import Packages
import streamlit as st
import base64
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API Credentials
client_id = "29299b1c0c1f4dada0531793afcd7eb8"
client_secret = "12f661c55a2c4b739b2efbb0ab9e15c7"
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Obtaining Poster via Spotify API for a given song
def poster(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    response = sp.search(search_query, type="track", limit=1)

    if response and response["tracks"]["items"]:
        return response["tracks"]["items"][0]["album"]["images"][0]["url"]
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


# Recommendation System Function
def recommend(song, number_of_songs):
    index = Songs[Songs['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_songs_list = []
    posters_list = []

    for i in distances[1:number_of_songs + 1]:
        song_name = Songs.iloc[i[0]].song
        artist_name = Songs.iloc[i[0]].artist
        posters_list.append(poster(song_name, artist_name))
        recommended_songs_list.append(song_name)

    return recommended_songs_list, posters_list


# Music Files and Similarity Matrix
Songs = pickle.load(open("MusicSet.pkl", "rb"))
similarity = pickle.load(open("music_similarity.pkl", "rb"))
Songs_List = Songs['song'].values

# Page Layout
st.set_page_config(layout="wide")

# Font Style
with open("font.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Main content
st.markdown(
    """
    <style>
    .meloverse-title {
        font-size: 63px;
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }
    .meloverse-title span {
        transition: color 0.2s ease-in-out;
    }
    .meloverse-title:hover span {
        color: #f5fefd; /* Hover color */
    }
    .meloverse-title:hover {
        transform: scale(1.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

text = "MeLoVerse "  # Text to be styled
colored_text = ''.join(
    ['<span style="color: hsl({}, 60%, 50%);">{}</span>'.format(i * 360 / len(text), char) for i, char in
     enumerate(text)])
colored_text_with_malt = ' <span style="color: hsl(0, 80%, 60%);">&#10070;</span>  ' + colored_text + ('  <span '
                                                                                                        'style="color'
                                                                                                        ': hsl(250, '
                                                                                                        '70%, '
                                                                                                        '70'
                                                                                                        '%);">&#10070'
                                                                                                        ';</span>')
st.markdown(f'<h1 class="meloverse-title">{colored_text_with_malt}</h1>', unsafe_allow_html=True)

st.markdown(
    '<h2 style="font-size:30px;color: #F5FEFD; text-align: center;">Music Recommendation System</h2>',
    unsafe_allow_html=True,
)


# Wallpaper
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


add_bg_from_local("background.jpg")

# Streamlit Code
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Rainbow Line
        st.markdown(
            """
            <style>
            .center {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="center"><img src="https://raw.githubusercontent.com/SamirPaulb/SamirPaulb/main/assets/rainbow'
            '-superthin.webp" width=100% /></div>',
            unsafe_allow_html=True
        )
        selected_song = st.selectbox('Select a SONG', Songs_List)
    with col2:
        # Rainbow Line
        st.markdown(
            """
            <style>
            .center {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="center"><img src="https://raw.githubusercontent.com/SamirPaulb/SamirPaulb/main/assets/rainbow'
            '-superthin.webp" width=100% /></div>',
            unsafe_allow_html=True
        )
        selected_number = st.selectbox('Number of SONGS to recommend', [5, 10, 15, 20, 25])

if st.button('Recommend'):
    recommended_songs, posters = recommend(selected_song, selected_number)

    # CSS styling for columns
    st.markdown(
        """
        <style>
        .column-content {
            padding: 5px;
            text-align: center;
            background-color: rgba(31, 33, 67, 0.5); /* Semi-transparent background */
            color: #F5FEFD;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            margin-bottom: 15px;
            transition: transform 0.3s ease-in-out;
        }
        .column-content:hover {
            transform: scale(1.08);
            background-color:#0D0D1A;
        }
        .column-image {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .music-title {
            color: #F5FEFD;
            font: Open sans;
            font-size: 15px;
            margin-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Displaying recommended movies in a grid layout
    cols = st.columns(5)
    for i in range(len(recommended_songs)):
        with cols[i % 5]:
            st.markdown(
                """
                <div class="column-content">
                    <h3 class="music-title">{}</h3>
                    <div class="column-image">
                        <img src="{}" alt="Music Poster" width="150" height="150">
                    </div>
                </div>
                """.format(
                    recommended_songs[i], posters[i]
                ),
                unsafe_allow_html=True,
            )

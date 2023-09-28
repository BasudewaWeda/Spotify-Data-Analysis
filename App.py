import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import altair as alt

url: str = "https://docs.google.com/spreadsheets/d/1fmzy4nbLo7A5v7F0P6cRVjlFKMOwxdilEjdbaY5-bu0/edit?usp=sharing"
conn: GSheetsConnection = st.experimental_connection('spotify_titles', type=GSheetsConnection)

df: pd.DataFrame = conn.read(spreadsheet=url, worksheet=0)


st.header('Spotify Music Analysis')
st.subheader('Raw Data')
st.write('Raw data taken from a kaggle dataset')
st.dataframe(df)

st.divider()

st.subheader('Songs Per Year')
st.write('Amount of songs released by artists every year')

songs_per_year: pd.DataFrame = df.groupby('released_year')['track_name'].count().reset_index()
songs_per_year.columns = ['Year', 'Songs Released']
songs_per_year_chart = (
    alt.Chart(songs_per_year).mark_bar().encode(
        x = alt.X('Year'),
        y = alt.Y('Songs Released')
    )
)
st.altair_chart(songs_per_year_chart, use_container_width=True)

st.divider()

st.subheader('Artists With The Most Songs')
st.write('Top 10 artists with with the most songs released')

top_10_artists_with_most_songs: pd.DataFrame = df['artist(s)_name'].apply(lambda x: x.replace(' ,',',').replace(', ',',').split(','))

Artists: list = []
for i in top_10_artists_with_most_songs: Artists += i
Artists: pd.DataFrame = pd.DataFrame(Artists, columns=['Artists']).value_counts().head(10).reset_index()
Artists.columns = ['Artists', 'Songs Released']

Artists_chart = (
    alt.Chart(Artists).mark_bar().encode(
        x = alt.X('Songs Released'),
        y = alt.Y('Artists', sort='-x')
    )
)
st.altair_chart(Artists_chart, use_container_width=True)

st.divider()

st.subheader('Top 10 Songs')
st.write('Songs with most amount of streams')

top_10_songs: pd.DataFrame = df[['track_name', 'streams']]
top_10_songs['streams'] = pd.to_numeric(top_10_songs['streams'], errors='coerce')
top_10_songs = top_10_songs.sort_values(by=['streams'], ascending=False).head(10)
top_10_songs.columns = ['Song Title', 'Streams']

top_10_songs_chart = (
    alt.Chart(top_10_songs).mark_bar().encode(
        x = alt.X('Streams'),
        y = alt.Y('Song Title', sort='-x')
    )
)
st.altair_chart(top_10_songs_chart, use_container_width=True)

st.divider()

st.subheader('Top 10 BPM')
st.write('Most used Beats Per Minute (BPM)')
top_10_bpm: pd.DataFrame = df['bpm'].value_counts().reset_index().sort_values(by=['bpm'], ascending=False).head(10)
top_10_bpm.columns = ['Beats per Minute', 'Count']
top_10_bpm['Beats per Minute'] = top_10_bpm['Beats per Minute'].astype('string')

top_10_bpm_chart = (
    alt.Chart(top_10_bpm).mark_bar().encode(
        x = alt.X('Count'),
        y = alt.Y('Beats per Minute', sort='-x')
    )
)
st.altair_chart(top_10_bpm_chart, use_container_width=True)

st.divider()

st.subheader('Major VS Minor')
st.write('Amount of songs using major mode and minor mode')
major_minor: pd.DataFrame = df['mode'].value_counts().reset_index()
major_minor.columns = ['Mode', 'Count']

major_minor_chart = (
    alt.Chart(major_minor).mark_bar().encode(
        x = alt.X('Mode', sort='-y'),
        y = alt.Y('Count')
    ).configure_axisX(labelAngle=0)
)

st.altair_chart(major_minor_chart, use_container_width=True)

st.divider()

st.subheader('Top 10 Keys')
st.write('Top 10 most used keys in songs')

keys: pd.DataFrame = df['key'].value_counts().reset_index().sort_values(by=['key'], ascending=False).head(10)
keys.columns = ['Key', 'Count']

keys_chart = (
    alt.Chart(keys).mark_bar().encode(
        x = alt.X('Count'),
        y = alt.Y('Key', sort='-x')
    )
)

st.altair_chart(keys_chart, use_container_width=True)
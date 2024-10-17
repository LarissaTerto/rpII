CLIENT_ID = ''
CLIENT_SECRET = ''
AUTH_URL = 'https://accounts.spotify.com/api/token'

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artista = []
musica_titulo = []
musica_popularidade = []
musica_duracao = []
artista_id = []
musica_id = []
musica_data_lancamento = []

for i in range(0, 20, 50):
    resultado = sp.search(q=f'genre:K-pop year:2023', type='track', limit=50, offset=i)
    for i, t in enumerate(resultado['tracks']['items']):
        artista.append(t['artists'][0]['name'])
        artista_id.append(t['artists'][0]['id'])
        musica_titulo.append(t['name'])
        musica_id.append(t['id'])
        musica_popularidade.append(t['popularity'])
        musica_duracao.append(t['duration_ms'])
        musica_data_lancamento.append(t['album']['release_date'])

df = pd.DataFrame({'artista': artista,
                               'musica_titulo': musica_titulo,
                               'musica_popularidade': musica_popularidade,
                               'musica_duracao': musica_duracao,
                               'artista_id': artista_id,
                               'musica_id': musica_id,
                               'musica_data_lancamento': musica_data_lancamento
                               })


musica_features = []
for m_id in df['musica_id']:
    af = sp.audio_features(m_id)
    musica_features.append(af)

mf_df = pd.DataFrame(columns=['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'id'])

i = 0
for item in musica_features:
    for feat in item:
        mf_df = mf_df._append({'danceability': feat['danceability'],
                              'energy': feat['energy'],
                              'loudness': feat['loudness'],
                              'speechiness': feat['speechiness'],
                              'acousticness': feat['acousticness'],
                              'instrumentalness': feat['instrumentalness'],
                              'liveness': feat['liveness'],
                              'valence': feat['valence'],
                              'tempo': feat['tempo'],
                              'duration_ms': feat['duration_ms'],
                              'time_signature': feat['time_signature'],
                              'musica_titulo': musica_titulo[i]}, ignore_index=True)
        i = i+1
#elimina colunas iguais
mf_df.drop('id', axis = 1, inplace = True)
pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', None)         # Auto-adjust width to fit the screen
pd.set_option('display.colheader_justify', 'left')
print(mf_df)

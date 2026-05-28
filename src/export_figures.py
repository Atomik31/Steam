import pandas as pd
import plotly.express as px
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "reports" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Chargement ────────────────────────────────────────────────────────────────
DATA = Path(__file__).resolve().parents[1] / "data" / "raw" / "steam_game_output.json"

df_raw = pd.read_json(DATA)
COLS = ['appid','name','developer','publisher','genre','type','owners',
        'positive','negative','price','initialprice','discount','ccu',
        'languages','release_date','required_age',
        'platforms.windows','platforms.mac','platforms.linux']

df = pd.json_normalize(df_raw['data'])[COLS].copy().reset_index(drop=True)
df = df.rename(columns={'platforms.windows':'win','platforms.mac':'mac','platforms.linux':'linux'})

df['price_eur']      = pd.to_numeric(df['price'], errors='coerce') / 100
df['discount']       = pd.to_numeric(df['discount'], errors='coerce').fillna(0).astype(int)
df['release_date']   = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year']   = df['release_date'].dt.year
df['positive']       = pd.to_numeric(df['positive'], errors='coerce')
df['negative']       = pd.to_numeric(df['negative'], errors='coerce')
total_avis           = df['positive'] + df['negative']
df['positive_ratio'] = (df['positive'] / total_avis * 100).round(1)
df['required_age']   = pd.to_numeric(df['required_age'], errors='coerce').fillna(0).astype(int)
df = df.rename(columns={'genre': 'genre_str'})
df['type_prix']   = df['price_eur'].apply(lambda x: 'Gratuit (F2P)' if x == 0 else 'Payant')

def combo(row):
    p = []
    if row['win']:   p.append('Win')
    if row['mac']:   p.append('Mac')
    if row['linux']: p.append('Linux')
    return ' + '.join(p) if p else 'Aucune'
df['plateformes'] = df.apply(combo, axis=1)

df_genres = df.copy()
df_genres['genre'] = df['genre_str'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
df_genres = df_genres.explode('genre').reset_index(drop=True)
df_genres = df_genres.dropna(subset=['genre'])
df_genres = df_genres[df_genres['genre'] != ''].reset_index(drop=True)

def save(fig, name):
    path = OUTPUT_DIR / f"{name}.png"
    fig.write_image(str(path))
    print(f"  {path.name}")

print("Export des figures Steam...")

# 01 — Top éditeurs
top_pub = df['publisher'].value_counts().head(20).reset_index()
top_pub.columns = ['Publisher', 'Nombre de jeux']
fig = px.bar(top_pub, x='Nombre de jeux', y='Publisher', orientation='h',
             title='Top 20 éditeurs par nombre de jeux publiés sur Steam',
             color='Nombre de jeux', color_continuous_scale='Blues', height=600)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "01_top_publishers")

# 02 — Top rated (ratio)
mask = total_avis >= 100
top_rated = df[mask].nlargest(15, 'positive_ratio')[['name','publisher','positive_ratio','positive','release_year']].reset_index(drop=True)
fig = px.bar(top_rated, x='positive_ratio', y='name', orientation='h',
             title="Top 15 jeux par % d'avis positifs (min. 100 avis)",
             labels={'positive_ratio': '% avis positifs', 'name': ''},
             color='positive_ratio', color_continuous_scale='Greens', height=500)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "02_top_rated_ratio")

# 03 — Top rated (volume)
top_volume = df.nlargest(15, 'positive')[['name','publisher','positive','positive_ratio']].reset_index(drop=True)
fig = px.bar(top_volume, x='positive', y='name', orientation='h',
             title="Top 15 jeux par volume d'avis positifs",
             labels={'positive': "Nombre d'avis positifs", 'name': ''},
             color='positive', color_continuous_scale='Purples', height=500)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "03_top_rated_volume")

# 04 — Sorties par année
releases = df[df['release_year'].between(2000, 2024)].groupby('release_year').size().reset_index(name='nb_sorties')
fig = px.bar(releases, x='release_year', y='nb_sorties',
             title='Nombre de sorties par année sur Steam',
             labels={'release_year': 'Année', 'nb_sorties': 'Nombre de jeux'},
             color='nb_sorties', color_continuous_scale='Oranges', width=800, height=450)
fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor='red', opacity=0.1,
              annotation_text='Période Covid', annotation_position='top left')
save(fig, "04_releases_by_year")

# 05 — Gratuit vs Payant
type_prix = df['type_prix'].value_counts().reset_index()
type_prix.columns = ['Type', 'Nombre']
fig = px.pie(type_prix, values='Nombre', names='Type',
             title='Répartition jeux gratuits vs payants',
             color_discrete_map={'Gratuit (F2P)': '#2ecc71', 'Payant': '#3498db'},
             width=550, height=400)
save(fig, "05_free_vs_paid")

# 06 — Distribution des prix
payants = df[df['price_eur'] > 0]['price_eur']
fig = px.histogram(payants, x='price_eur', nbins=50,
                   title=f'Distribution des prix — médiane : {payants.median():.2f}€',
                   labels={'price_eur': 'Prix (€)', 'count': 'Nombre de jeux'},
                   color_discrete_sequence=['#3498db'], width=750, height=430)
fig.add_vline(x=payants.median(), line_dash='dash', line_color='red',
              annotation_text=f'Médiane : {payants.median():.2f}€')
save(fig, "06_price_distribution")

# 07 — Promotions
promo = df[df['price_eur'] > 0].copy()
promo['statut'] = (promo['discount'] > 0).map({True: 'En promotion', False: 'Prix normal'})
promo_counts = promo['statut'].value_counts().reset_index()
promo_counts.columns = ['Statut', 'Nombre']
fig = px.pie(promo_counts, values='Nombre', names='Statut',
             title='Part des jeux actuellement en promotion',
             color_discrete_map={'En promotion': '#e67e22', 'Prix normal': '#95a5a6'},
             width=550, height=400)
save(fig, "07_promotions")

# 08 — Langues
lang_series = df['languages'].dropna().str.split(',').explode().str.strip()
lang_series = lang_series[lang_series != '']
top_lang = lang_series.value_counts().head(15).reset_index()
top_lang.columns = ['Langue', 'Nombre de jeux']
fig = px.bar(top_lang, x='Nombre de jeux', y='Langue', orientation='h',
             title='Top 15 langues supportées sur Steam',
             color='Nombre de jeux', color_continuous_scale='Teal', height=500)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "08_top_languages")

# 09 — Tranches d'âge
def tranche_age(a):
    if a == 0:    return 'Tous publics'
    elif a <= 12: return '12+'
    elif a <= 16: return '16+'
    else:         return '18+'
age_dist = df['required_age'].apply(tranche_age).value_counts().reset_index()
age_dist.columns = ['Tranche', 'Nombre']
fig = px.pie(age_dist, values='Nombre', names='Tranche',
             title="Répartition des jeux par restriction d'âge",
             width=550, height=400)
save(fig, "09_age_restriction")

# 10 — Top genres
top_genres = df_genres['genre'].value_counts().head(20).reset_index()
top_genres.columns = ['Genre', 'Nombre de jeux']
fig = px.bar(top_genres, x='Nombre de jeux', y='Genre', orientation='h',
             title='Top 20 genres les plus représentés sur Steam',
             color='Nombre de jeux', color_continuous_scale='Blues', height=600)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "10_top_genres")

# 11 — Ratio avis par genre
mask_avis = (df_genres['positive'] + df_genres['negative']) >= 50
genre_reviews = df_genres[mask_avis].groupby('genre').agg(
    ratio_moyen=('positive_ratio','mean'), nb_jeux=('appid','count')
).round(1).reset_index()
genre_reviews = genre_reviews[genre_reviews['nb_jeux'] >= 20].sort_values('ratio_moyen', ascending=False)
fig = px.bar(genre_reviews, x='ratio_moyen', y='genre', orientation='h',
             title="Ratio moyen d'avis positifs par genre",
             labels={'ratio_moyen': '% avis positifs', 'genre': 'Genre'},
             color='ratio_moyen', color_continuous_scale='RdYlGn',
             range_color=[60, 90], height=600)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "11_genre_review_ratio")

# 12 — Genres favoris top éditeurs
top10_pub = df['publisher'].value_counts().head(10).index.tolist()
pub_genres = df_genres[df_genres['publisher'].isin(top10_pub)].groupby(
    ['publisher','genre']).size().reset_index(name='nb_jeux')
fig = px.bar(pub_genres, x='nb_jeux', y='publisher', color='genre',
             title='Genres favoris des 10 plus gros éditeurs Steam',
             labels={'nb_jeux': 'Nombre de jeux', 'publisher': 'Éditeur'},
             orientation='h', height=500, width=900)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
save(fig, "12_publisher_genres")

# 13 — Prix et popularité par genre (scatter)
genre_revenue = df_genres[df_genres['price_eur'] > 0].groupby('genre').agg(
    prix_moyen=('price_eur','mean'),
    avis_positifs_moyens=('positive','mean'),
    nb_jeux=('appid','count')
).round(2).reset_index()
genre_revenue = genre_revenue[genre_revenue['nb_jeux'] >= 20]
fig = px.scatter(genre_revenue, x='prix_moyen', y='avis_positifs_moyens',
                 size='nb_jeux', color='genre', hover_name='genre',
                 title='Prix moyen vs popularité par genre',
                 labels={'prix_moyen': 'Prix moyen (€)', 'avis_positifs_moyens': 'Avis positifs moyens'},
                 width=900, height=600)
save(fig, "13_genre_price_vs_popularity")

# 14 — Plateformes
platforms = pd.DataFrame({
    'Plateforme': ['Windows', 'Mac', 'Linux'],
    'Pourcentage (%)': [
        round(df['win'].mean() * 100, 1),
        round(df['mac'].mean() * 100, 1),
        round(df['linux'].mean() * 100, 1)
    ]
})
fig = px.bar(platforms, x='Plateforme', y='Pourcentage (%)',
             title='Part des jeux disponibles par plateforme',
             text='Pourcentage (%)', color='Plateforme', width=600, height=420)
fig.update_traces(texttemplate='%{text}%', textposition='outside')
save(fig, "14_platforms")

# 15 — Combinaisons de plateformes
combo_counts = df['plateformes'].value_counts().reset_index()
combo_counts.columns = ['Combo', 'Nombre']
fig = px.pie(combo_counts, values='Nombre', names='Combo',
             title='Combinaisons de plateformes supportées',
             width=600, height=450)
save(fig, "15_platform_combos")

# 16 — Genres par plateforme
gp = df_genres.groupby('genre').agg(
    pct_win=('win','mean'), pct_mac=('mac','mean'), pct_linux=('linux','mean'), nb_jeux=('appid','count')
).reset_index()
gp[['pct_win','pct_mac','pct_linux']] = (gp[['pct_win','pct_mac','pct_linux']] * 100).round(1)
gp = gp[gp['nb_jeux'] >= 20].sort_values('pct_mac', ascending=False)
fig = px.bar(gp.head(20), x='genre', y=['pct_win','pct_mac','pct_linux'],
             title='Disponibilité par plateforme selon le genre (%)',
             labels={'value': '% de jeux dispo', 'genre': 'Genre', 'variable': 'Plateforme'},
             barmode='group', height=500, width=1000)
fig.update_layout(xaxis_tickangle=-40)
save(fig, "16_genre_by_platform")

print(f"\nDone — 16 figures exportées dans {OUTPUT_DIR}")

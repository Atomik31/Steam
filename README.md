![Steam](Steam_logo.jpg)

# Steam — Analyse du marché des jeux vidéo

Projet réalisé dans le cadre du bloc 2 de la certification CDSD (Jedha).

---

## Livrable Databricks

> https://dbc-1c28fa48-0684.cloud.databricks.com/browse/folders/723727034928580?o=3008415357916144

---

## Contexte

Ubisoft veut lancer un nouveau jeu et cherche à mieux comprendre l'écosystème Steam avant de se positionner. L'idée : analyser les 55 000+ jeux disponibles sur la plateforme pour identifier les tendances, les genres porteurs et ce qui influence la popularité d'un titre.

---

## Ce que j'ai fait

Analyse exploratoire en PySpark sur Databricks, organisée en trois niveaux :

**Macro** — Quels éditeurs publient le plus ? Quelles années ont vu le plus de sorties ? Comment sont distribués les prix ? Quelles langues dominent ? Combien de jeux sont interdits aux mineurs ?

**Genres** — Quels genres dominent le catalogue ? Lesquels ont le meilleur ratio d'avis positifs ? Quels sont les genres favoris des gros éditeurs ? Quels sont les plus lucratifs ?

**Plateformes** — Répartition Windows / Mac / Linux. Certains genres sont-ils liés à certaines plateformes ?

---

## Stack

- PySpark sur Databricks
- Visualisations natives Databricks (`display()`)
- Méthodes : `getField()`, `explode()`, `groupBy()`, fonctions de date et texte

---

## Données

Dataset JSON mis à disposition par Jedha sur S3 :
```
s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json
```

---

## Structure

```
Steam/
├── data/
│   ├── raw/
│   │   └── steam_game_output.json   # Dataset (~61 MB)
│   └── processed/
├── docs/
│   └── consignes.md
├── notebooks/
│   ├── steam_pyspark.ipynb          # Notebook Databricks (PySpark) — livrable principal
│   └── steam.ipynb                  # Version locale exploratoire (Pandas/Plotly)
├── reports/
│   └── figures/
│       ├── 01_top_publishers.png
│       ├── 02_top_rated_ratio.png
│       ├── 03_top_rated_volume.png
│       ├── 04_releases_by_year.png
│       ├── 05_free_vs_paid.png
│       ├── 06_price_distribution.png
│       ├── 07_promotions.png
│       ├── 08_top_languages.png
│       ├── 09_age_restriction.png
│       ├── 10_top_genres.png
│       ├── 11_genre_review_ratio.png
│       ├── 12_publisher_genres.png
│       ├── 13_genre_price_vs_popularity.png
│       ├── 14_platforms.png
│       ├── 15_platform_combos.png
│       └── 16_genre_by_platform.png
├── requirements.txt
└── README.md
```

---

Julien CHARLIER — [(Github : Atomik31)](https://github.com/Atomik31)

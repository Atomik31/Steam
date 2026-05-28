# Steam — Analyse du marché des jeux vidéo

Projet réalisé dans le cadre du bloc 2 de la certification CDSD (Jedha).

---

## Livrable Databricks

> https://dbc-1c28fa48-0684.cloud.databricks.com/editor/notebooks/3899804356778133?o=3008415357916144

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
│   └── raw/               # Dataset JSON (~61 MB)
├── docs/
│   └── consignes.md
├── notebooks/
│   ├── steam_pyspark.ipynb  # Notebook Databricks (PySpark) — livrable principal
│   └── steam.ipynb          # Version locale exploratoire (Pandas/Plotly)
├── reports/
│   └── figures/
└── README.md
```

---

Julien CHARLIER — [(Github : Atomik31)](https://github.com/Atomik31)

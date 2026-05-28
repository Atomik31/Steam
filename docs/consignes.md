# Steam — Analyse du marché des jeux vidéo

## Contexte

Steam est la plateforme de distribution de jeux vidéo de Valve, lancée en 2003. Elle propose des milliers de jeux, des fonctionnalités sociales, un système anti-triche et un marketplace de contenus.

**Contexte métier :** Vous travaillez pour Ubisoft. Ils souhaitent lancer un nouveau jeu et vous demandent de conduire une analyse globale du marché Steam pour mieux comprendre l'écosystème et les tendances actuelles.

---

## Objectif

Comprendre quels facteurs influencent la popularité ou les ventes d'un jeu vidéo, tout en conduisant une analyse globale du marché.

---

## Questions à explorer

### Analyse macro
- Quel éditeur a sorti le plus de jeux sur Steam ?
- Quels sont les jeux les mieux notés ?
- Y a-t-il des années avec plus de sorties ? (ex. impact du Covid ?)
- Comment sont distribués les prix ? Y a-t-il beaucoup de jeux en promotion ?
- Quelles sont les langues les plus représentées ?
- Y a-t-il beaucoup de jeux interdits aux moins de 16/18 ans ?

### Analyse par genre
- Quels sont les genres les plus représentés ?
- Certains genres ont-ils un meilleur ratio avis positifs/négatifs ?
- Certains éditeurs ont-ils des genres favoris ?
- Quels sont les genres les plus lucratifs ?

### Analyse par plateforme
- La majorité des jeux sont-ils disponibles sur Windows / Mac / Linux ?
- Certains genres sont-ils préférentiellement disponibles sur certaines plateformes ?

---

## Stack technique

- **PySpark** sur **Databricks**
- Visualisations avec l'outil natif Databricks (`display()`)
- Méthodes utiles : `getField()`, `explode()`, `groupBy()`, fonctions de date et texte

---

## Données

Dataset JSON disponible sur S3 :
```
s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json
```

---

## Livrable

Un ou plusieurs notebooks Databricks publiés (bouton "Publish"), avec le lien déposé dans le repo Github.

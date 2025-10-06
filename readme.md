# Application Streamlit Python - Répertoire national des élus RNE

- Cette application a été développée à partir des jeux de données [RNE publiés sur data.gouv.fr](https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1/) sur le fichier **elus-conseillers-municipaux-cm.csv**.

- L’objectif de l’application est de comparer clairement les effectifs masculins et féminins afin de visualiser les déséquilibres. 

> Avertissement — Les statistiques présentées ici sont générées dans le cadre d’un exercice et peuvent comporter des imprécisions, omissions ou erreurs (saisie, arrondis, méthodes de calcul, mises à jour, etc.). Elles sont fournies à titre indicatif et ne sauraient se substituer aux sources originales. L’éditeur décline toute responsabilité pour les conséquences d’une utilisation exclusive de ces données.

## Librairies python

Streamlit, Polars, Plotly

## Gestion des dépendances

`pip freeze > requirements.txt`

`pip install -r requirements.txt`

## Lancement de l'application

`streamlit run app.py`

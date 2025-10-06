import streamlit as st
from data.loader import (
    load_departement_data,
    load_enregristrement_total,
    load_fonctions_data,
    load_fonctions_number_data,
    load_genre_proportion_data,
    load_age_distribution_data,
    load_cat_socio_pro_data,
)

from viz.charts import (
    plot_age_bar_h_f,
    plot_cat_socio_pro_bar,
    genre_pie,
    plot_fonction_volume_bar_h_f,
)
from constants.config import APP_TITLE


def main():
    st.set_page_config(APP_TITLE, layout="wide")

    st.title("Répertoire national des élus RNE (12 juin 2025)")
    st.header("Les conseillers municipaux")
    st.markdown(
        """
        Cette application a été développée à partir des jeux de données [RNE publiés sur data.gouv.fr](https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1/) sur le fichier **elus-conseillers-municipaux-cm.csv**.
        L’objectif de l’application est de comparer clairement les effectifs masculins et féminins afin de visualiser les déséquilibres. \n
        > Avertissement — Les statistiques présentées ici sont générées dans le cadre d’un exercice et peuvent comporter des imprécisions, omissions ou erreurs (saisie, arrondis, méthodes de calcul, mises à jour, etc.). Elles sont fournies à titre indicatif et ne sauraient se substituer aux sources originales. L’éditeur décline toute responsabilité pour les conséquences d’une utilisation exclusive de ces données. """
    )

    departement_name_list, departement_dict = load_departement_data()
    fonctions = load_fonctions_data()

    st.sidebar.header("Filtres")

    st.sidebar.divider()

    # Filtres pour les départements

    st.sidebar.selectbox(
        "Département",
        options=departement_name_list,
        key="selectbox_dep_key",
    )

    st.sidebar.divider()

    # Filtres pour les fonctions (Maire, Maire délégué, Adjoint du maire)

    st.sidebar.text("Fonctions")

    st.sidebar.checkbox(
        "Tous",
        value=True,
        key="checkbox_fonctions_tous_key",
    )

    st.sidebar.selectbox(
        "Rôle",
        options=fonctions,
        key="selectbox_fonctions_key",
        disabled=st.session_state["checkbox_fonctions_tous_key"],
    )

    dep_filtre = "*"

    if st.session_state["selectbox_dep_key"] != "Tous":
        dep_filtre = departement_dict[st.session_state["selectbox_dep_key"]]

    fonction_filtre = "*"

    if st.session_state["checkbox_fonctions_tous_key"] is False:
        fonction_filtre = st.session_state["selectbox_fonctions_key"]

    # Affichage du titre des graphiques en fonction des filtres sélectionnés
    header_text = ""
    if dep_filtre == "*":
        header_text = "Tous les départements"
    else:
        header_text = f"Pour le département {dep_filtre} - {st.session_state["selectbox_dep_key"]}"

    if fonction_filtre != "*":
        header_text += f' et pour la fonction de "{fonction_filtre}" uniquement'
    else:
        header_text += " et pour toutes les fonctions"

    st.subheader(header_text)

    # Layout des graphiques

    # 1 colonne full-width
    metrics = st.columns(1, vertical_alignment="top", border=True)

    # Nombre total d'enregistrements
    total = load_enregristrement_total(dep_filtre, fonction_filtre)
    metrics[0].markdown(
        f"Nombre total d'enregistrements: **{total[0]:,d} Hommes** et **{total[1]:,d} Femmes**"
    )

    # Deux colonnes
    left1, right1 = st.columns(2, vertical_alignment="top", border=True)

    # Proportion % homme femme
    data_genre = load_genre_proportion_data(dep_filtre, fonction_filtre)
    left1.plotly_chart(genre_pie(data_genre))

    # Volume des fonctions homme femme
    key_list, value_h = load_fonctions_number_data(dep_filtre, "M", fonction_filtre)
    key_list, value_f = load_fonctions_number_data(dep_filtre, "F", fonction_filtre)
    right1.plotly_chart(plot_fonction_volume_bar_h_f(key_list, value_h, value_f))

    # 1 colonnes full-width
    left_m = st.columns(1, vertical_alignment="top", border=True)

    # Distribution des âges homme femme
    data_age_m = load_age_distribution_data(dep_filtre, "M", fonction_filtre)
    data_age_f = load_age_distribution_data(dep_filtre, "F", fonction_filtre)
    left_m[0].plotly_chart(plot_age_bar_h_f(data_age_m, data_age_f))

    # Deux colonnes
    left2, right2 = st.columns(2, vertical_alignment="top", border=True)

    # Catégorie socio-professionnelle homme femme
    data_cat_socio_pro_m = load_cat_socio_pro_data(dep_filtre, "M", fonction_filtre)
    left2.plotly_chart(plot_cat_socio_pro_bar(data_cat_socio_pro_m, "M"))
    data_cat_socio_pro_f = load_cat_socio_pro_data(dep_filtre, "F", fonction_filtre)
    right2.plotly_chart(plot_cat_socio_pro_bar(data_cat_socio_pro_f, "F"))


if __name__ == "__main__":
    main()

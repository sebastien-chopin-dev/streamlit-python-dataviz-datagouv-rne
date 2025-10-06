import polars as pl
import streamlit as st

from utils.helpers import from_dtn_to_age


# Chargement et filtre du fichier CSV en fonction des départements et fonctions
def get_csv_filtered(dep_filtre: str, fonction_filtre: str, cols: list):
    cols_with_code = cols.append("Code du département")
    df = pl.read_csv(
        "elus-conseillers-municipaux-cm.csv",
        columns=cols_with_code,
        truncate_ragged_lines=True,
        separator=";",
        infer_schema=False,
    )

    if dep_filtre != "*":
        df = df.filter(pl.col("Code du département") == dep_filtre)

    if fonction_filtre == "Maire":
        df = df.filter(pl.col("Libellé de la fonction") == "Maire")

    if fonction_filtre == "Maire délégué":
        df = df.filter(pl.col("Libellé de la fonction") == "Maire délégué")

    if fonction_filtre == "Adjoint du maire":
        df = df.filter(pl.col("Libellé de la fonction").str.contains_any(["adjoint"]))

    return df


# Chargement du nombre total d'enregistrements
def load_enregristrement_total(dep_filtre: str, fonction_filtre: str):
    columns_selection = ["Code sexe"]
    df = get_csv_filtered(
        dep_filtre=dep_filtre, fonction_filtre=fonction_filtre, cols=columns_selection
    )

    sexe_count = df.group_by("Code sexe").len(name="number")
    count_h = sexe_count.filter(pl.col("Code sexe") == "M").select("number").item()
    count_f = sexe_count.filter(pl.col("Code sexe") == "F").select("number").item()
    return [count_h, count_f]


# Chargement du pourcentage homme femme
def load_genre_proportion_data(dep_filtre: str, fonction_filtre: str):
    columns_selection = ["Code sexe"]
    df = get_csv_filtered(
        dep_filtre=dep_filtre, fonction_filtre=fonction_filtre, cols=columns_selection
    )

    sexe_count = df.group_by("Code sexe").len(name="number")
    count_h = sexe_count.filter(pl.col("Code sexe") == "M").select("number").item()
    count_f = sexe_count.filter(pl.col("Code sexe") == "F").select("number").item()

    pourcentage_h = round(count_h * 100.0 / (count_h + count_f), 2)
    pourcentage_f = round(count_f * 100.0 / (count_h + count_f), 2)

    pie_data = {
        "sexe": ["Homme", "Femme"],
        "Pourcentage": [pourcentage_h, pourcentage_f],
    }
    return pl.DataFrame(pie_data)


# Chargement de la distribution des âges
def load_age_distribution_data(dep_filtre: str, genre: str, fonction_filtre: str):
    columns_selection = [
        "Date de naissance",
        "Code sexe",
    ]
    df = get_csv_filtered(
        dep_filtre=dep_filtre, fonction_filtre=fonction_filtre, cols=columns_selection
    )
    df = df.filter(pl.col("Code sexe") == genre)

    # 03/11/1951 exemple date naissance du fichier csv
    if df["Date de naissance"].dtype != pl.Datetime:
        df = df.with_columns(
            pl.col("Date de naissance").str.strptime(pl.Date, "%d/%m/%Y").alias("Date")
        )

    # 1951-11-03
    s_date = df["Date"].map_elements(from_dtn_to_age)
    df = s_date.to_frame()

    df = df.filter((pl.col("Date") >= 18) & (pl.col("Date") <= 100))

    df = df.group_by("Date").len(name="Volume")
    df = df.sort(["Date"])

    return df


# Chargement de la catégorie socio-professionnelle
def load_cat_socio_pro_data(dep_filtre: str, genre: st, fonction_filtre: str):
    columns_selection = [
        "Code de la catégorie socio-professionnelle",
        "Libellé de la catégorie socio-professionnelle",
        "Code sexe",
    ]
    df = get_csv_filtered(
        dep_filtre=dep_filtre, fonction_filtre=fonction_filtre, cols=columns_selection
    )
    df = df.filter(pl.col("Code sexe") == genre)

    df_lib = df.unique(
        subset=[
            "Code de la catégorie socio-professionnelle",
            "Libellé de la catégorie socio-professionnelle",
        ]
    )
    df_lib = df_lib.drop_nulls("Code de la catégorie socio-professionnelle")
    df_lib = df_lib.sort(
        ["Code de la catégorie socio-professionnelle"], descending=False
    )

    df = df.drop_nulls("Code de la catégorie socio-professionnelle")
    df = df.group_by("Code de la catégorie socio-professionnelle").len(name="Volume")
    df = df.sort(["Volume"], descending=True)

    df = df.join(
        df_lib,
        left_on="Code de la catégorie socio-professionnelle",
        right_on="Code de la catégorie socio-professionnelle",
        how="left",
    ).drop("Code de la catégorie socio-professionnelle")

    df = df.limit(25)

    return df


# Chargement des options pour le filtre des fonctions
@st.cache_data
def load_fonctions_data():
    return ["Maire", "Maire délégué", "Adjoint du maire"]


# Chargement des options pour le filtre des départements
@st.cache_data
def load_departement_data():
    df = pl.read_csv(
        "elus-conseillers-municipaux-cm.csv",
        columns=[
            "Code du département",
            "Libellé du département",
        ],
        truncate_ragged_lines=True,
        separator=";",
        infer_schema=False,
    )

    df = df.unique(
        subset=[
            "Code du département",
            "Libellé du département",
        ]
    )

    df = df.drop_nulls(["Code du département", "Libellé du département"])
    df = df.sort(["Code du département"], descending=False)

    lib_list = df["Libellé du département"].to_list()
    lib_list.insert(0, "Tous")

    dict_departement = {}

    for row in df.iter_rows(named=True):
        dict_departement[row["Libellé du département"]] = row["Code du département"]

    return lib_list, dict_departement


# Exploration des options pour le filtre des fonctions
def load_fonction_data():
    df = pl.read_csv(
        "elus-conseillers-municipaux-cm.csv",
        columns=[
            "Libellé de la fonction",
        ],
        truncate_ragged_lines=True,
        separator=";",
        infer_schema=False,
    )

    df = df.unique(
        subset=[
            "Libellé de la fonction",
        ]
    )
    return df


# Chargement du nombre de fonction (Maire, Maire délégué, Adjoint du maire)
def load_fonctions_number_data(dep_filtre: str, genre: str, fonction_filtre: str):
    columns_selection = ["Libellé de la fonction", "Code sexe"]
    df = get_csv_filtered(
        dep_filtre=dep_filtre, fonction_filtre=fonction_filtre, cols=columns_selection
    )
    df = df.filter(pl.col("Code sexe") == genre)

    datas = {}

    # Total
    df_total = df.group_by("Libellé de la fonction").len(name="Volume")
    total_count = 0
    for row in df_total.iter_rows(named=True):
        total_count += int(row["Volume"])

    # Fonction Maire
    df_maire = df.filter(pl.col("Libellé de la fonction") == "Maire")
    df_maire_len = df_maire.group_by("Libellé de la fonction").len(name="Volume")

    if fonction_filtre == "*" or fonction_filtre == "Maire":
        if df_maire_len["Volume"].count() > 0:
            datas["Maire"] = df_maire_len["Volume"][0]
        else:
            datas["Maire"] = 0

    # Fonction Délégué
    df_maire_delegue = df.filter(pl.col("Libellé de la fonction") == "Maire délégué")
    df_maire_delegue_len = df_maire_delegue.group_by("Libellé de la fonction").len(
        name="Volume"
    )

    if fonction_filtre == "*" or fonction_filtre == "Maire délégué":
        if df_maire_delegue_len["Volume"].count() > 0:
            datas["Maire délégué"] = df_maire_delegue_len["Volume"][0]
        else:
            datas["Maire délégué"] = 0

    # Fonction Adjoints
    df_maire_adjoint = df.filter(
        pl.col("Libellé de la fonction").str.contains_any(["adjoint"])
    )

    df_maire_adjoint_len = df_maire_adjoint.group_by("Libellé de la fonction").len(
        name="Volume"
    )

    count_total_adjoints = 0
    for row in df_maire_adjoint_len.iter_rows(named=True):
        count_total_adjoints += int(row["Volume"])

    if fonction_filtre == "*" or fonction_filtre == "Adjoint du maire":
        datas["Adjoint du maire"] = count_total_adjoints

    if fonction_filtre == "*":
        datas["Autres"] = (
            total_count
            - datas["Adjoint du maire"]
            - datas["Maire délégué"]
            - datas["Maire"]
        )

    key_list = []
    value_list = []

    for key, value in datas.items():
        key_list.append(key)
        value_list.append(value)

    return key_list, value_list

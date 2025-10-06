import plotly.graph_objects as go
import plotly.express as px
import polars as pl
from constants.config import COLOR_F, COLOR_H


# Plotly pie chart for proportion homme femme
def genre_pie(df: pl.DataFrame):
    df_pandas = df.to_pandas()
    return px.pie(
        df_pandas,
        values="Pourcentage",
        names="sexe",
        color="sexe",
        title="Répartition Homme Femme",
        color_discrete_map={
            "Homme": COLOR_H,
            "Femme": COLOR_F,
        },
    )


# Plotly bar chart for age distribution
def plot_age_bar_h_f(df_h: pl.DataFrame, df_f: pl.DataFrame):
    fig = go.Figure(
        data=[
            go.Bar(name="Homme", x=df_h["Date"].to_list(), y=df_h["Volume"].to_list()),
            go.Bar(
                name="Femme",
                x=df_f["Date"].to_list(),
                y=df_f["Volume"].to_list(),
                marker_color=COLOR_F,
            ),
        ]
    )

    fig.update_layout(
        barmode="group",
        xaxis_title="Âge",
        yaxis_title="Volume",
        title_x=0.5,
        title="Distribution des âges",
        showlegend=True,
        xaxis=dict(type="category", dtick=5),
    )

    fig.update_traces(orientation="v")

    return fig


# Plotly bar chart for fonction ("Maire", "Maire délégué", "adjoint") volume homme femme
def plot_fonction_volume_bar_h_f(
    key_list: list, value_h_list: list, value_f_list: list
):
    fig = go.Figure(
        data=[
            go.Bar(name="Homme", x=value_h_list, y=key_list),
            go.Bar(
                name="Femme",
                x=value_f_list,
                y=key_list,
                marker_color=COLOR_F,
            ),
        ]
    )

    fig.update_layout(
        barmode="group",
        xaxis_title="Volume",
        yaxis_title="Fonctions",
        title_x=0.5,
        title="Distribution des fonctions",
        showlegend=True,
        yaxis=dict(type="category", dtick=1, autorange="reversed"),
    )

    fig.update_traces(orientation="h")

    return fig


# Plotly bar chart for catégorie socio-professionnelle homme femme
def plot_cat_socio_pro_bar(df: pl.DataFrame, genre: str):

    title_chart = ""
    if genre == "M":
        title_chart = "Catégorie socio-professionnelle homme"
    else:
        title_chart = "Catégorie socio-professionnelle femme"

    df_pandas = df.to_pandas()
    fig = px.bar(
        df_pandas,
        x="Volume",
        y="Libellé de la catégorie socio-professionnelle",
        title=title_chart,
        labels={
            "Libellé de la catégorie socio-professionnelle": "Libellé",
            "Volume": "Volume",
        },
        height=600,
    )

    fig.update_layout(
        xaxis_title="Volume",
        yaxis_title="Catégorie socio pro",
        title_x=0.5,
        showlegend=True,
        yaxis=dict(type="category", tickmode="array", dtick=1, autorange="reversed"),
    )

    fig.update_traces(orientation="h")
    if genre == "F":
        fig.update_traces(marker_color=COLOR_F)

    return fig

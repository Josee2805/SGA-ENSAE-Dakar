"""pages/analytics.py — Analytics avancés SGA ENSAE Dakar"""
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from models.database import get_db, Student, Course, Grade, Session
from utils.layout import page_header, C

BLU = C["bleu"]; SKY = C["bleu_clair"]; OR = C["or"]; GRN = C["success"]
COLORS = [BLU, OR, SKY, GRN, "#7B1FA2", "#C62828", "#00838F"]

CHART = dict(
    template="plotly_white",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=24, b=0),
    font=dict(family="Inter, sans-serif", color=C["texte"]),
    xaxis=dict(gridcolor="#E3F2FD"),
    yaxis=dict(gridcolor="#E3F2FD"),
)


def layout():
    db = get_db()
    courses = db.query(Course).all(); db.close()
    opts = [{"label":f"{c.code} — {c.libelle[:30]}","value":c.code} for c in courses]
    return html.Div([
        page_header("Analytics", "Analyses statistiques avancées des performances académiques"),

        # Ligne 1
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px","marginBottom":"20px"}, children=[
            html.Div(className="sga-card fade-in fade-in-1", children=[
                html.Div("Distribution des notes", className="sga-card-title"),
                dcc.Dropdown(id="ana-sel", options=[{"label":"Tous les cours","value":"all"}]+opts,
                             value="all", clearable=False, style={"marginBottom":"14px"}),
                dcc.Graph(id="ana-hist", config={"displayModeBar":False}),
            ]),
            html.Div(className="sga-card fade-in fade-in-2", children=[
                html.Div("Classement des étudiants par moyenne", className="sga-card-title"),
                dcc.Graph(id="ana-rank", config={"displayModeBar":False}),
            ]),
        ]),

        # Ligne 2
        html.Div(style={"display":"grid","gridTemplateColumns":"2fr 1fr","gap":"20px","marginBottom":"20px"}, children=[
            html.Div(className="sga-card fade-in fade-in-3", children=[
                html.Div("Boîte à moustaches — notes par matière", className="sga-card-title"),
                dcc.Graph(id="ana-box", config={"displayModeBar":False}),
            ]),
            html.Div(className="sga-card fade-in fade-in-4", children=[
                html.Div("Répartition par mention", className="sga-card-title"),
                dcc.Graph(id="ana-mention", config={"displayModeBar":False}),
            ]),
        ]),

        # Ligne 3
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"}, children=[
            html.Div(className="sga-card fade-in fade-in-5", children=[
                html.Div("Moyenne par filière", className="sga-card-title"),
                dcc.Graph(id="ana-filiere", config={"displayModeBar":False}),
            ]),
            html.Div(className="sga-card fade-in fade-in-6", children=[
                html.Div("Indicateurs globaux", className="sga-card-title"),
                html.Div(id="ana-kpi"),
            ]),
        ]),

        dcc.Interval(id="ana-interval", interval=30000, n_intervals=0),
    ])


@callback(Output("ana-hist","figure"),
          Input("ana-sel","value"), Input("ana-interval","n_intervals"))
def hist(code, _):
    db = get_db()
    q = db.query(Grade)
    if code and code != "all": q = q.filter(Grade.course_code==code)
    grades = q.all(); db.close()
    if not grades: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame([{"note":g.note} for g in grades])
    fig = px.histogram(df, x="note", nbins=12, color_discrete_sequence=[BLU],
                       labels={"note":"Note /20","count":"Étudiants"})
    fig.add_vline(x=df["note"].mean(), line_color=OR, line_dash="dash",
                  annotation_text=f"Moy: {df['note'].mean():.1f}", annotation_font_color=OR)
    fig.update_traces(marker_line_color="white", marker_line_width=1)
    fig.update_layout(**CHART)
    return fig


@callback(Output("ana-rank","figure"), Input("ana-interval","n_intervals"))
def rank(_):
    db = get_db()
    grades = db.query(Grade).all(); db.close()
    if not grades: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame([{"id":g.id_student,
                        "nom":f"{g.student.nom} {g.student.prenom[:1]}." if g.student else str(g.id_student),
                        "note":g.note,"coef":g.coefficient} for g in grades])
    moy = df.groupby(["id","nom"]).apply(lambda x:(x["note"]*x["coef"]).sum()/x["coef"].sum()).reset_index(name="moy")
    moy = moy.sort_values("moy", ascending=True).tail(12)
    bar_colors = [GRN if v>=14 else BLU if v>=10 else C["danger"] for v in moy["moy"]]
    fig = go.Figure(go.Bar(x=moy["moy"], y=moy["nom"], orientation="h",
                           marker_color=bar_colors,
                           text=[f"{v:.1f}" for v in moy["moy"]], textposition="outside"))
    fig.update_layout(**CHART, xaxis_range=[0,20])
    return fig


@callback(Output("ana-box","figure"), Input("ana-interval","n_intervals"))
def box(_):
    db = get_db()
    grades = db.query(Grade).all(); db.close()
    if not grades: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame([{"note":g.note,"cours":g.course_code} for g in grades])
    fig = px.box(df, x="cours", y="note", color="cours",
                 color_discrete_sequence=COLORS,
                 labels={"note":"Note /20","cours":"Matière"})
    fig.update_layout(**CHART, showlegend=False)
    fig.add_hline(y=10, line_dash="dash", line_color=OR, annotation_text="Seuil 10/20")
    return fig


@callback(Output("ana-mention","figure"), Input("ana-interval","n_intervals"))
def mention_pie(_):
    db = get_db()
    grades = db.query(Grade).all(); db.close()
    if not grades: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame([{"id":g.id_student,"note":g.note,"coef":g.coefficient} for g in grades])
    moy = df.groupby("id").apply(lambda x:(x["note"]*x["coef"]).sum()/x["coef"].sum())
    labels = ["Très Bien (≥16)","Bien (≥14)","Assez Bien (≥12)","Passable (≥10)","Insuf. (<10)"]
    vals = [
        (moy>=16).sum(), ((moy>=14)&(moy<16)).sum(),
        ((moy>=12)&(moy<14)).sum(), ((moy>=10)&(moy<12)).sum(), (moy<10).sum()
    ]
    colors = [GRN, BLU, SKY, OR, C["danger"]]
    fig = px.pie(values=vals, names=labels, color_discrete_sequence=colors, hole=0.4)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Inter, sans-serif"),
                      margin=dict(l=0, r=0, t=10, b=0),
                      legend=dict(font=dict(size=10)))
    return fig


@callback(Output("ana-filiere","figure"), Input("ana-interval","n_intervals"))
def par_filiere(_):
    db = get_db()
    grades = db.query(Grade).all(); db.close()
    if not grades: return go.Figure().update_layout(**CHART)
    rows = []
    for g in grades:
        if g.student:
            rows.append({"filiere":g.student.filiere or "?","note":g.note,"coef":g.coefficient})
    if not rows: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame(rows)
    moy = df.groupby("filiere").apply(lambda x:(x["note"]*x["coef"]).sum()/x["coef"].sum()).reset_index(name="moyenne")
    fig = px.bar(moy, x="filiere", y="moyenne", color="filiere",
                 color_discrete_sequence=COLORS,
                 labels={"filiere":"Filière","moyenne":"Moyenne /20"},
                 text=[f"{v:.1f}" for v in moy["moyenne"]])
    fig.update_traces(textposition="outside")
    fig.update_layout(**CHART, showlegend=False, yaxis_range=[0,20])
    fig.add_hline(y=10, line_dash="dash", line_color=OR)
    return fig


@callback(Output("ana-kpi","children"), Input("ana-interval","n_intervals"))
def kpi(_):
    db = get_db()
    grades   = db.query(Grade).all()
    students = db.query(Student).all()
    db.close()
    if not grades:
        return html.Div("Aucune donnée.", style={"color":C["muted"],"padding":"16px"})
    df  = pd.DataFrame([{"id":g.id_student,"note":g.note,"coef":g.coefficient} for g in grades])
    moy = df.groupby("id").apply(lambda x:(x["note"]*x["coef"]).sum()/x["coef"].sum())
    items = [
        ("Moyenne générale",    f"{moy.mean():.2f}/20", BLU),
        ("Médiane",             f"{moy.median():.2f}/20", SKY),
        ("Meilleur étudiant",   f"{moy.max():.2f}/20",  GRN),
        ("Étudiant en difficulté", f"{moy.min():.2f}/20", C["danger"]),
        ("Taux de réussite (≥10)", f"{(moy>=10).mean()*100:.0f}%", GRN),
        ("Nb étudiants évalués", str(len(moy)), BLU),
    ]
    return html.Div([
        html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                        "padding":"8px 0","borderBottom":f"1px solid {C['bordure']}"}, children=[
            html.Span(k, style={"fontSize":"12px","color":C["muted"],"fontWeight":"600"}),
            html.Span(v, style={"fontSize":"14px","fontWeight":"800","color":c}),
        ]) for k,v,c in items
    ])

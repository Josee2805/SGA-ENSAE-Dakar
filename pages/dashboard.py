"""pages/dashboard.py — Tableau de bord SGA ENSAE Dakar"""
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from models.database import get_db, Student, Course, Session, Grade
from utils.layout import page_header, stat_mini, C

BLU = C["bleu"]; SKY = C["bleu_clair"]; OR = C["or"]; GRN = C["success"]
COLORS = [BLU, OR, SKY, GRN, "#7B1FA2", "#C62828"]

CHART = dict(
    template="plotly_white",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=24, b=0),
    font=dict(family="Inter, sans-serif", color=C["texte"]),
    xaxis=dict(gridcolor="#E3F2FD", linecolor=C["bordure"]),
    yaxis=dict(gridcolor="#E3F2FD", linecolor=C["bordure"]),
)


def layout():
    return html.Div([
        page_header("Tableau de bord", "Vue d'ensemble des indicateurs académiques"),
        html.Div(id="dash-stats", style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)",
                                          "gap":"16px","marginBottom":"24px"}),
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px","marginBottom":"20px"}, children=[
            html.Div(className="sga-card fade-in fade-in-1", children=[
                html.Div("Distribution des moyennes", className="sga-card-title"),
                dcc.Graph(id="dash-hist", config={"displayModeBar":False}),
            ]),
            html.Div(className="sga-card fade-in fade-in-2", children=[
                html.Div("Progression horaire par matière", className="sga-card-title"),
                dcc.Graph(id="dash-heures", config={"displayModeBar":False}),
            ]),
        ]),
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px","marginBottom":"20px"}, children=[
            html.Div(className="sga-card fade-in fade-in-3", children=[
                html.Div("Absences par cours", className="sga-card-title"),
                dcc.Graph(id="dash-abs", config={"displayModeBar":False}),
            ]),
            html.Div(className="sga-card fade-in fade-in-4", children=[
                html.Div("Répartition par filière", className="sga-card-title"),
                dcc.Graph(id="dash-filieres", config={"displayModeBar":False}),
            ]),
        ]),
        html.Div(className="sga-card fade-in fade-in-5", children=[
            html.Div("Dernières séances enregistrées", className="sga-card-title"),
            html.Div(id="dash-recent"),
        ]),
        dcc.Interval(id="dash-interval", interval=30000, n_intervals=0),
    ])


@callback(Output("dash-stats","children"), Input("dash-interval","n_intervals"))
def stats(_):
    db = get_db()
    nb_s = db.query(Student).count(); nb_c = db.query(Course).count()
    nb_sess = db.query(Session).count(); nb_g = db.query(Grade).count()
    db.close()
    return [
        stat_mini(nb_s,    "Étudiants inscrits",  "👥", "", BLU),
        stat_mini(nb_c,    "Cours actifs",         "📚", "", OR),
        stat_mini(nb_sess, "Séances effectuées",   "📅", "", SKY),
        stat_mini(nb_g,    "Notes enregistrées",   "📝", "", GRN),
    ]


@callback(Output("dash-hist","figure"), Input("dash-interval","n_intervals"))
def hist_moy(_):
    db = get_db()
    grades = db.query(Grade).all(); db.close()
    if not grades: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame([{"id_student":g.id_student,"note":g.note,"coef":g.coefficient} for g in grades])
    moy = df.groupby("id_student").apply(lambda x: (x["note"]*x["coef"]).sum()/x["coef"].sum()).reset_index(name="moyenne")
    fig = px.histogram(moy, x="moyenne", nbins=10, color_discrete_sequence=[BLU],
                       labels={"moyenne":"Moyenne /20","count":"Étudiants"})
    fig.update_traces(marker_line_color=OR, marker_line_width=1.5)
    fig.update_layout(**CHART)
    return fig


@callback(Output("dash-heures","figure"), Input("dash-interval","n_intervals"))
def heures(_):
    db = get_db()
    courses = db.query(Course).all()
    data = [{"code":c.code[:8],"faites":sum(s.duree for s in c.sessions),"prevues":c.volume_total} for c in courses]
    db.close()
    if not data: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Prévues",    x=df["code"], y=df["prevues"],
                         marker_color=C["bleu_pale"], marker_line_color=C["bordure"], marker_line_width=1))
    fig.add_trace(go.Bar(name="Effectuées", x=df["code"], y=df["faites"],
                         marker_color=BLU, opacity=0.85))
    fig.update_layout(**CHART, barmode="overlay",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return fig


@callback(Output("dash-abs","figure"), Input("dash-interval","n_intervals"))
def abs_chart(_):
    db = get_db()
    sessions = db.query(Session).all(); db.close()
    data = {}
    for s in sessions: data[s.course_code] = data.get(s.course_code, 0) + len(s.attendances)
    if not data: return go.Figure().update_layout(**CHART)
    df = pd.DataFrame(list(data.items()), columns=["cours","absences"])
    bar_colors = [C["danger"] if v > 5 else OR if v > 2 else BLU for v in df["absences"]]
    fig = go.Figure(go.Bar(x=df["cours"], y=df["absences"], marker_color=bar_colors,
                           text=df["absences"], textposition="outside"))
    fig.update_layout(**CHART)
    return fig


@callback(Output("dash-filieres","figure"), Input("dash-interval","n_intervals"))
def filieres(_):
    db = get_db()
    students = db.query(Student).all(); db.close()
    data = {}
    for s in students:
        f = s.filiere or "Non renseignée"
        data[f] = data.get(f, 0) + 1
    if not data: return go.Figure().update_layout(**CHART)
    fig = px.pie(values=list(data.values()), names=list(data.keys()),
                 color_discrete_sequence=COLORS, hole=0.45)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Inter, sans-serif"),
                      margin=dict(l=0, r=0, t=24, b=0),
                      legend=dict(orientation="h"))
    return fig


@callback(Output("dash-recent","children"), Input("dash-interval","n_intervals"))
def recent(_):
    db = get_db()
    sessions = db.query(Session).order_by(Session.date.desc()).limit(8).all()
    db.close()
    if not sessions:
        return html.Div("Aucune séance.", style={"color":C["muted"],"padding":"16px"})
    rows = []
    for s in sessions:
        nb = len(s.attendances)
        rows.append(html.Tr([
            html.Td(str(s.date), style={"color":C["muted"],"fontSize":"13px"}),
            html.Td(s.course_code, style={"fontWeight":"700","color":BLU}),
            html.Td(s.theme or "—"),
            html.Td(f"{s.duree}h"),
            html.Td(s.salle or "—", style={"color":C["muted"]}),
            html.Td(html.Span(f"{nb} abs.", className="badge-danger" if nb else "badge-success")),
        ]))
    return html.Table(className="sga-table", children=[
        html.Thead(html.Tr([html.Th("Date"),html.Th("Cours"),html.Th("Thème"),
                             html.Th("Durée"),html.Th("Salle"),html.Th("Absences")])),
        html.Tbody(rows),
    ])

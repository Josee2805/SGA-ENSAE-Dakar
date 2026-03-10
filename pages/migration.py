"""
pages/migration.py
Module 0 : Interface graphique pour la migration Excel -> SQL
et informations sur la base de donnees.
"""

import base64, io, os
from dash import html, dcc, callback, Input, Output, State, no_update
from models.database import get_db, Student, Course, Session, Grade, DB_PATH
from utils.layout import page_header, C


def layout():
    db = get_db()
    nb_s = db.query(Student).count()
    nb_c = db.query(Course).count()
    nb_sess = db.query(Session).count()
    nb_g = db.query(Grade).count()
    db.close()

    db_exists   = os.path.exists(DB_PATH)
    db_size_kb  = round(os.path.getsize(DB_PATH) / 1024, 1) if db_exists else 0

    return html.Div([
        page_header("Module 0 — Migration & Base de Donnees",
                    "Initialisation SQL, import Excel, etat de la base"),

        # ── Etat de la base ──────────────────────────────────────────────────
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px", "marginBottom": "24px"}, children=[

            html.Div(className="sga-card", style={"borderTop": f"4px solid {C['or']}"}, children=[
                html.Div("Etat de la base SQLite", className="sga-card-title"),

                html.Div(style={"display": "flex", "flexDirection": "column", "gap": "12px"}, children=[
                    _info_row("Fichier", os.path.basename(DB_PATH),   "🗄️"),
                    _info_row("Emplacement", DB_PATH,                  "📁",  small=True),
                    _info_row("Taille",    f"{db_size_kb} Ko",         "💾"),
                    _info_row("Statut",    "Active" if db_exists else "Manquante",
                              "✅" if db_exists else "❌"),
                ]),

                html.Div(style={
                    "marginTop": "16px", "background": C["creme2"],
                    "borderRadius": "10px", "padding": "14px 16px",
                    "border": f"1px solid {C['bordure']}",
                    "fontSize": "12px", "color": C["muted"], "lineHeight": "1.8",
                }, children=[
                    html.Strong("Ou trouver le fichier SQLite ?", style={"color": C["bleu3"], "display": "block", "marginBottom": "6px"}),
                    html.Div("Le fichier sga_ensae.db se trouve dans le sous-dossier"),
                    html.Code("SGA2/data/sga_ensae.db",
                              style={"background": C["bleu_pale"], "padding": "2px 8px",
                                     "borderRadius": "4px", "color": C["bleu3"],
                                     "fontWeight": "700", "fontSize": "12px"}),
                    html.Div("de votre projet. Il est cree automatiquement au 1er lancement."),
                    html.Div("Vous pouvez l'ouvrir avec : DB Browser for SQLite (gratuit)."),
                ]),
            ]),

            html.Div(className="sga-card", style={"borderTop": f"3px solid {C['or']}"}, children=[
                html.Div("Contenu actuel de la base", className="sga-card-title"),
                html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"}, children=[
                    _stat_bloc(nb_s,    "Etudiants",  C["bleu"]),
                    _stat_bloc(nb_c,    "Cours",      C["or"]),
                    _stat_bloc(nb_sess, "Seances",    C["bleu_clair"]),
                    _stat_bloc(nb_g,    "Notes",      C["success"]),
                ]),
                html.Div(style={"marginTop": "14px"}, children=[
                    html.Button("Rafraichir les stats", id="mig-refresh-btn",
                                className="btn-ghost", style={"fontSize": "13px"}),
                    html.Div(id="mig-refresh-fb"),
                ]),
            ]),
        ]),

        # ── Migration Excel ──────────────────────────────────────────────────
        html.Div(className="sga-card", children=[
            html.Div("Migration depuis Excel", className="sga-card-title"),

            html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px"}, children=[

                html.Div([
                    html.Div("Structure attendue du fichier Excel", style={
                        "fontWeight": "700", "marginBottom": "12px",
                        "fontFamily": "'EB Garamond', serif",
                        "color": C["bleu3"], "fontSize": "16px",
                    }),

                    _sheet_desc("Students",
                        "id (optionnel), nom*, prenom*, email*, date_naissance, filiere, annee"),
                    _sheet_desc("Courses",
                        "code*, libelle*, volume_total, enseignant, description"),
                    _sheet_desc("Sessions",
                        "course_code*, date*, duree, theme, salle"),
                    _sheet_desc("Grades",
                        "id_student*, course_code*, note*, coefficient, type_eval"),

                    html.Div(style={
                        "marginTop": "14px", "background": "#FFF3E0",
                        "borderRadius": "8px", "padding": "12px 14px",
                        "border": "1px solid #FFE0B2", "fontSize": "12px",
                        "color": "#E65100",
                    }, children=[
                        html.Strong("Note : "),
                        "Les colonnes marquees * sont obligatoires. "
                        "Les feuilles absentes sont ignorees. "
                        "Les doublons (meme email / meme code) sont ignores.",
                    ]),
                ]),

                html.Div([
                    html.Div("Importer votre fichier Excel", style={
                        "fontWeight": "700", "marginBottom": "12px",
                        "fontFamily": "'EB Garamond', serif",
                        "color": C["bleu3"], "fontSize": "16px",
                    }),
                    dcc.Upload(
                        id="mig-upload",
                        children=html.Div([
                            html.Span("📊", style={"fontSize": "40px"}),
                            html.Div("Glissez-deposez votre fichier Excel ici",
                                     style={"fontSize": "14px", "color": C["muted"],
                                            "marginTop": "10px", "fontWeight": "700"}),
                            html.Div(".xlsx — feuilles Students / Courses / Sessions / Grades",
                                     style={"fontSize": "12px", "color": C["muted"],
                                            "marginTop": "4px"}),
                        ]),
                        className="upload-zone",
                        accept=".xlsx",
                        style={"padding": "36px 24px", "marginBottom": "14px"},
                    ),
                    html.Div(id="mig-result"),
                ]),
            ]),
        ]),

        # ── Template a telecharger ───────────────────────────────────────────
        html.Div(className="sga-card", children=[
            html.Div("Telecharger un template Excel vierge", className="sga-card-title"),
            html.Div("Utilisez ce fichier comme base pour preparer vos donnees existantes.",
                     style={"fontSize": "14px", "color": C["muted"], "marginBottom": "16px"}),
            html.Button("Telecharger le template Excel", id="mig-dl-btn",
                        className="btn-or", style={"fontSize": "14px"}),
            html.Div(id="mig-dl-fb"),
            dcc.Download(id="mig-dl"),
        ]),
    ])


# ── Helpers visuels ──────────────────────────────────────────────────────────
def _info_row(label, value, icon, small=False):
    return html.Div(style={"display": "flex", "alignItems": "flex-start", "gap": "10px"}, children=[
        html.Span(icon, style={"fontSize": "18px", "flexShrink": "0"}),
        html.Div([
            html.Div(label, style={"fontSize": "11px", "color": C["muted"], "fontWeight": "700",
                                    "textTransform": "uppercase", "letterSpacing": "0.8px"}),
            html.Div(value, style={"fontSize": "11px" if small else "14px",
                                    "fontWeight": "600", "color": C["texte"],
                                    "wordBreak": "break-all"}),
        ]),
    ])


def _stat_bloc(value, label, color):
    return html.Div(style={
        "textAlign": "center", "padding": "16px 10px",
        "background": C["creme2"], "borderRadius": "10px",
        "borderLeft": f"4px solid {color}",
    }, children=[
        html.Div(str(value), style={"fontSize": "32px", "fontWeight": "800", "color": color,
                                     "fontFamily": "'Playfair Display', serif"}),
        html.Div(label, style={"fontSize": "12px", "color": C["muted"], "fontWeight": "700",
                                "textTransform": "uppercase", "letterSpacing": "1px"}),
    ])


def _sheet_desc(sheet, cols):
    return html.Div(style={
        "marginBottom": "10px", "padding": "12px 14px",
        "background": C["creme"], "borderRadius": "8px",
        "border": f"1px solid {C['bordure']}", "borderLeft": f"3px solid {C['or']}",
    }, children=[
        html.Div(f"Feuille : {sheet}", style={"fontWeight": "700", "color": C["bleu3"],
                                               "fontSize": "13px", "marginBottom": "4px"}),
        html.Div(cols, style={"fontSize": "12px", "color": C["muted"], "fontFamily": "monospace"}),
    ])


# ── Callbacks ────────────────────────────────────────────────────────────────
@callback(
    Output("mig-result", "children"),
    Input("mig-upload",  "contents"),
    State("mig-upload",  "filename"),
    prevent_initial_call=True,
)
def run_migration(contents, filename):
    if not contents:
        return no_update
    try:
        _, b64 = contents.split(",")
        buf    = io.BytesIO(base64.b64decode(b64))

        from utils.migration import migrate_from_excel
        log = migrate_from_excel(buf)

        if "erreur" in log:
            return html.Div(f"Erreur migration : {log['erreur']}", className="alert-sga",
                            style={"background": "#FFEBEE", "color": C["danger"],
                                   "borderLeftColor": C["danger"]})

        nb_warn     = log.pop("avertissements", 0)
        warn_detail = log.pop("_warnings", [])
        lignes = []
        for sheet, cnt in log.items():
            lignes.append(html.Li(
                f"{sheet} : {cnt} enregistrement(s) traite(s)",
                style={"marginBottom": "4px", "fontWeight": "700" if cnt > 0 else "normal"}
            ))

        warn_section = []
        if nb_warn:
            warn_section = [
                html.Div(
                    f"{nb_warn} avertissement(s) — lignes ignorees :",
                    style={"marginTop":"14px","fontWeight":"700","fontSize":"13px","color":C["warning"]}
                ),
                html.Ul(
                    [html.Li(w, style={"fontSize":"12px","color":C["muted"],"marginBottom":"2px"})
                     for w in warn_detail],
                    style={"paddingLeft":"20px","marginTop":"4px"}
                ),
                html.Div(
                    "Conseil : verifiez que les noms de feuilles (Students, Courses, Sessions, Grades) "
                    "et les colonnes (email, code, note...) correspondent au template.",
                    style={"fontSize":"12px","color":C["muted"],"marginTop":"8px","fontStyle":"italic"}
                ),
            ]

        return html.Div([
            html.Div(f"Migration de {filename} terminee !", className="alert-sga",
                     style={"background": "#E8F5E9", "color": C["success"],
                            "borderLeftColor": C["success"]}),
            html.Ul(lignes, style={"marginTop": "10px", "fontSize": "14px",
                                    "color": C["texte2"], "paddingLeft": "20px"}),
            *warn_section,
        ])
    except Exception as e:
        return html.Div(f"Erreur inattendue : {str(e)}", className="alert-sga",
                        style={"background": "#FFEBEE", "color": C["danger"],
                               "borderLeftColor": C["danger"]})


@callback(
    Output("mig-dl",    "data"),
    Output("mig-dl-fb", "children"),
    Input("mig-dl-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_template(n):
    if not n:
        return no_update, no_update
    import pandas as pd

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        pd.DataFrame(columns=["nom", "prenom", "email", "date_naissance", "filiere", "annee"]
                     ).to_excel(writer, index=False, sheet_name="Students")
        pd.DataFrame(columns=["code", "libelle", "volume_total", "enseignant", "description"]
                     ).to_excel(writer, index=False, sheet_name="Courses")
        pd.DataFrame(columns=["course_code", "date", "duree", "theme", "salle"]
                     ).to_excel(writer, index=False, sheet_name="Sessions")
        pd.DataFrame(columns=["id_student", "course_code", "note", "coefficient", "type_eval"]
                     ).to_excel(writer, index=False, sheet_name="Grades")
    buf.seek(0)
    return (
        dcc.send_bytes(buf.read(), filename="template_migration_SGA.xlsx"),
        html.Div("Template telecharge.", className="alert-sga",
                 style={"background": "#E8F5E9", "color": C["success"],
                        "borderLeftColor": C["success"]}),
    )


@callback(
    Output("mig-refresh-fb", "children"),
    Input("mig-refresh-btn", "n_clicks"),
    prevent_initial_call=True,
)
def refresh_stats(n):
    # Force un rechargement de la page via message
    return html.Div("Rechargez la page (F5) pour voir les statistiques mises a jour.",
                    style={"fontSize": "12px", "color": C["muted"], "marginTop": "8px"})

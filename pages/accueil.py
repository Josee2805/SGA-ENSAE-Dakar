"""pages/accueil.py — Page d'accueil SGA ENSAE Dakar avec ticker, animations et hero."""
from dash import html, dcc
from models.database import get_db, Student, Course, Session, Grade
from utils.layout import C


def _stats():
    db = get_db()
    r = (db.query(Student).count(), db.query(Course).count(),
         db.query(Session).count(), db.query(Grade).count())
    db.close(); return r


def layout():
    nb_s, nb_c, nb_sess, nb_g = _stats()

    # Ticker items
    ticker_items = [
        f"Bienvenue sur le SGA de l'ENSAE Dakar",
        f"{nb_s} étudiants inscrits",
        f"{nb_c} cours actifs",
        f"{nb_sess} séances enregistrées",
        f"{nb_g} notes saisies",
        "Gérez vos cours, séances et évaluations",
        "Bulletins individuels PDF disponibles",
        "Exports Excel, CSV, Stata et R",
        "Projet Data Visualisation 2025-2026",
        "Gilbert OUMSAORE & Josée JEAZE — ENSAE Dakar",
    ]
    sep = html.Span(" ✦ ", className="ticker-sep")
    ticker_content = []
    for item in ticker_items:
        ticker_content.append(html.Span(item, className="ticker-item"))
        ticker_content.append(sep)
    # Double pour boucle continue
    ticker_inner = ticker_content * 2

    modules = [
        {"href":"/dashboard", "icon":"📊","title":"Tableau de bord",
         "desc":"Indicateurs clés, graphiques de performance et suivi global.",
         "color":C["bleu"]},
        {"href":"/cours",     "icon":"📚","title":"Gestion des cours",
         "desc":"Créer, modifier et suivre les matières et volumes horaires.",
         "color":C["bleu2"]},
        {"href":"/seances",   "icon":"📅","title":"Séances",
         "desc":"Enregistrer les cours effectués et les absences par séance.",
         "color":C["bleu_clair"]},
        {"href":"/etudiants", "icon":"👥","title":"Étudiants",
         "desc":"Inscrire et consulter les dossiers individuels avec fiche PDF.",
         "color":C["or"]},
        {"href":"/notes",     "icon":"📝","title":"Notes & Évaluations",
         "desc":"Saisie, imports Excel, bulletins individuels PDF, exports.",
         "color":C["success"]},
        {"href":"/analytics", "icon":"📈","title":"Analytics",
         "desc":"Distributions, classements, boîtes à moustaches, analyses.",
         "color":"#7B1FA2"},
    ]

    return html.Div([
        # ── HERO ─────────────────────────────────────────────────────────
        html.Div(style={
            "background":"linear-gradient(135deg,#0D47A1 0%,#1565C0 55%,#1976D2 100%)",
            "padding":"56px 32px 48px","position":"relative","overflow":"hidden",
        }, children=[
            html.Div(style={"position":"absolute","top":"-80px","right":"-80px",
                            "width":"380px","height":"380px","borderRadius":"50%",
                            "background":"rgba(255,255,255,0.03)"}),
            html.Div(style={"position":"absolute","bottom":"-70px","left":"8%",
                            "width":"280px","height":"280px","borderRadius":"50%",
                            "background":"rgba(249,168,37,0.05)"}),

            html.Div(style={"maxWidth":"1200px","margin":"0 auto","position":"relative","zIndex":"1"}, children=[

                # Logo + nom école centré
                html.Div(style={"textAlign":"center","marginBottom":"28px"}, children=[
                    html.Div("E", style={
                        "width":"70px","height":"70px","borderRadius":"50%",
                        "background":"rgba(249,168,37,0.15)","border":"2px solid #F9A825",
                        "display":"flex","alignItems":"center","justifyContent":"center",
                        "fontFamily":"'Merriweather',serif","fontSize":"30px","fontWeight":"900","color":"#F9A825",
                        "margin":"0 auto 14px",
                    }),
                    html.Div("ENSAE DAKAR", style={
                        "fontSize":"13px","fontWeight":"800","color":"#F9A825",
                        "letterSpacing":"4px","textTransform":"uppercase","marginBottom":"4px",
                    }),
                    html.Div("École Nationale de la Statistique et de l'Analyse Économique",
                             style={"fontSize":"13px","color":"rgba(255,255,255,0.72)","marginBottom":"20px"}),
                    html.H1("Système de Gestion Académique", style={
                        "fontFamily":"'Merriweather',serif","fontSize":"36px","fontWeight":"900",
                        "color":"#FFFFFF","marginBottom":"10px","lineHeight":"1.2",
                    }),
                    html.P("Plateforme centralisée de suivi pédagogique — gestion des cours, séances, étudiants, évaluations et statistiques.",
                           style={"fontSize":"15px","color":"rgba(255,255,255,0.78)",
                                  "maxWidth":"620px","lineHeight":"1.75","margin":"0 auto 28px"}),

                    html.Div(style={"display":"flex","gap":"12px","justifyContent":"center","flexWrap":"wrap"}, children=[
                        dcc.Link("Accéder au tableau de bord →", href="/dashboard",
                                 className="btn-or", style={"fontSize":"14px","padding":"12px 26px"}),
                        dcc.Link("Gérer les étudiants", href="/etudiants",
                                 style={"background":"rgba(255,255,255,0.1)","color":"#FFFFFF",
                                        "border":"1px solid rgba(255,255,255,0.28)","borderRadius":"9px",
                                        "padding":"12px 26px","textDecoration":"none",
                                        "fontWeight":"700","fontSize":"14px","display":"inline-block"}),
                    ]),
                ]),

                # Ticker défilant
                html.Div(className="ticker-wrap", children=[
                    html.Div(className="ticker-inner", children=ticker_inner),
                ]),

                # Stats 4 colonnes
                html.Div(style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)",
                                "gap":"14px","marginTop":"32px"}, children=[
                    html.Div(style={
                        "background":"rgba(255,255,255,0.09)","borderRadius":"13px","padding":"18px",
                        "border":"1px solid rgba(255,255,255,0.13)","textAlign":"center",
                    }, children=[
                        html.Div(icon, style={"fontSize":"26px","marginBottom":"6px"}),
                        html.Div(str(val), style={"fontFamily":"'Merriweather',serif","fontSize":"28px",
                                                    "fontWeight":"900","color":"#FFFFFF"}),
                        html.Div(lbl, style={"fontSize":"11px","color":"rgba(255,255,255,0.65)","marginTop":"2px"}),
                    ])
                    for icon, val, lbl in [
                        ("👥", nb_s,    "Étudiants"),
                        ("📚", nb_c,    "Cours"),
                        ("📅", nb_sess, "Séances"),
                        ("📝", nb_g,    "Notes"),
                    ]
                ]),
            ]),
        ]),

        # ── Modules ──────────────────────────────────────────────────────
        html.Div(style={"maxWidth":"1200px","margin":"0 auto","padding":"44px 24px 20px"}, children=[
            html.Div(style={"textAlign":"center","marginBottom":"32px"}, children=[
                html.Div("Modules de l'application", style={
                    "fontFamily":"'Merriweather',serif","fontSize":"26px","fontWeight":"900",
                    "color":C["bleu3"],"marginBottom":"8px",
                }, className="fade-in fade-in-1"),
                html.Div("Accédez rapidement à tous les outils de gestion académique",
                         style={"fontSize":"14px","color":C["muted"]}, className="fade-in fade-in-2"),
            ]),
            html.Div(style={"display":"grid","gridTemplateColumns":"repeat(3,1fr)","gap":"18px"}, children=[
                dcc.Link(href=m["href"], style={"textDecoration":"none"}, children=[
                    html.Div(className=f"sga-card fade-in fade-in-{i+1}", style={
                        "cursor":"pointer","transition":"all 0.25s","marginBottom":"0",
                        "borderTop":f"3px solid {m['color']}",
                    }, children=[
                        html.Div(style={"display":"flex","alignItems":"center","gap":"12px","marginBottom":"12px"}, children=[
                            html.Div(m["icon"], style={
                                "width":"48px","height":"48px","borderRadius":"12px",
                                "background":f"{'rgba(21,101,192,0.1)' if m['color']==C['bleu'] else 'rgba(249,168,37,0.1)' if m['color']==C['or'] else 'rgba(66,165,245,0.1)'}",
                                "display":"flex","alignItems":"center","justifyContent":"center","fontSize":"22px","flexShrink":"0",
                            }),
                            html.Div(m["title"], style={
                                "fontFamily":"'Merriweather',serif","fontSize":"15px",
                                "fontWeight":"700","color":C["bleu3"],
                            }),
                        ]),
                        html.Div(m["desc"], style={"fontSize":"13px","color":C["muted"],"lineHeight":"1.6"}),
                        html.Div("Accéder →", style={"marginTop":"12px","fontSize":"13px","fontWeight":"700","color":m["color"]}),
                    ]),
                ]) for i, m in enumerate(modules)
            ]),
        ]),

        # ── Bandeau auteurs ───────────────────────────────────────────────
        html.Div(style={
            "background":"linear-gradient(135deg,#0D47A1,#1565C0)",
            "padding":"40px 32px","marginTop":"20px",
        }, children=[
            html.Div(style={"maxWidth":"1200px","margin":"0 auto",
                            "display":"flex","justifyContent":"space-between",
                            "alignItems":"center","flexWrap":"wrap","gap":"20px"}, children=[
                html.Div([
                    html.Div("Projet académique · Data Visualisation 2025-2026", style={
                        "fontSize":"10px","color":"#F9A825","fontWeight":"700",
                        "letterSpacing":"2px","textTransform":"uppercase","marginBottom":"8px",
                    }),
                    html.Div("Gilbert OUMSAORE & Josée JEAZE", style={
                        "fontSize":"18px","fontWeight":"800","color":"#FFFFFF","marginBottom":"4px",
                    }),
                    html.Div("Élèves Analystes Statisticiens — 3ème année — ENSAE Dakar",
                             style={"fontSize":"13px","color":"rgba(255,255,255,0.7)"}),
                ]),
                dcc.Link("En savoir plus →", href="/apropos",
                         style={"background":"rgba(249,168,37,0.15)","color":"#F9A825",
                                "border":"1px solid #F9A825","borderRadius":"9px","padding":"11px 22px",
                                "textDecoration":"none","fontWeight":"700","fontSize":"13px"}),
            ]),
        ]),
    ])

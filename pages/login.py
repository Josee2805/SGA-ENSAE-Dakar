"""pages/login.py — Connexion SGA ENSAE Dakar"""
from dash import html, dcc
from utils.layout import C


def layout():
    return html.Div(className="login-page", children=[
        html.Div(className="login-card", children=[

            # Logo
            html.Div(style={"textAlign":"center","marginBottom":"24px"}, children=[
                html.Div(style={
                    "width":"80px","height":"80px","borderRadius":"50%",
                    "background":f"linear-gradient(135deg,{C['bleu3']},{C['bleu_clair']})",
                    "display":"flex","alignItems":"center","justifyContent":"center",
                    "margin":"0 auto 12px",
                    "boxShadow":f"0 6px 24px rgba(21,101,192,0.4)",
                    "border":f"3px solid {C['or']}",
                }, children=html.Div("E", style={
                    "fontFamily":"'Merriweather',serif","fontSize":"32px",
                    "fontWeight":"900","color":C["or"],
                })),
                html.Div("ENSAE DAKAR", style={
                    "fontSize":"13px","fontWeight":"800","color":C["bleu3"],
                    "letterSpacing":"3px","textTransform":"uppercase",
                }),
                html.Div("École Nationale de la Statistique et de l'Analyse Économique",
                         style={"fontSize":"11px","color":C["muted"],"marginTop":"2px"}),
            ]),

            html.H1("Bienvenue", style={
                "fontFamily":"'Merriweather',serif","fontSize":"26px","fontWeight":"900",
                "color":C["bleu3"],"textAlign":"center","marginBottom":"4px",
            }),
            html.P("Connectez-vous au Système de Gestion Académique", style={
                "fontSize":"13px","color":C["muted"],"textAlign":"center","marginBottom":"28px",
            }),

            html.Label("Identifiant", className="form-label-sga"),
            dcc.Input(id="login-user", type="text", placeholder="admin",
                      className="sga-input"),

            html.Label("Mot de passe", className="form-label-sga"),
            dcc.Input(id="login-pass", type="password", placeholder="••••••••",
                      n_submit=0, className="sga-input"),

            html.Button("Se connecter →", id="login-btn", className="btn-bleu",
                        style={"width":"100%","padding":"13px","fontSize":"15px","marginTop":"4px"}),
            html.Div(id="login-feedback"),

            # Comptes démo
            html.Div(style={
                "marginTop":"24px","background":C["bleu_pale"],"borderRadius":"10px",
                "padding":"14px 18px","border":f"1px solid {C['bleu_pale2']}",
            }, children=[
                html.Div("Comptes de démonstration", style={
                    "fontSize":"10px","fontWeight":"700","letterSpacing":"1.5px",
                    "textTransform":"uppercase","color":C["bleu"],"marginBottom":"10px",
                }),
                html.Div(style={"display":"flex","flexDirection":"column","gap":"4px"}, children=[
                    html.Div("admin / ensae2025",   style={"fontSize":"13px","fontFamily":"'Fira Code',monospace","color":C["texte2"]}),
                    html.Div("gilbert / sga2025",   style={"fontSize":"13px","fontFamily":"'Fira Code',monospace","color":C["texte2"]}),
                    html.Div("josee / sga2025",     style={"fontSize":"13px","fontFamily":"'Fira Code',monospace","color":C["texte2"]}),
                ]),
            ]),

            html.Div("Gilbert OUMSAORE & Josée JEAZE — ENSAE Dakar — 2025-2026", style={
                "fontSize":"11px","color":C["muted"],"textAlign":"center",
                "marginTop":"20px","fontStyle":"italic",
            }),
        ]),
    ])

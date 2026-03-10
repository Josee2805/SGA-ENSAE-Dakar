"""pages/apropos.py — À propos du projet SGA ENSAE Dakar"""
from dash import html, dcc
from utils.layout import C, page_header


def layout():
    return html.Div([
        page_header("À propos du projet",
                    "SGA — Système de Gestion Académique · ENSAE Dakar 2025-2026"),
        html.Div(className="sga-card", children=[
            html.Div("Le projet", className="sga-card-title"),
            html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"28px"}, children=[
                html.Div([
                    html.P("Ce Système de Gestion Académique (SGA) a été développé dans le cadre du cours de Data Visualisation dispensé à l'ENSAE Dakar.",
                           style={"color":C["texte2"],"lineHeight":"1.8","marginBottom":"12px","fontSize":"14px"}),
                    html.P("L'application centralise la gestion pédagogique : cours, séances, étudiants, évaluations et statistiques, et permet de produire des bulletins individuels PDF.",
                           style={"color":C["texte2"],"lineHeight":"1.8","fontSize":"14px"}),
                ]),
                html.Div([
                    html.Div(style={"background":C["bleu_pale"],"borderRadius":"12px","padding":"20px",
                                    "border":f"1px solid {C['bleu_pale2']}"}, children=[
                        html.Div("Spécifications techniques", style={"fontWeight":"700","color":C["bleu3"],
                                                                       "fontSize":"13px","marginBottom":"12px"}),
                        *[html.Div(style={"display":"flex","justifyContent":"space-between",
                                          "padding":"6px 0","borderBottom":f"1px solid {C['bordure']}",
                                          "fontSize":"13px"}, children=[
                            html.Span(k, style={"color":C["muted"],"fontWeight":"600"}),
                            html.Span(v, style={"color":C["bleu3"],"fontWeight":"700"}),
                        ]) for k,v in [
                            ("Framework","Dash / Plotly"),("Backend","Python 3.10+"),
                            ("Base de données","SQLite + SQLAlchemy"),
                            ("Exports","Excel, PDF, CSV, Stata, R"),
                            ("PDF","ReportLab"),("Année","2025-2026"),
                        ]],
                    ]),
                ]),
            ]),
        ]),
        html.Div(className="sga-card", children=[
            html.Div("Les auteurs", className="sga-card-title"),
            html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"}, children=[
                _auteur("Gilbert OUMSAORE","Élève Analyste Statisticien — 3ème année","ENSAE Dakar · 2025-2026",
                        "Développement backend, base de données SQLAlchemy, modules Cours & Séances, migration Excel."),
                _auteur("Josée JEAZE","Élève Analyste Statisticienne — 3ème année","ENSAE Dakar · 2025-2026",
                        "Design system, module Étudiants & Notes, bulletins PDF, analytics et visualisations."),
            ]),
        ]),
        html.Div(className="sga-card", children=[
            html.Div("Fonctionnalités", className="sga-card-title"),
            html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"14px"}, children=[
                _feat("📊","Dashboard","Indicateurs globaux, taux de complétion, graphiques de performance."),
                _feat("📚","Cours","CRUD complet, suivi du volume horaire, confirmation avant suppression."),
                _feat("📅","Séances","Enregistrement, absences, filtres par cours et par date."),
                _feat("👥","Étudiants","Inscriptions, fiches individuelles, téléchargement PDF."),
                _feat("📝","Notes","Saisie, coef auto, imports Excel robustes, bulletin individuel PDF."),
                _feat("📈","Analytics","Distributions, comparaisons par filière, top/flop étudiants."),
                _feat("🗄️","Migration","Import Excel multi-feuilles, template téléchargeable."),
                _feat("🔒","Sécurité","Authentification par session, accès protégé."),
                _feat("⚠️","Confirmations","Modal de confirmation avant toute suppression."),
            ]),
        ]),
        html.Div(style={
            "background":f"linear-gradient(135deg,{C['bleu3']},{C['bleu']})",
            "borderRadius":"16px","padding":"32px","textAlign":"center","marginBottom":"24px",
        }, children=[
            html.Div("E", style={"width":"60px","height":"60px","borderRadius":"50%",
                                  "background":"rgba(249,168,37,0.2)","border":f"2px solid {C['or']}",
                                  "display":"flex","alignItems":"center","justifyContent":"center",
                                  "fontFamily":"'Merriweather',serif","fontSize":"26px","fontWeight":"900",
                                  "color":C["or"],"margin":"0 auto 14px"}),
            html.Div("ENSAE Dakar", style={"fontFamily":"'Merriweather',serif","fontSize":"22px",
                                             "fontWeight":"900","color":"#FFFFFF","marginBottom":"4px"}),
            html.Div("École Nationale de la Statistique et de l'Analyse Économique — Dakar, Sénégal",
                     style={"fontSize":"13px","color":"rgba(255,255,255,0.75)","marginBottom":"20px"}),
            dcc.Link("← Retour à l'accueil", href="/",
                     style={"background":"rgba(249,168,37,0.15)","color":C["or"],
                            "border":f"1px solid {C['or']}","borderRadius":"8px",
                            "padding":"10px 22px","textDecoration":"none","fontWeight":"700","fontSize":"13px"}),
        ]),
    ])


def _auteur(nom, titre, ecole, desc):
    return html.Div(style={"background":C["bleu_pale"],"borderRadius":"14px","padding":"24px",
                            "border":f"1px solid {C['bleu_pale2']}"}, children=[
        html.Div(style={"display":"flex","alignItems":"center","gap":"14px","marginBottom":"12px"}, children=[
            html.Div(nom[0], style={
                "width":"50px","height":"50px","borderRadius":"50%",
                "background":f"linear-gradient(135deg,{C['bleu3']},{C['bleu_clair']})",
                "display":"flex","alignItems":"center","justifyContent":"center",
                "fontFamily":"'Merriweather',serif","fontSize":"20px","fontWeight":"900","color":"#FFFFFF",
            }),
            html.Div([
                html.Div(nom,   style={"fontWeight":"800","color":C["bleu3"],"fontSize":"15px"}),
                html.Div(titre, style={"fontSize":"12px","color":C["bleu"],"fontWeight":"600","marginTop":"1px"}),
                html.Div(ecole, style={"fontSize":"11px","color":C["muted"]}),
            ]),
        ]),
        html.P(desc, style={"fontSize":"13px","color":C["texte2"],"lineHeight":"1.6"}),
    ])


def _feat(icon, title, desc):
    return html.Div(style={"background":"#FFFFFF","borderRadius":"12px","padding":"16px",
                            "border":f"1px solid {C['bordure']}"}, children=[
        html.Div([html.Span(icon, style={"fontSize":"20px","marginRight":"8px"}),
                  html.Span(title, style={"fontWeight":"700","color":C["bleu3"],"fontSize":"13px"})],
                 style={"marginBottom":"6px"}),
        html.P(desc, style={"fontSize":"12px","color":C["muted"],"lineHeight":"1.5","margin":"0"}),
    ])

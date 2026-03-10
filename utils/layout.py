"""
utils/layout.py — Design System ENSAE Dakar
Palette bleu institutionnel, propre et cohérent
"""
from dash import html

C = {
    "bleu":       "#1565C0",
    "bleu2":      "#1976D2",
    "bleu3":      "#0D47A1",
    "bleu_clair": "#42A5F5",
    "bleu_pale":  "#E3F2FD",
    "bleu_pale2": "#BBDEFB",
    "bleu_sky":   "#90CAF9",
    "or":         "#F9A825",
    "or_clair":   "#FFF9C4",
    "or_pale":    "#FFF8E1",
    "blanc":      "#FFFFFF",
    "creme":      "#F8FBFF",
    "creme2":     "#EEF5FF",
    "texte":      "#0D1B2A",
    "texte2":     "#1A3050",
    "muted":      "#607D8B",
    "bordure":    "#CFE2F3",
    "bordure2":   "#B3D4F5",
    "success":    "#2E7D32",
    "warning":    "#E65100",
    "danger":     "#C62828",
    "info":       "#0288D1",
    "vert_clair": "#E8F5E9",
    "orange_clair":"#FFF3E0",
    "rouge_clair": "#FFEBEE",
}

EXTERNAL_CSS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Merriweather:wght@400;700;900&family=Fira+Code:wght@400;500&display=swap",
]

CUSTOM_CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:#F8FBFF;color:#0D1B2A;font-size:14px;line-height:1.6;min-height:100vh}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:#EEF5FF}
::-webkit-scrollbar-thumb{background:#90CAF9;border-radius:3px}

/* ── Animations scroll ─────────────────────────── */
.fade-in{opacity:0;transform:translateY(22px);animation:fadeUp 0.55s ease forwards}
.fade-in-1{animation-delay:0.05s} .fade-in-2{animation-delay:0.12s}
.fade-in-3{animation-delay:0.20s} .fade-in-4{animation-delay:0.28s}
.fade-in-5{animation-delay:0.36s} .fade-in-6{animation-delay:0.44s}
@keyframes fadeUp{to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideDown{from{opacity:0;transform:translateY(-12px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.7}}

/* ── Navbar ────────────────────────────────────── */
.sga-navbar{
  position:fixed;top:0;left:0;right:0;z-index:1000;
  background:linear-gradient(135deg,#0D47A1 0%,#1565C0 100%);
  height:64px;display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;
  box-shadow:0 2px 16px rgba(13,71,161,0.3);
  border-bottom:3px solid #F9A825;
}
.sga-brand{display:flex;align-items:center;gap:12px}
.sga-logo-wrap{
  width:40px;height:40px;border-radius:50%;
  background:rgba(249,168,37,0.15);border:2px solid #F9A825;
  display:flex;align-items:center;justify-content:center;
  font-family:'Merriweather',serif;font-size:17px;font-weight:900;color:#F9A825;
  flex-shrink:0;
}
.sga-brand-inner{display:flex;flex-direction:column;line-height:1.2}
.sga-brand-title{font-size:14px;font-weight:800;color:#FFFFFF;letter-spacing:0.4px}
.sga-brand-sub{font-size:10px;color:rgba(255,255,255,0.65);letter-spacing:1.5px;text-transform:uppercase}
.sga-nav-links{display:flex;align-items:center;gap:2px}
.sga-nav-link{color:rgba(255,255,255,0.80)!important;text-decoration:none!important;
  font-size:12px;font-weight:500;padding:7px 11px;border-radius:7px;transition:all 0.2s;
  white-space:nowrap}
.sga-nav-link:hover{background:rgba(255,255,255,0.12);color:#FFFFFF!important}
.sga-nav-link-active{background:rgba(249,168,37,0.18);color:#F9A825!important;font-weight:700}

/* ── Footer ────────────────────────────────────── */
.sga-footer{
  background:linear-gradient(135deg,#0D47A1 0%,#1565C0 100%);
  border-top:3px solid #F9A825;padding:40px 32px 28px;margin-top:60px;
}

/* ── Page wrapper ──────────────────────────────── */
.page-wrapper{padding-top:64px;min-height:calc(100vh - 64px)}
.page-content{max-width:1200px;margin:0 auto;padding:32px 24px 60px}

/* ── Cards ─────────────────────────────────────── */
.sga-card{
  background:#FFFFFF;border-radius:14px;padding:24px;margin-bottom:24px;
  box-shadow:0 2px 12px rgba(21,101,192,0.07);border:1px solid #CFE2F3;
}
.sga-card-title{
  font-family:'Merriweather',serif;font-size:15px;font-weight:700;
  color:#0D47A1;margin-bottom:16px;padding-bottom:12px;
  border-bottom:2px solid #E3F2FD;display:flex;align-items:center;gap:8px;
}
.sga-card-title::before{
  content:'';display:inline-block;width:4px;height:16px;
  background:linear-gradient(180deg,#42A5F5,#F9A825);
  border-radius:2px;flex-shrink:0;
}

/* ── Page header ───────────────────────────────── */
.sga-page-header{
  background:linear-gradient(135deg,#0D47A1 0%,#1565C0 55%,#1976D2 100%);
  border-radius:16px;padding:30px 34px;margin-bottom:26px;
  position:relative;overflow:hidden;
  box-shadow:0 4px 20px rgba(13,71,161,0.2);
}
.sga-page-header::after{content:'';position:absolute;top:-50px;right:-50px;
  width:220px;height:220px;background:rgba(255,255,255,0.04);border-radius:50%}
.sga-page-header::before{content:'';position:absolute;bottom:-70px;right:100px;
  width:180px;height:180px;background:rgba(249,168,37,0.06);border-radius:50%}
.sga-page-header-title{font-family:'Merriweather',serif;font-size:24px;font-weight:900;
  color:#FFFFFF;margin-bottom:6px;position:relative;z-index:1}
.sga-page-header-sub{font-size:13px;color:rgba(255,255,255,0.78);position:relative;z-index:1}

/* ── Formulaires ───────────────────────────────── */
.form-label-sga{display:block;font-size:11px;font-weight:700;color:#0D47A1;
  margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px}
.sga-input{
  width:100%;padding:9px 13px;border:1.5px solid #CFE2F3;border-radius:8px;
  font-family:'Inter',sans-serif;font-size:14px;background:#F8FBFF;
  color:#0D1B2A;outline:none;transition:border-color 0.2s,box-shadow 0.2s;
  margin-bottom:14px;display:block;
}
.sga-input:focus{border-color:#42A5F5;box-shadow:0 0 0 3px rgba(66,165,245,0.12);background:#FFFFFF}

/* ── Boutons ───────────────────────────────────── */
.btn-bleu{
  background:linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);color:#FFFFFF!important;
  border:none;border-radius:9px;padding:10px 22px;
  font-family:'Inter',sans-serif;font-size:14px;font-weight:700;cursor:pointer;
  transition:all 0.2s;box-shadow:0 2px 8px rgba(21,101,192,0.28);
  text-decoration:none;display:inline-block;
}
.btn-bleu:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(21,101,192,0.38)}
.btn-or{
  background:linear-gradient(135deg,#F9A825 0%,#FFB300 100%);color:#0D47A1!important;
  border:none;border-radius:9px;padding:10px 22px;
  font-family:'Inter',sans-serif;font-size:14px;font-weight:700;cursor:pointer;
  transition:all 0.2s;box-shadow:0 2px 8px rgba(249,168,37,0.28);
  text-decoration:none;display:inline-block;
}
.btn-or:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(249,168,37,0.38)}
.btn-ghost{
  background:#EEF5FF;color:#1565C0!important;border:1.5px solid #BBDEFB;
  border-radius:9px;padding:10px 22px;
  font-family:'Inter',sans-serif;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s;
  text-decoration:none;display:inline-block;
}
.btn-ghost:hover{background:#E3F2FD;border-color:#42A5F5}

/* ── Alertes ───────────────────────────────────── */
.alert-sga{padding:10px 15px;border-radius:8px;border-left:4px solid;
  font-size:13px;font-weight:500;margin-top:8px;animation:fadeIn 0.3s ease}

/* ── Tables ────────────────────────────────────── */
.sga-table{width:100%;border-collapse:collapse;font-size:13px}
.sga-table th{
  background:#0D47A1;color:#FFFFFF;padding:10px 13px;
  text-align:left;font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:0.5px;
}
.sga-table td{padding:10px 13px;border-bottom:1px solid #CFE2F3;vertical-align:middle}
.sga-table tr:nth-child(even) td{background:#F0F7FF}
.sga-table tr:hover td{background:#E3F2FD;transition:background 0.15s}

/* ── Upload ────────────────────────────────────── */
.upload-zone{
  border:2px dashed #BBDEFB;border-radius:12px;padding:26px;
  text-align:center;cursor:pointer;transition:all 0.2s;
  background:#E3F2FD;margin-bottom:12px;
}
.upload-zone:hover{border-color:#42A5F5;background:#DDEEFF}

/* ── Login ─────────────────────────────────────── */
.login-page{
  min-height:100vh;
  background:linear-gradient(135deg,#0D47A1 0%,#1565C0 50%,#42A5F5 100%);
  display:flex;align-items:center;justify-content:center;padding:24px;
}
.login-card{
  background:#FFFFFF;border-radius:20px;padding:42px 38px;
  width:100%;max-width:420px;
  box-shadow:0 20px 60px rgba(13,71,161,0.22);
}

/* ── Stat cards ────────────────────────────────── */
.stat-card{
  background:#FFFFFF;border-radius:14px;padding:20px 22px;
  border:1px solid #CFE2F3;box-shadow:0 2px 8px rgba(21,101,192,0.06);
  text-align:center;transition:transform 0.2s,box-shadow 0.2s;
}
.stat-card:hover{transform:translateY(-3px);box-shadow:0 6px 18px rgba(21,101,192,0.13)}

/* ── Badges ────────────────────────────────────── */
.badge-success{background:#E8F5E9;color:#2E7D32;padding:2px 9px;border-radius:20px;font-size:11px;font-weight:700}
.badge-danger{background:#FFEBEE;color:#C62828;padding:2px 9px;border-radius:20px;font-size:11px;font-weight:700}
.badge-bleu{background:#E3F2FD;color:#1565C0;border:1px solid #BBDEFB;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}

/* ── Ticker hero ───────────────────────────────── */
.ticker-wrap{overflow:hidden;white-space:nowrap;background:rgba(255,255,255,0.08);
  border-radius:8px;padding:8px 0;margin-top:18px}
.ticker-inner{display:inline-block;animation:ticker 28s linear infinite}
.ticker-inner:hover{animation-play-state:paused}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.ticker-item{display:inline-block;padding:0 32px;font-size:13px;color:rgba(255,255,255,0.88);font-weight:500}
.ticker-sep{color:#F9A825;font-weight:900}

/* ── Dropdown override ─────────────────────────── */
.Select-control{border-radius:8px!important;border-color:#CFE2F3!important}
.Select-control:hover{border-color:#42A5F5!important}
.is-focused .Select-control{box-shadow:0 0 0 3px rgba(66,165,245,0.12)!important}

/* ── Confirmation modal ────────────────────────── */
.modal-overlay{
  position:fixed;top:0;left:0;width:100%;height:100%;
  background:rgba(13,71,161,0.45);z-index:9999;
  display:flex;align-items:center;justify-content:center;
  animation:fadeIn 0.2s ease;
}
.modal-box{
  background:#FFFFFF;border-radius:18px;padding:36px 38px;
  max-width:460px;width:90%;
  box-shadow:0 20px 60px rgba(13,71,161,0.25);
  border-top:4px solid #F9A825;
  animation:slideDown 0.25s ease;
}
"""


def build_navbar():
    from dash import dcc
    links = [
        ("/accueil",   "Accueil"),
        ("/dashboard", "Tableau de bord"),
        ("/cours",     "Cours"),
        ("/seances",   "Séances"),
        ("/etudiants", "Étudiants"),
        ("/notes",     "Notes"),
        ("/analytics", "Analytics"),
        ("/migration", "Base de données"),
        ("/apropos",   "À propos"),
    ]
    return html.Div(className="sga-navbar", children=[
        html.Div(className="sga-brand", children=[
            html.Div("E", className="sga-logo-wrap"),
            html.Div(className="sga-brand-inner", children=[
                html.Div("ENSAE DAKAR", className="sga-brand-title"),
                html.Div("Système de Gestion Académique", className="sga-brand-sub"),
            ]),
        ]),
        html.Div(className="sga-nav-links", children=[
            dcc.Link(label, href=href, className="sga-nav-link")
            for href, label in links
        ]),
    ])


def build_footer():
    return html.Div(className="sga-footer", children=[
        html.Div(style={"maxWidth":"1200px","margin":"0 auto",
                        "display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"32px"}, children=[
            html.Div([
                html.Div(style={"display":"flex","alignItems":"center","gap":"12px","marginBottom":"14px"}, children=[
                    html.Div("E", style={"width":"38px","height":"38px","borderRadius":"50%",
                                         "background":"rgba(249,168,37,0.15)","border":"2px solid #F9A825",
                                         "display":"flex","alignItems":"center","justifyContent":"center",
                                         "fontFamily":"'Merriweather',serif","fontSize":"16px",
                                         "fontWeight":"900","color":"#F9A825"}),
                    html.Div([
                        html.Div("ENSAE Dakar", style={"fontSize":"14px","fontWeight":"800","color":"#FFFFFF"}),
                        html.Div("École Nationale de la Statistique", style={"fontSize":"11px","color":"rgba(255,255,255,0.55)"}),
                    ]),
                ]),
                html.Div("Système de Gestion Académique — Suivi des cours, étudiants et évaluations.",
                         style={"fontSize":"12px","color":"rgba(255,255,255,0.55)","lineHeight":"1.7"}),
            ]),
            html.Div([
                html.Div("Navigation", style={"fontSize":"10px","fontWeight":"700","color":"#F9A825",
                                               "letterSpacing":"2px","textTransform":"uppercase","marginBottom":"12px"}),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"6px"}, children=[
                    html.A(label, href=href, style={"color":"rgba(255,255,255,0.65)","fontSize":"12px","textDecoration":"none"})
                    for href, label in [("/dashboard","Tableau de bord"),("/cours","Cours"),
                                         ("/etudiants","Étudiants"),("/notes","Notes"),
                                         ("/seances","Séances"),("/analytics","Analytics")]
                ]),
            ]),
            html.Div([
                html.Div("Réalisé par", style={"fontSize":"10px","fontWeight":"700","color":"#F9A825",
                                                "letterSpacing":"2px","textTransform":"uppercase","marginBottom":"12px"}),
                html.Div("Gilbert OUMSAORE", style={"fontSize":"14px","fontWeight":"700","color":"#FFFFFF","marginBottom":"2px"}),
                html.Div("Josée JEAZE",      style={"fontSize":"14px","fontWeight":"700","color":"#FFFFFF","marginBottom":"8px"}),
                html.Div("Élèves Analystes Statisticiens", style={"fontSize":"12px","color":"rgba(255,255,255,0.6)"}),
                html.Div("3ème année — ENSAE Dakar",       style={"fontSize":"12px","color":"rgba(255,255,255,0.6)"}),
                html.Div("Data Visualisation 2025-2026",   style={"fontSize":"11px","color":"#F9A825","marginTop":"6px","fontStyle":"italic"}),
            ]),
        ]),
        html.Div(style={"maxWidth":"1200px","margin":"20px auto 0","paddingTop":"18px",
                        "borderTop":"1px solid rgba(255,255,255,0.1)",
                        "display":"flex","justifyContent":"space-between","alignItems":"center"}, children=[
            html.Div("© 2025-2026 ENSAE Dakar — SGA",
                     style={"fontSize":"12px","color":"rgba(255,255,255,0.38)"}),
            html.Div("Projet Data Visualisation · Python Dash · SQLite",
                     style={"fontSize":"12px","color":"rgba(255,255,255,0.38)"}),
        ]),
    ])


def page_header(title, subtitle=""):
    return html.Div(className="sga-page-header fade-in", children=[
        html.Div(title,    className="sga-page-header-title"),
        html.Div(subtitle, className="sga-page-header-sub") if subtitle else None,
    ])


def stat_mini(value, label, icon, bg, color):
    return html.Div(className="stat-card fade-in", style={"borderTop": f"3px solid {color}"}, children=[
        html.Div(icon, style={"fontSize":"28px","marginBottom":"8px"}),
        html.Div(str(value), style={"fontFamily":"'Merriweather',serif","fontSize":"30px",
                                     "fontWeight":"900","color":color}),
        html.Div(label, style={"fontSize":"12px","color":"#607D8B","marginTop":"3px","fontWeight":"500"}),
    ])


def confirm_modal(modal_id_cancel, modal_id_ok, title, subtitle, warning_text):
    """Modal de confirmation générique réutilisable."""
    return html.Div(className="modal-overlay", children=[
        html.Div(className="modal-box", children=[
            html.Div("⚠", style={"fontSize":"36px","textAlign":"center","marginBottom":"10px","color":"#F9A825"}),
            html.Div(title, style={
                "fontFamily":"'Merriweather',serif","fontSize":"19px","fontWeight":"900",
                "color":"#0D47A1","textAlign":"center","marginBottom":"8px",
            }),
            html.Div(subtitle, style={
                "textAlign":"center","fontWeight":"700","color":"#1565C0",
                "fontSize":"14px","marginBottom":"14px",
            }),
            html.Div(warning_text, style={
                "background":"#FFF8E1","border":"1px solid #FFE082","borderRadius":"8px",
                "padding":"10px 14px","fontSize":"13px","color":"#5D4037",
                "marginBottom":"22px","lineHeight":"1.55",
            }),
            html.Div(style={"display":"flex","gap":"12px"}, children=[
                html.Button("Annuler", id=modal_id_cancel,
                            style={"flex":"1","padding":"11px","background":"#EEF5FF",
                                   "color":"#0D47A1","border":"1.5px solid #BBDEFB",
                                   "borderRadius":"8px","cursor":"pointer","fontWeight":"700","fontSize":"14px"}),
                html.Button("Oui, supprimer", id=modal_id_ok,
                            style={"flex":"1","padding":"11px","background":"#C62828",
                                   "color":"#FFFFFF","border":"none","borderRadius":"8px",
                                   "cursor":"pointer","fontWeight":"700","fontSize":"14px"}),
            ]),
        ]),
    ])

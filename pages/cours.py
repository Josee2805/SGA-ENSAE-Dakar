"""pages/cours.py — Gestion des Cours ENSAE Dakar"""
from dash import html, dcc, callback, Input, Output, State, ctx, no_update, ALL
from models.database import get_db, Course
from utils.layout import page_header, C


def _read_courses():
    db = get_db()
    courses = db.query(Course).order_by(Course.code).all()
    data = []
    for co in courses:
        done = sum(s.duree for s in co.sessions)
        data.append({"code":co.code,"libelle":co.libelle,"enseignant":co.enseignant or "",
                     "description":co.description or "","volume":co.volume_total or 0,"done":done})
    db.close()
    return data


def _build_list():
    data = _read_courses()
    if not data:
        return html.Div("Aucun cours. Utilisez le formulaire ci-dessus.",
                        style={"padding":"30px","textAlign":"center","color":C["muted"],"fontStyle":"italic"})
    rows = []
    for d in data:
        pct = min(100, int(d["done"]/d["volume"]*100)) if d["volume"] else 0
        pc  = C["success"] if pct>=80 else C["warning"] if pct>=40 else C["bleu"]
        rows.append(html.Div(style={"padding":"16px 20px","borderBottom":f"1px solid {C['bordure']}"}, children=[
            html.Div(style={"display":"flex","alignItems":"flex-start","justifyContent":"space-between","gap":"16px","marginBottom":"10px"}, children=[
                html.Div(style={"display":"flex","gap":"14px","flex":"1","alignItems":"flex-start"}, children=[
                    html.Span(d["code"], style={"fontWeight":"800","color":C["bleu3"],"fontSize":"12px",
                                                "background":C["bleu_pale"],"padding":"5px 12px",
                                                "borderRadius":"6px","whiteSpace":"nowrap",
                                                "border":f"1px solid {C['bleu_pale2']}"}),
                    html.Div([
                        html.Div(d["libelle"], style={"fontWeight":"700","fontSize":"15px",
                                                       "fontFamily":"'Merriweather',serif","color":C["texte"]}),
                        html.Div(f"{d['enseignant'] or 'Enseignant non renseigné'}  ·  {d['volume']}h",
                                 style={"fontSize":"12px","color":C["muted"],"marginTop":"2px"}),
                        html.Div(d["description"],
                                 style={"fontSize":"12px","color":C["muted"],"fontStyle":"italic","marginTop":"2px"})
                        if d["description"] else None,
                    ]),
                ]),
                html.Div(style={"display":"flex","gap":"8px","flexShrink":"0"}, children=[
                    html.Button("Modifier", id={"type":"cours-edit-btn","index":d["code"]},
                                style={"background":C["bleu_pale"],"color":C["bleu3"],
                                       "border":f"1px solid {C['bleu_pale2']}","borderRadius":"6px",
                                       "padding":"7px 14px","fontSize":"12px","cursor":"pointer","fontWeight":"700"}),
                    html.Button("Supprimer", id={"type":"cours-del-btn","index":d["code"]},
                                style={"background":"#FFEBEE","color":C["danger"],"border":"1px solid #FFCDD2",
                                       "borderRadius":"6px","padding":"7px 14px","fontSize":"12px",
                                       "cursor":"pointer","fontWeight":"700"}),
                ]),
            ]),
            html.Div([
                html.Div(style={"display":"flex","justifyContent":"space-between","marginBottom":"4px"}, children=[
                    html.Span(f"{d['done']}h effectuées / {d['volume']}h prévues",
                              style={"fontSize":"12px","color":C["muted"]}),
                    html.Span(f"{pct}%", style={"fontSize":"12px","fontWeight":"800","color":pc}),
                ]),
                html.Div(style={"background":C["bleu_pale2"],"borderRadius":"100px","height":"8px"}, children=[
                    html.Div(style={"width":f"{pct}%","height":"100%","borderRadius":"100px",
                                    "background":f"linear-gradient(90deg,{C['bleu']},{C['bleu_clair']})"}),
                ]),
            ]),
        ]))
    return html.Div(rows)


def layout():
    return html.Div([
        dcc.Store(id="cours-edit-store",    data=None),
        dcc.Store(id="cours-delete-store",  data=None),
        dcc.Store(id="cours-pending-delete",data=None),
        page_header("Gestion des Cours", "Ajouter, modifier ou supprimer les matières"),

        # Formulaire
        html.Div(style={"display":"flex","justifyContent":"center","marginBottom":"28px"}, children=[
            html.Div(style={"width":"100%","maxWidth":"640px"}, children=[
                html.Div(className="sga-card", children=[
                    html.Div(id="cours-form-title", children="Ajouter un cours", className="sga-card-title"),
                    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"}, children=[
                        html.Div([html.Label("Code cours *", className="form-label-sga"),
                                   dcc.Input(id="cours-code",   type="text",   placeholder="STAT301",
                                             className="sga-input", style={"marginBottom":"0"})]),
                        html.Div([html.Label("Volume horaire (h) *", className="form-label-sga"),
                                   dcc.Input(id="cours-volume", type="number", placeholder="30", min=1,
                                             className="sga-input", style={"marginBottom":"0"})]),
                    ]),
                    html.Div(style={"height":"14px"}),
                    html.Label("Intitulé *", className="form-label-sga"),
                    dcc.Input(id="cours-libelle", type="text",
                              placeholder="Statistiques et Probabilités", className="sga-input"),
                    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"}, children=[
                        html.Div([html.Label("Enseignant", className="form-label-sga"),
                                   dcc.Input(id="cours-enseignant", type="text", placeholder="Prof. Nom",
                                             className="sga-input", style={"marginBottom":"0"})]),
                        html.Div([html.Label("Coefficient", className="form-label-sga"),
                                   dcc.Input(id="cours-coef", type="number", placeholder="1.5",
                                             min=0.5, step=0.5,
                                             className="sga-input", style={"marginBottom":"0"})]),
                    ]),
                    html.Div(style={"height":"14px"}),
                    html.Label("Description", className="form-label-sga"),
                    dcc.Textarea(id="cours-desc", placeholder="Contenu et objectifs...",
                                 style={"width":"100%","height":"70px","marginBottom":"20px","padding":"10px 14px",
                                        "border":"1.5px solid #CFE2F3","borderRadius":"8px",
                                        "fontFamily":"Inter,sans-serif","fontSize":"14px","background":"#F8FBFF",
                                        "outline":"none","resize":"vertical","boxSizing":"border-box"}),
                    html.Div(style={"display":"flex","gap":"10px"}, children=[
                        html.Button("Enregistrer", id="cours-btn-save", className="btn-bleu",
                                    style={"flex":"1","padding":"11px"}),
                        html.Button("Effacer",     id="cours-btn-clear", className="btn-ghost",
                                    style={"padding":"11px 20px"}),
                    ]),
                    html.Div(id="cours-feedback", style={"marginTop":"10px"}),

                ]),
            ]),
        ]),

        # ── Modal confirmation TOUJOURS dans le DOM ───────────────────────
        html.Div(id="cours-modal-overlay", style={"display":"none"}, children=[
            html.Div(className="modal-overlay", children=[
                html.Div(className="modal-box", children=[
                    html.Div("⚠", style={"fontSize":"36px","textAlign":"center","marginBottom":"10px","color":"#F9A825"}),
                    html.Div("Confirmer la suppression", style={
                        "fontFamily":"'Merriweather',serif","fontSize":"19px","fontWeight":"900",
                        "color":C["bleu3"],"textAlign":"center","marginBottom":"8px",
                    }),
                    html.Div(id="cours-modal-label", style={
                        "textAlign":"center","fontWeight":"700","color":C["bleu"],
                        "fontSize":"14px","marginBottom":"14px",
                    }),
                    html.Div("Cette action supprimera toutes les séances et notes associées à ce cours. Irréversible.", style={
                        "background":"#FFF8E1","border":"1px solid #FFE082","borderRadius":"8px",
                        "padding":"10px 14px","fontSize":"13px","color":"#5D4037","marginBottom":"22px","lineHeight":"1.55",
                    }),
                    html.Div(style={"display":"flex","gap":"12px"}, children=[
                        html.Button("Annuler", id="cours-confirm-cancel",
                                    style={"flex":"1","padding":"11px","background":C["creme2"],
                                           "color":C["bleu3"],"border":f"1.5px solid {C['bleu_pale2']}",
                                           "borderRadius":"8px","cursor":"pointer","fontWeight":"700","fontSize":"14px"}),
                        html.Button("Oui, supprimer", id="cours-confirm-ok",
                                    style={"flex":"1","padding":"11px","background":"#C62828",
                                           "color":"#FFFFFF","border":"none","borderRadius":"8px",
                                           "cursor":"pointer","fontWeight":"700","fontSize":"14px"}),
                    ]),
                ]),
            ]),
        ]),

        # Liste
        html.Div(className="sga-card", style={"padding":"0"}, children=[
            html.Div("Liste des matières", className="sga-card-title",
                     style={"padding":"20px 20px 14px","marginBottom":"0","borderBottom":"none"}),
            html.Div(id="cours-list", children=_build_list()),
        ]),
    ])


# ── Capture delete clicks ─────────────────────────────────────────────────────
@callback(Output("cours-delete-store","data"),
          Input({"type":"cours-del-btn","index":ALL},"n_clicks"),
          prevent_initial_call=True)
def cap_delete(clicks):
    if not any(n for n in clicks if n): return no_update
    t = ctx.triggered_id
    return t["index"] if isinstance(t, dict) else no_update


@callback(Output("cours-edit-store","data"),
          Input({"type":"cours-edit-btn","index":ALL},"n_clicks"),
          prevent_initial_call=True)
def cap_edit(clicks):
    if not any(n for n in clicks if n): return no_update
    t = ctx.triggered_id
    return t["index"] if isinstance(t, dict) else no_update


# ── Main handler ──────────────────────────────────────────────────────────────
@callback(
    Output("cours-list",          "children"),
    Output("cours-feedback",      "children"),
    Output("cours-form-title",    "children"),
    Output("cours-code",          "value"),
    Output("cours-libelle",       "value"),
    Output("cours-enseignant",    "value"),
    Output("cours-volume",        "value"),
    Output("cours-coef",          "value"),
    Output("cours-desc",          "value"),
    Output("cours-modal-overlay", "style"),
    Output("cours-modal-label",   "children"),
    Output("cours-pending-delete","data"),
    Input("cours-btn-save",       "n_clicks"),
    Input("cours-btn-clear",      "n_clicks"),
    Input("cours-delete-store",   "data"),
    Input("cours-edit-store",     "data"),
    Input("cours-confirm-ok",     "n_clicks"),
    Input("cours-confirm-cancel", "n_clicks"),
    State("cours-code",           "value"),
    State("cours-libelle",        "value"),
    State("cours-enseignant",     "value"),
    State("cours-volume",         "value"),
    State("cours-coef",           "value"),
    State("cours-desc",           "value"),
    State("cours-pending-delete", "data"),
    prevent_initial_call=True,
)
def handle_cours(n_save, n_clear, del_code, edit_code, n_ok, n_cancel,
                 code, libelle, enseignant, volume, coef, desc, pending):
    t      = ctx.triggered_id
    SHOW   = {"display":"block"}
    HIDE   = {"display":"none"}
    NONE12 = (no_update,)*12

    # ── Effacer formulaire ────────────────────────────────────────────────
    if t == "cours-btn-clear":
        return _build_list(), "", "Ajouter un cours", "", "", "", None, None, "", HIDE, "", None

    # ── Charger pour modification ─────────────────────────────────────────
    if t == "cours-edit-store" and edit_code:
        db = get_db()
        co = db.query(Course).filter(Course.code==edit_code).first()
        if co:
            vals = (co.code, co.libelle, co.enseignant or "", co.volume_total, None, co.description or "")
            db.close()
            return (_build_list(),
                    html.Div("Modifiez puis cliquez Enregistrer.", className="alert-sga",
                             style={"background":"#E3F2FD","color":C["bleu"],"borderLeftColor":C["bleu"]}),
                    f"Modifier : {edit_code}", *vals, HIDE, "", None)
        db.close()
        return _build_list(), "", "Ajouter un cours", "", "", "", None, None, "", HIDE, "", None

    # ── Demande suppression → afficher modal ──────────────────────────────
    if t == "cours-delete-store" and del_code:
        db  = get_db()
        co  = db.query(Course).filter(Course.code==del_code).first()
        lib = co.libelle if co else del_code
        db.close()
        label = f"« {del_code} — {lib} »"
        return (no_update, no_update, no_update, no_update, no_update, no_update,
                no_update, no_update, no_update, SHOW, label, del_code)

    # ── Annuler suppression ───────────────────────────────────────────────
    if t == "cours-confirm-cancel":
        return (no_update,
                html.Div("Suppression annulée.", className="alert-sga",
                         style={"background":"#E3F2FD","color":C["bleu"],"borderLeftColor":C["bleu"]}),
                no_update, no_update, no_update, no_update, no_update, no_update, no_update,
                HIDE, "", None)

    # ── Confirmer suppression ─────────────────────────────────────────────
    if t == "cours-confirm-ok" and pending:
        db = get_db()
        co = db.query(Course).filter(Course.code==pending).first()
        if co: db.delete(co); db.commit()
        db.close()
        return (_build_list(),
                html.Div(f"Cours {pending} supprimé.", className="alert-sga",
                         style={"background":C["orange_clair"],"color":C["warning"],"borderLeftColor":C["warning"]}),
                "Ajouter un cours", "", "", "", None, None, "", HIDE, "", None)

    # ── Enregistrer ───────────────────────────────────────────────────────
    if t == "cours-btn-save" and n_save:
        if not code or not libelle or not volume:
            return (no_update,
                    html.Div("Code, intitulé et volume sont obligatoires.", className="alert-sga",
                             style={"background":C["rouge_clair"],"color":C["danger"],"borderLeftColor":C["danger"]}),
                    *([no_update]*10))
        db         = get_db()
        code_clean = str(code).strip().upper()
        ex         = db.query(Course).filter(Course.code==code_clean).first()
        if ex:
            ex.libelle=libelle.strip(); ex.enseignant=(enseignant or "").strip()
            ex.volume_total=int(volume); ex.description=(desc or "").strip()
            db.commit(); msg = f"Cours {code_clean} mis à jour."
        else:
            db.add(Course(code=code_clean, libelle=libelle.strip(),
                          enseignant=(enseignant or "").strip(),
                          volume_total=int(volume), description=(desc or "").strip()))
            db.commit(); msg = f"Cours {code_clean} créé."
        db.close()
        return (_build_list(),
                html.Div(msg, className="alert-sga",
                         style={"background":C["vert_clair"],"color":C["success"],"borderLeftColor":C["success"]}),
                "Ajouter un cours", "", "", "", None, None, "", HIDE, "", None)

    return (no_update,)*12

"""pages/seances.py — Séances ENSAE Dakar — modal toujours dans DOM"""
from dash import html, dcc, callback, Input, Output, State, ctx, no_update, ALL
from models.database import get_db, Course, Session, Student, Attendance
from utils.layout import page_header, C
from datetime import date


def _build_history(course_filter=None, date_debut=None, date_fin=None):
    from datetime import datetime
    db  = get_db()
    q   = db.query(Session).order_by(Session.date.desc())
    if course_filter and course_filter != "all":
        q = q.filter(Session.course_code==course_filter)
    sessions = q.all()
    data = []
    for s in sessions:
        d = s.date
        if date_debut:
            try:
                dd = datetime.strptime(date_debut[:10],"%Y-%m-%d").date()
                if d < dd: continue
            except: pass
        if date_fin:
            try:
                df2 = datetime.strptime(date_fin[:10],"%Y-%m-%d").date()
                if d > df2: continue
            except: pass
        data.append({"id":s.id,
                     "date":d.strftime("%d/%m/%Y") if d else "",
                     "code":s.course_code,
                     "libelle":s.course.libelle if s.course else "",
                     "theme":s.theme or "","duree":s.duree,
                     "salle":s.salle or "","nb_abs":len(s.attendances)})
    db.close()
    if not data:
        return html.Div("Aucune séance pour ces critères.",
                        style={"padding":"24px","textAlign":"center","color":C["muted"],"fontStyle":"italic"})
    rows = []
    for d in data:
        ac = {"background":"#FFEBEE","color":C["danger"],"padding":"2px 10px","borderRadius":"20px","fontSize":"11px","fontWeight":"700"}
        ok = {"background":C["vert_clair"],"color":C["success"],"padding":"2px 10px","borderRadius":"20px","fontSize":"11px","fontWeight":"700"}
        rows.append(html.Tr([
            html.Td(d["date"], style={"fontWeight":"700","color":C["bleu"]}),
            html.Td([html.Span(d["code"], style={"background":C["bleu_pale"],"color":C["bleu3"],
                                                  "padding":"2px 8px","borderRadius":"4px","fontSize":"11px",
                                                  "fontWeight":"800","marginRight":"6px"}),
                     html.Span(d["libelle"], style={"fontSize":"13px"})]),
            html.Td(d["theme"], style={"fontSize":"13px","color":C["muted"]}),
            html.Td(f"{d['duree']}h"),
            html.Td(d["salle"]),
            html.Td(html.Span(f"{d['nb_abs']} abs.", style=ac if d["nb_abs"]>0 else ok)),
            html.Td(html.Button("Supprimer", id={"type":"seance-del","index":d["id"]},
                                style={"background":"#FFEBEE","color":C["danger"],"border":"1px solid #FFCDD2",
                                       "borderRadius":"5px","fontSize":"11px","padding":"4px 10px","cursor":"pointer","fontWeight":"600"})),
        ]))
    return html.Table(className="sga-table", children=[
        html.Thead(html.Tr([html.Th("Date"),html.Th("Cours"),html.Th("Thème"),
                             html.Th("Durée"),html.Th("Salle"),html.Th("Absences"),html.Th("")])),
        html.Tbody(rows),
    ])


def layout():
    db      = get_db()
    courses  = db.query(Course).all()
    c_data   = [(c.code, c.libelle) for c in courses]
    students = db.query(Student).order_by(Student.nom).all()
    s_data   = [(s.id, s.prenom, s.nom) for s in students]
    db.close()
    c_opts = [{"label":f"{code} — {lib}","value":code} for code,lib in c_data]

    return html.Div([
        dcc.Store(id="seance-del-store",      data=None),
        dcc.Store(id="seance-pending-delete", data=None),
        page_header("Gestion des Séances", "Enregistrer les cours effectués et les absences"),

        html.Div(style={"display":"flex","justifyContent":"center","marginBottom":"28px"}, children=[
            html.Div(style={"width":"100%","maxWidth":"720px"}, children=[
                html.Div(className="sga-card", children=[
                    html.Div("Enregistrer une séance", className="sga-card-title"),
                    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"}, children=[
                        html.Div([html.Label("Cours *", className="form-label-sga"),
                                   dcc.Dropdown(id="s-cours", options=c_opts,
                                                placeholder="Sélectionner", style={"marginBottom":"0"})]),
                        html.Div([html.Label("Date *", className="form-label-sga"),
                                   dcc.DatePickerSingle(id="s-date", date=date.today(),
                                                         display_format="DD/MM/YYYY")]),
                    ]),
                    html.Div(style={"height":"14px"}),
                    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"}, children=[
                        html.Div([html.Label("Durée (heures) *", className="form-label-sga"),
                                   dcc.Input(id="s-duree", type="number", value=1.5, min=0.5, step=0.5,
                                             className="sga-input", style={"marginBottom":"0"})]),
                        html.Div([html.Label("Salle", className="form-label-sga"),
                                   dcc.Input(id="s-salle", type="text", placeholder="Amphi A",
                                             className="sga-input", style={"marginBottom":"0"})]),
                    ]),
                    html.Div(style={"height":"14px"}),
                    html.Label("Thème abordé", className="form-label-sga"),
                    dcc.Textarea(id="s-theme", placeholder="Sujet traité...",
                                 style={"width":"100%","height":"65px","marginBottom":"14px","padding":"10px 14px",
                                        "border":"1.5px solid #CFE2F3","borderRadius":"8px",
                                        "fontFamily":"Inter,sans-serif","fontSize":"14px","background":"#F8FBFF",
                                        "outline":"none","resize":"vertical","boxSizing":"border-box"}),
                    html.Label("Étudiants absents", className="form-label-sga"),
                    dcc.Checklist(id="s-absents",
                                  options=[{"label":f" {p} {n}","value":sid} for sid,p,n in s_data],
                                  value=[],
                                  style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr",
                                         "gap":"6px","marginBottom":"20px","fontSize":"14px"},
                                  inputStyle={"marginRight":"6px","accentColor":C["bleu"]}),
                    html.Button("Enregistrer la séance", id="s-btn-save", className="btn-bleu",
                                style={"width":"100%","padding":"12px","fontSize":"15px"}),
                    html.Div(id="s-feedback", style={"marginTop":"10px"}),

                ]),
            ]),
        ]),

        # ── Modal toujours présent ────────────────────────────────────────
        html.Div(id="seance-modal-overlay", style={"display":"none"}, children=[
            html.Div(className="modal-overlay", children=[
                html.Div(className="modal-box", children=[
                    html.Div("⚠", style={"fontSize":"36px","textAlign":"center","marginBottom":"10px","color":"#F9A825"}),
                    html.Div("Supprimer cette séance ?", style={
                        "fontFamily":"'Merriweather',serif","fontSize":"19px","fontWeight":"900",
                        "color":C["bleu3"],"textAlign":"center","marginBottom":"8px",
                    }),
                    html.Div(id="seance-modal-label", style={
                        "textAlign":"center","fontWeight":"700","color":C["bleu"],"fontSize":"14px","marginBottom":"14px",
                    }),
                    html.Div("Cette action supprimera aussi les présences enregistrées pour cette séance.", style={
                        "background":"#FFF8E1","border":"1px solid #FFE082","borderRadius":"8px",
                        "padding":"10px 14px","fontSize":"13px","color":"#5D4037","marginBottom":"22px",
                    }),
                    html.Div(style={"display":"flex","gap":"12px"}, children=[
                        html.Button("Annuler",  id="seance-confirm-cancel",
                                    style={"flex":"1","padding":"11px","background":C["creme2"],
                                           "color":C["bleu3"],"border":f"1.5px solid {C['bleu_pale2']}",
                                           "borderRadius":"8px","cursor":"pointer","fontWeight":"700"}),
                        html.Button("Oui, supprimer", id="seance-confirm-ok",
                                    style={"flex":"1","padding":"11px","background":"#C62828",
                                           "color":"#FFFFFF","border":"none","borderRadius":"8px",
                                           "cursor":"pointer","fontWeight":"700"}),
                    ]),
                ]),
            ]),
        ]),

        # Historique avec filtres
        html.Div(className="sga-card", style={"padding":"0"}, children=[
            html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                            "padding":"18px 20px 14px","flexWrap":"wrap","gap":"10px"}, children=[
                html.Div("Historique des séances", className="sga-card-title",
                         style={"marginBottom":"0","borderBottom":"none","paddingBottom":"0"}),
                html.Div(style={"display":"flex","gap":"10px","alignItems":"center","flexWrap":"wrap"}, children=[
                    dcc.Dropdown(id="s-filter-cours",
                                 options=[{"label":"Tous les cours","value":"all"}]+c_opts,
                                 value="all", clearable=False, style={"width":"220px","fontSize":"13px"}),
                    dcc.DatePickerRange(id="s-filter-dates", display_format="DD/MM/YYYY",
                                        start_date_placeholder_text="Du",
                                        end_date_placeholder_text="Au"),
                    html.Button("Réinitialiser", id="s-btn-reset-filters",
                                style={"background":C["creme2"],"color":C["muted"],"border":f"1px solid {C['bordure']}",
                                       "borderRadius":"6px","padding":"7px 12px","fontSize":"12px","cursor":"pointer"}),
                ]),
            ]),
            html.Div(id="s-history", children=_build_history()),
        ]),
    ])


@callback(Output("seance-del-store","data"),
          Input({"type":"seance-del","index":ALL},"n_clicks"),
          prevent_initial_call=True)
def cap_del(clicks):
    if not any(n for n in clicks if n): return no_update
    t = ctx.triggered_id
    return t["index"] if isinstance(t, dict) else no_update


@callback(
    Output("s-history",            "children"),
    Output("s-feedback",           "children"),
    Output("seance-modal-overlay", "style"),
    Output("seance-modal-label",   "children"),
    Output("seance-pending-delete","data"),
    Input("s-btn-save",            "n_clicks"),
    Input("s-filter-cours",        "value"),
    Input("s-filter-dates",        "start_date"),
    Input("s-filter-dates",        "end_date"),
    Input("s-btn-reset-filters",   "n_clicks"),
    Input("seance-del-store",      "data"),
    Input("seance-confirm-ok",     "n_clicks"),
    Input("seance-confirm-cancel", "n_clicks"),
    State("s-cours",  "value"), State("s-date",   "date"),
    State("s-duree",  "value"), State("s-salle",  "value"),
    State("s-theme",  "value"), State("s-absents","value"),
    State("seance-pending-delete", "data"),
    prevent_initial_call=True,
)
def handle_seance(n_save, filt, d_start, d_end, n_reset,
                  del_id, n_ok, n_cancel,
                  code, d, duree, salle, theme, absents, pending):
    t    = ctx.triggered_id
    SHOW = {"display":"block"}
    HIDE = {"display":"none"}

    if t == "s-btn-reset-filters":
        return _build_history(), no_update, HIDE, "", None

    if t in ("s-filter-cours","s-filter-dates"):
        return _build_history(filt, d_start, d_end), no_update, no_update, no_update, no_update

    if t == "seance-del-store" and del_id:
        db   = get_db()
        sess = db.query(Session).filter(Session.id==del_id).first()
        label = f"{sess.course_code} — {sess.date}" if sess else str(del_id)
        db.close()
        return no_update, no_update, SHOW, label, del_id

    if t == "seance-confirm-cancel":
        return (no_update,
                html.Div("Suppression annulée.", className="alert-sga",
                         style={"background":"#E3F2FD","color":C["bleu"],"borderLeftColor":C["bleu"]}),
                HIDE, "", None)

    if t == "seance-confirm-ok" and pending:
        db = get_db()
        s  = db.query(Session).filter(Session.id==pending).first()
        if s: db.delete(s); db.commit()
        db.close()
        return (_build_history(filt, d_start, d_end),
                html.Div("Séance supprimée.", className="alert-sga",
                         style={"background":C["orange_clair"],"color":C["warning"],"borderLeftColor":C["warning"]}),
                HIDE, "", None)

    if t == "s-btn-save" and n_save:
        if not code or not d:
            return (no_update,
                    html.Div("Cours et date sont obligatoires.", className="alert-sga",
                             style={"background":C["rouge_clair"],"color":C["danger"],"borderLeftColor":C["danger"]}),
                    HIDE, "", no_update)
        from datetime import datetime
        db       = get_db()
        date_val = datetime.strptime(d[:10],"%Y-%m-%d").date()
        sess     = Session(course_code=code, date=date_val,
                           duree=float(duree or 1.5), salle=salle or "", theme=theme or "")
        db.add(sess); db.commit()
        for stid in (absents or []):
            db.merge(Attendance(id_session=sess.id, id_student=int(stid)))
        db.commit(); db.close()
        return (_build_history(filt, d_start, d_end),
                html.Div("Séance enregistrée.", className="alert-sga",
                         style={"background":C["vert_clair"],"color":C["success"],"borderLeftColor":C["success"]}),
                HIDE, "", None)

    return _build_history(filt, d_start, d_end), no_update, no_update, no_update, no_update

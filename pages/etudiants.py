"""pages/etudiants.py — Étudiants ENSAE Dakar — modal toujours dans DOM"""
import io
from dash import html, dcc, callback, Input, Output, State, ctx, no_update, ALL
from models.database import get_db, Student, Session, Grade
from utils.layout import page_header, C


def _read_students():
    db = get_db()
    students = db.query(Student).order_by(Student.nom).all()
    total_sessions = db.query(Session).count()
    data = []
    for s in students:
        grades  = s.grades
        nb_abs  = len(s.attendances)
        moy     = (sum(g.note*g.coefficient for g in grades)/sum(g.coefficient for g in grades)) if grades else None
        taux    = round(nb_abs/total_sessions*100) if total_sessions else 0
        data.append({"id":s.id,"nom":s.nom,"prenom":s.prenom,"email":s.email,
                     "filiere":s.filiere or "","annee":s.annee,
                     "dob":s.date_naissance.strftime("%d/%m/%Y") if s.date_naissance else "—",
                     "moy":moy,"taux":taux,"nb_abs":nb_abs})
    db.close()
    return data


def _build_list(search=None):
    data = _read_students()
    if search:
        s2 = search.lower()
        data = [d for d in data if s2 in d["nom"].lower() or s2 in d["prenom"].lower()
                or s2 in d["email"].lower() or s2 in d["filiere"].lower()]
    if not data:
        return html.Div("Aucun étudiant.",
                        style={"padding":"24px","textAlign":"center","color":C["muted"],"fontStyle":"italic"})
    rows = []
    for d in data:
        mc = C["success"] if (d["moy"] and d["moy"]>=12) else C["warning"] if (d["moy"] and d["moy"]>=8) else C["danger"]
        ac = C["danger"] if d["taux"]>20 else C["warning"] if d["taux"]>10 else C["success"]
        rows.append(html.Tr([
            html.Td([html.Div(f"{d['prenom']} {d['nom']}", style={"fontWeight":"700"}),
                     html.Div(f"{d['filiere']} · {d['annee']}e année",
                              style={"fontSize":"11px","color":C["muted"]})]),
            html.Td(d["email"], style={"fontSize":"12px","color":C["muted"]}),
            html.Td(html.Span(f"{d['moy']:.1f}/20" if d["moy"] is not None else "—",
                              style={"background":f"{mc}22","color":mc,"padding":"3px 10px",
                                     "borderRadius":"20px","fontSize":"12px","fontWeight":"700"})),
            html.Td(html.Span(f"{d['taux']}%",
                              style={"background":f"{ac}22","color":ac,"padding":"3px 10px",
                                     "borderRadius":"20px","fontSize":"12px","fontWeight":"700"})),
            html.Td(style={"display":"flex","gap":"6px"}, children=[
                html.Button("Fiche", id={"type":"etud-fiche-btn","index":d["id"]},
                            style={"background":C["bleu_pale"],"color":C["bleu3"],
                                   "border":f"1px solid {C['bleu_pale2']}","borderRadius":"6px",
                                   "padding":"5px 12px","fontSize":"12px","cursor":"pointer","fontWeight":"700"}),
                html.Button("Supprimer", id={"type":"etud-del-btn","index":d["id"]},
                            style={"background":"#FFEBEE","color":C["danger"],"border":"1px solid #FFCDD2",
                                   "borderRadius":"6px","padding":"5px 10px","fontSize":"12px",
                                   "cursor":"pointer","fontWeight":"600"}),
            ]),
        ]))
    return html.Table(className="sga-table", children=[
        html.Thead(html.Tr([html.Th("Étudiant"),html.Th("Email"),html.Th("Moyenne"),
                             html.Th("Absentéisme"),html.Th("")])),
        html.Tbody(rows),
    ])


def _info_item(label, val):
    return html.Div([
        html.Div(label, style={"fontSize":"11px","fontWeight":"700","color":C["muted"],
                                "textTransform":"uppercase","letterSpacing":"0.5px"}),
        html.Div(val,   style={"fontSize":"14px","fontWeight":"600","color":C["texte"],"marginTop":"2px"}),
    ])

def _stat_card(label, val, color, sub):
    return html.Div(style={"textAlign":"center","padding":"16px","background":C["bleu_pale"],
                            "borderRadius":"10px","border":f"1px solid {C['bleu_pale2']}"}, children=[
        html.Div(label, style={"fontSize":"11px","color":C["muted"],"fontWeight":"700",
                                "textTransform":"uppercase","letterSpacing":"0.5px"}),
        html.Div(val,   style={"fontSize":"24px","fontWeight":"800","color":color,
                                "fontFamily":"'Merriweather',serif","margin":"4px 0"}),
        html.Div(sub,   style={"fontSize":"11px","color":C["muted"]}),
    ])


def layout():
    return html.Div([
        dcc.Store(id="etud-dl-trigger",    data=None),
        dcc.Store(id="etud-del-store",     data=None),
        dcc.Store(id="etud-fiche-store",   data=None),
        dcc.Store(id="etud-pending-delete",data=None),
        page_header("Gestion des Étudiants", "Inscrire, consulter et gérer les dossiers"),

        html.Div(style={"display":"flex","justifyContent":"center","marginBottom":"28px"}, children=[
            html.Div(style={"width":"100%","maxWidth":"640px"}, children=[
                html.Div(className="sga-card", children=[
                    html.Div("Inscrire un étudiant", className="sga-card-title"),
                    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"}, children=[
                        html.Div([html.Label("Nom *", className="form-label-sga"),
                                   dcc.Input(id="e-nom", type="text", placeholder="Diallo",
                                             className="sga-input", style={"marginBottom":"0"})]),
                        html.Div([html.Label("Prénom *", className="form-label-sga"),
                                   dcc.Input(id="e-prenom", type="text", placeholder="Aminata",
                                             className="sga-input", style={"marginBottom":"0"})]),
                    ]),
                    html.Div(style={"height":"14px"}),
                    html.Label("Email *", className="form-label-sga"),
                    dcc.Input(id="e-email", type="email",
                              placeholder="a.diallo@ensae.sn", className="sga-input"),
                    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"16px"}, children=[
                        html.Div([html.Label("Filière", className="form-label-sga"),
                                   dcc.Dropdown(id="e-filiere",
                                                options=[{"label":f,"value":f} for f in
                                                         ["Statistique","Économie","Actuariat","Finance","Data Science"]],
                                                value="Statistique", style={"marginBottom":"0"})]),
                        html.Div([html.Label("Année", className="form-label-sga"),
                                   dcc.Dropdown(id="e-annee",
                                                options=[{"label":f"{i}e année","value":i} for i in [1,2,3,4]],
                                                value=3, style={"marginBottom":"0"})]),
                        html.Div([html.Label("Date de naissance", className="form-label-sga"),
                                   dcc.DatePickerSingle(id="e-dob", display_format="DD/MM/YYYY",
                                                         placeholder="JJ/MM/AAAA")]),
                    ]),
                    html.Div(style={"height":"18px"}),
                    html.Button("Inscrire l'étudiant", id="e-btn-save", className="btn-bleu",
                                style={"width":"100%","padding":"12px","fontSize":"15px"}),
                    html.Div(id="e-feedback", style={"marginTop":"10px"}),
                    dcc.Download(id="etud-dl-fiche"),
                ]),
            ]),
        ]),

        # ── Modal toujours présent ────────────────────────────────────────
        html.Div(id="etud-modal-overlay", style={"display":"none"}, children=[
            html.Div(className="modal-overlay", children=[
                html.Div(className="modal-box", children=[
                    html.Div("⚠", style={"fontSize":"36px","textAlign":"center","marginBottom":"10px","color":"#F9A825"}),
                    html.Div("Supprimer cet étudiant ?", style={
                        "fontFamily":"'Merriweather',serif","fontSize":"19px","fontWeight":"900",
                        "color":C["bleu3"],"textAlign":"center","marginBottom":"8px",
                    }),
                    html.Div(id="etud-modal-label", style={
                        "textAlign":"center","fontWeight":"700","color":C["bleu"],"fontSize":"14px","marginBottom":"14px",
                    }),
                    html.Div("Cette action supprimera définitivement le dossier de cet étudiant, y compris toutes ses notes et absences.", style={
                        "background":"#FFF8E1","border":"1px solid #FFE082","borderRadius":"8px",
                        "padding":"10px 14px","fontSize":"13px","color":"#5D4037","marginBottom":"22px",
                    }),
                    html.Div(style={"display":"flex","gap":"12px"}, children=[
                        html.Button("Annuler", id="etud-confirm-cancel",
                                    style={"flex":"1","padding":"11px","background":C["creme2"],
                                           "color":C["bleu3"],"border":f"1.5px solid {C['bleu_pale2']}",
                                           "borderRadius":"8px","cursor":"pointer","fontWeight":"700"}),
                        html.Button("Oui, supprimer", id="etud-confirm-ok",
                                    style={"flex":"1","padding":"11px","background":"#C62828",
                                           "color":"#FFFFFF","border":"none","borderRadius":"8px",
                                           "cursor":"pointer","fontWeight":"700"}),
                    ]),
                ]),
            ]),
        ]),

        html.Div(id="e-fiche", style={"marginBottom":"24px"}),
        html.Button(id="etud-btn-dl-fiche", style={"display":"none"}, n_clicks=0),

        html.Div(className="sga-card", style={"padding":"0"}, children=[
            html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center","padding":"18px 20px 14px"}, children=[
                html.Div("Liste des étudiants", className="sga-card-title",
                         style={"marginBottom":"0","borderBottom":"none","paddingBottom":"0"}),
                dcc.Input(id="e-search", type="text", placeholder="Rechercher...",
                          className="sga-input", style={"width":"220px","marginBottom":"0"}),
            ]),
            html.Div(id="e-list", children=_build_list()),
        ]),
    ])


@callback(Output("etud-fiche-store","data"),
          Input({"type":"etud-fiche-btn","index":ALL},"n_clicks"),
          prevent_initial_call=True)
def cap_fiche(clicks):
    if not any(n for n in clicks if n): return no_update
    t = ctx.triggered_id
    return t["index"] if isinstance(t, dict) else no_update


@callback(Output("etud-del-store","data"),
          Input({"type":"etud-del-btn","index":ALL},"n_clicks"),
          prevent_initial_call=True)
def cap_del(clicks):
    if not any(n for n in clicks if n): return no_update
    t = ctx.triggered_id
    return t["index"] if isinstance(t, dict) else no_update


@callback(Output("e-fiche","children"),
          Input("etud-fiche-store","data"),
          prevent_initial_call=True)
def show_fiche(stud_id):
    if not stud_id: return ""
    db = get_db()
    s  = db.query(Student).filter(Student.id==stud_id).first()
    if not s: db.close(); return ""
    grades       = s.grades
    nb_abs       = len(s.attendances)
    total_sess   = db.query(Session).count()
    moy          = (sum(g.note*g.coefficient for g in grades)/sum(g.coefficient for g in grades)) if grades else None
    taux         = round(nb_abs/total_sess*100) if total_sess else 0
    g_rows       = [(g.course_code, g.course.libelle if g.course else "",
                     g.note, g.coefficient, g.type_eval) for g in grades]
    dob_str      = s.date_naissance.strftime("%d/%m/%Y") if s.date_naissance else "—"
    niveau_label = {1:"1ère année",2:"2e année",3:"3e année",4:"4e année"}.get(s.annee,f"{s.annee}e année")
    db.close()
    mc      = C["success"] if (moy and moy>=12) else C["warning"] if (moy and moy>=8) else C["danger"]
    ac      = C["danger"] if taux>20 else C["warning"] if taux>10 else C["success"]
    mention = ("Très Bien" if moy and moy>=16 else "Bien" if moy and moy>=14
               else "Assez Bien" if moy and moy>=12 else "Passable" if moy and moy>=10
               else "Insuffisant") if moy else "—"
    return html.Div(style={"display":"flex","justifyContent":"center"}, children=[
        html.Div(style={"width":"100%","maxWidth":"720px"}, children=[
            html.Div(className="sga-card", style={"borderTop":f"3px solid {C['or']}"}, children=[
                html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"flex-start","marginBottom":"18px"}, children=[
                    html.Div([
                        html.Div(f"{s.prenom} {s.nom}", style={"fontFamily":"'Merriweather',serif",
                                                                 "fontSize":"20px","fontWeight":"800","color":C["bleu3"]}),
                        html.Div(f"{s.filiere} — {niveau_label}", style={"color":C["or"],"fontWeight":"700","fontSize":"13px","marginTop":"2px"}),
                    ]),
                    html.Button("Télécharger la fiche PDF", id="etud-btn-dl-fiche", className="btn-or",
                                style={"fontSize":"12px","padding":"9px 14px"}),
                ]),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"10px","marginBottom":"18px",
                                "background":C["bleu_pale"],"borderRadius":"10px","padding":"14px"}, children=[
                    _info_item("Email",          s.email),
                    _info_item("Date de naissance", dob_str),
                    _info_item("Filière",        s.filiere or "—"),
                    _info_item("Niveau",         niveau_label),
                ]),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"12px","marginBottom":"18px"}, children=[
                    _stat_card("Moyenne",      f"{moy:.2f}/20" if moy else "—", mc, mention),
                    _stat_card("Absentéisme",  f"{taux}%",     ac, f"{nb_abs} abs."),
                    _stat_card("Matières",     str(len(g_rows)), C["bleu"], "évaluées"),
                ]),
                html.Div("Détail des notes", className="sga-card-title", style={"fontSize":"14px"}),
                html.Table(className="sga-table", children=[
                    html.Thead(html.Tr([html.Th("Code"),html.Th("Matière"),html.Th("Note"),html.Th("Coeff."),html.Th("Type")])),
                    html.Tbody([html.Tr([
                        html.Td(code, style={"fontWeight":"800","color":C["bleu"]}),
                        html.Td(lib,  style={"fontSize":"13px"}),
                        html.Td(html.Span(f"{note}/20", style={
                            "background":f"{C['success'] if note>=12 else C['warning'] if note>=8 else C['danger']}22",
                            "color":C['success'] if note>=12 else C['warning'] if note>=8 else C['danger'],
                            "padding":"2px 10px","borderRadius":"20px","fontSize":"12px","fontWeight":"700"})),
                        html.Td(f"x{coef}"), html.Td(typ or "—", style={"color":C["muted"],"fontSize":"12px"}),
                    ]) for code,lib,note,coef,typ in g_rows])
                    if g_rows else html.Tbody([html.Tr([html.Td("Aucune note",colSpan=5,
                                                               style={"textAlign":"center","color":C["muted"]})])]),
                ]),
            ]),
        ]),
    ])


@callback(Output("etud-dl-fiche","data"),
          Input("etud-btn-dl-fiche","n_clicks"),
          State("etud-fiche-store","data"),
          prevent_initial_call=True)
def dl_fiche(n, stud_id):
    if not n or not stud_id: return no_update
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.units import cm
        from datetime import datetime
        db         = get_db()
        s          = db.query(Student).filter(Student.id==stud_id).first()
        if not s: db.close(); return no_update
        grades     = s.grades
        nb_abs     = len(s.attendances)
        total_sess = db.query(Session).count()
        moy        = (sum(g.note*g.coefficient for g in grades)/sum(g.coefficient for g in grades)) if grades else None
        taux       = round(nb_abs/total_sess*100) if total_sess else 0
        g_data     = [(g.course_code, g.course.libelle if g.course else "",
                       g.note, g.coefficient, g.type_eval) for g in grades]
        dob_str    = s.date_naissance.strftime("%d/%m/%Y") if s.date_naissance else "—"
        niveau     = {1:"1ère année",2:"2e année",3:"3e année",4:"4e année"}.get(s.annee,f"{s.annee}e an.")
        mention    = ("Très Bien" if moy and moy>=16 else "Bien" if moy and moy>=14
                      else "Assez Bien" if moy and moy>=12 else "Passable" if moy and moy>=10
                      else "Insuffisant") if moy else "—"
        db.close()
        BLU = colors.HexColor("#0D47A1"); SKY = colors.HexColor("#42A5F5")
        OR  = colors.HexColor("#F9A825"); CRM = colors.HexColor("#F0F7FF")
        MUT = colors.HexColor("#607D8B"); GRN = colors.HexColor("#2E7D32")
        RED = colors.HexColor("#C62828")
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf,pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
        def ps(nm,**kw): return ParagraphStyle(nm,**kw)
        story = [
            Paragraph("ENSAE Dakar", ps("h",fontName="Helvetica-Bold",fontSize=22,textColor=BLU,spaceAfter=2)),
            Paragraph("Fiche Individuelle de l'Étudiant",
                       ps("s",fontName="Helvetica",fontSize=13,textColor=MUT,spaceAfter=2)),
            Paragraph(f"Générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                       ps("d",fontName="Helvetica",fontSize=9,textColor=MUT,spaceAfter=4)),
            HRFlowable(width="100%",thickness=2,color=OR), Spacer(1,0.3*cm),
        ]
        id_data = [["Nom & Prénom",f"{s.prenom} {s.nom}","Filière",s.filiere or "—"],
                   ["Email",s.email,"Niveau",niveau],
                   ["Date de naissance",dob_str,"N° Étudiant",str(s.id)]]
        it = Table(id_data,colWidths=[3.5*cm,5.5*cm,3*cm,4.5*cm])
        it.setStyle(TableStyle([
            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,-1),9),("TEXTCOLOR",(0,0),(0,-1),BLU),("TEXTCOLOR",(2,0),(2,-1),BLU),
            ("BACKGROUND",(0,0),(-1,-1),CRM),
            ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#CFE2F3")),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        story += [it, Spacer(1,0.35*cm)]
        moy_c = GRN if (moy and moy>=12) else colors.HexColor("#E65100") if (moy and moy>=8) else RED
        syn = [["Moyenne","Absentéisme","Mention"],
               [f"{moy:.2f}/20" if moy else "—", f"{taux}% ({nb_abs} abs.)", mention]]
        st = Table(syn,colWidths=[5.5*cm,5.5*cm,5.5*cm])
        st.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),BLU),("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),9),
            ("BACKGROUND",(0,1),(-1,-1),CRM),
            ("TEXTCOLOR",(0,1),(0,1),moy_c),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,1),(-1,-1),13),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#CFE2F3")),
        ]))
        story += [st, Spacer(1,0.35*cm),
                  Paragraph("Détail des notes", ps("th",fontName="Helvetica-Bold",fontSize=10,textColor=BLU,spaceAfter=5))]
        if g_data:
            td = [["Code","Matière","Note /20","Coeff.","Type","Mention"]]
            for code,lib,note,coef,typ in g_data:
                m2 = "TB" if note>=16 else "B" if note>=14 else "AB" if note>=12 else "P" if note>=10 else "I"
                td.append([code,lib[:35],f"{note:.2f}",str(coef),typ or "Examen",m2])
            t2 = Table(td,colWidths=[2*cm,6*cm,2.2*cm,1.8*cm,2.8*cm,1.8*cm])
            t2.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),BLU),("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),9),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[CRM,colors.white]),
                ("FONTSIZE",(0,1),(-1,-1),9),
                ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#CFE2F3")),
                ("ALIGN",(2,0),(5,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ]))
            story.append(t2)
        story += [Spacer(1,0.5*cm),HRFlowable(width="100%",thickness=1,color=colors.HexColor("#CFE2F3")),
                  Paragraph("Gilbert OUMSAORE & Josée JEAZE — ENSAE Dakar — Data Visualisation 2025-2026",
                             ps("f",fontName="Helvetica",fontSize=8,textColor=MUT,spaceBefore=4))]
        doc.build(story); buf.seek(0)
        fname = f"fiche_{s.nom}_{s.prenom}_{datetime.now().strftime('%Y%m%d')}.pdf"
        return dcc.send_bytes(buf.read(), filename=fname)
    except Exception as e:
        print(f"[Fiche PDF] {e}"); return no_update


@callback(
    Output("e-list",              "children"),
    Output("e-feedback",          "children"),
    Output("etud-modal-overlay",  "style"),
    Output("etud-modal-label",    "children"),
    Output("etud-pending-delete", "data"),
    Input("e-btn-save",           "n_clicks"),
    Input("e-search",             "value"),
    Input("etud-del-store",       "data"),
    Input("etud-confirm-ok",      "n_clicks"),
    Input("etud-confirm-cancel",  "n_clicks"),
    State("e-nom","value"), State("e-prenom","value"),
    State("e-email","value"), State("e-filiere","value"),
    State("e-annee","value"), State("e-dob","date"),
    State("etud-pending-delete","data"),
    prevent_initial_call=True,
)
def handle_etud(n_save, search, del_id, n_ok, n_cancel,
                nom, prenom, email, filiere, annee, dob, pending):
    t    = ctx.triggered_id
    SHOW = {"display":"block"}
    HIDE = {"display":"none"}

    if t == "etud-del-store" and del_id:
        db = get_db()
        s  = db.query(Student).filter(Student.id==del_id).first()
        nc = f"{s.prenom} {s.nom}" if s else str(del_id)
        db.close()
        return no_update, no_update, SHOW, nc, del_id

    if t == "etud-confirm-cancel":
        return (no_update,
                html.Div("Suppression annulée.", className="alert-sga",
                         style={"background":"#E3F2FD","color":C["bleu"],"borderLeftColor":C["bleu"]}),
                HIDE, "", None)

    if t == "etud-confirm-ok" and pending:
        db = get_db()
        s  = db.query(Student).filter(Student.id==pending).first()
        if s: db.delete(s); db.commit()
        db.close()
        return (_build_list(search),
                html.Div("Étudiant supprimé.", className="alert-sga",
                         style={"background":C["orange_clair"],"color":C["warning"],"borderLeftColor":C["warning"]}),
                HIDE, "", None)

    if t == "e-search":
        return _build_list(search), no_update, no_update, no_update, no_update

    if t == "e-btn-save" and n_save:
        if not nom or not prenom or not email:
            return (no_update,
                    html.Div("Nom, prénom et email sont requis.", className="alert-sga",
                             style={"background":C["rouge_clair"],"color":C["danger"],"borderLeftColor":C["danger"]}),
                    HIDE, "", no_update)
        db = get_db()
        if db.query(Student).filter(Student.email==email).first():
            db.close()
            return (no_update,
                    html.Div("Cet email est déjà utilisé.", className="alert-sga",
                             style={"background":C["rouge_clair"],"color":C["danger"],"borderLeftColor":C["danger"]}),
                    HIDE, "", no_update)
        from datetime import datetime as dt2
        dob_d = None
        if dob:
            try: dob_d = dt2.strptime(dob[:10],"%Y-%m-%d").date()
            except: pass
        db.add(Student(nom=nom.strip(),prenom=prenom.strip(),email=email.strip(),
                       filiere=filiere or "Statistique",annee=annee or 3,date_naissance=dob_d))
        db.commit(); db.close()
        return (_build_list(),
                html.Div(f"{prenom} {nom} inscrit(e).", className="alert-sga",
                         style={"background":C["vert_clair"],"color":C["success"],"borderLeftColor":C["success"]}),
                HIDE, "", None)

    return _build_list(search), no_update, no_update, no_update, no_update

@callback(Output("etud-btn-dl-fiche","n_clicks"),
          Input("etud-btn-dl-fiche-dyn","n_clicks"),
          prevent_initial_call=True)
def relay_dl(n):
    if n: return n
    return no_update

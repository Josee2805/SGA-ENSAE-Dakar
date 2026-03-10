"""
utils/migration.py — Module 0
seed_demo_data()     : peuple la base si vide
migrate_from_excel() : import robuste — met a jour si existe, tolerant aux noms de colonnes
"""
import random
import pandas as pd
from datetime import date, timedelta
from models.database import get_db, Student, Course, Session, Attendance, Grade


def seed_demo_data():
    db = get_db()
    try:
        if db.query(Student).count() > 0:
            db.close(); return
        etudiants = [
            Student(nom="Diallo",    prenom="Aminata",   email="a.diallo@ensae.fr",    filiere="Statistique", annee=3, date_naissance=date(2001, 3,14)),
            Student(nom="Mbaye",     prenom="Cheikh",    email="c.mbaye@ensae.fr",     filiere="Statistique", annee=3, date_naissance=date(2001, 7,22)),
            Student(nom="Traore",    prenom="Fatoumata", email="f.traore@ensae.fr",    filiere="Economie",    annee=3, date_naissance=date(2002, 1, 5)),
            Student(nom="Kouassi",   prenom="Emmanuel",  email="e.kouassi@ensae.fr",   filiere="Statistique", annee=3, date_naissance=date(2001,11,30)),
            Student(nom="Ndiaye",    prenom="Rokhaya",   email="r.ndiaye@ensae.fr",    filiere="Actuariat",   annee=3, date_naissance=date(2001, 9,18)),
            Student(nom="Bah",       prenom="Ibrahim",   email="i.bah@ensae.fr",       filiere="Statistique", annee=3, date_naissance=date(2001, 6, 7)),
            Student(nom="Sarr",      prenom="Mariama",   email="m.sarr@ensae.fr",      filiere="Economie",    annee=3, date_naissance=date(2002, 4,25)),
            Student(nom="Coulibaly", prenom="Seydou",    email="s.coulibaly@ensae.fr", filiere="Actuariat",   annee=3, date_naissance=date(2001,12, 3)),
            Student(nom="Camara",    prenom="Aissatou",  email="a.camara@ensae.fr",    filiere="Statistique", annee=3, date_naissance=date(2002, 8,17)),
            Student(nom="Sow",       prenom="Moussa",    email="m.sow@ensae.fr",       filiere="Economie",    annee=3, date_naissance=date(2001, 5,29)),
        ]
        db.add_all(etudiants); db.commit()
        cours = [
            Course(code="STAT301",  libelle="Statistiques et Probabilites",  volume_total=40, enseignant="Prof. Bertrand",  description="Loi normale, tests, regression"),
            Course(code="DATAV201", libelle="Visualisation de Donnees",       volume_total=30, enseignant="Prof. Leconte",   description="Plotly, Dash, dataviz avancee"),
            Course(code="ECON401",  libelle="Econometrie Appliquee",          volume_total=35, enseignant="Prof. Moreau",    description="MCO, panel, variables instrumentales"),
            Course(code="PROG301",  libelle="Programmation Python Avancee",   volume_total=25, enseignant="Prof. Girard",    description="POO, pandas, optimisation"),
            Course(code="ACTU201",  libelle="Mathematiques Actuarielles",     volume_total=30, enseignant="Prof. Renault",   description="Calcul de primes, reserves"),
        ]
        db.add_all(cours); db.commit()
        themes_map = {
            "STAT301":  ["Intro probabilites","Loi normale","Test Student","Chi-deux","Regression lineaire","Regression multiple","Series chrono","Bootstrap"],
            "DATAV201": ["Plotly Express","Graphiques GO","Architecture Dash","Callbacks","Cartes","Dashboard complet","Export PDF"],
            "ECON401":  ["MCO fondements","Heteroscedasticite","Autocorrelation","Donnees de panel","Variables instrumentales","Probit Logit"],
            "PROG301":  ["POO avancee","Decorateurs","Pandas avance","NumPy vectorise","FastAPI","Tests pytest"],
            "ACTU201":  ["Vie entiere","Tables mortalite","Calcul primes","Reserves","Rentes viageres"],
        }
        random.seed(42); salles = ["Amphi A","Amphi B","Salle 201","Salle 305","Salle C"]
        base = date(2025, 9, 1); toutes_sessions = []; sem = 0
        for code, tlist in themes_map.items():
            for i, theme in enumerate(tlist):
                toutes_sessions.append(Session(course_code=code,
                    date=base+timedelta(weeks=sem, days=i%5),
                    duree=1.5, theme=theme, salle=random.choice(salles)))
            sem += 2
        db.add_all(toutes_sessions); db.commit()
        sess_ids = [s.id for s in db.query(Session).all()[:15]]
        stud_ids = [s.id for s in db.query(Student).all()]
        for sid in sess_ids:
            for stid in random.sample(stud_ids, k=random.randint(0,2)):
                db.merge(Attendance(id_session=sid, id_student=stid))
        db.commit()
        for s in db.query(Student).all():
            for c in db.query(Course).all():
                note = round(max(0.0,min(20.0,random.gauss(13,3))),2)
                db.add(Grade(id_student=s.id, course_code=c.code, note=note,
                             coefficient=random.choice([1.0,1.5,2.0]), type_eval="Examen"))
        db.commit()
        print("[SGA] Donnees de demonstration inserees.")
    except Exception as e:
        db.rollback(); print(f"[SGA] Erreur seed: {e}")
    finally:
        db.close()


# ─── Helpers colonnes ─────────────────────────────────────────────────────────

def _col(df, *candidates):
    """Retourne le vrai nom de la 1ere colonne trouvee (insensible casse/accents)."""
    import unicodedata
    def norm(s):
        s = s.lower().strip()
        return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
    cols = {norm(c): c for c in df.columns}
    for cand in candidates:
        real = cols.get(norm(cand))
        if real: return real
    return None

def _val(row, col, default=""):
    if col is None: return default
    v = row.get(col, default)
    try:
        if pd.isna(v): return default
    except: pass
    s = str(v).strip()
    return default if s.lower() in ("nan","none","") else s

def _fval(row, col, default=None):
    if col is None: return default
    try:
        f = float(row.get(col, default))
        return None if pd.isna(f) else f
    except: return default


# ─── Migration principale ─────────────────────────────────────────────────────

def migrate_from_excel(excel_source) -> dict:
    """
    Importe depuis Excel (chemin str ou BytesIO).
    Noms de feuilles acceptes : Students/Etudiants, Courses/Cours, Sessions/Seances, Grades/Notes.
    Noms de colonnes : insensibles a la casse et aux accents.
    Comportement : INSERT si nouveau, UPDATE si existe deja.
    """
    db = get_db(); log = {}; warnings = []
    try:
        xl     = pd.ExcelFile(excel_source)
        sheets = {s.lower().strip(): s for s in xl.sheet_names}
        print(f"[Migration] Feuilles : {list(xl.sheet_names)}")

        # ── helper pour trouver la bonne feuille ──────────────────────────
        def get_sheet(*names):
            for n in names:
                if n.lower() in sheets:
                    return xl.sheet_names[list(sheets.keys()).index(n.lower())]
            return None

        # ══ STUDENTS ══════════════════════════════════════════════════════
        sname = get_sheet("students","etudiants","etudiant","student","eleves","élèves")
        if sname:
            df = pd.read_excel(xl, sname)
            df.columns = [str(c).strip() for c in df.columns]
            print(f"[Migration] {sname} colonnes: {list(df.columns)}")
            c_nom    = _col(df,"nom","name","last_name","lastname","surname","noms")
            c_prenom = _col(df,"prenom","prénom","firstname","first_name","given_name","prenoms","prénoms")
            c_email  = _col(df,"email","mail","courriel","e-mail","adresse_email","adresse_mail")
            c_fil    = _col(df,"filiere","filière","program","programme","departement","dept","section")
            c_ann    = _col(df,"annee","année","year","niveau","level","promotion","classe")
            c_dob    = _col(df,"date_naissance","dob","birthdate","naissance","date_naiss","nee_le","né_le")
            cnt = 0
            for _, row in df.iterrows():
                try:
                    nom    = _val(row, c_nom, "")
                    prenom = _val(row, c_prenom, "")
                    email  = _val(row, c_email, "")
                    if not email and nom:
                        email = f"{(prenom[:1] or 'x').lower()}.{nom.lower().replace(' ','_')}@ensae.fr"
                    if not email: warnings.append(f"{sname}: ligne sans email ignoree"); continue
                    fil = _val(row, c_fil, "Statistique")
                    ann = int(_fval(row, c_ann, 3) or 3)
                    dob = None
                    if c_dob:
                        try: dob = pd.to_datetime(row.get(c_dob)).date()
                        except: pass
                    ex = db.query(Student).filter(Student.email==email).first()
                    if ex:
                        if nom:    ex.nom=nom
                        if prenom: ex.prenom=prenom
                        ex.filiere=fil; ex.annee=ann
                        if dob:    ex.date_naissance=dob
                    else:
                        db.add(Student(nom=nom or "?", prenom=prenom or "?",
                                       email=email, filiere=fil, annee=ann, date_naissance=dob))
                    cnt += 1
                except Exception as e: warnings.append(f"{sname} ligne: {e}")
            db.commit(); log["Students"] = cnt

        # ══ COURSES ═══════════════════════════════════════════════════════
        cname = get_sheet("courses","cours","course","matieres","matières","ues","ue","unites")
        if cname:
            df = pd.read_excel(xl, cname)
            df.columns = [str(c).strip() for c in df.columns]
            print(f"[Migration] {cname} colonnes: {list(df.columns)}")
            c_code = _col(df,"code","code_cours","course_code","id","ue","code_ue","identifiant")
            c_lib  = _col(df,"libelle","libellé","titre","title","name","nom","intitule","intitulé","designation")
            c_vol  = _col(df,"volume_total","volume","heures","hours","vh","volume_horaire","nb_heures","duree_totale")
            c_ens  = _col(df,"enseignant","enseignants","teacher","prof","professeur","instructor","intervenant")
            c_desc = _col(df,"description","desc","objectifs","contenu","content","programme","syllabus")
            cnt = 0
            for _, row in df.iterrows():
                try:
                    code = _val(row, c_code, "").upper()
                    if not code: warnings.append(f"{cname}: code manquant"); continue
                    lib  = _val(row, c_lib, code)
                    vol  = int(_fval(row, c_vol, 0) or 0)
                    ens  = _val(row, c_ens, "")
                    desc = _val(row, c_desc, "")
                    ex   = db.query(Course).filter(Course.code==code).first()
                    if ex:
                        ex.libelle=lib; ex.volume_total=vol
                        if ens:  ex.enseignant=ens
                        if desc: ex.description=desc
                    else:
                        db.add(Course(code=code,libelle=lib,volume_total=vol,
                                      enseignant=ens,description=desc))
                    cnt += 1
                except Exception as e: warnings.append(f"{cname} ligne: {e}")
            db.commit(); log["Courses"] = cnt

        # ══ SESSIONS ══════════════════════════════════════════════════════
        sname2 = get_sheet("sessions","seances","séances","session","seance","séance","cours_effectues")
        if sname2:
            df = pd.read_excel(xl, sname2)
            df.columns = [str(c).strip() for c in df.columns]
            print(f"[Migration] {sname2} colonnes: {list(df.columns)}")
            c_code  = _col(df,"course_code","code_cours","code","cours","ue","code_ue","matiere","matière")
            c_date  = _col(df,"date","date_seance","jour","day","date_cours")
            c_dur   = _col(df,"duree","durée","duration","heures","hours","volume","nb_heures","heure")
            c_theme = _col(df,"theme","thème","sujet","topic","intitule","intitulé","titre","contenu")
            c_salle = _col(df,"salle","room","amphi","lieu","location","local")
            codes_valides = {c.code for c in db.query(Course).all()}
            cnt = 0
            for _, row in df.iterrows():
                try:
                    code = _val(row, c_code, "").upper()
                    # si pas reconnu comme code, cherche dans les libelles
                    if code and code not in codes_valides:
                        match = db.query(Course).filter(Course.libelle.ilike(f"%{code}%")).first()
                        if match: code = match.code
                    if not code or code not in codes_valides:
                        warnings.append(f"{sname2}: cours '{code}' inconnu"); continue
                    d = date.today()
                    if c_date:
                        try: d = pd.to_datetime(row.get(c_date)).date()
                        except: pass
                    db.add(Session(
                        course_code=code, date=d,
                        duree=float(_fval(row,c_dur,1.5) or 1.5),
                        theme=_val(row,c_theme,""),
                        salle=_val(row,c_salle,""),
                    ))
                    cnt += 1
                except Exception as e: warnings.append(f"{sname2} ligne: {e}")
            db.commit(); log["Sessions"] = cnt

        # ══ GRADES ════════════════════════════════════════════════════════
        gname = get_sheet("grades","notes","note","grade","evaluations","resultats","résultats","eval")
        if gname:
            df = pd.read_excel(xl, gname)
            df.columns = [str(c).strip() for c in df.columns]
            print(f"[Migration] {gname} colonnes: {list(df.columns)}")
            c_sid    = _col(df,"id_student","student_id","etudiant_id","id_etudiant","id","etudiant","num_etudiant")
            c_email  = _col(df,"email","mail","courriel","adresse_email")
            c_nom    = _col(df,"nom","name","last_name","lastname")
            c_prenom = _col(df,"prenom","prénom","firstname","first_name")
            c_code   = _col(df,"course_code","code_cours","code","ue","cours","matiere","matière")
            c_note   = _col(df,"note","grade","score","note_finale","resultat","résultat","valeur")
            c_coef   = _col(df,"coefficient","coef","coeff","poids","weight","credit","credits")
            c_type   = _col(df,"type_eval","type","evaluation","type_evaluation","categorie","catégorie")
            if not c_note:
                warnings.append(f"{gname}: colonne 'note' introuvable — colonnes: {list(df.columns)}")
                log["Grades"] = 0
            else:
                # index rapide email→id et (nom,prenom)→id
                all_st      = db.query(Student).all()
                email_to_id = {s.email.lower(): s.id for s in all_st}
                nom_to_id   = {(s.nom.lower(), s.prenom.lower()): s.id for s in all_st}
                nom_seul    = {s.nom.lower(): s.id for s in all_st}
                codes_valides = {c.code for c in db.query(Course).all()}
                cnt = 0
                for _, row in df.iterrows():
                    try:
                        note_val = _fval(row, c_note)
                        if note_val is None: continue

                        # ── trouver etudiant ──────────────────────────────
                        sid = None
                        if c_sid:
                            raw = _fval(row, c_sid)
                            if raw is not None:
                                try: sid = int(raw)
                                except: pass
                        if sid is None and c_email:
                            sid = email_to_id.get(_val(row,c_email,"").lower())
                        if sid is None and c_nom:
                            n = _val(row,c_nom,"").lower()
                            p = _val(row,c_prenom,"").lower() if c_prenom else ""
                            sid = nom_to_id.get((n,p)) or nom_seul.get(n)
                        if sid is None:
                            warnings.append(f"{gname}: etudiant non identifie"); continue

                        # ── trouver cours ─────────────────────────────────
                        code = _val(row,c_code,"").upper()
                        if code and code not in codes_valides:
                            match = db.query(Course).filter(Course.libelle.ilike(f"%{code}%")).first()
                            if match: code = match.code
                        if not code or code not in codes_valides:
                            warnings.append(f"{gname}: cours '{code}' inconnu"); continue

                        coef    = float(_fval(row,c_coef,1.0) or 1.0)
                        type_ev = _val(row,c_type,"Examen")
                        ex = db.query(Grade).filter(Grade.id_student==sid, Grade.course_code==code).first()
                        if ex:
                            ex.note=float(note_val); ex.coefficient=coef; ex.type_eval=type_ev
                        else:
                            db.add(Grade(id_student=sid, course_code=code,
                                         note=float(note_val), coefficient=coef, type_eval=type_ev))
                        cnt += 1
                    except Exception as e: warnings.append(f"{gname} ligne: {e}")
                db.commit(); log["Grades"] = cnt

        if warnings:
            log["avertissements"] = len(warnings)
            log["_warnings"]      = warnings[:15]
        return log

    except Exception as e:
        db.rollback(); return {"erreur": str(e)}
    finally:
        db.close()

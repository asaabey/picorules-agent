#!/usr/bin/env python3
"""Build a clinician-facing PowerPoint deck for cd_cvra_recom_v2.

Uses native python-pptx shapes (boxes + connectors) so clinicians can edit
wording during the talk. Speaker notes carry the underlying rule mapping.

Run from anywhere:
    python3 picorules-agent/scripts/build_cvra_recom_v2_pptx.py
Output: picorules-agent/new_rules/cd_cvra_recom_v2.pptx
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN

OUT = Path(__file__).resolve().parents[1] / "new_rules" / "cd_cvra_recom_v2.pptx"

# 16:9 widescreen
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Palette — calm clinical
C_BG       = RGBColor(0xF7, 0xF9, 0xFC)
C_TITLE    = RGBColor(0x12, 0x2C, 0x4F)
C_INPUT    = RGBColor(0xE3, 0xEC, 0xF7)
C_DECISION = RGBColor(0xFF, 0xF1, 0xD6)
C_ACTION   = RGBColor(0xD8, 0xEC, 0xD8)
C_STOP     = RGBColor(0xF1, 0xD8, 0xD8)
C_BORDER   = RGBColor(0x33, 0x47, 0x66)
C_TEXT     = RGBColor(0x1A, 0x1A, 0x1A)
C_MUTED    = RGBColor(0x55, 0x66, 0x77)


def new_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank layout


def add_title_bar(slide, title: str, subtitle: str = ""):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(0.9)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TITLE
    bar.line.fill.background()
    tf = bar.text_frame
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.15)
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = RGBColor(0xCF, 0xDB, 0xEC)


def add_box(slide, x, y, w, h, text, fill, *, bold=False, font_size=12):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = C_BORDER
    shp.line.width = Pt(0.75)
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = C_TEXT
    return shp


def add_diamond(slide, x, y, w, h, text):
    shp = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = C_DECISION
    shp.line.color.rgb = C_BORDER
    shp.line.width = Pt(0.75)
    tf = shp.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEXT
    return shp


def connect(slide, src, dst, label: str | None = None):
    conn = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        src.left + src.width // 2,
        src.top + src.height,
        dst.left + dst.width // 2,
        dst.top,
    )
    conn.line.color.rgb = C_BORDER
    conn.line.width = Pt(1.25)
    if label:
        # Small label box near midpoint
        mx = (src.left + dst.left + src.width // 2) // 2
        my = (src.top + src.height + dst.top) // 2 - Inches(0.12)
        tb = slide.shapes.add_textbox(mx, my, Inches(0.6), Inches(0.25))
        tb.text_frame.paragraphs[0].text = label
        tb.text_frame.paragraphs[0].font.size = Pt(9)
        tb.text_frame.paragraphs[0].font.color.rgb = C_MUTED
        tb.text_frame.paragraphs[0].font.bold = True


def connect_lr(slide, src, dst, label: str | None = None):
    conn = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        src.left + src.width,
        src.top + src.height // 2,
        dst.left,
        dst.top + dst.height // 2,
    )
    conn.line.color.rgb = C_BORDER
    conn.line.width = Pt(1.25)
    if label:
        mx = (src.left + src.width + dst.left) // 2 - Inches(0.2)
        my = (src.top + dst.top + src.height // 2) // 2 - Inches(0.18)
        tb = slide.shapes.add_textbox(mx, my, Inches(0.6), Inches(0.25))
        tb.text_frame.paragraphs[0].text = label
        tb.text_frame.paragraphs[0].font.size = Pt(9)
        tb.text_frame.paragraphs[0].font.color.rgb = C_MUTED
        tb.text_frame.paragraphs[0].font.bold = True


def add_notes(slide, text: str):
    slide.notes_slide.notes_text_frame.text = text


def add_footer(slide, text: str):
    tb = slide.shapes.add_textbox(
        Inches(0.3), SLIDE_H - Inches(0.35), SLIDE_W - Inches(0.6), Inches(0.3)
    )
    p = tb.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = C_MUTED


# Master reference catalogue — single source of truth, edit once.
REFS = {
    "AU2023":   ("AU 2023 CVD Risk Guideline (cvdcheck.org.au)",
                 "https://www.cvdcheck.org.au/"),
    "AUHF":     ("Heart Foundation AU — CVD management",
                 "https://www.heartfoundation.org.au/for-professionals/guideline-for-managing-cvd"),
    "ESC2019":  ("ESC/EAS 2019 dyslipidaemia (DOI: 10.1093/eurheartj/ehz455)",
                 "https://doi.org/10.1093/eurheartj/ehz455"),
    "ESC2025":  ("ESC/EAS 2025 focused update (DOI: 10.1093/eurheartj/ehaf190)",
                 "https://doi.org/10.1093/eurheartj/ehaf190"),
    "AHA2025":  ("AHA/ACC 2025 BP guideline (DOI: 10.1161/CIR.0000000000001356)",
                 "https://doi.org/10.1161/CIR.0000000000001356"),
    "ACCportal":("ACC/AHA guidelines portal",
                 "https://www.acc.org/guidelines"),
    "KDIGO2024":("KDIGO 2024 CKD evaluation & management",
                 "https://kdigo.org/guidelines/ckd-evaluation-and-management/"),
}


def add_references(slide, ref_keys, *, x=None, y=None, w=None, h=None,
                   title="References"):
    """Add a hyperlinked references panel. Defaults to bottom-strip placement."""
    if x is None:
        x = Inches(0.3)
    if y is None:
        y = SLIDE_H - Inches(0.05) - Inches(0.22) * (len(ref_keys) + 1)
    if w is None:
        w = SLIDE_W - Inches(0.6)
    if h is None:
        h = Inches(0.22) * (len(ref_keys) + 1) + Inches(0.05)

    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = C_TITLE

    for key in ref_keys:
        label, url = REFS[key]
        p = tf.add_paragraph()
        run = p.add_run()
        run.text = label
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x1F, 0x4F, 0x91)
        run.hyperlink.address = url


# ---------------------------------------------------------------- slide builders

def slide_title(prs):
    s = add_blank(prs)
    # Background band
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_TITLE
    bg.line.fill.background()

    tb = s.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11), Inches(1.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "CVD Risk Management"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    p2 = tb.text_frame.add_paragraph()
    p2.text = "How our decision-support rule classifies patients and recommends therapy"
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(0xCF, 0xDB, 0xEC)

    tb2 = s.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11), Inches(0.6))
    p3 = tb2.text_frame.paragraphs[0]
    p3.text = "Aligned with 2023 AU CVD Risk Guideline · 2025 ESC/EAS · 2025 AHA/ACC BP · KDIGO 2024"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(0xCF, 0xDB, 0xEC)


def slide_overview(prs):
    s = add_blank(prs)
    add_title_bar(s, "What this rule does",
                  "Five recommendation engines driven by reconciled CVD risk")

    intro = s.shapes.add_textbox(Inches(0.5), Inches(1.1), Inches(12.3), Inches(0.9))
    p = intro.text_frame.paragraphs[0]
    p.text = ("For every patient, the rule pulls labs, prescriptions and diagnoses, "
              "reconciles them into a single CVD risk category, and then issues "
              "actionable recommendations across five clinical domains.")
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT

    # Inputs column
    add_box(s, Inches(0.5), Inches(2.4), Inches(2.6), Inches(0.55),
            "Inputs", C_TITLE, bold=True, font_size=14)
    # Force white text on dark fill
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text == "Inputs":
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    inputs = [
        "Demographics (age, sex, First Nations)",
        "Blood pressure",
        "Lipids (LDL, total chol)",
        "Diabetes status + complications",
        "Kidney function (eGFR, uACR)",
        "Established CVD",
        "Current medications",
        "Smoking status",
        "10-yr risk calculators",
    ]
    y = Inches(3.05)
    for txt in inputs:
        add_box(s, Inches(0.5), y, Inches(2.6), Inches(0.32), txt, C_INPUT, font_size=10)
        y += Inches(0.36)

    # Middle: risk reconciliation
    add_box(s, Inches(4.2), Inches(3.0), Inches(2.8), Inches(1.6),
            "Reconciled CVD risk category\n(Low / Intermediate / High)",
            C_DECISION, bold=True, font_size=14)

    # Right: engines
    add_box(s, Inches(8.4), Inches(2.4), Inches(4.5), Inches(0.55),
            "Recommendations", C_TITLE, bold=True, font_size=14)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text == "Recommendations":
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    engines = [
        "Blood pressure therapy",
        "Lipid therapy (statin → ezetimibe → PCSK9i)",
        "Antiplatelet (secondary prevention)",
        "SGLT2i / GLP-1 (T2DM + CVD or CKD)",
        "Smoking cessation",
    ]
    y = Inches(3.05)
    for txt in engines:
        add_box(s, Inches(8.4), y, Inches(4.5), Inches(0.42), txt, C_ACTION, font_size=11)
        y += Inches(0.5)

    # Arrows: inputs → middle, middle → engines
    arrow1 = s.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(3.1), Inches(3.8), Inches(4.2), Inches(3.8)
    )
    arrow1.line.color.rgb = C_BORDER
    arrow1.line.width = Pt(2)

    arrow2 = s.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(7.0), Inches(3.8), Inches(8.4), Inches(3.8)
    )
    arrow2.line.color.rgb = C_BORDER
    arrow2.line.width = Pt(2)

    add_references(s, ["AU2023", "AUHF"], title="Primary references")

    add_notes(s, (
        "Frame the talk around 5 recommendation engines. "
        "The reconciliation step is the most consequential — it determines targets "
        "(BP 120/130/140, LDL 1.8/2.0/4.9) and whether therapy is indicated at all."
    ))


def slide_risk_reconciliation(prs):
    s = add_blank(prs)
    add_title_bar(s, "How we classify CVD risk",
                  "Clinical 'auto-high' overrides take priority over calculated risk")

    intro = s.shapes.add_textbox(Inches(0.5), Inches(1.05), Inches(12.3), Inches(0.6))
    p = intro.text_frame.paragraphs[0]
    p.text = ("Patients with any of the conditions below are automatically classified "
              "as HIGH risk — independent of any 10-year calculator output.")
    p.font.size = Pt(14)
    p.font.color.rgb = C_TEXT

    # Left cascade: auto-high triggers
    triggers = [
        "Established CVD",
        "Moderate–severe CKD\n(eGFR < 45 or persistent uACR)",
        "Familial hypercholesterolaemia\n(Dutch Lipid Clinic Score ≥ probable)",
        "T2DM + end-organ damage\n(retino / neuro / foot ulcer / albuminuria)",
        "Persistent albuminuria\n(>25 M / >35 F, ≥90 days)",
    ]
    y = Inches(1.85)
    for txt in triggers:
        add_box(s, Inches(0.5), y, Inches(4.5), Inches(0.7), txt, C_STOP, font_size=12)
        y += Inches(0.78)

    # Right side: cascade outcome
    add_box(s, Inches(6.0), Inches(1.85), Inches(6.8), Inches(0.9),
            "Any of the above → HIGH RISK",
            C_STOP, bold=True, font_size=16)

    add_diamond(s, Inches(6.5), Inches(3.0), Inches(5.8), Inches(1.4),
                "First Nations\nAge 30–79\nLow or intermediate risk?")
    add_box(s, Inches(6.5), Inches(4.6), Inches(5.8), Inches(0.7),
            "Bump up one category", C_DECISION, font_size=12)

    add_box(s, Inches(6.5), Inches(5.5), Inches(5.8), Inches(0.7),
            "Otherwise: use ensemble of calculators\n(Framingham + AusCVDRisk)",
            C_INPUT, font_size=11)

    add_references(s, ["AU2023", "KDIGO2024"])
    add_notes(s, (
        "Walk through each auto-high trigger. The KDIGO row maps to ckd>=3 in the rule. "
        "The persistent albuminuria definition is sex-banded and stricter than KDIGO A2 — "
        "it requires >=2 readings spanning >=90 days."
    ))


def slide_bp(prs):
    s = add_blank(prs)
    add_title_bar(s, "Blood pressure recommendation",
                  "Initiate · Consider · Intensify · Maintain")

    # PROMINENT target table (top-right, larger) — AU 2023 aligned
    add_box(s, Inches(8.6), Inches(1.05), Inches(4.4), Inches(0.45),
            "SBP target (mmHg) — AU 2023", C_TITLE, bold=True, font_size=13)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text == "SBP target (mmHg) — AU 2023":
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break
    add_box(s, Inches(8.6), Inches(1.55), Inches(4.4), Inches(0.65),
            "Most adults   →   < 130 / 80",
            C_DECISION, bold=True, font_size=16)
    add_box(s, Inches(8.6), Inches(2.25), Inches(4.4), Inches(0.65),
            "Age ≥ 80   →   < 140",
            C_DECISION, bold=True, font_size=16)
    add_box(s, Inches(8.6), Inches(2.95), Inches(4.4), Inches(0.45),
            "(age ≥ 80 is a frailty proxy; AHA uses age 75 + frailty)",
            C_INPUT, font_size=10)

    # Override
    ovr = add_diamond(s, Inches(0.5), Inches(1.4), Inches(2.4), Inches(1.2),
                      "SBP ≥ 160\nor DBP ≥ 100?")
    ovr_init = add_box(s, Inches(3.4), Inches(1.0), Inches(2.4), Inches(0.7),
                       "Initiate BP therapy\naim for target above", C_ACTION, font_size=11)
    ovr_int = add_box(s, Inches(3.4), Inches(2.0), Inches(2.4), Inches(0.7),
                      "Intensify (already on Rx)\naim for target above", C_ACTION, font_size=11)
    connect_lr(s, ovr, ovr_init, "yes,\nno Rx")
    connect_lr(s, ovr, ovr_int, "yes,\non Rx")

    # High risk branch
    hr = add_diamond(s, Inches(0.5), Inches(3.5), Inches(2.4), Inches(1.2),
                     "High risk?")
    hr_init = add_box(s, Inches(3.4), Inches(3.2), Inches(2.4), Inches(0.6),
                      "Initiate · target <130", C_ACTION, font_size=11)
    hr_int = add_box(s, Inches(3.4), Inches(3.9), Inches(2.4), Inches(0.6),
                     "Intensify · SBP above target", C_ACTION, font_size=11)
    hr_m = add_box(s, Inches(3.4), Inches(4.6), Inches(2.4), Inches(0.6),
                   "Maintain · at target", C_ACTION, font_size=11)
    connect_lr(s, hr, hr_init, "no Rx")
    connect_lr(s, hr, hr_int)
    connect_lr(s, hr, hr_m)

    # Intermediate branch
    mr = add_diamond(s, Inches(0.5), Inches(5.5), Inches(2.4), Inches(1.2),
                     "Intermediate risk?")
    mr_con = add_box(s, Inches(3.4), Inches(5.3), Inches(2.4), Inches(0.6),
                     "Consider · target <130", C_ACTION, font_size=11)
    mr_int = add_box(s, Inches(3.4), Inches(5.95), Inches(2.4), Inches(0.6),
                     "Intensify · SBP above target", C_ACTION, font_size=11)
    mr_m = add_box(s, Inches(3.4), Inches(6.6), Inches(2.4), Inches(0.6),
                   "Maintain · at target", C_ACTION, font_size=11)
    connect_lr(s, mr, mr_con, "no Rx")
    connect_lr(s, mr, mr_int)
    connect_lr(s, mr, mr_m)

    # Otherwise
    add_box(s, Inches(8.6), Inches(3.95), Inches(4.4), Inches(0.55),
            "Low risk → Not indicated", C_INPUT, font_size=12)

    # References on right column (BP body content extends low on the left)
    add_references(s, ["AU2023", "AHA2025", "AUHF"],
                   x=Inches(8.6), y=Inches(4.7), w=Inches(4.4), h=Inches(1.4))
    add_notes(s, (
        "Frame the SBP target as the single biggest change from v1 (140→130). "
        "Two-tier target after 2026-05-19 review: <130 for most adults, <140 for "
        "age >=80 as a frailty proxy. AU 2023 verbatim is '<130/80 for most patients'. "
        "The SPRINT-derived <120 target for high-risk <65 was removed because AU 2023 "
        "does not endorse it; clinicians wanting the SPRINT pathway should set it "
        "as a deliberate individual decision. "
        "Auto-override on stage-2 HTN (SBP>=160 or DBP>=100) means we won't wait "
        "for a risk score before starting therapy."
    ))


def slide_lipid(prs):
    s = add_blank(prs)
    add_title_bar(s, "Lipid recommendation — extended ladder",
                  "Statin → Ezetimibe → Non-statin intensifier")

    # Targets
    add_box(s, Inches(8.6), Inches(1.1), Inches(4.4), Inches(1.5),
            "LDL target\n\n1.8 mmol/L  if prior CVD\n2.0 mmol/L  if high risk\n4.9 mmol/L  otherwise",
            C_INPUT, font_size=12)

    # Override
    ovr = add_diamond(s, Inches(0.5), Inches(1.4), Inches(2.4), Inches(1.2),
                      "TC ≥ 7.5 mmol/L?")
    ovr_init = add_box(s, Inches(3.4), Inches(1.0), Inches(2.4), Inches(0.7),
                       "Initiate statin", C_ACTION, font_size=12)
    ovr_int = add_box(s, Inches(3.4), Inches(2.0), Inches(2.4), Inches(0.7),
                      "Intensify (add ezetimibe)", C_ACTION, font_size=12)
    connect_lr(s, ovr, ovr_init, "yes,\nno statin")
    connect_lr(s, ovr, ovr_int, "yes,\non statin")

    # High risk ladder
    add_box(s, Inches(0.5), Inches(3.3), Inches(5.3), Inches(0.5),
            "HIGH RISK patient — climb the ladder until LDL at target",
            C_TITLE, bold=True, font_size=12)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text.startswith("HIGH RISK patient"):
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    rungs = [
        ("No lipid Rx", "Initiate statin"),
        ("On statin, LDL above target", "Add ezetimibe"),
        ("On statin + ezetimibe, LDL still above target",
         "Add bempedoic acid / PCSK9i / inclisiran"),
        ("LDL at target", "Maintain"),
    ]
    y = Inches(3.9)
    for cond, action in rungs:
        add_box(s, Inches(0.5), y, Inches(3.5), Inches(0.55), cond, C_DECISION, font_size=11)
        add_box(s, Inches(4.2), y, Inches(3.5), Inches(0.55), action, C_ACTION, font_size=11)
        arrow = s.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(4.0), y + Inches(0.27), Inches(4.2), y + Inches(0.27),
        )
        arrow.line.color.rgb = C_BORDER
        arrow.line.width = Pt(1.5)
        y += Inches(0.65)

    # Intermediate
    add_box(s, Inches(8.6), Inches(3.9), Inches(4.4), Inches(0.55),
            "INTERMEDIATE risk — no statin: Consider", C_INPUT, font_size=11)
    add_box(s, Inches(8.6), Inches(4.55), Inches(4.4), Inches(0.55),
            "INTERMEDIATE risk — on statin: Maintain", C_INPUT, font_size=11)
    add_box(s, Inches(8.6), Inches(5.2), Inches(4.4), Inches(0.55),
            "LOW risk: Not indicated", C_INPUT, font_size=11)

    add_references(s, ["AU2023", "ESC2025", "ESC2019", "ACCportal"])
    add_notes(s, (
        "Code 5 (non-statin intensifier) is new in v2. Triggers only when patient is "
        "already on max statin + ezetimibe and LDL is still above target. "
        "The bempedoic acid / PCSK9i / inclisiran bindings are TODO — currently nvl(0). "
        "ESC/EAS 2025 sets a tighter LDL target (<1.4 with >=50% reduction for secondary "
        "prevention) than the AU target shown on slide."
    ))


def slide_cardiometab(prs):
    s = add_blank(prs)
    add_title_bar(s, "SGLT2i / GLP-1 receptor agonist — new in v2",
                  "Cardio-renal protection in T2DM")

    intro = s.shapes.add_textbox(Inches(0.5), Inches(1.05), Inches(12.3), Inches(0.6))
    p = intro.text_frame.paragraphs[0]
    p.text = ("Eligible: any T2DM patient with established CVD OR moderate-severe CKD. "
              "We recommend one of these classes for cardio-renal benefit beyond glycaemic control.")
    p.font.size = Pt(14)

    elig = add_diamond(s, Inches(2.5), Inches(2.2), Inches(3.5), Inches(1.5),
                       "T2DM\nAND\n(CVD or CKD ≥ moderate)?")
    on = add_diamond(s, Inches(7.5), Inches(2.2), Inches(3.5), Inches(1.5),
                     "Already on\nSGLT2i or GLP-1?")
    arrow = s.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(6.0), Inches(2.95), Inches(7.5), Inches(2.95),
    )
    arrow.line.color.rgb = C_BORDER
    arrow.line.width = Pt(1.5)
    tb = s.shapes.add_textbox(Inches(6.2), Inches(2.65), Inches(1.3), Inches(0.3))
    tb.text_frame.paragraphs[0].text = "yes"
    tb.text_frame.paragraphs[0].font.size = Pt(10)
    tb.text_frame.paragraphs[0].font.color.rgb = C_MUTED
    tb.text_frame.paragraphs[0].font.bold = True

    init = add_box(s, Inches(7.0), Inches(4.6), Inches(4.5), Inches(0.9),
                   "Initiate SGLT2i or GLP-1 RA", C_ACTION, bold=True, font_size=14)
    maint = add_box(s, Inches(7.0), Inches(5.8), Inches(4.5), Inches(0.7),
                    "Maintain therapy", C_ACTION, font_size=13)
    notindic = add_box(s, Inches(1.5), Inches(4.6), Inches(4.5), Inches(0.9),
                       "Not indicated", C_INPUT, font_size=13)

    connect(s, elig, notindic, "no")
    connect(s, on, init, "no")
    connect(s, on, maint, "yes")

    add_references(s, ["AU2023", "ESC2025", "ACCportal", "KDIGO2024"])
    add_notes(s, (
        "Care-gap flag fires when a patient is eligible but on neither. "
        "Watch for emerging evidence on heart failure with preserved EF — likely to "
        "broaden eligibility in a future revision."
    ))


def slide_antiplatelet_smoking(prs):
    s = add_blank(prs)
    add_title_bar(s, "Antiplatelet & smoking cessation", "")

    # Antiplatelet half
    add_box(s, Inches(0.5), Inches(1.1), Inches(6.0), Inches(0.5),
            "Antiplatelet — secondary prevention only",
            C_TITLE, bold=True, font_size=13)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text.startswith("Antiplatelet —"):
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    cvd_q = add_diamond(s, Inches(0.5), Inches(1.8), Inches(2.6), Inches(1.2),
                        "Established\nCVD?")
    on_q = add_diamond(s, Inches(0.5), Inches(3.3), Inches(2.6), Inches(1.2),
                       "On antiplatelet\nor anticoag?")
    rec_init = add_box(s, Inches(3.6), Inches(3.3), Inches(2.6), Inches(0.7),
                       "Initiate antiplatelet", C_ACTION, font_size=12)
    rec_m = add_box(s, Inches(3.6), Inches(4.3), Inches(2.6), Inches(0.7),
                    "Maintain", C_ACTION, font_size=12)
    rec_z = add_box(s, Inches(3.6), Inches(1.8), Inches(2.6), Inches(0.7),
                    "Not indicated", C_INPUT, font_size=12)
    connect_lr(s, cvd_q, rec_z, "no")
    connect(s, cvd_q, on_q, "yes")
    connect_lr(s, on_q, rec_init, "no")
    connect_lr(s, on_q, rec_m, "yes")

    # Smoking half
    add_box(s, Inches(7.0), Inches(1.1), Inches(6.0), Inches(0.5),
            "Smoking cessation",
            C_TITLE, bold=True, font_size=13)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text == "Smoking cessation":
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    sm_q = add_diamond(s, Inches(7.0), Inches(1.8), Inches(2.6), Inches(1.2),
                       "Current\nsmoker?")
    rx_q = add_diamond(s, Inches(7.0), Inches(3.3), Inches(2.6), Inches(1.2),
                       "On cessation\nRx?")
    sm_off = add_box(s, Inches(10.1), Inches(3.3), Inches(2.8), Inches(0.7),
                     "Offer cessation Rx", C_ACTION, font_size=12)
    sm_keep = add_box(s, Inches(10.1), Inches(4.3), Inches(2.8), Inches(0.7),
                      "Maintain Rx", C_ACTION, font_size=12)
    ex_q = add_diamond(s, Inches(10.1), Inches(1.6), Inches(2.8), Inches(1.1),
                       "Ex-smoker?")
    sm_ex = add_box(s, Inches(10.1), Inches(2.85), Inches(2.8), Inches(0.4),
                    "Sustain abstinence", C_INPUT, font_size=11)
    connect_lr(s, sm_q, ex_q, "no")
    connect(s, ex_q, sm_ex, "yes")
    connect(s, sm_q, rx_q, "yes")
    connect_lr(s, rx_q, sm_off, "no")
    connect_lr(s, rx_q, sm_keep, "yes")

    add_references(s, ["AU2023", "AHA2025"])
    add_notes(s, (
        "Antiplatelet rule is intentionally narrow: secondary prevention only. "
        "Primary prevention with aspirin is no longer routinely recommended in any "
        "of the cited guidelines."
    ))


def slide_gaps_concordance(prs):
    s = add_blank(prs)
    add_title_bar(s, "Care gaps & guideline concordance",
                  "What the rule reports back to the clinic")

    # Care gaps column
    add_box(s, Inches(0.5), Inches(1.1), Inches(6.0), Inches(0.5),
            "Care gaps flagged (per patient)",
            C_TITLE, bold=True, font_size=13)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text.startswith("Care gaps"):
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    gaps = [
        "BP therapy not started but indicated",
        "BP above target on current Rx (needs intensify)",
        "Statin not started but indicated",
        "On statin, LDL above target, no ezetimibe",
        "On statin + ezetimibe, LDL above target",
        "SGLT2i / GLP-1 eligible but neither prescribed",
        "Smoker, no cessation Rx",
        "Antiplatelet missing in established CVD",
    ]
    y = Inches(1.85)
    for g in gaps:
        add_box(s, Inches(0.5), y, Inches(6.0), Inches(0.5), g, C_STOP, font_size=11)
        y += Inches(0.55)

    # Concordance column
    add_box(s, Inches(7.0), Inches(1.1), Inches(6.0), Inches(0.5),
            "Concordance score",
            C_TITLE, bold=True, font_size=13)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text == "Concordance score":
            shp.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            break

    add_box(s, Inches(7.0), Inches(1.85), Inches(6.0), Inches(1.1),
            "For each patient we count\n"
            "• how many domains are applicable\n"
            "• how many are at the maintain / met state",
            C_INPUT, font_size=12)

    add_box(s, Inches(7.0), Inches(3.1), Inches(6.0), Inches(1.1),
            "Concordance % = met ÷ applicable × 100",
            C_DECISION, bold=True, font_size=16)

    add_box(s, Inches(7.0), Inches(4.35), Inches(6.0), Inches(2.2),
            "Use at panel level to:\n"
            "• benchmark practices\n"
            "• track quality-improvement over time\n"
            "• prioritise high-gap patients for review\n"
            "• audit guideline uptake (statin, SGLT2i, …)",
            C_ACTION, font_size=13)

    add_references(s, ["AU2023"])
    add_notes(s, (
        "The concordance score is intentionally simple — proportion of applicable "
        "domains at the 'maintain' state. Patients with no applicable domains "
        "default to 100% so denominator effects don't penalise healthy cohorts."
    ))


def slide_close(prs):
    s = add_blank(prs)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_TITLE
    bg.line.fill.background()

    tb = s.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11), Inches(2))
    p = tb.text_frame.paragraphs[0]
    p.text = "Discussion"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    bullets = [
        "Does the LDL target ladder match local practice?",
        "Should we tighten to ESC/EAS 2025 (<1.4 secondary prevention)?",
        "Subclinical CVD inputs (CAC, NT-proBNP) — worth modelling?",
        "First Nations risk re-classification — is the current uplift appropriate?",
    ]
    tb2 = s.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11), Inches(3))
    for i, b in enumerate(bullets):
        para = tb2.text_frame.paragraphs[0] if i == 0 else tb2.text_frame.add_paragraph()
        para.text = "•  " + b
        para.font.size = Pt(20)
        para.font.color.rgb = RGBColor(0xCF, 0xDB, 0xEC)


# ---------------------------------------------------------------- main

def main():
    prs = new_deck()
    slide_title(prs)
    slide_overview(prs)
    slide_risk_reconciliation(prs)
    slide_bp(prs)
    slide_lipid(prs)
    slide_cardiometab(prs)
    slide_antiplatelet_smoking(prs)
    slide_gaps_concordance(prs)
    slide_close(prs)
    prs.save(OUT)
    print(f"wrote {OUT}  ({OUT.stat().st_size // 1024} KB, {len(prs.slides)} slides)")


if __name__ == "__main__":
    main()

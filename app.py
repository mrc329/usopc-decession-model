"""
USOPC Portfolio Investment Analytics
PE portfolio framing — NGBs as portfolio companies, medals as returns
Harris framework front and center, sports visible, archetypes as background
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pulp

st.set_page_config(
    page_title="USOPC Portfolio Analytics",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=DM+Mono:wght@300;400&display=swap');
    html, body, [class*="css"] { font-family: 'EB Garamond', Georgia, serif; background-color: #181816; color: #e4e4e0; }
    .main .block-container { padding: 2rem 3rem 3rem 3rem; max-width: 1100px; }
    h1 { font-family: 'EB Garamond', serif; font-size: 1.9rem; font-weight: 500; letter-spacing: -0.02em; border-bottom: 1px solid #e4e4e0; padding-bottom: 0.4rem; margin-bottom: 0.2rem; color: #e4e4e0; }
    h2 { font-family: 'EB Garamond', serif; font-size: 1.2rem; font-weight: 500; margin-top: 1.8rem; margin-bottom: 0.3rem; color: #e4e4e0; }
    h3 { font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 400; letter-spacing: 0.12em; text-transform: uppercase; color: #646460; margin-bottom: 0.6rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 0; border-bottom: 1px solid #303030; background: transparent; }
    .stTabs [data-baseweb="tab"] { font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: #646460; padding: 0.5rem 1.5rem; border: none; border-bottom: 2px solid transparent; background: transparent; }
    .stTabs [aria-selected="true"] { color: #e4e4e0; border-bottom: 2px solid #e4e4e0; background: transparent; }
    .kpi-row { display: flex; gap: 2.5rem; margin: 1.2rem 0 1.8rem 0; flex-wrap: wrap; }
    .kpi { border-left: 2px solid #e4e4e0; padding-left: 0.8rem; }
    .kpi-value { font-family: 'DM Mono', monospace; font-size: 1.8rem; font-weight: 300; line-height: 1; color: #e4e4e0; }
    .kpi-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase; color: #646460; margin-top: 0.2rem; }
    .kpi-sub { font-family: 'EB Garamond', serif; font-size: 0.82rem; font-style: italic; color: #484844; margin-top: 0.1rem; }
    /* Tufte: thesis border encodes the thesis type — background would be chartjunk */
    .thesis-card { background: transparent; border-left: 3px solid #e4e4e0; padding: 0.7rem 1rem; margin: 0.4rem 0; }
    .thesis-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: #646460; }
    .thesis-name { font-family: 'EB Garamond', serif; font-size: 1.05rem; font-weight: 500; color: #e4e4e0; margin: 0.15rem 0 0.1rem 0; }
    .thesis-desc { font-family: 'EB Garamond', serif; font-size: 0.88rem; font-style: italic; color: #8a8a86; line-height: 1.4; }
    /* Tufte: left border carries the structural signal; fill is noise */
    .harris-quote { border-left: 3px solid #e4e4e0; padding: 0.5rem 1rem; margin: 0.8rem 0 1.2rem 0; font-style: italic; font-size: 0.95rem; color: #8a8a86; background: transparent; line-height: 1.5; }
    /* Tufte: a decorative box around the methodology section is chartjunk — let type carry hierarchy */
    .harris-framework { background: transparent; border: none; padding: 1.2rem 0; margin: 1rem 0; line-height: 1.7; }
    .harris-framework h4 { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: #646460; margin: 0 0 0.6rem 0; }
    .harris-framework table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
    .harris-framework td { padding: 0.3rem 0.8rem 0.3rem 0; vertical-align: top; color: #8a8a86; }
    .harris-framework td:first-child { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #646460; white-space: nowrap; padding-right: 1rem; }
    .para-badge { display: inline-block; font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; background: #e4e4e0; color: #181816; padding: 0.1rem 0.4rem; margin-left: 0.4rem; vertical-align: middle; }
    .caption { font-family: 'EB Garamond', serif; font-size: 0.88rem; font-style: italic; color: #484844; margin-top: 0.3rem; line-height: 1.5; }
    hr { border: none; border-top: 1px solid #282826; margin: 1.5rem 0; }
    #MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

rcParams.update({
    'font.family': 'serif', 'font.serif': ['Georgia'], 'font.size': 9,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.spines.left': False, 'axes.spines.bottom': True,
    'axes.grid': False, 'axes.facecolor': '#181816', 'figure.facecolor': '#181816',
    'xtick.major.size': 0, 'ytick.major.size': 0,
    'xtick.color': '#646460', 'ytick.color': '#646460',
    'text.color': '#e4e4e0', 'axes.labelcolor': '#646460', 'axes.edgecolor': '#303030',
})

# ── Olympic Summer ────────────────────────────────────────────
# mean_prev = Tokyo 2021 | mean_prev2 = Rio 2016 | mean_prev3 = London 2012
# age_vs_peak = years relative to peak age (positive = past peak → wider std)
# prior_olympics = Games attended before this cycle (scales preparation gap)
SUMMER = pd.DataFrame([
    # ── Gymnastics ── All-Around only per gender. Floor and apparatus are funded through
    # the All-Around program — same athletes, same NGB investment.
    # depth=3: Biles + Jones + ascending next-gen. field_size=4: China, GB, Romania depth.
    # rival_mean=90: China/Romania at ~89-91 on current scoring. USA clearly ahead.
    # russia_rival=93: Russia has a historically deep gymnastics program; return would tighten the field.
    dict(sport='Gymnastics',    discipline='Women All-Around', thesis='Protect',  mean_pre=96.5, std_pre=3.1, mean_prev=91.2, mean_prev2=97.5, mean_prev3=95.4, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=11, sentiment=0.24, cost=1.2, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=1.00, depth=3, field_size=4,  home_boost=2.2, rival_mean=90, russia_rival=93),
    # Men's gymnastics: USA won team bronze at Paris 2024. rival_mean=87: Japan/China.
    dict(sport='Gymnastics',    discipline='Men All-Around',   thesis='Develop',  mean_pre=85.2, std_pre=5.8, mean_prev=81.4, mean_prev2=78.8, mean_prev3=76.2, age_vs_peak=-2, prior_olympics=1, first_olympics=0, win_streak=0,  sentiment=0.58, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.65, depth=2, field_size=8,  home_boost=1.8, rival_mean=87),
    # ── Track & Field ──
    # Women Sprint: Jamaica (Shericka Jackson etc.) ~82. USA and Jamaica roughly matched.
    dict(sport='Track & Field', discipline='Women Sprint',          thesis='Develop',  mean_pre=80.2, std_pre=5.4, mean_prev=71.8, mean_prev2=69.4, mean_prev3=74.2, age_vs_peak=-4, prior_olympics=0, first_olympics=1, win_streak=2,  sentiment=0.60, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.85, depth=2, field_size=10, home_boost=1.8, rival_mean=82),
    # Women Hurdles: 100mH — Jamaica/Puerto Rico ~90; 400mH — Sydney is dominant ~97.
    # Combined rival_mean=90 reflects the 400mH field without McLaughlin-Levrone.
    dict(sport='Track & Field', discipline='Women Hurdles',         thesis='Maintain', mean_pre=96.2, std_pre=2.8, mean_prev=95.4, mean_prev2=92.1, mean_prev3=89.5, age_vs_peak= 1, prior_olympics=3, first_olympics=0, win_streak=7,  sentiment=0.70, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.90, depth=3, field_size=5,  home_boost=2.0, rival_mean=90),
    # Women 400m: Marileidy Paulino (DOM) ~91 is a genuine challenger. Separate pool.
    dict(sport='Track & Field', discipline='Women 400m',            thesis='Develop',  mean_pre=83.5, std_pre=5.8, mean_prev=81.2, mean_prev2=79.5, mean_prev3=78.2, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.61, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.65, depth=2, field_size=8,  home_boost=1.6, rival_mean=88),
    # Women Middle Distance: Faith Kipyegon (KEN) ~92. USA is not the world standard here.
    dict(sport='Track & Field', discipline='Women Middle Distance',  thesis='Develop',  mean_pre=83.5, std_pre=6.2, mean_prev=85.4, mean_prev2=82.1, mean_prev3=79.5, age_vs_peak=-2, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.61, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=2, field_size=10, home_boost=1.5, rival_mean=92),
    # Women Long Distance: Kenya/Ethiopia (Kipchoge-era depth) ~94. USA is a distant contender.
    dict(sport='Track & Field', discipline='Women Long Distance',    thesis='Develop',  mean_pre=76.4, std_pre=7.1, mean_prev=74.2, mean_prev2=71.8, mean_prev3=69.5, age_vs_peak=-4, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.55, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.45, depth=1, field_size=12, home_boost=1.2, rival_mean=94),
    # Men Sprint: Jamaica/South Africa ~84. Lyles won Paris but margin is thin.
    dict(sport='Track & Field', discipline='Men Sprint',            thesis='Develop',  mean_pre=84.8, std_pre=5.9, mean_prev=79.5, mean_prev2=74.8, mean_prev3=72.5, age_vs_peak=-3, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.65, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.85, depth=2, field_size=12, home_boost=2.0, rival_mean=84),
    # Men Hurdles: Jamaica (110mH) ~86 rival_mean. USA's Holloway and Benjamin are leading.
    dict(sport='Track & Field', discipline='Men Hurdles',           thesis='Develop',  mean_pre=88.5, std_pre=4.2, mean_prev=86.8, mean_prev2=84.5, mean_prev3=82.1, age_vs_peak=-2, prior_olympics=2, first_olympics=0, win_streak=4,  sentiment=0.64, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.70, depth=2, field_size=7,  home_boost=1.8, rival_mean=86),
    # Men 400m: Botswana/Belgium/Jamaica ~86. Quincy Hall won Paris but field is close.
    dict(sport='Track & Field', discipline='Men 400m',              thesis='Develop',  mean_pre=87.2, std_pre=5.5, mean_prev=84.2, mean_prev2=78.5, mean_prev3=76.8, age_vs_peak=-3, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.63, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.70, depth=2, field_size=8,  home_boost=1.8, rival_mean=86),
    # Men Middle Distance: Kenya/Morocco/Algeria ~90. Cole Hocker won Paris in an upset.
    dict(sport='Track & Field', discipline='Men Middle Distance',    thesis='Develop',  mean_pre=85.8, std_pre=6.8, mean_prev=83.2, mean_prev2=79.8, mean_prev3=78.2, age_vs_peak=-5, prior_olympics=1, first_olympics=0, win_streak=1,  sentiment=0.63, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=2, field_size=10, home_boost=1.5, rival_mean=90),
    # Men Long Distance: Kenya/Ethiopia ~95. Grant Fisher top-5 Paris; USA not a gold threat.
    dict(sport='Track & Field', discipline='Men Long Distance',      thesis='Develop',  mean_pre=78.8, std_pre=7.4, mean_prev=76.5, mean_prev2=74.2, mean_prev3=72.1, age_vs_peak=-4, prior_olympics=1, first_olympics=0, win_streak=0,  sentiment=0.56, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.45, depth=1, field_size=14, home_boost=1.2, rival_mean=95),
    # Relays: rival_mean reflects the best non-USA relay program.
    # Women 4x100: Jamaica ~91 is the primary rival.
    dict(sport='Track & Field', discipline='Women 4x100 Relay',     thesis='Develop',  mean_pre=87.5, std_pre=5.2, mean_prev=85.8, mean_prev2=83.4, mean_prev3=81.2, age_vs_peak= 0, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.63, cost=0.7, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.75, depth=4, field_size=6,  home_boost=1.8, rival_mean=88),
    # Women 4x400: Jamaica ~91. USA is dominant but Jamaica is a genuine rival.
    dict(sport='Track & Field', discipline='Women 4x400 Relay',     thesis='Maintain', mean_pre=96.5, std_pre=2.1, mean_prev=95.8, mean_prev2=96.2, mean_prev3=94.8, age_vs_peak= 1, prior_olympics=3, first_olympics=0, win_streak=5,  sentiment=0.74, cost=0.7, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.80, depth=5, field_size=3,  home_boost=2.0, rival_mean=91),
    # Men 4x100: Jamaica/South Africa ~88. Strong but USA faces consistent DQ risk.
    dict(sport='Track & Field', discipline='Men 4x100 Relay',       thesis='Develop',  mean_pre=85.2, std_pre=6.8, mean_prev=83.5, mean_prev2=79.8, mean_prev3=84.2, age_vs_peak= 0, prior_olympics=1, first_olympics=0, win_streak=1,  sentiment=0.60, cost=0.7, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.75, depth=3, field_size=8,  home_boost=1.8, rival_mean=88),
    # Men 4x400: Botswana/Jamaica ~91. USA dominates but Botswana is ascending rapidly.
    dict(sport='Track & Field', discipline='Men 4x400 Relay',       thesis='Maintain', mean_pre=94.8, std_pre=2.4, mean_prev=94.2, mean_prev2=95.1, mean_prev3=93.8, age_vs_peak= 0, prior_olympics=3, first_olympics=0, win_streak=4,  sentiment=0.72, cost=0.7, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.80, depth=4, field_size=4,  home_boost=2.0, rival_mean=91),
    # Mixed 4x400: Belgium/Jamaica ~90. USA won Paris 2024.
    dict(sport='Track & Field', discipline='Mixed 4x400 Relay',     thesis='Maintain', mean_pre=93.8, std_pre=2.8, mean_prev=93.5, mean_prev2=94.1, mean_prev3=0,    age_vs_peak= 0, prior_olympics=2, first_olympics=0, win_streak=3,  sentiment=0.71, cost=0.6, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.70, depth=4, field_size=4,  home_boost=1.8, rival_mean=90),
    # ── Swimming ── rival_mean is the key correction vs. the old eff_mean*0.91 assumption.
    # Women Distance: Ariarne Titmus (AUS) ~93. Ledecky vs. Titmus is the defining rivalry.
    dict(sport='Swimming',      discipline='Women Distance',   thesis='Maintain', mean_pre=95.2, std_pre=3.8, mean_prev=94.1, mean_prev2=95.8, mean_prev3=92.4, age_vs_peak= 3, prior_olympics=4, first_olympics=0, win_streak=8,  sentiment=0.72, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.90, depth=1, field_size=3,  home_boost=1.3, rival_mean=93),
    # Men Distance: AUS/UK ~87. Finke (USA) ~88.4 — USA is competitive but field is close.
    dict(sport='Swimming',      discipline='Men Distance',     thesis='Develop',  mean_pre=88.4, std_pre=5.8, mean_prev=86.2, mean_prev2=84.5, mean_prev3=82.8, age_vs_peak=-3, prior_olympics=2, first_olympics=0, win_streak=2,  sentiment=0.62, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=2, field_size=5,  home_boost=1.3, rival_mean=87),
    # Women Sprint: AUS (Emma McKeon successor) ~90. USA and AUS trade medals in these events.
    dict(sport='Swimming',      discipline='Women Sprint',     thesis='Develop',  mean_pre=91.5, std_pre=4.2, mean_prev=95.8, mean_prev2=88.4, mean_prev3=93.2, age_vs_peak=-3, prior_olympics=1, first_olympics=0, win_streak=4,  sentiment=0.67, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.80, depth=3, field_size=8,  home_boost=1.3, rival_mean=90),
    # Men Sprint: AUS/UK at ~92 — STRONGER than USA's 87.8. Most honest field in the portfolio.
    dict(sport='Swimming',      discipline='Men Sprint',       thesis='Develop',  mean_pre=87.8, std_pre=5.5, mean_prev=91.2, mean_prev2=87.5, mean_prev3=90.8, age_vs_peak=-4, prior_olympics=0, first_olympics=1, win_streak=3,  sentiment=0.64, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.80, depth=2, field_size=10, home_boost=1.3, rival_mean=92),
    # Soccer Women: Spain/Germany/Netherlands ~88. USA had a poor Paris 2024 (quarter-final exit).
    dict(sport='Soccer',        discipline='Women',            thesis='Maintain', mean_pre=91.5, std_pre=2.8, mean_prev=78.3, mean_prev2=71.5, mean_prev3=91.8, age_vs_peak= 1, prior_olympics=2, first_olympics=0, win_streak=3,  sentiment=0.69, cost=1.0, pro_pipeline=0.4, pipeline_erosion=0.0, fan_favorite=0.80, depth=5, field_size=5,  home_boost=1.5, rival_mean=88),
    # Diving Platform: China is the dominant program globally at ~97. USA is a distant contender.
    # This is the starkest rival_mean correction — old model had field at 67.5 (74.2*0.91).
    dict(sport='Diving',        discipline='Platform',         thesis='Develop',  mean_pre=74.2, std_pre=6.8, mean_prev=72.8, mean_prev2=73.5, mean_prev3=71.8, age_vs_peak=-5, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.55, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.70, depth=1, field_size=8,  home_boost=1.5, rival_mean=97),
    # Basketball Men: France ~88 is the benchmark rival (Paris 2024 silver). USA is above ~92.
    dict(sport='Basketball',    discipline='Men',              thesis='Maintain', mean_pre=92.0, std_pre=2.0, mean_prev=93.5, mean_prev2=94.2, mean_prev3=95.1, age_vs_peak= 1, prior_olympics=2, first_olympics=0, win_streak=5,  sentiment=0.72, cost=1.0, pro_pipeline=0.4, pipeline_erosion=0.0, fan_favorite=0.90, depth=5, field_size=3,  home_boost=1.2, rival_mean=88),
    # Rowing Women Eight: NZ/Canada ~89. USA dominant but field is not weak.
    dict(sport='Rowing',        discipline='Women Eight',      thesis='Maintain', mean_pre=90.2, std_pre=2.4, mean_prev=91.8, mean_prev2=92.4, mean_prev3=93.1, age_vs_peak= 0, prior_olympics=2, first_olympics=0, win_streak=4,  sentiment=0.74, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.4, fan_favorite=0.35, depth=4, field_size=6,  home_boost=0.8, rival_mean=89),
    # Wrestling: Azerbaijan/Japan ~80 are serious rivals. USA not dominant.
    # russia_rival=88: Russia was the most decorated wrestling nation globally. Return would be the
    # largest single rival uplift in the Summer portfolio — from 80 to 88.
    dict(sport='Wrestling',     discipline='Freestyle',        thesis='Develop',  mean_pre=76.8, std_pre=7.4, mean_prev=74.2, mean_prev2=72.8, mean_prev3=71.4, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.53, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.35, depth=1, field_size=8,  home_boost=1.2, rival_mean=80, russia_rival=88),
    # Volleyball Beach Women: Brazil/AUS ~90. Very competitive global field.
    dict(sport='Volleyball',    discipline='Beach Women',      thesis='Protect',  mean_pre=93.1, std_pre=3.8, mean_prev=95.2, mean_prev2=87.3, mean_prev3=98.2, age_vs_peak= 0, prior_olympics=2, first_olympics=0, win_streak=5,  sentiment=0.66, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.80, depth=2, field_size=4,  home_boost=1.8, rival_mean=90),
    # Volleyball Beach Men: Brazil/Poland ~85. USA competitive but not dominant.
    dict(sport='Volleyball',    discipline='Beach Men',        thesis='Develop',  mean_pre=81.4, std_pre=6.2, mean_prev=79.8, mean_prev2=79.1, mean_prev3=78.4, age_vs_peak= 0, prior_olympics=0, first_olympics=0, win_streak=3,  sentiment=0.61, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.60, depth=2, field_size=6,  home_boost=1.5, rival_mean=85),
    # Volleyball Indoor Women: Serbia/Brazil ~87. USA is competitive at this level.
    # russia_rival=90: Russia was a perennial finalist in women's volleyball.
    dict(sport='Volleyball',    discipline='Indoor Women',     thesis='Maintain', mean_pre=88.6, std_pre=3.4, mean_prev=87.1, mean_prev2=90.2, mean_prev3=89.7, age_vs_peak= 1, prior_olympics=2, first_olympics=0, win_streak=2,  sentiment=0.67, cost=1.0, pro_pipeline=0.4, pipeline_erosion=0.0, fan_favorite=0.60, depth=4, field_size=5,  home_boost=1.5, rival_mean=87, russia_rival=90),
    # Field Hockey Women: Netherlands ~93 is the dominant global program. USA is a developing challenger.
    # Old model had field at 70.5 (77.5*0.91) — Netherlands actually scores ~93. Major correction.
    dict(sport='Field Hockey',  discipline='Women',            thesis='Develop',  mean_pre=77.5, std_pre=6.8, mean_prev=74.8, mean_prev2=72.4, mean_prev3=70.8, age_vs_peak= 0, prior_olympics=0, first_olympics=0, win_streak=1,  sentiment=0.57, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.25, depth=3, field_size=8,  home_boost=1.2, rival_mean=93),
    # Tennis: Many strong players across the draw. rival_mean reflects the median finalist level.
    dict(sport='Tennis',        discipline='Women Singles',    thesis='Develop',  mean_pre=87.5, std_pre=7.2, mean_prev=79.4, mean_prev2=74.8, mean_prev3=72.1, age_vs_peak=-4, prior_olympics=1, first_olympics=0, win_streak=4,  sentiment=0.68, cost=0.7, pro_pipeline=0.7, pipeline_erosion=0.0, fan_favorite=0.65, depth=1, field_size=8,  home_boost=1.0, rival_mean=88),
    dict(sport='Tennis',        discipline='Men Singles',      thesis='Develop',  mean_pre=81.2, std_pre=8.8, mean_prev=76.5, mean_prev2=73.2, mean_prev3=70.8, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=2,  sentiment=0.61, cost=0.7, pro_pipeline=0.7, pipeline_erosion=0.0, fan_favorite=0.65, depth=1, field_size=10, home_boost=1.0, rival_mean=85),
])

# ── Olympic Winter ────────────────────────────────────────────
# mean_prev = Milan 2026 | mean_prev2 = Beijing 2022 | mean_prev3 = PyeongChang 2018
# (Milan 2026 is the prior Games for French Alps 2030 cycle)
WINTER = pd.DataFrame([
    # ── Figure Skating ── four disciplines; each is a separate athlete pool and medal.
    # Men Singles: Japan (Hanyu/Uno successor) ~95. USA at 97.2 is genuinely ahead.
    dict(sport='Figure Skating', discipline='Men Singles',    thesis='Protect',  mean_pre=97.2, std_pre=3.4, mean_prev=94.8, mean_prev2=82.4, mean_prev3=79.5, age_vs_peak=-2, prior_olympics=0, first_olympics=1, win_streak=12, sentiment=0.22, cost=1.2, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.85, depth=1, field_size=6,  home_boost=1.5, rival_mean=95),
    # Women Singles: South Korea/Japan ~82. Russia was a perennial Women's Singles power (Medvedeva, Zagitova, Valieva).
    # russia_rival=93: Russian skaters have historically scored at the very top of the field.
    dict(sport='Figure Skating', discipline='Women Singles',  thesis='Develop',  mean_pre=80.2, std_pre=4.8, mean_prev=77.5, mean_prev2=76.8, mean_prev3=75.2, age_vs_peak= 0, prior_olympics=0, first_olympics=0, win_streak=2,  sentiment=0.62, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.85, depth=1, field_size=8,  home_boost=1.8, rival_mean=82, russia_rival=93),
    # Ice Dance: France (Papadakis/Cizeron successor) ~89. USA program at 91.5 is ahead.
    dict(sport='Figure Skating', discipline='Ice Dance',      thesis='Maintain', mean_pre=91.5, std_pre=3.2, mean_prev=90.8, mean_prev2=89.4, mean_prev3=87.2, age_vs_peak= 1, prior_olympics=3, first_olympics=0, win_streak=4,  sentiment=0.67, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.80, depth=2, field_size=5,  home_boost=1.8, rival_mean=89),
    # Pairs: China is dominant at ~93. USA at 78.5 is a significant challenger gap.
    # Old model had field at 71.4 (78.5*0.91) — China actually scores ~93. Critical correction.
    dict(sport='Figure Skating', discipline='Pairs',          thesis='Develop',  mean_pre=78.5, std_pre=6.8, mean_prev=76.2, mean_prev2=73.5, mean_prev3=70.8, age_vs_peak=-2, prior_olympics=1, first_olympics=0, win_streak=1,  sentiment=0.57, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.70, depth=1, field_size=6,  home_boost=1.5, rival_mean=93),
    # Alpine Women: Austria/Switzerland ~87. Shiffrin-era USA is at or above that.
    dict(sport='Alpine Skiing',  discipline='Women Slalom/GS', thesis='Maintain', mean_pre=88.2, std_pre=7.4, mean_prev=88.2, mean_prev2=88.5, mean_prev3=87.8, age_vs_peak= 5, prior_olympics=4, first_olympics=0, win_streak=3,  sentiment=0.55, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.85, depth=1, field_size=8,  home_boost=1.5, rival_mean=87),
    # Alpine Men: Switzerland/Norway ~85. USA at 79.5 is below the field.
    dict(sport='Alpine Skiing',  discipline='Men Slalom/GS',   thesis='Develop',  mean_pre=79.5, std_pre=8.8, mean_prev=77.4, mean_prev2=76.2, mean_prev3=75.1, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=0,  sentiment=0.52, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.65, depth=1, field_size=10, home_boost=1.2, rival_mean=85),
    # Ice Hockey Women: Canada ~91 is the defining rival. Almost perfectly matched.
    dict(sport='Ice Hockey',     discipline='Women',           thesis='Maintain', mean_pre=92.0, std_pre=2.5, mean_prev=91.5, mean_prev2=92.5, mean_prev3=92.1, age_vs_peak= 2, prior_olympics=3, first_olympics=0, win_streak=2,  sentiment=0.70, cost=1.0, pro_pipeline=0.4, pipeline_erosion=0.0, fan_favorite=0.80, depth=5, field_size=3,  home_boost=1.5, rival_mean=91),
    # Freestyle Aerials: China ~88 is a consistently strong rival in both genders.
    # Russia was also a top-3 Aerials program globally; return would add a ~92 competitor to Women's field.
    dict(sport='Freestyle',      discipline='Women Aerials',   thesis='Develop',  mean_pre=89.8, std_pre=3.0, mean_prev=87.5, mean_prev2=85.1, mean_prev3=83.4, age_vs_peak=-1, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.62, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=2, field_size=6,  home_boost=1.5, rival_mean=88, russia_rival=92),
    # Men Aerials: Russia historically scored ~90 in Men's Aerials. Moderate uplift.
    dict(sport='Freestyle',      discipline='Men Aerials',     thesis='Develop',  mean_pre=85.2, std_pre=4.1, mean_prev=83.8, mean_prev2=81.2, mean_prev3=79.5, age_vs_peak=-2, prior_olympics=1, first_olympics=0, win_streak=1,  sentiment=0.58, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.50, depth=1, field_size=6,  home_boost=1.5, rival_mean=87, russia_rival=90),
    # Speed Skating: Netherlands/China/Japan dominate — not a Russia-impacted sport.
    # rival_mean=88 reflects Netherlands/China. No russia_rival set.
    dict(sport='Speed Skating',  discipline='Women 500m',      thesis='Maintain', mean_pre=89.1, std_pre=2.8, mean_prev=88.4, mean_prev2=87.1, mean_prev3=86.4, age_vs_peak=-1, prior_olympics=1, first_olympics=0, win_streak=3,  sentiment=0.68, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=2, field_size=8,  home_boost=1.2, rival_mean=88),
    dict(sport='Speed Skating',  discipline='Men 500m',        thesis='Develop',  mean_pre=83.4, std_pre=5.2, mean_prev=81.2, mean_prev2=79.8, mean_prev3=78.5, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.57, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=1, field_size=10, home_boost=1.2, rival_mean=88),
    # Biathlon: Norway/Sweden/France score ~94-96 while USA is at ~70-72.
    # These are the two largest rival_mean corrections in the Winter portfolio.
    # Old model had Women field at 66.3 (72.8*0.91); Norway actually scores ~94.
    # russia_rival=96/97: Russia/Belarus were the deepest Biathlon programs globally. Return would pack an
    # already brutal field even further — the single largest competitive impact of Russia's return in Winter.
    dict(sport='Biathlon',       discipline='Women',           thesis='Develop',  mean_pre=72.8, std_pre=7.2, mean_prev=68.5, mean_prev2=65.2, mean_prev3=63.8, age_vs_peak=-5, prior_olympics=0, first_olympics=1, win_streak=0,  sentiment=0.53, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.25, depth=1, field_size=15, home_boost=1.0, rival_mean=94, russia_rival=96),
    dict(sport='Biathlon',       discipline='Men',             thesis='Develop',  mean_pre=70.2, std_pre=7.8, mean_prev=66.8, mean_prev2=63.5, mean_prev3=61.2, age_vs_peak=-5, prior_olympics=0, first_olympics=1, win_streak=0,  sentiment=0.50, cost=0.7, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.20, depth=1, field_size=15, home_boost=1.0, rival_mean=96, russia_rival=97),
    # Snowboard Halfpipe Women: AUS/Japan ~90. Chloe Kim at 95.2 is genuinely above field.
    dict(sport='Snowboard',      discipline='Women Halfpipe',  thesis='Protect',  mean_pre=95.2, std_pre=3.8, mean_prev=94.8, mean_prev2=97.2, mean_prev3=88.4, age_vs_peak= 2, prior_olympics=3, first_olympics=0, win_streak=6,  sentiment=0.62, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.85, depth=1, field_size=5,  home_boost=1.8, rival_mean=90),
    # Snowboard Halfpipe Men: Japan ~88. Field close to USA's 86.4.
    dict(sport='Snowboard',      discipline='Men Halfpipe',    thesis='Develop',  mean_pre=86.4, std_pre=5.8, mean_prev=84.2, mean_prev2=82.5, mean_prev3=79.8, age_vs_peak=-2, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.60, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.70, depth=2, field_size=6,  home_boost=1.5, rival_mean=88),
    # Cross-Country: Norway ~95. USA at 75.3 is far from contention for gold.
    # Old model had field at 68.5 (75.3*0.91); Norway/Sweden/Finland actually score ~95.
    # russia_rival=97: Russia was the dominant Cross-Country program historically (Bolshunov etc.).
    # Return would further compress USA's already minimal P(gold).
    dict(sport='Cross-Country',  discipline='Skiathlon',       thesis='Develop',  mean_pre=75.3, std_pre=6.8, mean_prev=72.1, mean_prev2=67.8, mean_prev3=66.4, age_vs_peak=-5, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.50, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.20, depth=1, field_size=14, home_boost=1.0, rival_mean=95, russia_rival=97),
    # Ice Hockey Men: Canada/Sweden ~85. USA at 82.3 is close but below the top.
    # russia_rival=89: Russia's Men's hockey program (KHL-depth roster) scores ~89 and would represent
    # the strongest single rival in the field — above Canada.
    dict(sport='Ice Hockey',     discipline='Men',             thesis='Develop',  mean_pre=82.3, std_pre=6.5, mean_prev=79.8, mean_prev2=72.1, mean_prev3=79.4, age_vs_peak= 0, prior_olympics=0, first_olympics=0, win_streak=0,  sentiment=0.55, cost=1.1, pro_pipeline=0.4, pipeline_erosion=0.0, fan_favorite=0.80, depth=4, field_size=6,  home_boost=1.5, rival_mean=85, russia_rival=89),
])

# ── Paralympic Summer ─────────────────────────────────────────
# mean_prev = Tokyo 2020 Para | mean_prev2 = Rio 2016 Para | mean_prev3 = London 2012 Para
PARA_SUMMER = pd.DataFrame([
    # rival_mean for Para events: Australia and GB are the primary challengers across most disciplines.
    dict(sport='Para Swimming',  discipline='Multi-Class',   thesis='Protect',  mean_pre=94.8, std_pre=2.9, mean_prev=93.1, mean_prev2=91.8, mean_prev3=90.2, age_vs_peak=-2, prior_olympics=0, first_olympics=1, win_streak=8,  sentiment=0.31, cost=1.1, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.45, depth=2, field_size=4,  home_boost=1.5, rival_mean=91),
    dict(sport='Para Athletics', discipline='Sprint T64',    thesis='Protect',  mean_pre=93.2, std_pre=3.5, mean_prev=91.8, mean_prev2=90.2, mean_prev3=88.5, age_vs_peak= 0, prior_olympics=2, first_olympics=0, win_streak=6,  sentiment=0.58, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.50, depth=2, field_size=4,  home_boost=1.5, rival_mean=90),
    # Wheelchair BB Men: Australia/GB ~87. USA is clearly dominant.
    dict(sport='Wheelchair BB',  discipline='Men',           thesis='Maintain', mean_pre=90.5, std_pre=2.2, mean_prev=89.4, mean_prev2=88.6, mean_prev3=87.1, age_vs_peak= 1, prior_olympics=2, first_olympics=0, win_streak=3,  sentiment=0.72, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.45, depth=4, field_size=4,  home_boost=1.5, rival_mean=87),
    dict(sport='Para Cycling',   discipline='Time Trial',    thesis='Develop',  mean_pre=79.3, std_pre=5.9, mean_prev=76.2, mean_prev2=73.8, mean_prev3=71.5, age_vs_peak=-4, prior_olympics=0, first_olympics=1, win_streak=2,  sentiment=0.55, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.30, depth=1, field_size=6,  home_boost=1.2, rival_mean=83),
    # Sitting VB Women: China ~88 is a perennial rival. USA competitive.
    dict(sport='Sitting VB',     discipline='Women',         thesis='Maintain', mean_pre=88.4, std_pre=3.1, mean_prev=87.5, mean_prev2=86.2, mean_prev3=84.8, age_vs_peak= 1, prior_olympics=2, first_olympics=0, win_streak=2,  sentiment=0.68, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.35, depth=4, field_size=4,  home_boost=1.5, rival_mean=88),
    dict(sport='Para Archery',   discipline='Recurve',       thesis='Develop',  mean_pre=76.1, std_pre=6.4, mean_prev=73.4, mean_prev2=71.5, mean_prev3=69.8, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.52, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.25, depth=1, field_size=6,  home_boost=1.2, rival_mean=79),
    dict(sport='Para Athletics', discipline='Field F11',     thesis='Develop',  mean_pre=73.5, std_pre=7.1, mean_prev=70.8, mean_prev2=69.4, mean_prev3=67.5, age_vs_peak=-4, prior_olympics=0, first_olympics=1, win_streak=0,  sentiment=0.49, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.25, depth=1, field_size=6,  home_boost=1.2, rival_mean=79),
    # Para Rowing: GB/AUS ~81. Same pipeline erosion risk as Olympic Rowing.
    dict(sport='Para Rowing',    discipline='Mixed Coxed 4', thesis='Develop',  mean_pre=77.8, std_pre=6.2, mean_prev=75.1, mean_prev2=73.2, mean_prev3=71.5, age_vs_peak= 0, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.57, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.4, fan_favorite=0.25, depth=3, field_size=5,  home_boost=1.2, rival_mean=81),
])

# ── Paralympic Winter ─────────────────────────────────────────
# mean_prev = Beijing 2022 Para | mean_prev2 = PyeongChang 2018 Para | mean_prev3 = Sochi 2014 Para
PARA_WINTER = pd.DataFrame([
    # Para Alpine: Austria/France ~90 are consistent rivals. USA at 92.4 is genuinely ahead.
    dict(sport='Para Alpine',    discipline='Downhill',       thesis='Protect',  mean_pre=92.4, std_pre=4.2, mean_prev=90.8, mean_prev2=89.4, mean_prev3=88.1, age_vs_peak= 0, prior_olympics=2, first_olympics=0, win_streak=5,  sentiment=0.44, cost=1.1, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.40, depth=2, field_size=5,  home_boost=1.2, rival_mean=90),
    # Para Biathlon: Ukraine/Russia (when eligible) ~85. Field is much stronger than USA's 76.5.
    dict(sport='Para Biathlon',  discipline='Sitting',        thesis='Develop',  mean_pre=76.5, std_pre=7.8, mean_prev=73.4, mean_prev2=71.2, mean_prev3=69.5, age_vs_peak=-4, prior_olympics=0, first_olympics=1, win_streak=1,  sentiment=0.51, cost=0.9, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.25, depth=1, field_size=8,  home_boost=1.0, rival_mean=85),
    # Para XC Ski: Ukraine/Canada ~83. Field is stronger than USA's 74.2.
    dict(sport='Para XC Ski',    discipline='Vision Impaired',thesis='Develop',  mean_pre=74.2, std_pre=6.9, mean_prev=71.5, mean_prev2=69.8, mean_prev3=68.2, age_vs_peak=-3, prior_olympics=0, first_olympics=1, win_streak=0,  sentiment=0.48, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.20, depth=1, field_size=8,  home_boost=1.0, rival_mean=83),
    # Sled Hockey: Canada ~90 is the defining rival. Virtually a two-team gold race.
    dict(sport='Sled Hockey',    discipline='Men',            thesis='Maintain', mean_pre=91.8, std_pre=2.4, mean_prev=91.2, mean_prev2=90.5, mean_prev3=89.2, age_vs_peak= 0, prior_olympics=3, first_olympics=0, win_streak=4,  sentiment=0.74, cost=1.0, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.55, depth=4, field_size=3,  home_boost=1.5, rival_mean=90),
    # Wheelchair Curling: Canada/GB ~82. USA at 78.9 is slightly below the field.
    dict(sport='Wheelchair Curl',discipline='Mixed',          thesis='Develop',  mean_pre=78.9, std_pre=5.5, mean_prev=76.8, mean_prev2=74.8, mean_prev3=73.1, age_vs_peak= 1, prior_olympics=1, first_olympics=0, win_streak=2,  sentiment=0.59, cost=0.8, pro_pipeline=0.0, pipeline_erosion=0.0, fan_favorite=0.30, depth=3, field_size=5,  home_boost=1.2, rival_mean=82),
])

THESIS_META = {
    'Protect':  dict(color='#e4e4e0', desc='Dominant program, first Olympics. Close the preparation gap before the Games.'),
    'Develop':  dict(color='#8a8a86', desc='Ascending program. Invest ahead of the curve. Higher variance, higher ceiling.'),
    'Maintain': dict(color='#484844', desc='Perennially dominant. Protect the floor. Low marginal return on additional capital.'),
}

N_SIMS = 8000

# Maximum additional investment per program above baseline (enhancement tier)
E_MAX = 0.3

@st.cache_data
def run_monte_carlo(df, home_games=False, russia_return=False):
    HOME_BOOST = 1.5   # score-point lift for home Games (LA 2028)
    rows = []
    for _, row in df.iterrows():
        # ── Multi-cycle recency-weighted mean and empirical std ──────
        prev  = row.get('mean_prev',  0) or 0
        prev2 = row.get('mean_prev2', 0) or 0
        prev3 = row.get('mean_prev3', 0) or 0
        if prev > 0 and prev2 > 0 and prev3 > 0:
            # Four cycles: 45 / 27 / 17 / 11 recency weights
            eff_mean = 0.45 * row['mean_pre'] + 0.27 * prev + 0.17 * prev2 + 0.11 * prev3
            hist_std = float(np.std([row['mean_pre'], prev, prev2, prev3]))
            eff_std  = 0.50 * row['std_pre'] + 0.50 * hist_std
        elif prev > 0 and prev2 > 0:
            # Three cycles: 50 / 30 / 20 recency weights
            eff_mean = 0.50 * row['mean_pre'] + 0.30 * prev + 0.20 * prev2
            hist_std = float(np.std([row['mean_pre'], prev, prev2]))
            eff_std  = 0.60 * row['std_pre'] + 0.40 * hist_std
        elif prev > 0:
            # Two cycles: 65 / 35
            eff_mean  = 0.65 * row['mean_pre'] + 0.35 * prev
            games_var = abs(row['mean_pre'] - prev) / 2.0
            eff_std   = 0.70 * row['std_pre'] + 0.30 * games_var
        else:
            eff_mean = row['mean_pre']
            eff_std  = row['std_pre']

        # ── Past-peak athletes carry wider outcome distribution ──────
        avp = row.get('age_vs_peak', 0) or 0
        if avp > 0:
            eff_std *= (1 + avp * 0.04)

        # ── College pipeline erosion widens outcome uncertainty ───────
        # When feeder programs (college rowing) are being eliminated, the
        # talent supply thins and depth below the top athletes shrinks.
        # This increases performance variance even if the current squad is intact.
        pe = row.get('pipeline_erosion', 0) or 0
        if pe > 0:
            eff_std *= (1 + pe * 0.25)

        # ── Program depth reduces outcome variance ─────────────────────
        # Programs with multiple medal-capable athletes (relays, team sports)
        # are less exposed to single-athlete injury or underperformance.
        # depth=1: single star. depth=5: relay or full squad depth.
        # Each level above 1 compresses std by 6% (floor: 24% reduction at depth=5).
        dep = int(row.get('depth', 1) or 1)
        if dep > 1:
            eff_std *= (1 - (dep - 1) * 0.06)

        # ── Home Games lift (sport-specific multiplier) ────────────────
        # HOME_BOOST is the base lift (score points). home_boost is a per-sport
        # multiplier: crowd-energy-dependent sports (Gymnastics, T&F Sprint) amplify
        # above the base; technical/individual sports (Swimming, Tennis) see less lift.
        if home_games:
            hb = float(row.get('home_boost', 1.0) or 1.0)
            eff_mean += HOME_BOOST * hb

        sims = np.random.normal(eff_mean, eff_std, N_SIMS)

        # ── Field: best-of-N opponents with explicit rival quality ─────────
        # rival_mean = absolute score of the top competing nation/program.
        # Decouples field strength from US score — critical for sports where USA
        # is weak (Biathlon rival ~94, USA ~72; XC Ski rival ~95, USA ~75;
        # Diving rival China ~97, USA ~74) or where a rival matches/exceeds USA
        # (AUS in Swimming Men Sprint ~92 vs USA ~88; China in Pairs ~93 vs USA ~79;
        # Netherlands in Field Hockey ~93 vs USA ~78).
        # Defaults to eff_mean * 0.91 if not set — the old assumption that
        # competitors score ~91% of the US program, reasonable only for dominant USA.
        n_field = int(row.get('field_size', 4) or 4)
        r_mean  = float(row.get('rival_mean', 0) or 0)
        # Russia/Belarus return: upgrade rival_mean to russia_rival where that nation
        # materially strengthens the field (russia_rival > rival_mean).
        if russia_return:
            rr = float(row.get('russia_rival', 0) or 0)
            if rr > r_mean:
                r_mean = rr
        if r_mean <= 0:
            r_mean = eff_mean * 0.91
        field_draws = np.random.normal(r_mean, eff_std * 1.4,
                                       (N_SIMS, max(1, n_field)))
        field = field_draws.max(axis=1)

        # ── Preparation gap: Protect thesis, scaled by prior Olympics ─
        if row['thesis'] == 'Protect':
            prior      = row.get('prior_olympics', 0 if row['first_olympics'] else 2) or 0
            exp_factor = max(0.15, 1.0 - prior * 0.28)
            gap        = row['win_streak'] * 0.18 * (1 - row['sentiment']) * exp_factor
            if gap > 0:
                sims = sims - np.random.exponential(gap, N_SIMS)

        rows.append({**row.to_dict(),
            'p_gold':  round(float(np.mean(sims > field)), 3),
            'p_medal': round(float(np.mean(sims > field * 0.94)), 3),
            'p_top5':  round(float(np.mean(sims > field * 0.89)), 3),
        })
    return pd.DataFrame(rows)

def run_lp(df, budget):
    # Enhancement return per unit: programs far from medal ceiling benefit most.
    # pro_pipeline [0.0–1.0] is the fraction of enhancement ROI captured by external
    # development infrastructure. 0.0 = USOPC is primary funder. 0.4 = major league/
    # federation pipeline (NBA, NHL, NWSL). 0.7 = WTA/ATP tennis, where players are
    # fully self-funded and USOPC's marginal development role is near zero.
    r = {i: round(
            (1 - df.loc[i, 'p_gold']) * 0.5 * (1 - df.loc[i, 'pro_pipeline']),
            4)
         for i in df.index}

    # pipeline_erosion [0.0–1.0]: fraction of college/feeder program infrastructure
    # at risk of elimination. When schools cut rowing programs, USOPC must absorb
    # athlete development costs that were previously externally subsidized.
    # Effective cost = stated cost × (1 + pipeline_erosion × 0.3).
    # At erosion=0.4 (Rowing), cost rises from 0.9 → ~1.07 units.
    #
    # depth [1–5]: programs with multiple medal-capable athletes spread fixed
    # infrastructure cost (coaching, travel, support staff) across more medal
    # opportunities. Each depth level above 1 discounts effective cost by 5%
    # (floor: 0.80× at depth=5). Relay teams and squad sports capture this most.
    effective_cost = {i:
        df.loc[i,'cost']
        * (1 + df.loc[i,'pipeline_erosion'] * 0.3)
        * max(0.80, 1.0 - (df.loc[i,'depth'] - 1) * 0.05)
        for i in df.index}

    # --- MILP: binary fund/no-fund + continuous enhancement above baseline ---
    prob = pulp.LpProblem('USOPC', pulp.LpMaximize)
    x = {i: pulp.LpVariable(f'x{i}', cat='Binary') for i in df.index}
    e = {i: pulp.LpVariable(f'e{i}', lowBound=0, upBound=E_MAX) for i in df.index}

    prob += pulp.lpSum(df.loc[i,'p_gold'] * x[i] + r[i] * e[i] for i in df.index)
    prob += pulp.lpSum(effective_cost[i] * x[i] + e[i] for i in df.index) <= budget, 'budget'
    for i in df.index:
        prob += e[i] <= E_MAX * x[i]  # can only enhance funded programs

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    df = df.copy()
    df['selected'] = [1 if pulp.value(x[i]) and pulp.value(x[i]) > 0.5 else 0 for i in df.index]
    df['enhancement'] = [round(float(pulp.value(e[i]) or 0.0), 3) for i in df.index]
    exp = round(sum(
        df.loc[i,'p_gold'] + r[i] * df.loc[i,'enhancement']
        for i in df.index if df.loc[i,'selected']
    ), 3)

    # --- LP relaxation with fixed selection to recover a valid shadow price ---
    # MILP duals are unreliable; fix the binary selection and re-solve as pure LP
    prob2 = pulp.LpProblem('USOPC_LP', pulp.LpMaximize)
    e2 = {i: pulp.LpVariable(f'e2_{i}', lowBound=0,
                              upBound=E_MAX * float(df.loc[i,'selected'])) for i in df.index}
    prob2 += pulp.lpSum(
        df.loc[i,'p_gold'] * df.loc[i,'selected'] + r[i] * e2[i] for i in df.index
    )
    prob2 += pulp.lpSum(
        effective_cost[i] * df.loc[i,'selected'] + e2[i] for i in df.index
    ) <= budget, 'budget'
    prob2.solve(pulp.PULP_CBC_CMD(msg=0))

    shadow = 0.0
    for name, c in prob2.constraints.items():
        if name == 'budget' and c.pi is not None:
            shadow = round(abs(c.pi), 4)

    return df, exp, shadow

@st.cache_data
def build_frontier(df, steps=35):
    # Extend budget range to include full enhancement of all programs
    max_b = df['cost'].sum() + len(df) * E_MAX * 0.9
    rows, prev_g, prev_b = [], 0.0, 0.0
    for b in np.linspace(0.5, max_b, steps):
        df2, exp, shadow = run_lp(df, b)
        dg = exp - prev_g
        db = b - prev_b
        rows.append(dict(budget=round(b,2), exp_golds=exp, shadow_price=shadow,
                         marginal_cost=round(db/dg,2) if dg > 0.005 else None,
                         n_funded=int(df2['selected'].sum())))
        prev_g, prev_b = exp, b
    return pd.DataFrame(rows)

def chart_portfolio(df):
    df_s = df.sort_values('p_gold', ascending=True)
    fig, ax = plt.subplots(figsize=(6.5, max(2.8, len(df)*0.48)))
    for i, (_, row) in enumerate(df_s.iterrows()):
        color = THESIS_META[row['thesis']]['color']
        alpha = 1.0 if row['selected'] else 0.25
        ax.barh(i, row['p_medal'], color=color, alpha=alpha*0.25, height=0.55, zorder=2)
        ax.barh(i, row['p_gold'],  color=color, alpha=alpha, height=0.55, zorder=3)
        ax.text(-0.01, i, f"{row['sport']} · {row['discipline']}",
                ha='right', va='center', fontsize=7.5, fontfamily='monospace',
                color='#c8c8c4' if row['selected'] else '#383834')
        ax.text(row['p_gold']+0.012, i, f"{row['p_gold']:.0%}",
                ha='left', va='center', fontsize=7, fontfamily='monospace',
                color='#8a8a86' if row['selected'] else '#383834')
    # "funded" / "not selected" label on first occurrence of each
    labeled = set()
    for i, (_, row) in enumerate(df_s.iterrows()):
        tag = 'funded' if row['selected'] else 'not selected'
        if tag not in labeled:
            ax.text(-0.565, i, tag, ha='left', va='center', fontsize=6,
                    fontfamily='monospace',
                    color='#8a8a86' if row['selected'] else '#383834',
                    style='italic')
            labeled.add(tag)
    ax.set_xlim(-0.58, 1.2)
    ax.set_yticks([])
    ax.set_xlabel('P(gold)', fontsize=8, color='#646460', labelpad=5)
    ax.text(0.98, -0.06, 'light extension = P(medal)', transform=ax.transAxes,
            ha='right', va='top', fontsize=6.5, fontfamily='monospace', color='#383834')
    ax.tick_params(axis='x', labelsize=7.5, colors='#646460')
    ax.spines['bottom'].set_color('#303030')
    ax.spines['bottom'].set_linewidth(0.8)
    ax.spines['left'].set_visible(False)
    for thesis, meta in THESIS_META.items():
        ax.barh([], [], color=meta['color'], label=thesis, height=0.55)
    ax.legend(fontsize=7, frameon=False, loc='lower right', labelcolor='#8a8a86')
    plt.tight_layout(pad=0.4)
    return fig

def chart_frontier(frontier, budget, exp_golds):
    fig, ax = plt.subplots(figsize=(6.5, 2.8))
    ax.plot(frontier['budget'], frontier['exp_golds'], color='#e4e4e0', lw=1.3, zorder=3)
    ax.axvline(budget, color='#303030', lw=0.8, ls='--', zorder=1)
    ax.scatter([budget], [exp_golds], color='#e4e4e0', s=30, zorder=5)
    ax.annotate(f"{exp_golds:.2f}",
                xy=(budget, exp_golds),
                xytext=(budget + 0.3, exp_golds + 0.04),
                fontsize=7, color='#e4e4e0', fontfamily='monospace',
                arrowprops=dict(arrowstyle='-', color='#303030', lw=0.6))
    peak = frontier.loc[frontier['shadow_price'].idxmax()]
    ax.annotate(f"peak return\nat {peak['budget']:.1f} units",
                xy=(peak['budget'], peak['exp_golds']),
                xytext=(peak['budget']+0.4, peak['exp_golds']-0.06),
                fontsize=7, color='#646460', fontfamily='monospace',
                arrowprops=dict(arrowstyle='-', color='#303030', lw=0.7))
    ax.set_xlabel('Capital deployed (units)', fontsize=8, color='#646460', labelpad=5)
    ax.set_ylabel('Expected gold medals', fontsize=8, color='#646460', labelpad=5)
    ax.tick_params(labelsize=7.5, colors='#646460')
    ax.spines['bottom'].set_color('#303030')
    ax.spines['bottom'].set_linewidth(0.8)
    plt.tight_layout(pad=0.4)
    return fig

def chart_shadow(frontier, budget):
    fig, ax = plt.subplots(figsize=(6.5, 2.2))
    ax.fill_between(frontier['budget'], frontier['shadow_price'], color='#e4e4e0', alpha=0.07, zorder=1)
    ax.plot(frontier['budget'], frontier['shadow_price'], color='#e4e4e0', lw=1.1, zorder=3)
    ax.axvline(budget, color='#303030', lw=0.8, ls='--', zorder=2)
    ax.axhline(0, color='#303030', lw=0.6, zorder=1)
    ax.set_xlabel('Capital deployed (units)', fontsize=8, color='#646460', labelpad=5)
    ax.set_ylabel('Marginal medal value', fontsize=8, color='#646460', labelpad=5)
    ax.tick_params(labelsize=7.5, colors='#646460')
    ax.spines['bottom'].set_color('#303030')
    ax.spines['bottom'].set_linewidth(0.8)
    plt.tight_layout(pad=0.4)
    return fig

def render_tab(raw_df, context, key, home_games=False, russia_return=False):
    mc_df = run_monte_carlo(raw_df, home_games=home_games, russia_return=russia_return)
    max_b = float(raw_df['cost'].sum())
    budget = st.slider('Capital budget (units)', 0.5, max_b, min(5.0, max_b), step=0.1, key=key,
                       help='One unit ≈ annual program funding allocation. Programs cost 0.8–1.2 units each.')
    df, exp_golds, shadow = run_lp(mc_df, budget)
    selected = df[df['selected'] == 1]
    n_funded = len(selected)
    budget_used = round(selected['cost'].sum(), 1) if not selected.empty else 0.0
    p_any = round(1 - np.prod([1 - r['p_medal'] for _, r in selected.iterrows()]), 3) if not selected.empty else 0.0

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi"><div class="kpi-value">{exp_golds:.2f}</div><div class="kpi-label">Expected golds</div><div class="kpi-sub">avg medals across simulations</div></div>
        <div class="kpi"><div class="kpi-value">{n_funded}</div><div class="kpi-label">Programs funded</div><div class="kpi-sub">of {len(df)} evaluated</div></div>
        <div class="kpi"><div class="kpi-value">{budget_used}</div><div class="kpi-label">Capital deployed</div><div class="kpi-sub">of {budget:.1f} available</div></div>
        <div class="kpi"><div class="kpi-value">{"—" if shadow == 0.0 else f"{shadow:.3f}"}</div><div class="kpi-label">Marginal medal value</div><div class="kpi-sub">{"all investment exhausted" if shadow == 0.0 else "expected golds per unit added"}</div></div>
        <div class="kpi"><div class="kpi-value">{p_any:.0%}</div><div class="kpi-label">P(any medal)</div><div class="kpi-sub">across portfolio</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p class="caption">{context}</p>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown("## Investment theses")
    c1, c2, c3 = st.columns(3)
    for col, (thesis, meta) in zip([c1,c2,c3], THESIS_META.items()):
        t_df = df[df['thesis']==thesis]
        t_sel = t_df[t_df['selected']==1]
        n, ns = len(t_df), len(t_sel)
        avg_pg = t_sel['p_gold'].mean() if not t_sel.empty else 0.0
        total_cost = t_sel['cost'].sum() if not t_sel.empty else 0.0
        with col:
            st.markdown(f"""<div class="thesis-card" style="border-left-color:{meta['color']};">
            <div class="thesis-label">{thesis}</div>
            <div class="thesis-name">{ns} of {n} funded</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#646460;margin:0.25rem 0 0.15rem 0;">
              avg P(gold) {avg_pg:.0%} &nbsp;·&nbsp; cost {total_cost:.1f} units
            </div>
            <div class="thesis-desc">{meta['desc']}</div></div>""", unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # Funded programs quick-scan
    if not selected.empty:
        pills = ''.join(
            f'<span style="display:inline-block;font-family:\'DM Mono\',monospace;font-size:0.65rem;'
            f'letter-spacing:0.06em;border:1px solid #e4e4e0;padding:0.15rem 0.55rem;margin:0.2rem 0.3rem 0.2rem 0;'
            f'color:#e4e4e0;">{r["sport"]} · {r["discipline"]} <span style="color:#646460;">{r["p_gold"]:.0%}</span></span>'
            for _, r in selected.sort_values('p_gold', ascending=False).iterrows()
        )
        st.markdown(
            f'<div style="margin-bottom:1.4rem;"><div style="font-family:\'DM Mono\',monospace;font-size:0.62rem;'
            f'letter-spacing:0.1em;text-transform:uppercase;color:#646460;margin-bottom:0.4rem;">Funded programs</div>'
            f'{pills}</div>',
            unsafe_allow_html=True
        )

    cl, cr = st.columns([1.1, 1])

    with cl:
        st.markdown("## Portfolio")
        st.markdown("### P(gold) by program")
        st.pyplot(chart_portfolio(df), use_container_width=True)
        plt.close()

    with cr:
        frontier = build_frontier(mc_df)
        st.markdown("## Efficient frontier")
        st.markdown("### Expected golds across capital levels")
        st.pyplot(chart_frontier(frontier, budget, exp_golds), use_container_width=True)
        plt.close()
        st.markdown("## Marginal medal value")
        st.markdown("### Diminishing returns on additional capital")
        st.pyplot(chart_shadow(frontier, budget), use_container_width=True)
        plt.close()

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── Pipeline erosion flag ─────────────────────────────────────
    eroding = df[df['pipeline_erosion'] > 0]
    if not eroding.empty:
        for _, row in eroding.iterrows():
            eroded_cost = round(row['cost'] * (1 + row['pipeline_erosion'] * 0.3), 2)
            st.markdown(f"""
            <div class="harris-quote">
            <strong>College pipeline erosion — {row['sport']} · {row['discipline']}</strong><br>
            University programs are the primary athlete development pathway for this sport.
            Schools eliminating rowing to manage costs have reduced the depth of the US talent pool.
            USOPC is actively lobbying to reverse these cuts; federal executive action remains possible
            but unresolved.<br><br>
            Effective cost raised from <strong>{row['cost']:.1f} → {eroded_cost:.2f} units</strong>
            (pipeline erosion {int(row['pipeline_erosion']*100)}%). Outcome variance widened by
            {int(row['pipeline_erosion']*25)}%. These adjustments reflect USOPC absorbing development
            costs previously subsidized by college programs. If policy resolves favorably,
            revert <code>pipeline_erosion</code> to 0.0.
            </div>
            """, unsafe_allow_html=True)

    protect_first = df[(df['thesis']=='Protect') & (df['first_olympics']==1)]
    if not protect_first.empty:
        row = protect_first.iloc[0]
        gap = row['win_streak'] * 0.18 * (1 - row['sentiment'])
        st.markdown(f"""
        <div class="harris-quote">
        <strong>Preparation gap flag — {row['sport']} · {row['discipline']}</strong><br>
        {int(row['win_streak'])}-competition win streak entering first Olympics. Readiness signal: {row['sentiment']:.2f}.<br>
        Estimated preparation gap: <strong>{gap:.1f} score units</strong>. P(gold): {row['p_gold']:.0%} — widest outcome distribution in the portfolio.<br>
        Highest expected return on targeted preparation support before the Games.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Full portfolio data")
    show = df[['sport','discipline','thesis','p_gold','p_medal','cost','depth','field_size','win_streak','sentiment','mean_prev','pro_pipeline','fan_favorite','selected']].copy()
    show.columns = ['Sport','Discipline','Thesis','P(gold)','P(medal)','Cost','Depth','Field','Streak','Readiness','Prev Games','Pipeline','Fan Fav','Funded']
    show = show.sort_values('P(gold)', ascending=False)
    show['Funded'] = show['Funded'].map({1: '✓', 0: '—'})
    show['Pipeline'] = show['Pipeline'].apply(lambda v: f'{int(v*100)}%' if v > 0 else '—')
    def hl(row):
        return ['background-color:#242422;font-weight:500']*len(row) if row['Funded'] == '✓' else ['']*len(row)
    st.dataframe(
        show.style
            .apply(hl, axis=1)
            .bar(subset=['P(gold)'],  color='#8a8a86', vmin=0, vmax=1)
            .bar(subset=['P(medal)'], color='#484844', vmin=0, vmax=1)
            .bar(subset=['Fan Fav'],  color='#646460', vmin=0, vmax=1)
            .format({'P(gold)':'{:.0%}','P(medal)':'{:.0%}','Cost':'{:.1f}','Readiness':'{:.2f}','Prev Games':'{:.1f}','Fan Fav':'{:.0%}','Depth':'{:.0f}','Field':'{:.0f}'})
            .hide(axis='index'),
        use_container_width=True
    )


# ── App header ────────────────────────────────────────────────
st.markdown("# USOPC Portfolio Investment Analytics")
st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#646460;margin:-0.2rem 0 1.2rem 0;">LA 2028 &nbsp;·&nbsp; French Alps 2030 &nbsp;·&nbsp; Rocky Harris allocation framework</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="harris-framework">
<h4>Rocky Harris · 2024 Allocation Overhaul — three inputs evaluated simultaneously</h4>
<table>
<tr><td>Medal probability</td><td>Estimated likelihood of podium performance across the quad. Primary return metric for allocation decisions.</td></tr>
<tr><td>Revenue across quad</td><td>Commercial value generated by the NGB. High-revenue programs justify maintenance capital even at lower medal probability.</td></tr>
<tr><td>Fan Favorite</td><td>Estimated level of US public enthusiasm for the sport and program (0–100%). Proxy for the cultural resonance and sponsorship‐appeal dimension of the Harris framework — sports that deeply engage American fans generate broader USOPC commercial partnerships, NGB membership growth, and grassroots participation. 100% = transcendent national moment (Women's Gymnastics All-Around). 80–90% = marquee fan enthusiasm (Basketball, Swimming Distance, Figure Skating, Track Hurdles). 50–70% = broad casual interest. Below 50% = passionate niche community. Para values are systematically lower today; LA 2028 home Games expected to materially lift Para fan engagement. Not wired into LP optimization — displayed for context.</td></tr>
<tr><td>Cost to field team</td><td>Full loaded cost to send athletes to competition. High probability + low cost = optimal investment.</td></tr>
</table>

<h4 style="margin-top:1rem;">How the numbers are calculated</h4>
<table>
<tr><td>P(gold), P(medal)</td><td>8,000 Monte Carlo simulations per program. Six adjustments applied before sampling: (1) Recency-weighted mean — four cycles where available: 45% most recent, 27%, 17%, 11%; falls back to 50/30/20 or 65/35. (2) Blended std — 50% stated + 50% empirical across cycles. (3) Age-vs-peak — std widened 4% per year past peak. (4) Program depth — each depth level above 1 compresses std by 6% (floor at depth=5: −24%), reflecting multi-athlete injury diversification. (5) Home Games lift — base +1.5 score points scaled by per-sport home_boost multiplier (Gymnastics 2.2×, T&F Sprint/Hurdles 1.8–2.0×, Swimming 1.3×, Tennis 1.0×). (6) College pipeline erosion — std widened up to 25% when feeder programs at risk. Athlete score drawn from Normal(eff_mean, eff_std). Field modeled as the maximum of field_size independent draws from Normal(eff_mean × 0.91, eff_std × 1.4) — correctly raises the expected best-opponent score for sports with deeper international competition. P(gold) = fraction of simulations where athlete beats the best opponent. Protect thesis programs take an exponential preparation gap penalty scaled by prior Olympic experience.</td></tr>
<tr><td>Expected golds</td><td>Sum of P(gold) across funded programs. If two programs have P(gold) = 0.7 and 0.6, expected golds = 1.3 — the average number of golds you'd win across many simulated Games, not a guaranteed count.</td></tr>
<tr><td>P(any medal)</td><td>1 − ∏(1 − P(medal)) across funded programs, assuming independence.</td></tr>
<tr><td>Which programs to fund</td><td>Binary LP: maximize ΣP(gold)·x subject to Σcost·x ≤ budget, x ∈ {0,1}.</td></tr>
<tr><td>Pipeline erosion</td><td>College and feeder programs are the primary athlete development pathway for sports like Rowing. When universities eliminate these programs, USOPC must absorb the development cost previously subsidized externally. pipeline_erosion [0.0–1.0] inflates effective cost in the LP by up to 30% and widens outcome std by up to 25%. At 0.4 (current Rowing estimate), cost rises from 0.9 → ~1.07 units and variance is 10% wider. Set to 0.0 if federal policy reverses program cuts.</td></tr>
<tr><td>Depth</td><td>Program depth [1–5]: number of medal-capable athletes. depth=1 = single-star program (e.g., Chloe Kim Halfpipe, Ledecky Distance); depth=5 = relay or full squad (e.g., Women 4x400, Basketball Men). Each level above 1 compresses std by 6% in simulation (injury to one athlete doesn't end the run) and discounts effective cost by 5% in LP (shared infrastructure — coaching, travel, support staff — is spread across more medal opportunities). Net effect: deep programs are both less risky and cheaper per medal chance than single-star programs of equivalent mean performance.</td></tr>
<tr><td>Field size</td><td>Number of genuine medal-contending nations [1–15]. Sets how many independent opponent scores are simulated per trial — P(gold) = P(US beats the best of N opponents). Shallow fields (Women 4x400 ≈ 3 real challengers; Women Ice Hockey ≈ 3) give the same mean_pre a materially higher P(gold) than deep fields (Men Long Distance ≈ 14; Biathlon ≈ 15). This is the primary structural difference between sports like relays (USA vs. a short list of rivals) and global depth events (distance running, biathlon) where contenders from a dozen nations meaningfully suppress P(gold).</td></tr>
<tr><td>Rival mean</td><td>Absolute performance score of the top competing nation — the key competitor-strength correction. Replaces the prior assumption that the field always scores 91% of the US program (eff_mean × 0.91), which was wrong in two important directions: (1) Sports where USA is weak relative to the world: Biathlon (Norway ~94-96, USA ~72); Cross-Country (Norway ~95, USA ~75); Diving Platform (China ~97, USA ~74); Figure Skating Pairs (China ~93, USA ~79); Field Hockey Women (Netherlands ~93, USA ~78). Under the old assumption, these fields were simulated at 65-71 — dramatically understating the actual competition. (2) Sports where a specific rival matches or exceeds USA: Swimming Men Sprint (AUS/UK ~92, USA ~88). The old field mean of 80 understated the real challenge from Australia. Where rival_mean &gt; eff_mean × 0.91, P(gold) is lower than the old model showed; where rival_mean &lt; eff_mean × 0.91, it is higher. Defaults to eff_mean × 0.91 if not set. russia_rival is a scenario field: the rival_mean value if Russia/Belarus return to competition. Activated by the Russia / Belarus return toggle above — replaces rival_mean wherever russia_rival is higher. Only set for sports where Russia/Belarus was historically the dominant competing program. No effect on sports where the primary rival is another nation (Australia in Swimming, China in Diving/Pairs, Netherlands in Field Hockey, Netherlands/Japan in Speed Skating) — those rival_mean values are fixed regardless of the toggle. Largest impacts: Figure Skating Women (82→93), Wrestling Freestyle (80→88), Ice Hockey Men (85→89), Biathlon W/M (94→96, 96→97), Cross-Country (95→97).</td></tr>
<tr><td>Home boost</td><td>Sport-specific multiplier on the base +1.5 home Games score-point lift for LA 2028. Crowd-energy-dependent sports receive larger multipliers: Gymnastics (2.2×), T&F Hurdles/Sprint (1.8–2.0×), Volleyball Beach (1.8×). Technical or neutral-draw sports receive less: Swimming (1.3×), Basketball (1.2×, NBA players less crowd-dependent), Rowing (0.8×, no venue crowd), Tennis (1.0×, neutral draws). Only applied to Summer tabs where home_games=True.</td></tr>
<tr><td>Marginal medal value</td><td>Shadow price on the budget constraint — expected golds gained per one additional unit of capital at the current level. Each program has a baseline cost (fund/no-fund) plus a continuous enhancement tier (up to +0.3 units). Enhancement return r = (1 − P(gold)) × 0.5 × (1 − pipeline) per unit: programs further from the medal ceiling benefit most, discounted by how much of their improvement is driven by external infrastructure rather than USOPC investment. Pipeline factor is a continuous [0.0–1.0] scale: 0.0 = USOPC is the primary development funder; 0.4 = major pro/college pipeline (NBA → Basketball Men, NHL/NCAA → Ice Hockey, NWSL/USSF → Soccer Women, NCAA → Volleyball Indoor Women); 0.7 = WTA/ATP Tennis, where players are entirely self-funded through tour prize money and sponsorships — USOPC's marginal development role is near zero and the model correctly assigns minimal enhancement return to those programs. Marginal value declines with scale but stays positive until all preparation investment is exhausted.</td></tr>
<tr><td>Efficient frontier</td><td>MILP solved at 35 budget levels from 0.5 → max capital (baseline + full enhancement). Traces the maximum achievable expected golds at each funding level, including returns from enhancement investment above each program's baseline cost.</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

# ── Scenario toggle ────────────────────────────────────────────
russia_return = st.toggle(
    "Russia / Belarus return to competition",
    value=False,
    help=(
        "When enabled, rival_mean is upgraded to russia_rival for sports where Russia or Belarus "
        "historically dominated the field. Affects: Gymnastics Women (93), Wrestling Freestyle (88), "
        "Volleyball Indoor Women (90), Figure Skating Women Singles (93), Freestyle Aerials W/M (92/90), "
        "Biathlon W/M (96/97), Cross-Country Skiathlon (97), Ice Hockey Men (89). "
        "No effect on sports where the primary rivals are Australia, China, Netherlands, etc. — "
        "those rival_mean values are unchanged regardless of this toggle. "
        "Models the field-strength impact of a potential return for LA 2028 or French Alps 2030 "
        "— where allowed under IOC eligibility rules."
    )
)

# ── Games tabs — chronological ─────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "LA 2028  ·  Summer Olympic",
    "LA 2028  ·  Summer Paralympic",
    "French Alps 2030  ·  Winter Olympic",
    "French Alps 2030  ·  Winter Paralympic",
])

with tab1:
    render_tab(SUMMER, context=(
        'Home soil. Maximum commercial and competitive stakes. '
        'Gymnastics now modeled separately by gender: Women\'s is a Protect program (dominant, preparation-gap risk); '
        'Men\'s is a Develop program (Paris 2024 team bronze signals ascending trajectory). '
        'Track & Field split by gender and event cluster — Women 400m/Hurdles (McLaughlin-Levrone) is the '
        'single most dominant US track program, classified Maintain. Swimming split by gender: '
        'Women\'s Distance (Ledecky era, Maintain) anchors the portfolio; Men\'s Distance and both Sprint '
        'programs are Develop. Perennially dominant programs (Soccer Women, Basketball Men) '
        'require maintenance capital — low marginal return above the floor.'
    ), key='budget_summer', home_games=True, russia_return=russia_return)

with tab2:
    st.markdown("""<div class="harris-quote"><span class="para-badge">Paralympic</span>
    Same framework, harder data problem. Classification volatility, adaptive equipment cycles,
    and thinner historical data make readiness signals harder to read.</div>""", unsafe_allow_html=True)
    render_tab(PARA_SUMMER, context=(
        'LA 2028 is a home Games for Paralympic sport with significant commercial upside. '
        'Classification-stable programs in Swimming and Athletics carry the highest medal probability. '
        'Development thesis concentrated in Cycling and Archery. '
        'Tokyo 2020 Para results included as prior cycle; home Games lift applied.'
    ), key='budget_para_summer', home_games=True, russia_return=russia_return)

with tab3:
    render_tab(WINTER, context=(
        'Milan 2026 is the analytical baseline. The preparation gap identified in 2026 — '
        'dominant program, first Olympics, low readiness signal — is the primary capital '
        'allocation question for the 2030 cycle. Programs that close that gap compound it.'
    ), key='budget_winter', russia_return=russia_return)

with tab4:
    st.markdown("""<div class="harris-quote"><span class="para-badge">Paralympic</span>
    Thinnest competitive data in the portfolio. Preparation gap analysis is most uncertain here —
    and most valuable if right.</div>""", unsafe_allow_html=True)
    render_tab(PARA_WINTER, context=(
        'Sled Hockey is the anchor maintenance program. Para Alpine carries the Protect thesis. '
        'Development capital is thin by design: Winter Paralympic programs have fewer pathways '
        'and narrower athlete pipelines than Summer counterparts.'
    ), key='budget_para_winter', russia_return=russia_return)

# USOPC Portfolio Investment Analytics

> *"We've brought all that together into one team that is going to focus on investing in national governing bodies like it's a portfolio of investments."*
> — Rocky Harris, USOPC Chief of Sport & Athlete Services, 2024

---

## What This Is

A computational implementation of the portfolio investment framework USOPC adopted in 2024 under Rocky Harris. The allocation process consolidates NGB grants into a single simultaneous evaluation — Summer and Winter separately — with decisions tied explicitly to medal probability, revenue across the quad, and strategic plan priorities.

This repository formalizes that logic analytically using three interlocking models:

- **Monte Carlo simulation** — probability distributions over Olympic and Paralympic outcomes for each program. Not point predictions. Distributions that capture the difference between a narrow-interval consistent performer and a wide-interval high-variance program.
- **LP optimization** — given a budget constraint, which combination of NGBs maximizes expected medals. The efficient frontier shows where additional investment stops buying additional outcomes. The shadow price on the budget constraint tells you exactly what one more dollar is worth.
- **Preparation gap analysis** — programs entering their first Games with dominant pre-Games records carry a structural readiness gap that statistical dominance alone cannot close. The model flags this as the highest-return target for proactive preparation investment.

---

## Four Games Horizons

| Games | Type | Key Thesis |
|-------|------|------------|
| **LA 2028** | Summer Olympic | Home soil. Breakout programs from Paris 2024 are the primary Development thesis. Volleyball, gymnastics, track anchor the portfolio. |
| **French Alps 2030** | Winter Olympic | Milan 2026 as analytical baseline. Preparation gap from 2026 informs 2030 capital allocation. Figure skating, snowboard, ice hockey. |
| **LA 2028** | Summer Paralympic | Classification-stable programs in Swimming and Athletics carry highest medal probability. Sitting Volleyball and Wheelchair Basketball are maintenance capital. |
| **French Alps 2030** | Winter Paralympic | Thinnest data in the portfolio. Sled Hockey is the anchor maintenance program. Para Alpine carries the Protect thesis. |

---

## Investment Theses

| Thesis | Logic | Capital implication |
|--------|-------|-------------------|
| **Protect** | Dominant program, first Olympics. Preparation gap is structurally present. | Highest ROI on targeted readiness investment before the Games. |
| **Develop** | Ascending program. Breakout trajectory, high variance. | Invest ahead of the curve. Higher ceiling, wider outcome distribution. |
| **Maintain** | Perennially dominant. Medal probability high but stable. | Protect the floor. Marginal return on additional capital is low. |

---

## The Harris Framework

Rocky Harris described USOPC's 2024 allocation overhaul as portfolio investment optimization. Three allocation inputs:

1. **Medal probability** — IRR equivalent. Primary return metric.
2. **Revenue across the quad** — commercial value of the NGB and its athletes.
3. **Cost to field the team** — determines capital efficiency.

83% of quad resources flow directly to athlete programs.

**What the model adds:** Harris's framework is qualitative. This model makes it computational — running Monte Carlo simulations on medal probability, applying LP optimization across the full program portfolio, and generating an efficient frontier that shows exactly where the marginal value of additional capital diminishes to zero. The preparation gap analysis adds a fourth input: the systematic underperformance risk that [Kiss and Cry](https://medium.com) identified across generational favorites at the Games.

---

## Repository Structure

```
app.py                          ← Streamlit app (4-game dropdown, PE framing throughout)
requirements.txt

/notebooks
  usopc_public_LA2028.ipynb     ← Summer Olympic analysis
  usopc_public_Winter2030.ipynb ← Winter Olympic analysis

/data/demo
  archetypes.csv                ← Composite archetype reference profiles

/docs
  harris_framework.md           ← USOPC allocation process + Paralympic extension
  archetype_key.md              ← Archetype definitions and investment implications
```

---

## Archetype System

All athlete data uses **composite archetypes** — pattern-based profiles derived from multiple athletes across multiple Games cycles. No individual is named or identifiable.

| Code | Pattern | Investment Implication |
|------|---------|----------------------|
| `DOMINANT_FIRST` | Top pre-Games record, no prior Olympics | Highest preparation gap — readiness investment priority |
| `DOMINANT_EXP` | Top pre-Games record, experienced | Maintenance — protect the floor |
| `ASCENDING` | Post-breakout trajectory | Development — invest ahead of the curve |
| `MAINTENANCE` | Perennially dominant program | Floor protection — low marginal return |
| `VOLATILE` | High variance, inconsistent | Consistency investment most valuable |
| `DEVELOPMENT` | Emerging program | Long-horizon bet — low floor, high ceiling |

---

## Deploy

```bash
# Clone and run locally
pip install -r requirements.txt
streamlit run app.py

# Deploy to Streamlit Cloud
# share.streamlit.io → connect GitHub → select repo → app.py → Deploy
```

---

## Author

Matt | AI Product Manager | Olympic analytics

[Kiss and Cry: The Favorite Gap](https://medium.com) — the essay that motivated this model

*Named athlete data and full validation results are maintained in a private repository.*

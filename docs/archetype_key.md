# Archetype Key

Composite archetypes represent cross-athlete, cross-cycle performance patterns. Each archetype is derived from multiple historical instances sharing the same structural profile.

---

## DOMINANT_FIRST

**Pattern:** Objectively dominant pre-Games record. Long win streak. Zero prior Olympic experience.

**Key features:**
- `first_olympics = True`
- `win_streak` elevated (typically 4+)
- `consistency_load` high (streak × variance interaction)
- `sentiment` often low — burden of expectation in pre-Games statements
- Wide prediction interval despite high mean

**Investment implication:** Highest preparation gap. The gap between competitive dominance and Olympic readiness is not closed by more training — it requires specific psychological preparation and stress inoculation. This is where proactive support investment has the highest expected return.

**Historical basis:** Multiple disciplines, multiple cycles. The pattern repeats.

---

## DOMINANT_EXP

**Pattern:** Dominant pre-Games record with prior Olympic experience.

**Key features:**
- `first_olympics = False`
- `prior_olympics >= 1`
- Narrow prediction interval
- High sentiment — preparation complete

**Investment implication:** Maintenance. Protect the floor. The preparation gap is closed. Marginal return on additional investment is low — resources better deployed elsewhere.

---

## ELITE_RETURN

**Pattern:** Elite athlete returning to competition after adversity, withdrawal, or significant interruption.

**Key features:**
- High `seasons_elite` (deep experience)
- Prior Olympic medals
- Wide prediction interval — outcome highly support-dependent
- `ascending = True` post-return

**Investment implication:** High variance. When support investment is adequate, outcome approaches pre-adversity level. When support is insufficient, outcome is unpredictable. Highest leverage for targeted psychological services investment.

---

## ASCENDING

**Pattern:** Program on upward trajectory. Recent breakout result. Short elite career.

**Key features:**
- Low `seasons_elite`
- `ascending = True`
- Improving trend across recent seasons
- Often `first_olympics = True`

**Investment implication:** Development thesis. Invest ahead of the curve. Higher variance, higher ceiling. LA 2028 is the primary horizon for this archetype — programs that produced breakout results at Paris 2024.

---

## MAINTENANCE

**Pattern:** Perennially dominant program. Medal near-certain every cycle.

**Key features:**
- High `prior_olympics`
- Low `cv_pre` (consistent)
- P(medal) approaches 0.90+ every cycle
- Shadow price on budget constraint is low at current investment level

**Investment implication:** Protection investment. The efficient frontier flattens here — additional dollars do not meaningfully increase expected medals. Resources are better deployed toward ASCENDING or DOMINANT_FIRST archetypes.

**The hockey analogy:** A program with a 0.95 P(medal) every cycle still needs investment to maintain that floor against improving international competition. But the marginal return on *additional* investment above maintenance level is low.

---

## VOLATILE

**Pattern:** High pre-Games average, high variance. Inconsistent results. Medal or DNF — rarely middle.

**Key features:**
- High `cv_pre` (coefficient of variation)
- Wide prediction interval
- `std_pre` elevated
- DNF or withdrawal in historical record

**Investment implication:** Consistency training most valuable. The problem is not capability — it is reliability under pressure. Periodization and technical consistency investment narrows the distribution without necessarily raising the mean.

---

## DEVELOPMENT

**Pattern:** Emerging athlete. Short elite career. No Olympic history.

**Key features:**
- Low `seasons_elite`
- `first_olympics = True`
- Lower `mean_pre` relative to field
- High `ascending` potential

**Investment implication:** Long-horizon bet. Low floor, high ceiling. The LP model typically does not select DEVELOPMENT archetypes at current budget levels — they enter the portfolio as budget expands. The efficient frontier identifies the exact budget point where development investment becomes worthwhile.

---

## Using Archetypes in the LP Model

The LP optimization selects a portfolio of archetypes — not individuals — to maximize expected medals within a budget constraint.

The shadow price on the budget constraint answers: at the current funding level, what is one additional dollar worth in expected medals?

- **High shadow price:** Budget is the binding constraint. There are fundable programs still waiting. Additional capital buys real medal probability.
- **Low shadow price:** The frontier is nearly flat. Only marginal programs remain unfunded. Additional capital has diminishing returns.
- **Shadow price of zero:** Every program worth funding is funded. Additional capital has no effect on expected medals.

Reading the shadow price column down the efficient frontier identifies the inflection point — the budget level above which marginal returns flatten. That is the analytically defensible funding floor.

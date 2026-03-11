# The Harris Portfolio Framework

## What Changed in 2024

Rocky Harris, USOPC Chief of Sport & Athlete Services, overhauled the NGB funding allocation process starting in 2024.

**Before:** NGBs received 11 different grants through an opaque process. Decisions were made without NGBs understanding the criteria. Grants arrived without explanation.

**After:** All grants consolidated into a single simultaneous request process — Summer and Winter evaluated separately. NGBs submit all requests at once. Decisions are explained in person. The rationale is transparent.

Harris described the new approach explicitly as portfolio investment optimization:

> "We've brought all that together into one team that is going to focus on investing in national governing bodies like it's a portfolio of investments."

The allocation logic rests on three inputs:
1. **Likely revenue across the quad** — commercial value of the sport and its athletes
2. **Cost to send a team to the Games** — operational investment required
3. **Strategic plan priorities** — where USOPC needs to build or maintain competitive standing

83% of quad resources go directly toward programs supporting athletes.

---

## The Analytical Gap This Framework Creates

Harris's framework is a portfolio investment thesis stated in qualitative terms. The three inputs — revenue, cost, strategic priority — are described but not weighted, not scored, and not optimized across the full NGB portfolio simultaneously.

The result is a process that is transparent and intentional but not yet computational. Allocation decisions depend on judgment, negotiation, and institutional knowledge rather than a consistent quantitative framework.

This is the gap this repository addresses.

---

## What the Model Adds

**Input 1 — Revenue across the quad:** Not yet modeled. This is the next analytical layer. Understanding which NGBs and athletes generate the commercial return that funds the system requires separate revenue modeling. The model flags this gap explicitly.

**Input 2 — Cost to send a team:** Captured in the `cost` parameter per athlete/NGB. The LP optimization runs against a budget constraint that reflects relative investment required.

**Input 3 — Strategic priorities:** Captured through the archetype system and the trajectory component. `ASCENDING` archetypes represent programs where strategic investment ahead of LA 2028 or French Alps 2030 is the priority. `MAINTENANCE` archetypes represent programs where protecting existing competitive standing is sufficient.

**Medal probability:** Not in Harris's stated three inputs, but implicit in "likely revenue" (medal-winning athletes generate more commercial value) and "strategic plan priorities" (medals are the mission). The Monte Carlo simulation makes this explicit.

---

## The Portfolio Logic Harris Described

> "In some sports, if an athlete has already risen to the top, fewer resources go to that NGB versus one with seven athletes who could medal."

This is the core LP insight. A dominant athlete in a sport where the medal is near-certain does not generate the same marginal return on investment as seven athletes approaching the medal threshold simultaneously.

The model captures this through:
- Shadow price on the budget constraint — marginal value of one more dollar at current allocation
- Reduced costs per archetype — how far below the selection threshold each non-selected archetype sits
- Efficient frontier — where the curve flattens and additional investment stops buying medals

The flattening point is the analytically defensible answer to Harris's implicit question: how much is enough for the dominant program, and where does the next dollar go?

---

## The Preparation Gap Extension

Harris's framework addresses NGB-level allocation. The model extends it to athlete-level preparation investment within an NGB.

The `DOMINANT_FIRST` archetype finding — that the most dominant pre-Games athlete profile carries the widest outcome distribution when Olympic experience is zero — is not captured in revenue, cost, or strategic priority as typically stated.

It suggests a fourth input: **preparation readiness**. The gap between competitive dominance and Olympic readiness is a structural risk that NGB-level investment decisions should account for, not just athlete-level training budgets.

The policy simulation in Section 5 of the notebooks models what happens to P(medal) when stress inoculation and psychological preparation investment is applied to `DOMINANT_FIRST` archetypes. The counterfactual is the clearest argument for including preparation readiness as a formal allocation input.

---

## Paralympic Extension

The 2024 allocation overhaul explicitly extended the portfolio investment model to Paralympic sport. The USOPC serves as both the National Olympic Committee and National Paralympic Committee — the same three-input framework applies across both programs.

The analytical challenge is harder in Paralympic sport:
- **Classification volatility** — athletes can be reclassified between Games cycles, disrupting historical baselines
- **Equipment dependency** — performance distributions in wheelchair and adaptive disciplines are partially a function of equipment investment, not athlete preparation alone
- **Thinner data** — fewer international competitions, smaller fields, and shorter competitive histories make medal probability estimation less reliable

The model addresses this by widening standard deviation parameters for Paralympic archetypes and flagging preparation gap calculations as higher-uncertainty estimates. The framework is the same; the confidence intervals are wider.

**Programs covered in this repository:**
- LA 2028 Summer Paralympic: Swimming, Athletics, Wheelchair Basketball, Cycling, Sitting Volleyball, Archery, Rowing
- French Alps 2030 Winter Paralympic: Alpine, Biathlon, Cross-Country, Sled Hockey, Wheelchair Curling

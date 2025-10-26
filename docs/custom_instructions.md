# Custom Instructions for Dynasty Oracle LLM

**Persona:** You are a world-class dynasty fantasy football analyst named 'Dynasty Oracle.' Your purpose is to provide users with insightful, data-driven, and strategic advice to help them win their dynasty leagues. You are analytical, forward-thinking, and objective.

**Core Directives:**
1.  **Data First:** Your primary source of truth for player market value, age, team, and contract status is the `dynasty_market_data.csv` file in your knowledge base. Always refer to this data when answering questions about player value or trades.
2.  **Strategic Context:** Use the strategy and analytics articles in your knowledge base (`strategy_*.txt`, `analytics_*.txt`) to frame your analysis. Don't just state a player's value; explain *why* they have that value based on their age, contract, and strategic archetype.
3.  **Explain the 'Why':** Never just give an answer. Explain the reasoning behind it. Reference concepts like age curves, contending/rebuilding windows, draft capital, and advanced metrics.
4.  **Acknowledge Data Limitations:** Your data is updated periodically. If a user asks about a very recent event (e.g., a trade or injury that happened today), state that your knowledge files may not yet reflect the latest information and advise them based on the principles you know.
5.  **Use LaTeX for Clarity:** For any formulas, metrics, or mathematical representations, use LaTeX formatting (e.g., $YPRR = \frac{\text{Yards}}{\text{Routes Run}}$).

---

# Knowledge Base

## Analytics: Key Advanced Metrics in Dynasty
Yards Per Route Run (YPRR):
YPRR measures a receiver’s efficiency by dividing total receiving yards by the number of routes run. It captures both opportunity and productivity, making it a strong predictor of future success.
Formula: $YPRR = \frac{\text{Yards}}{\text{Routes Run}}$
Target Share:
Target share is the percentage of a team’s total pass attempts that go to a specific player. High target share indicates a player is a focal point of the offense, which is especially important for wide receivers and tight ends.
Formula: $\text{Target Share} = \frac{\text{Player Targets}}{\text{Team Pass Attempts}}$
Air Yards Share:
Air yards represent the total distance the ball travels in the air toward a receiver. Air yards share is the percentage of a team’s total air yards that a player accounts for, highlighting deep-threat ability and offensive role.
Formula: $\text{Air Yards Share} = \frac{\text{Player Air Yards}}{\text{Team Air Yards}}$
Breakaway Run Rate:
For running backs, breakaway run rate measures the percentage of carries that go for 15+ yards. It reflects a player’s explosiveness and big-play potential, which can separate elite backs from the rest.
Formula: $\text{Breakaway Run Rate} = \frac{\text{Breakaway Runs}}{\text{Total Carries}}$
Summary:
Incorporating these metrics into your analysis allows for a more nuanced understanding of player value and upside. They help identify breakout candidates, spot declining assets, and make more informed trade and draft decisions.

## Dynasty Strategy: Understanding Age Curves
Age curves are a foundational concept in dynasty fantasy football, as player value is closely tied to career trajectory and longevity. Each position—quarterback (QB), running back (RB), wide receiver (WR), and tight end (TE)—has a unique age curve that influences how managers should value players.
Quarterbacks (QB):
QBs generally have the longest productive careers in fantasy football. Elite quarterbacks can maintain top-tier performance into their mid-to-late 30s, thanks to the position’s reliance on experience, decision-making, and less physical wear compared to skill positions. Value peaks for QBs often occur between ages 25-32, but top options can remain valuable well beyond that window.
Running Backs (RB):
RBs have the shortest and most volatile value curves. Most running backs peak between ages 22-26, with a sharp decline often beginning after age 27. The physical demands of the position—frequent contact, high injury risk, and team tendency to rotate backs—make RB value fragile. Even elite talents can see rapid value drops due to injury or changes in usage. Dynasty managers should be cautious about investing heavily in older RBs and should look to sell before the decline.
Wide Receivers (WR):
WRs typically break out in their second or third season and can sustain high-level production into their late 20s and early 30s. The value curve is less steep than RBs, with many top receivers remaining fantasy-relevant through age 30. However, athleticism and target volume are key, and a decline in either can signal a downturn.
Tight Ends (TE):
TEs often develop more slowly, with many not reaching their fantasy peak until age 25-28. Once established, elite TEs can remain productive into their early 30s, especially if they are key parts of their team’s passing attack. The scarcity of difference-makers at the position can extend the value window for top TEs.
Summary:
Understanding age curves helps dynasty managers anticipate value shifts and make informed decisions about when to buy, hold, or sell players. Running backs are the most fragile assets, while quarterbacks and tight ends can offer longer-term stability. Wide receivers provide a balance of longevity and upside, making them cornerstone assets for many dynasty rosters.

## Dynasty Strategy: Rebuilding vs. Contending
In dynasty fantasy football, your approach to roster management is shaped by your team's competitive window. The two primary strategies—rebuilding and contending—require distinct mindsets, player targets, and asset management philosophies.
Rebuilding:
A rebuilding team is not positioned to win the championship in the current season. The focus is on accumulating assets that will appreciate in value over time. This means targeting young players with upside, acquiring future rookie draft picks, and being patient with player development. Rebuilders should be willing to trade away aging veterans, especially those whose value is likely to decline before the team is ready to compete. The goal is to maximize roster value and flexibility, even if it means sacrificing short-term points.
Key tactics for rebuilding include:
- Trading productive veterans for draft picks or young, unproven players.
- Prioritizing players with high draft capital, athletic profiles, or those entering their second or third NFL seasons.
- Accumulating multiple first- and second-round picks in upcoming rookie drafts.
- Avoiding investments in players with declining roles or expiring contracts.
Contending:
A contending team is built to win now. The focus shifts to maximizing weekly point production and minimizing risk. Contenders should target proven producers, especially those in stable situations with secure roles. While age and long-term value matter, the priority is players who can help win a championship in the current or upcoming season.
Key tactics for contending include:
- Trading future draft picks for established starters.
- Acquiring veterans who may be undervalued due to age but still produce at a high level.
- Prioritizing depth to withstand injuries and bye weeks.
- Monitoring the waiver wire for short-term contributors.
Mindset:
Rebuilders must be patient and disciplined, resisting the urge to chase points in a lost season. Contenders should be aggressive, willing to sacrifice future value for present gains. The best dynasty managers regularly reassess their team’s trajectory and pivot between strategies as circumstances change.
Ultimately, understanding your team’s timeline and acting accordingly is the foundation of successful dynasty play.

## Dynasty Strategy: Valuing Rookie Draft Picks
Rookie draft picks are the lifeblood of dynasty roster construction, offering managers the chance to infuse their teams with young, high-upside talent. However, not all picks are created equal, and their value fluctuates throughout the year.
Early, Mid, and Late Picks:
- Early 1st Round: These picks (typically 1.01–1.03) are the most valuable, often yielding elite prospects with high draft capital and clear paths to opportunity. They are cornerstone assets and can command proven veterans in trades.
- Mid 1st Round: Picks in the 1.04–1.07 range still offer strong upside but come with more uncertainty. These are ideal for targeting players who may have slipped due to landing spot concerns or positional value.
- Late 1st and 2nd Round: These picks are more volatile, often used on players with upside but greater risk. They are valuable for depth or as trade sweeteners but less likely to yield immediate starters.
- 3rd Round and Later: These picks are dart throws, best used to target high-upside prospects or to move up in the draft.
Seasonal Value Fluctuations:
Draft pick value peaks in the weeks leading up to the rookie draft, when managers are most optimistic about incoming prospects. During the season, picks can be undervalued as teams focus on immediate production. Savvy managers acquire picks during the season from contenders and sell or use them to move up the board during draft season.
Framework for Valuing Picks:
- Consider your team’s timeline: picks are more valuable to rebuilding teams.
- Use picks to acquire young, ascending players or to move up for elite prospects.
- Don’t be afraid to trade picks for proven production if you’re contending.
- Monitor class strength: not all draft classes are equal, and future picks may gain or lose value based on early scouting reports.
Conclusion:
Draft picks are flexible assets that can accelerate a rebuild or push a contender over the top. Understanding their value in context—and how it changes throughout the year—is key to successful dynasty management.

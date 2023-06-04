match1 = '<div class="match-container initial-view" data-team1="Verona" data-team2="Empoli"><div class="prob-header upcoming"><span>win</span><span class="tie">draw</span></div><table><tbody><tr class="match-top"><td class="date" rowspan="2"><div>28/5</div></td><td class="team" data-str="Verona"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><div class="name">Verona</div></div></td><td class="prob" style="background-color:#ffc244">46%</td><td class="prob tie-prob" rowspan="2"><div style="background-color:#ffde76">27%</div></td></tr><tr class="match-bottom"><td class="team" data-str="Empoli"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i(1)" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><span class="name">Empoli</span></div></td><td class="prob" style="background-color:#ffe078">26%</td></tr></tbody></table></div>'

match2 = '<div class="match-container initial-view" data-team1="Verona" data-team2="Empoli"><div class="prob-header upcoming"><span>win</span><span class="tie">draw</span></div><table><tbody><tr class="match-top"><td class="date" rowspan="2"><div>28/5</div></td><td class="team" data-str="Verona"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><div class="name">Verona</div></div></td><td class="prob" style="background-color:#ffc244">46%</td><td class="prob tie-prob" rowspan="2"><div style="background-color:#ffde76">27%</div></td></tr><tr class="match-bottom"><td class="team" data-str="Empoli"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i(1)" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><span class="name">'

match3 = '<div class="match initial-view" data-team1="Verona" data-team2="Empoli"><div class="prob-header upcoming"><span>win</span><span class="tie">draw</span></div><table><tbody><tr class="match-top"><td class="date" rowspan="2"><div>28/5</div></td><td class="team" data-str="Verona"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><div class="name">Verona</div></div></td><td class="prob" style="background-color:#ffc244">46%</td><td class="prob tie-prob" rowspan="2"><div style="background-color:#ffde76">27%</div></td></tr><tr class="match-bottom"><td class="team" data-str="Empoli"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i(1)" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><span class="name">Empoli</span></div></td><td class="prob" style="background-color:#ffe078">26%</td></tr></tbody></table></div>'

match4 = ''

match5 = '<div class="match-container initial-view" data-team1="Verona" data-team2="Empoli"><div class="prob-header upcoming"><span>win</span><span class="tie">draw</span></div><table><tbody><tr class="match-top"><td class="date" rowspan="2"><div>28/5</div></td><td class="team" data-str="Verona"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><div class="name">Verona</div></div></td><td class="prob" style="background-color:#ffc244">46%</td><td class="prob tie-prob" rowspan="2"><div style="background-color:#ffde76">27%</div></td></tr><tr class="match-bottom"><td class="team" data-str="Empoli"><div class="logo"><img src="./Predicciones de clubes de fútbol _ FiveThirtyEight_files/i(1)" alt="team-logo" onerror="this.onerror=null; this.src="https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&amp;w=56";" class="loading" data-was-processed="true"></div><div class="team-div" style="top: 0px;"><span class="name"></span></div></td><td class="prob" style="background-color:#ffe078"></td></tr></tbody></table></div>'

match1_result = {
    "home_team":"Verona",
    "away_team":"Empoli",
    "odds_HOME": round(100/46,2),
    "odds_DRAW": round(100/27,2),
    "odds_AWAY": round(100/26,2),
}

match2_result = {
    "match":1,
    "home_team":"Verona",
    "away_team":"Empoli",
    "odds_HOME": round(100/46,2),
    "odds_DRAW": round(100/27,2),
}

match3_result = {
    "home_team":"Test City",
    "away_team":"Test Utd",
    "odds_HOME": 3.1,
    "odds_DRAW": round(100/27,2),
    "odds_AWAY": round(100/26,2),
}

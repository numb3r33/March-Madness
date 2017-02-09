import numpy as np
from utility import expected

def get_teams_in_season(season):
	reg_season_shape = len(season)
	reg_season_1D    = season[['Wteam', 'Lteam']].values\
						   .reshape(reg_season_shape * 2, 1).squeeze()

	all_teams = np.unique(reg_season_1D)
	return all_teams


def rate_team_for_season(season, ratings):
	"""
	Assign elo ratings to teams
	:param teams: All teams in the season
	"""
	teams = get_teams_in_season(season)

	for i in range(len(season)):
		row = season.iloc[i,2:7]

		Wteam = row.Wteam
		Lteam = row.Lteam
		Wscore = row.Wscore
		Lscore = row.Lscore
		# wloc   = row.Wloc
		score_diff = Wscore - Lscore

		mov_multiplier = ((score_diff + 3) ** 0.8) / \
							   (7.5 + .006*(ratings[Wteam] - ratings[Lteam]))

		expected_score_wteam = expected(ratings[Wteam], ratings[Lteam])
		expected_score_lteam = expected(ratings[Lteam], ratings[Wteam])

		actual_score_Wteam   = 1
		actual_score_Lteam   = 0


		ratings[Wteam] = ratings[Wteam] + 10 * (actual_score_Wteam - expected_score_wteam)
		#+ mov_multiplier * (score_diff)

		# if wloc == 'H':
			# ratings[Wteam] += 5 # 5 extra elo points

		ratings[Lteam] = ratings[Lteam] + 10 * (actual_score_Lteam - expected_score_lteam)

	for team in teams:
		ratings[team] = (0.75 * ratings[team]) + (0.25 * 1505)

	return ratings

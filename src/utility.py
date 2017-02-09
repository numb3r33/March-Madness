import numpy as np

def expected(A, B):
		"""
		Calculate expected score of A in a match against B
		:param A: Elo rating for player A
		:param B: Elo rating for player B
		"""
		return 1 / (1 + 10 ** ((B - A) / 400))


def get_all_teams(reg_season_compact):
	reg_season_shape = len(reg_season_compact)
	reg_season_1D    = reg_season_compact[['Wteam', 'Lteam']].values\
						   .reshape(reg_season_shape * 2, 1).squeeze()

	all_teams = np.unique(reg_season_1D)
	return all_teams

def predict(sub, elo_ratings):
	predictions = []

	for id_, pred in zip(sub['id'], sub['pred']):
		season, team_1, team_2 = id_.split('_')
		team_1 = int(team_1)
		team_2 = int(team_2)

		if team_1 < team_2:
			predictions.append(expected(elo_ratings[team_1],
											   elo_ratings[team_2]))
		else:
			predictions.append(expected(elo_ratings[team_2],
											   elo_ratings[team_1]))

	return predictions

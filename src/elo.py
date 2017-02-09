import numpy as np


class Season:
	def __init__(self, season_perf):
		self.season_perf = season_perf

	def get_teams_in_season(self):
		season_perf_shape = len(self.season_perf)
		season_perf_1D = self.season_perf[['Wteam', 'Lteam']].values.reshape(season_perf_shape * 2, 1).squeeze()
		self.teams = np.unique(season_perf_1D)

		return self.teams

	def get_opponents_list(self):
		opponents = {} # maintains list of opponents for every team

		for team in self.teams:
			winning_mask = self.season_perf.Wteam == team
			losing_mask  = self.season_perf.Lteam == team

			opponents[team]  = self.season_perf.loc[winning_mask, 'Lteam'].tolist() + \
						 self.season_perf.loc[losing_mask, 'Wteam'].tolist()

		self.opponents = opponents
		return opponents

	def get_actual_performance(self, opponents):
		self.actual_perf = {}
		winning_perf = self.season_perf.groupby('Wteam').size().to_dict()

		for team in opponents.keys():
			if team in winning_perf:
				self.actual_perf[team] = winning_perf[team]
			else:
				self.actual_perf[team] = 0

		return self.actual_perf

	@staticmethod
	def expected(A, B):
		"""
		Calculate expected score of A in a match against B
		:param A: Elo rating for player A
		:param B: Elo rating for player B
		"""
		return 1 / (1 + 10 ** ((B - A) / 400))

	def get_expected(self, ratings, opponents):
		expected_perf = {}

		for k, opp in opponents.items():
			score = 0
			for team in opp:
				score += Season.expected(ratings[k], ratings[team])

			expected_perf[k] = score

		self.expected_perf = expected_perf

		return expected_perf

	def elo(self, old, exp, score, k=10):
		"""
		Calculate the new Elo rating for a player
		:param old: The previous Elo rating
		:param exp: The expected score for this match
		:param score: The actual score for this match
		:param k: The k-factor for Elo (default: 32)
		"""
		return old + k * (score - exp)

	def winning_loc_advantage(self, team):
		mask = self.season_perf.Wteam == team

		return ((self.season_perf.loc[mask, 'Wloc'] != 'H').astype(np.int)).sum() * 5

	def update_ratings(self, ratings):
		for team in self.actual_perf.keys():
			new_rating = self.elo(ratings[team],
									 self.expected_perf[team],
									 self.actual_perf[team])

			location_advantage = self.winning_loc_advantage(team)
			print('Location advantage ', location_advantage)
			ratings[team] = (0.25 * 1505) + (.75 * new_rating) + location_advantage

		return ratings



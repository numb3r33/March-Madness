class Season:
	"""
	Represents regular season with all the details
	after year 2003.
	"""

	def __init__(self, perf, year):
		"""
		:param perf: Performance data for this season
		:param year: Year of the season
		"""

		self.perf = perf
		self.year = year

	def get_total_wins(self, team_id):
		"""
		Gets total number of wins in a season for a team
		"""
		mask = self.perf.Wteam == team_id

		return len(self.perf.loc[mask])

	def get_total_losses(self, team_id):
		"""
		Gets total number of losses in a season for a team
		"""
		mask = self.perf.Lteam == team_id

		return len(self.perf.loc[mask])

	def get_total_games(self, team_id):
		"""
		Gets total number of games played by a team in a season
		"""
		return self.get_total_wins(team_id) + self.get_total_losses(team_id)

	def get_year(self):
		return self.year


class Settings():
	"""所有设置的类"""
	def __init__(self):	
		#屏幕设置
		self.screenwidth = 1366
		self.screenheight = 768
		self.color = (255,255,255)

		#飞船设置
		self.ship_limit = 3

		#子弹设置
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullet_allowd = 10

		#外星人设置
		self.alien_drop_speed = 10
		self.score_scale = 1.5

		#游戏节奏
		self.speedup_scale = 1.1
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1.0
		self.fleet_direction = 1
		self.aliens_points = 50

	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.aliens_points = int(self.score_scale*self.aliens_points)
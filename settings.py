import easycolors as ec
import pygame
import math

class Settings:
	"""Class for game settings"""

	def __init__(self, game):
		"""Init. game settings"""
		# Window settings
		self.screen_width, self.screen_height = 1200, 600
		self.bg_color = ec.transform(ec.darkgrey, 0)
		self.gr_color = ec.transform(ec.darkgrey, -20)
		self.FPS = 60
		self.DRAWAIMLINE = False
		self.DRAWCURSOR = True
		self.game = game


		self.speed = 0.01		# a speed value applied to a lot of stuff
		self.rotate_speed = 1	# rotation speed
		self.walk_speed = 1.5	# walking speed
		self.thrust = 0.06*100	# thrust of jetpack
		self.thrust2 = 0.12		# thrust of jetpack if going down
		self.jumpboost = 2		# boost applied when jumping
		self.ground_friction = 0.03 # friction of ground 
		self.air_friction = 0.01	# air friction
		self.g = 0.04	# gravity vector applied

		self.xthrustdivider = 50	
		self.ythrustdivider = 100
		self.max_rotation = 30
		self.yvector_min = -6
		self.yvector_max = 2

		self.takeoff_boost_time = 0.45 # sec
		self.max_thrust = 10 # sec
		self.fuel_recharge_time = 15 # sec 
		self.time_until_recharge = 3 # sec
		self.min_thrust = 2 # of max_thrust
		self.thrust_is_zero = 0.02

		self.max_health = 100
		self.fall_damage_scalar = 3

		self.falling_hurts_speed = -4
		self.skylimit = 50
		self.gr_height = 550
		self.gravity = True
		self.player_start_pos = (200, self.gr_height - 100)

		# image settings
		self.player_image_size_multiplier = 4
		self.cursor_image_size_multiplier = 1

		# cursor
		self.aim_color = ec.red
		self.aim_line_length = 150
		self.facingleft = False


		# BULLET SETTINGS
		self.bullet_width = 4
		self.bullet_height = 60
		self.max_bullets = 10
		self.bullet_speed = 70
		self.bullet_color = ec.red
		self.max_dispersion = math.radians(5)
		self.reload_time = 3 # secs


		# CAM SETTINGS
		self.cam_start_x = 0
		self.cam_start_y = 0


		# SOUNDS
		# shoot
		self.shoot_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/shoot-04.wav')
		pygame.mixer.Sound.set_volume(self.shoot_sound, 0.5)
		self.shoot_sound_channel = 0
		# bullet hit wall
		self.wall_hit_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/open-00.wav')
		pygame.mixer.Sound.set_volume(self.wall_hit_sound, 0.5)
		self.wall_hit_sound_channel = 1
		# jump
		self.jump_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/jump-00.wav')
		pygame.mixer.Sound.set_volume(self.jump_sound, 0.5)
		self.jump_sound_channel = 2
		# walk
		self.walk_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/step-00.wav')
		pygame.mixer.Sound.set_volume(self.walk_sound, 0.7)
		self.walk_sound_channel = 3
		# thrust
		self.thrust_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/fire-03.wav')
		pygame.mixer.Sound.set_volume(self.thrust_sound, 0.4)
		self.thrust_sound_channel = 4
		# low thrust
		self.low_thrust_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/fire-03.wav')
		pygame.mixer.Sound.set_volume(self.low_thrust_sound, 0.2)
		self.low_thrust_sound_channel = 4
		# reload
		self.reload_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/reload-00.wav')
		pygame.mixer.Sound.set_volume(self.reload_sound, 0.3)
		self.reload_sound_channel = 5
		# hurt
		self.hurt_sound = pygame.mixer.Sound(f'{self.game.DIR}/sounds/hurt-00.wav')
		pygame.mixer.Sound.set_volume(self.hurt_sound, 0.3)
		self.hurt_sound_channel = 6


		# FONTS
		# ammo
		self.ammo_font = pygame.font.Font(f'{self.game.DIR}/art/font-00.TTF', 20)

	def fpstrans(self, value):
		return value * (120/self.FPS)
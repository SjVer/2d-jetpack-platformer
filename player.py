import pygame, math, time
import easycolors as ec
from soundplayer import *

class Player:
	"""class for player"""

	def __init__(self, game):
		"""Init. attributes"""
		# Get attributes from main class
		self.WIN = game.WIN
		self.settings = game.settings
		self.screen_rect = game.WIN.get_rect()
		self.game = game

		self.ALIGN_TO_CAM = True

		# load player images
		self.image = pygame.image.load(f'{self.game.DIR}/art/player.png')
		self.image2 = pygame.image.load(f'{self.game.DIR}/art/player2.png')
		self.image3 = pygame.image.load(f'{self.game.DIR}/art/player3.png')
		self.image3_1 = pygame.image.load(f'{self.game.DIR}/art/player3_1.png')
		self.rect = self.image.get_rect()
		# resize
		w, h = self.rect.width*self.settings.player_image_size_multiplier, self.rect.height*self.settings.player_image_size_multiplier
		self.image = pygame.transform.scale(self.image, (w, h))
		self.image2 = pygame.transform.scale(self.image2, (w, h))
		self.image3 = pygame.transform.scale(self.image3, (w, h))
		self.image3_1 = pygame.transform.scale(self.image3_1, (w, h))
		self.rect = self.image.get_rect()
		self.new_image = None
		self.new_rect = None

		# load gun image
		self.gun_image = pygame.image.load(f'{self.game.DIR}/art/gun.png')
		self.gun_rect = self.gun_image.get_rect()
		w, h = self.gun_rect.width*self.settings.player_image_size_multiplier, self.gun_rect.height*self.settings.player_image_size_multiplier
		self.gun_image = pygame.transform.scale(self.gun_image, (w, h))
		self.gun_rect = self.gun_image.get_rect
		self.new_gun_image = None
		self.new_gun_rect = None

		# player rect values
		self.rect.center = self.settings.player_start_pos
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		self.r = 0	# rotation

		# vectors
		self.xvector = 0
		self.yvector = 0
		self.rvector = 0

		# misc. vars
		self.thrust_left = self.settings.max_thrust
		self.health = self.settings.max_health

		# set flags
		self.thrusting = False
		self.moving_left = False
		self.moving_right = False
		self.walking_left = False
		self.walking_right = False
		self.rotating_left = False
		self.rotating_right = False
		self.hovering = False
		self.air_friction_on = True
		self.grounded = False
		self.takeoff = False

	def blitme(self):
		"""Draw the player at its current location."""
		selected_image, selected_rect = None, None

		if self.new_image == None:	# if no rotated image blit default
			selected_image, selected_rect = self.image, self.rect
		else: # blit rotated image
			selected_image, selected_rect = self.new_image, self.new_rect

		if self.new_gun_image == None:
			selected_gun_image, selected_gun_rect = self.gun_image, self.gun_rect
		else:
			selected_gun_image, selected_gun_rect = self.new_gun_image, self.new_gun_rect

		if self.ALIGN_TO_CAM:

			oldpos = selected_rect.topleft
			selected_rect.topleft = self.game.cam.align(oldpos)
			self.WIN.blit(selected_image, selected_rect)

			oldpos = selected_gun_rect.topleft
			selected_gun_rect.topleft = self.game.cam.align(oldpos)
			self.WIN.blit(selected_gun_image, selected_gun_rect)

		else:
			self.WIN.blit(selected_image, selected_rect)

	def keymovement(self):
		"""Movement by keys"""
		# THRUSTING
		if self.thrusting and not self.game.recharging:
			# play sound
			if not soundplaying(self, 'thrust_sound'):
				playsound(self, 'thrust_sound')
			# manage thrust left
			if self.game.limited:
				self.thrust_left -= self.settings.fpstrans(1/60)
			# get distance vector
			d = (self.r + 90) * (math.pi / 180) * -1	# get angle (up rel. to player)
			targx = self.settings.thrust * math.cos(d) + self.rect.center[0]	#
			targy = self.settings.thrust * math.sin(d) + self.rect.center[1]

			distvec = (self.rect.center[0] - targx, self.rect.center[1] - targy)
			
			# Apply distance vector
			self.xvector -= self.settings.fpstrans(distvec[0] / self.settings.xthrustdivider)
			if self.yvector < -2:
				self.yvector += self.settings.fpstrans(distvec[1] / (0.5 * self.settings.ythrustdivider))
			else:
				self.yvector += self.settings.fpstrans(distvec[1] / self.settings.ythrustdivider)


		# friction
		if self.air_friction_on:
			# Apply air friction to horizontal movement
			if self.xvector > 0:
				self.xvector -= self.settings.fpstrans(self.settings.air_friction * self.xvector)
			if self.xvector < 0:
				self.xvector += self.settings.fpstrans(self.settings.air_friction * -1 *self.xvector)

		# ROTATING
		if self.rotating_left and self.r < self.settings.max_rotation:
			self.r += self.settings.fpstrans(self.settings.rotate_speed)
		if self.rotating_right and self.r > -1* self.settings.max_rotation:
			self.r -= self.settings.fpstrans(self.settings.rotate_speed)
		
	def vectormovement(self):
		"""Movement by vectors"""
		# Apply gravity to yvector
		if self.settings.gravity and self.yvector - self.settings.fpstrans(self.settings.g) >= self.settings.yvector_min:
			self.yvector -= self.settings.fpstrans(self.settings.g)

		# Move by vectors

		# ON GROUND
		if self.rect.bottom - self.settings.fpstrans(self.yvector) > self.settings.gr_height and self.grounded == False and self.yvector < -1:
			# LANDED
			playsound(self, 'walk_sound')
			if self.yvector <= self.settings.falling_hurts_speed:
				# TAKEN FALLDAMAGE
				if self.game.limited:
					self.health -= self.settings.fall_damage_scalar * -1 * (self.yvector - self.settings.falling_hurts_speed)
				playsound(self, 'hurt_sound')

		if self.rect.bottom - self.settings.fpstrans(self.yvector) > self.settings.gr_height:
			self.grounded = True
			# Set yvector to 0, correct ypos, correct rotation, apply ground friction on xvector
			self.yvector = 0
			self.rect.bottom = self.settings.gr_height
			self.r = 0
			if self.xvector > 0:
				self.xvector -= self.settings.fpstrans(self.settings.ground_friction)
			elif self.xvector < 0:
				self.xvector += self.settings.fpstrans(self.settings.ground_friction)

			# apply walking force on xvector
			if self.walking_left:
				if not soundplaying(self, 'walk_sound'):
					playsound(self, 'walk_sound')

				if self.hovering and self.rect.left - self.settings.fpstrans(self.settings.walk_speed) / 3 > 0:
					self.x -= self.settings.fpstrans(self.settings.walk_speed) / 3

				elif self.rect.left - self.settings.fpstrans(self.settings.walk_speed) > 0:
					self.x -= self.settings.fpstrans(self.settings.walk_speed)

			if self.walking_right:
				if not soundplaying(self, 'walk_sound'):
					playsound(self, 'walk_sound')

				if self.hovering and self.rect.right + self.settings.fpstrans(self.settings.walk_speed) / 3 < self.settings.screen_width:
					self.x += self.settings.fpstrans(self.settings.walk_speed) / 3

				elif self.rect.right + self.settings.fpstrans(self.settings.walk_speed) < self.settings.screen_width:
					self.x += self.settings.fpstrans(self.settings.walk_speed)

		# Hit skylimit
		elif self.rect.top - self.settings.fpstrans(self.yvector) < self.settings.skylimit - 200:
			self.grounded = False
			self.yvector = 0
			self.rect.top = self.settings.skylimit - 200
		else:
			# can freely apply yvector
			self.grounded = False
			self.y -= self.settings.fpstrans(self.yvector)

		# apply rvector to rotation
		self.r += self.settings.fpstrans(self.rvector)

		# Apply xvector to x pos if possible
		if self.rect.left + self.settings.fpstrans(self.xvector) > 0 and self.rect.right + self.settings.fpstrans(self.xvector) < self.settings.screen_width:
			self.x += self.settings.fpstrans(self.xvector)
		else:
			# hit a wall
			self.xvector = 0

	def rotateimage(self):
		# ROTATE OG IMAGE
		if (self.thrusting or (self.hovering and not self.grounded)) and self.thrust_left > 0: # load thrusting image rotated to self.r
			if self.takeoff > 0:
				if self.takeoff/self.settings.FPS > 0.15:
					selected = self.image3
				else:
					selected = self.image3_1
			else:
				selected = self.image2
		else:
			selected = self.image
			# recharge fuel
			addition = 0.05
			if (self.thrust_left + addition <= self.settings.max_thrust):
				if self.game.recharging and self.game.recharging_time >= self.settings.time_until_recharge:
					self.thrust_left += addition
				elif self.game.recharging_time == 0:
					self.thrust_left += addition
			elif self.thrust_left + addition > self.settings.max_thrust:
				self.thrust_left = self.settings.max_thrust

		if self.settings.facingleft:
			self.new_image = pygame.transform.flip(selected, True, False)
		else:
			self.new_image = selected
		self.new_image = pygame.transform.rotate(self.new_image, self.r)
		self.new_rect = self.new_image.get_rect(center=self.rect.center)	# get rect

		# ROTATE AND POSITION GUN IMAGE
		if not self.settings.facingleft:
			angle = math.degrees(self.game.cursor.angle) * -1
			self.new_gun_image = pygame.transform.rotate(self.gun_image, angle)
			self.new_gun_rect = self.new_gun_image.get_rect(center=(self.rect.center[0], self.rect.center[1]-5))
		else:
			angle = math.degrees(self.game.cursor.angle)
			self.new_gun_image = pygame.transform.rotate(self.gun_image, angle)
			self.new_gun_image = pygame.transform.flip(self.new_gun_image, True, False)
			self.new_gun_rect = self.new_gun_image.get_rect(center=(self.rect.center[0], self.rect.center[1]-5))

	def is_hovering(self):
		"""Ëxecuted when hovering"""
		if not self.grounded:
			if not soundplaying(self, 'low_thrust_sound'):
				playsound(self, 'low_thrust_sound')
			# manage thrust left
			if self.game.limited:
				self.thrust_left -= self.settings.fpstrans(1/60)
		# Apply thrust for hovering
		if self.yvector < 0:
			self.yvector += self.settings.fpstrans(self.settings.thrust2 / 0.8)
		# Apply smaller air friction
		if self.xvector > 0:
			self.xvector -= self.settings.fpstrans(self.settings.air_friction * self.xvector / 2)
		if self.xvector < 0:
			self.xvector += self.settings.fpstrans(self.settings.air_friction * -1 *self.xvector / 2)

		# Leaning left/right
		if self.rotating_left:
			self.rotating_right = False
			self.xvector -= self.settings.fpstrans(self.settings.walk_speed / 100)
			if self.yvector > 0:
				self.yvector -= self.settings.fpstrans(self.settings.thrust2 / 1.1)
			else:
				self.yvector -= self.settings.fpstrans(self.settings.thrust2 / 1.5)

		elif self.rotating_right:
			self.rotating_left = False
			self.xvector += self.settings.fpstrans(self.settings.walk_speed / 100)
			if self.yvector > 0:
				self.yvector -= self.settings.fpstrans(self.settings.thrust2 / 1.1)
			else:
				self.yvector -= self.settings.fpstrans(self.settings.thrust2 / 1.5)

		# slowly correct rotation
		if self.r < 0:
			self.r += 0.5
		if self.r > 0:
			self.r -= 0.5

	def update(self):
		"""Update the ship's position based on movement flags."""
		if self.takeoff:
			self.takeoff -= 1
		self.keymovement()	# update movement from user interaction
		self.vectormovement()	# update movement from vectors
		self.rotateimage()
		if self.hovering and not self.thrusting and self.thrust_left > 0:
			self.is_hovering()	# run hovering function

		self.rect.x, self.rect.y = self.x, self.y # update rect pos

		self.blitme()
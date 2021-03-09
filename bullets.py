import pygame, math
from pygame.sprite import Sprite
import easycolors as ec
from random import uniform, randint
from soundplayer import *
 
class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self, game):
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.WIN = game.WIN
		self.settings = game.settings
		self.color = self.settings.bullet_color
		self.game = game

		self.ALIGN_TO_CAM = True

		# load image
		self.image = pygame.image.load(f'{self.game.DIR}/art/lazer.png')
		self.rect = self.image.get_rect()

		# resize image
		#w, h = self.rect.width*self.settings.laser_image_size_multiplier, self.rect.height*self.settings.laser_image_size_multiplier
		w, h = self.settings.bullet_height, self.settings.bullet_width
		self.image = pygame.transform.smoothscale(self.image, (w, h))
		self.rect = self.image.get_rect()

		# rotate image
		if self.game.player.hovering:
			self.a = self.game.cursor.angle
		else:
			added = uniform(0, self.settings.max_dispersion)
			if randint(0, 1):
				self.a = self.game.cursor.angle + added
			else:
				self.a = self.game.cursor.angle - added

		self.image = pygame.transform.rotate(self.image, -1*math.degrees(self.a))
		self.rect = self.image.get_rect()

		# hitbox rect
		self.hitbox = None

		# Create a bullet rect at (0, 0) and then set correct position.
		self.rect.center = (game.player.rect.center[0], game.player.rect.center[1] - 5)
		
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)

		if self.settings.facingleft:
			self.dir = 'left'
		else:
			self.dir = 'right'

		self.vec = self.getvec()

	def getvec(self):
		"""Get vector of bullet"""
		# get distance vector
		targx = self.settings.bullet_speed * math.cos(self.a) + self.rect.center[0]
		targy = self.settings.bullet_speed * math.sin(self.a) + self.rect.center[1]

		return (self.rect.center[0] - targx, self.rect.center[1] - targy)

	def getcorner(self):
		"""Gets correct corner of image rect for hitbox rect"""
		print(self.a)

	def update(self):
		"""Move the bullet"""
		# Apply distance vector
		if self.dir == 'left':
			self.x += self.vec[0]
			self.y += self.vec[1]
		else:
			self.x -= self.vec[0]
			self.y -= self.vec[1]

		# Update the rect position.
		self.rect.x = self.x
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		if self.ALIGN_TO_CAM:
			newrect = self.rect
			newrect.topleft = self.game.cam.align(newrect.topleft) 
			self.WIN.blit(self.image, newrect)
		else:
			self.WIN.blit(self.image, self.rect)

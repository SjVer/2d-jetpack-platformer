import pygame
from time import sleep
import os, sys
import easycolors as ec
from soundplayer import *
import math
from pygame.sprite import Sprite

class Environment:
	"""class for the environment of the game"""

	def __init__(self, game):
		"""init. attributes"""
		# get other attr.
		self.WIN = game.WIN
		self.settings = game.settings
		self.game = game

		# bars
		self.bars_offset = (15,15)
		self.border_width = 2
		self.border_color = ec.white
		self.fillcolor = ec.black
		self.health_bar_length = 300
		self.health_bar_height = 20
		self.health_bar_color = ec.transform(ec.red, -20)
		self.fuel_bar_length = 200
		self.fuel_bar_height = 10
		self.fuel_bar_color = ec.cyan

	def drawammo(self):
		# player ammo
		if self.game.reloading:
			ammotext = self.settings.ammo_font.render(f"Reloading: {float(round(self.game.reload_time_left, 1))}", True, ec.transform(ec.red, -20))
			ammotextrect = ammotext.get_rect()
			ammotextrect.topleft = (self.settings.screen_width - 190, 15)
			self.WIN.blit(ammotext, ammotextrect)
		else:
			if 10 - self.game.fired_since_reload < 10:
				fill = " "
			else:
				fill = ""
			ammotext = self.settings.ammo_font.render(f"Ammo: {fill}{10 - self.game.fired_since_reload}/{self.settings.max_bullets}", True, ec.transform(ec.red, -20))
			ammotextrect = ammotext.get_rect()
			ammotextrect.topleft = (self.settings.screen_width - 180, 15)
			self.WIN.blit(ammotext, ammotextrect)

	def drawbars(self):
		"""draw health and fuel bars"""
		# HEALTH
		pygame.draw.rect(self.WIN, self.fillcolor, (self.bars_offset[0], self.bars_offset[1], self.health_bar_length, self.health_bar_height))
		health_length = self.health_bar_length/self.settings.max_health * self.game.player.health
		health_bar_rect = pygame.Rect(self.bars_offset[0], self.bars_offset[1], health_length, self.health_bar_height)
		pygame.draw.rect(self.WIN, self.health_bar_color, health_bar_rect)

		# FUEL
		pygame.draw.rect(self.WIN, self.fillcolor, (self.bars_offset[0], self.bars_offset[1] + self.health_bar_height + self.border_width, self.fuel_bar_length, self.fuel_bar_height))
		fuel_length = self.fuel_bar_length/self.settings.max_thrust * self.game.player.thrust_left
		fuel_bar_rect = pygame.Rect(self.bars_offset[0], self.bars_offset[1] + self.health_bar_height + self.border_width, fuel_length, self.fuel_bar_height)
		pygame.draw.rect(self.WIN, self.fuel_bar_color, fuel_bar_rect)
		minthrustx = self.fuel_bar_length/self.settings.max_thrust * self.settings.min_thrust + self.bars_offset[0]
		pygame.draw.line(self.WIN, ec.red, (minthrustx, fuel_bar_rect[1]), (minthrustx, fuel_bar_rect[1] + self.fuel_bar_height - self.border_width), self.border_width)
		
		# OUTLINES
		pygame.draw.line(self.WIN, self.border_color, self.bars_offset, (self.bars_offset[0] + self.health_bar_length, self.bars_offset[1]), self.border_width)
		pygame.draw.line(self.WIN, self.border_color, (self.bars_offset[0], self.bars_offset[1] + self.health_bar_height), (self.bars_offset[0] + self.health_bar_length, self.bars_offset[1] + self.health_bar_height), self.border_width)
		pygame.draw.line(self.WIN, self.border_color, self.bars_offset, (self.bars_offset[0], self.bars_offset[1] + self.health_bar_height + self.fuel_bar_height), self.border_width)
		pygame.draw.line(self.WIN, self.border_color, (self.bars_offset[0] + self.health_bar_length, self.bars_offset[1]), (self.bars_offset[0] + self.health_bar_length, self.bars_offset[1] + self.health_bar_height), self.border_width)
		pygame.draw.line(self.WIN, self.border_color, (self.bars_offset[0], self.bars_offset[1] + self.health_bar_height + self.fuel_bar_height), (self.bars_offset[0] + self.fuel_bar_length, self.bars_offset[1] + self.health_bar_height + self.fuel_bar_height), self.border_width)
		pygame.draw.line(self.WIN, self.border_color, (self.bars_offset[0] + self.fuel_bar_length, self.bars_offset[1] + self.health_bar_height), (self.bars_offset[0] + self.fuel_bar_length, self.bars_offset[1] + self.health_bar_height + self.fuel_bar_height), self.border_width)

	def update(self):
		self.drawammo()
		self.drawbars()


class Background(Sprite):
	"""Class for one background part"""

	def __init__(self, game):
		"""init. attributes"""
		super().__init__()
		# get other attr.
		self.WIN = game.WIN
		self.settings = game.settings
		self.game = game

		# background
		self.bg_image = None
		self.LOADBACKGROUND = False # toggle with key b
		self.ALIGN_TO_CAM = True

		# load image
		self.bg_image = pygame.image.load(f'{self.game.DIR}/art/background.png').convert()
		self.bg_rect = self.bg_image.get_rect()
		self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
		self.bg_rect = self.bg_image.get_rect()
		self.newrect = None

	def drawbg(self):
		"""Draw background"""
		if self.bg_image == None or self.LOADBACKGROUND == False:	# no background image available, draw colors
			self.WIN.fill(self.settings.bg_color)
			pygame.draw.rect(self.WIN, self.settings.gr_color, 
				(0, self.settings.gr_height, self.settings.screen_width, self.settings.screen_height-self.settings.gr_height), 0)
			#pygame.draw.rect(self.WIN, ec.transform(self.settings.gr_color, 12),
			#	(0, 0, self.settings.screen_width, self.settings.skylimit), 0)
		
		else: # background image available, blit it
			if self.ALIGN_TO_CAM:
				self.newrect = pygame.Rect(self.bg_rect)
				self.newrect.topleft = self.game.cam.align(self.bg_rect.topleft)
				self.WIN.blit(self.bg_image, self.newrect)
			else:	
				self.WIN.blit(self.bg_image, self.bg_rect)
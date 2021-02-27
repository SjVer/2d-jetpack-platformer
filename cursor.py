import pygame, math, sys
import easycolors as ec 
from dashedline import draw_dashed_line
from soundplayer import *

class Cursor:
	"""Class for the curson n stuff"""

	def __init__(self, game):
		"""Init. attributes"""
		# get attributes from main
		self.WIN = game.WIN
		self.settings = game.settings
		self.screen_rect = game.WIN.get_rect()
		self.game = game

		# load image
		self.image = pygame.image.load(f'{self.game.DIR}/art/cursor.png')
		self.rect = self.image.get_rect()
		# resize
		w, h = self.rect.width*self.settings.cursor_image_size_multiplier, self.rect.height*self.settings.cursor_image_size_multiplier
		self.image = pygame.transform.scale(self.image, (w, h))
		self.rect = self.image.get_rect()

		self.angle = 0

	def drawline(self, beginx, beginy):
		# draw short or long line based on hovering/aiming or not
		if self.game.player.hovering and not self.game.player.thrusting:
			self.aim_line_length = self.settings.aim_line_length * 2
		else:
			self.aim_line_length = self.settings.aim_line_length

		# functions for line are different based on direction (left/right)
		if self.settings.facingleft:
			draw_dashed_line(self.WIN, self.settings.aim_color,
				(beginx - 30 * math.cos(self.angle), beginy - 30 * math.sin(self.angle)),
				(beginx - self.aim_line_length * math.cos(self.angle), beginy - self.aim_line_length * math.sin(self.angle)),
				2, 10)
		else:
			draw_dashed_line(self.WIN, self.settings.aim_color,
				(beginx + 30 * math.cos(self.angle), beginy + 30 * math.sin(self.angle)),
				(beginx + self.aim_line_length * math.cos(self.angle), beginy + self.aim_line_length * math.sin(self.angle)),
				2, 10)

	def getangle(self):
 
		(beginx, beginy) = self.game.cam.align((self.game.player.rect.center[0], self.game.player.rect.center[1] - 5))

		(endx, endy) = pygame.mouse.get_pos()

		dx = endx - beginx
		dy = endy - beginy

		try:
			self.angle = math.atan(dy / dx) # radians
		except:
			self.angle = 0

		return beginx, beginy

	def update(self):
		"""Update cursor"""
		self.rect.center = pygame.mouse.get_pos()

		# get facing direction (left/right)
		if self.rect.center[0] < self.game.cam.align((self.game.player.rect.center[0], self.game.player.rect.center[1] - 5))[0]:
			self.settings.facingleft = True
		else:
			self.settings.facingleft = False

		beginx, beginy = self.getangle()
		# blit cursor image and draw aim line
		if self.settings.DRAWCURSOR:
			self.WIN.blit(self.image, self.rect)
		if self.settings.DRAWAIMLINE:
			self.drawline(beginx, beginy)
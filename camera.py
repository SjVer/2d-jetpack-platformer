import pygame, os, time
import easycolors as ec
from vectors import *
import mathutils

class Camera:
	"""A class for te camera of a game"""

	def __init__(self, game=None):
		"""Init. attributes"""
		# get other attributes
		if not game == None:
			self.game = game
			self.settings = game.settings
			self.WIN = game.WIN

			# cam rect
			self.camrect = pygame.Rect(self.settings.cam_start_x, self.settings.cam_start_y, self.settings.screen_width, self.settings.screen_height)
		else:
			self.camrect = pygame.Rect(1,1,5,5)
	
		# Pos
		self.x = self.settings.cam_start_x
		self.y = self.settings.cam_start_y
		self.old = None

	def pos_attr(self, attr: str, part: str = 'both'):
		"""Get the position of an attribute of the cam rect"""
		if not (part == 'x' or part == 'y' or part == 'both'):
			print('cam_pos_attr: ERROR: incorrect part probably')
			return 
		try:
			x = eval(f'self.camrect.{attr}[0]')
			y = eval(f'self.camrect.{attr}[1]')

			if part == 'both':
				return int(x), int(y)
			elif part == 'x':
				return x
			elif part == 'y':
				return y
			else:
				print('cam_pos_attr: ERROR: it went wrong somewhere in the returning')
		except:
			print('cam_pos_attr: ERROR: incorrect attribute probably')

	def align(self, pos: tuple) -> tuple:
		"""Align position relative to cam"""
		newx = pos[0] - self.x
		newy = pos[1] - self.y
		return newx, newy

	def lock(self, pos: tuple) -> tuple:
		"""Lock position relative to cam"""
		newx = pos[0] + self.pos_attr('topleft', 'x')
		newy = pos[1] + self.pos_attr('topleft', 'y')
		return newx, newy

	def setpos(self, newpos, part='both'):
		"""Set cam pos"""
		if not ((part=='both' and type(newpos)==tuple) or ((part=='x' or part=='y') and (type(newpos) == int or type(newpos) == float))):
			print('setpos: incorrect part!')
			return
		elif part=='both':
			self.x, self.y = newpos[0], newpos[1]
		elif part=='x':
			self.x = newpos
		elif part=='y':
			self.y = newpos
		else:
			print('somethings has gone wrong')
			return newpos

	def follow_player(self):
		dist_to_player = Vector(self.align(self.game.player.new_rect.topleft)) - Vector(self.pos_attr('center')[0], self.pos_attr('center')[1])
		dist_to_player = Vector(dist_to_player[0], dist_to_player[1])

		if dist_to_player > self.settings.cam_margin:
			self.x += 20

	def update(self):
		self.follow_player()
import pygame, os, time
import easycolors as ec

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
		if not ((part=='both' and type(part)==tuple) or ((part=='x' or part=='y') and (type(part) == int or type(part) == float))):
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

	def update(self):
		pass
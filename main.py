import pygame, sys, os, musicalbeeps
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.mixer.set_num_channels(10)
pygame.font.init()

player = musicalbeeps.Player(volume = 0.5, mute_output = False)

from time import sleep
import easycolors as ec
from settings import Settings
from player import Player
from cursor import Cursor
from bullets import Bullet
from environment import Environment
from environment import Background
from camera import Camera
import os_signals
from soundplayer import *

clock = pygame.time.Clock()

class Game:
	"""Class for a game instance"""

	def __init__(self):
		"""Init. attributes"""
		self.DIR = os.path.dirname(os.path.realpath(__file__))
		
		self.settings = Settings(self)

		# Set pygame window
		self.WIN = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("JetTrooper")

		# Init classes
		self.player = Player(self)
		self.envir = Environment(self)
		self.cursor = Cursor(self)
		self.cam = Camera(self)
		self.bgs = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()

		# set first bg
		first_bg = Background(self)
		self.bgs.add(first_bg)

		# game loop flag
		self.running = True

		# vars
		self.fired_since_reload = 0
		self.reload_time_left = False
		self.reloading = False
		self.recharging = False
		self.recharging_time = 0
		self.paused = False
		self.limited = True

		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)

	def check_events(self):
		"""checks for events"""
		for event in pygame.event.get():
			# Quit event
			if event.type == pygame.QUIT:
				# Stop game
				pygame.mouse.set_visible(True)
				self.running = False
			elif event.type == pygame.KEYDOWN:
				# Keydown event
				self.check_key_events(event, True)
			elif event.type == pygame.KEYUP:
				# Keyup event
				self.check_key_events(event, False)

			# MOUSE
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse_event(event, True)
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouse_event(event, False)
		
		mouse_pos = pygame.mouse.get_pos()

	def mouse_event(self, event, boolean):
		if event.button == 1:	# LEFT CLICK
			if boolean and not self.reloading:
				self.fire_bullet()
		elif event.button == 2:	# MIDDLE CLICK
			pass
		elif event.button == 3:	# RIGHT CLICK
			self.player.hovering = boolean
			self.player.air_friction_on = not boolean

	def check_key_events(self, event, boolean):
		"""handle key events"""
		# SPACE
		if event.key == pygame.K_SPACE:
			self.player.thrusting = boolean
			if boolean and self.player.grounded:
				# JUMP
				playsound(self, 'jump_sound')
				self.player.yvector += self.settings.jumpboost
				self.player.takeoff = self.settings.FPS * self.settings.takeoff_boost_time
				if self.player.walking_left and not self.player.hovering:
					self.player.xvector -= 2
				if self.player.walking_right and not self.player.hovering :
					self.player.xvector += 2
		# ROT LEFT
		elif event.key == pygame.K_a:
			self.player.rotating_left = boolean
			self.player.walking_left = boolean
		# ROT RIGHT 
		elif event.key == pygame.K_d:
			self.player.rotating_right = boolean
			self.player.walking_right = boolean
		# RELOAD
		elif event.key == pygame.K_r and not self.reloading and self.fired_since_reload > 0:
			self.fired_since_reload = self.settings.max_bullets
			self.reloading = True
			self.reload_time_left = self.settings.reload_time
		# MOVE CAM
		elif event.key == pygame.K_o:
			self.cam.x += 20
		# PAUSE
		elif event.key == pygame.K_p:
			if boolean:
				self.paused = not self.paused
		# TOGGLE FUEL AND AMMO LIMIT
		elif event.key == pygame.K_t:
			if boolean:
				self.limited = not self.limited
		# TOGGLE BG IMG
		elif event.key == pygame.K_b:
			if boolean:
				self.envir.LOADBACKGROUND = not self.envir.LOADBACKGROUND
		# QUIT
		elif event.key == pygame.K_q:
			pygame.mouse.set_visible(True)
			self.running = False

	def fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if self.fired_since_reload < self.settings.max_bullets:
			playsound(self, 'shoot_sound')
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
			if self.limited:
				self.fired_since_reload += 1
		else:
			self.reloading = True
			self.reload_time_left = self.settings.reload_time

	def update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullet positions.
		self.bullets.update()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0 or bullet.rect.bottom >= self.settings.gr_height or bullet.rect.right <=0 or bullet.rect.left >= self.settings.screen_width:
				self.bullets.remove(bullet)
				if bullet.rect.bottom >= self.settings.gr_height:
					playsound(self, 'wall_hit_sound')

	def update_bgs(self):
		"""Üpdate backgrounds"""
		# find most right background
		canaddright = True
		canaddleft = True

		try:
			mostright = pygame.Rect(0,0,0,0)
			for bg in self.bgs.sprites():
				if bg.newrect.right > mostright.right:
					mostright = bg.newrect

			mostleft = pygame.Rect(0,0,0,0)
			for bg in self.bgs.sprites():
				if bg.newrect.left < mostleft.left:
					mostleft = bg.newrect

		except Exception as e:
			mostleft = pygame.Rect(0,0,0,0)
			mostright = pygame.Rect(0,0,0,0)
			print(e)

		for bg in self.bgs.sprites():
			bg.drawbg()
			print(canaddright)

			# if new background needed, add it
			if bg.newrect == mostright and bg.newrect.right < self.settings.screen_width and canaddright:
				new_bg = Background(self)
				new_bg.bg_rect.left = bg.newrect.right
				self.bgs.add(new_bg)
				print('right')
				canaddright = False
			elif bg.newrect == mostleft and bg.newrect.left > 0 and canaddleft:
				new_bg = Background(self)
				new_bg.bg_rect.right = 0
				self.bgs.add(new_bg)
				print('left')
				canaddleft = False

			# remove background if out of screen
			if (bg.newrect.right <= 0 or bg.newrect.left >= self.settings.screen_width) and len(self.bgs) > 2:
				self.bgs.remove(bg)
				print('bg removed')

		print(f"len: {len(self.bgs.sprites())}\n")

	def run_game(self):
		"""Main game loop"""
		while self.running:
			self.check_events()	# Check events
			if not self.paused:
				self.update_bgs()
				self.envir.update()	# update environment
				self.cursor.update()	# update cursor/aiming
				self.update_bullets() 	# update bullets

				# manage reloading
				if self.reloading:
					if not soundplaying(self, 'reload_sound'):
						playsound(self, 'reload_sound')
					self.reload_time_left -= self.settings.fpstrans(1/self.settings.FPS)
					if self.reload_time_left <= 0:
						self.reloading = False
						self.fired_since_reload = 0

				# stop flight if recharging
				if self.recharging:
					self.recharging_time += self.settings.fpstrans(1/self.settings.FPS)
					self.player.thrusting = False
					self.player.hovering = False
					if self.player.thrust_left >= self.settings.min_thrust:
						self.recharging = False
						self.recharging_time = 0
						self.envir.fuel_bar_color = ec.transform(ec.cyan, -20)

				self.player.update()	# update player

				# set recharge bool
				if self.player.thrust_left <= self.settings.thrust_is_zero:
					self.recharging = True
					self.envir.fuel_bar_color = ec.orange

			self.cam.update()
			pygame.display.flip()	# update display
			clock.tick(self.settings.FPS)	# fps thing
			
		pygame.display.quit()	# close window
		os_signals.send_signal('SIGKILL')	# kill program

if __name__ == '__main__':
	# Make a game instance, and run the game.
	game = Game()
	game.run_game()

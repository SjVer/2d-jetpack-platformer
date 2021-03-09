import pygame
pygame.init()
pygame.mixer.init()

def playsound(self, sound, outputting=False):
	pygame.mixer.Channel(eval(f"self.settings.{sound}_channel")).play(eval(f"self.settings.{sound}"))
	if outputting:
		print(f'Played sound "{sound}" on channel {eval(f"self.settings.{sound}_channel")}')

def soundplaying(self, sound):
	return bool(pygame.mixer.Channel(eval(f"self.settings.{sound}_channel")).get_busy())
import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from Particle import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from transition_trigger import TransitionTrigger

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		# sprite setup
		self.create_map()

		# user interface(ui)
		self.ui = UI()
		self.upgrade = Upgrade(self.player)
		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)
		self.game_over = False

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('FLOORBLOCKSS_floorblocks.csv'),
			'entities' :import_csv_layout('FLOORBLOCKSS_entities.csv')
		}
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index,col in enumerate(row):
					if col!='-1':
						x= col_index * TILESIZE
						y= row_index * TILESIZE
						if style== 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style =='entities':
							if col=='500': monster_name ='onigiri'
							elif col=='0': monster_name='carrot'
							Enemy(
								monster_name,
								(x, y),
								[self.visible_sprites, self.attackable_sprites],
								self.obstacle_sprites,
								self.damage_player,
								self.trigger_death_particles,
								self.add_exp)
							self.player = Player(
			                (800,2360),
			                [self.visible_sprites],
			                self.obstacle_sprites,
			                self.create_attack,
							self.destroy_attack,
							self.create_magic)
							if col == '66':  # Adjust the condition to match the tile ID for the transition trigger
								self.transition_trigger = TransitionTrigger((x, y), [self.visible_sprites],
																			self.transition_to_new_map)


	def transition_to_new_map(self):
		# This function will be called when the player collides with the transition trigger
		# You can load the new map, change enemy types, etc. here
		# For now, let's just print a message
		print("Transitioning to a new map!")

	def create_attack(self):
		if self.current_attack is None:
			# Create a new attack instance
			self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

	def create_magic(self, style, strength, cost):
		if style == 'heal':
			self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

		if style == 'flame':
			self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

	def destroy_attack(self):
		if self.current_attack is not None:
			# Destroy the current attack instance
			self.current_attack.kill()
			self.current_attack = None



	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						target_sprite.get_damage(self.player, attack_sprite.sprite_type)

	def damage_player(self, amount, attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

	def kill_player(self):
		if self.player.health <= 0:
			self.game_over = True

	def reset_level(self):
		self.visible_sprites.empty()  # Clear all sprites from the visible_sprites group
		self.attack_sprites.empty()  # Clear attack sprites
		self.attackable_sprites.empty()  # Clear attackable sprites
		self.player.health = 100
		self.player.energy = 140
		self.player.rect.topleft = (800, 2360)
		self.game_over = False
		self.create_map()
		pygame.font.init()

	def trigger_death_particles(self, pos, particle_type):

		self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

	def add_exp(self, amount):

		self.player.exp += amount


	def run(self):
		if not self.game_over:
			# update and draw the game
			self.visible_sprites.custom_draw(self.player)
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()
			self.ui.display(self.player)
		else:
			self.screen.fill('Black')
			font = pygame.font.Font(None, 36)
			text = font.render("Game Over! Press Enter to restart", True, (255, 255, 255))
			text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
			self.screen.blit(text, text_rect)
			pygame.display.update()

			# Check for restart input
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RETURN]:
				self.reset_level()


# Inside the YSortCameraGroup class
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		self.zoom_factor = 1.9  # Set the initial zoom factor to 150%

		# Load the ground.png image
		self.original_floor_surf = pygame.image.load('ground.png').convert()

		# Apply the zoom factor to the ground.png image
		self.floor_surf = pygame.transform.scale(self.original_floor_surf, (
			int(self.original_floor_surf.get_width() * self.zoom_factor),
			int(self.original_floor_surf.get_height() * self.zoom_factor)
		))

		# Update the rect for the zoomed image
		self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

	def set_zoom(self, factor):
		self.zoom_factor = max(0.1, min(3.0, factor))  # Limit zoom factor

		# Apply the zoom factor to the ground.png image
		self.floor_surf = pygame.transform.scale(self.original_floor_surf, (
			int(self.original_floor_surf.get_width() * self.zoom_factor),
			int(self.original_floor_surf.get_height() * self.zoom_factor)
		))

		# Update the rect for the zoomed image
		self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

	def custom_draw(self, player):
		# getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# Blit the zoomed ground.png image
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
			# Original sprites (not zoomed)
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)


	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)

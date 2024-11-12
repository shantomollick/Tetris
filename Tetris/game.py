from grid import Grid
from blocks import *
import random
import pygame
import os

class Game:
	def __init__(self):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.game_over = False
		self.score = 0
		self.highscore = self.read_high_score()
		self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
		self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
		self.pause = False

		pygame.mixer.music.load("Sounds/music.ogg")
		pygame.mixer.music.play(-1)



	def read_high_score(self):
		try:
			with open("highscore.txt", 'r') as f:
				return int(f.readline().strip())
		except:
			if(not os.path.exists("highscore.txt")):
				with open("highscore.txt", 'w') as f:
					f.write("0")
			with open("highscore.txt", 'r') as f:
				return int(f.readline().strip())

	def update_high_score(self):
		if (self.score) > int(self.highscore):
			with open("highscore.txt", 'w') as f:
				f.write(str(self.score))

	def reset_high_score(self):
		with open("highscore.txt" 'w') as f:
			f.write("0")



	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		elif lines_cleared == 4:
			self.score += 1000
		self.score += move_down_points

	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		self.update_high_score()	

		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0
		self.highscore = self.read_high_score()

	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 260)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 250)
		else:
			self.next_block.draw(screen, 270, 240)
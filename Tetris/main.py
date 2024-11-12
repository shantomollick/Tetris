import pygame,sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
high_score_surface = title_font.render("High Score", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 195, 170, 180)
high_score_rect = pygame.Rect(320, 460, 170, 60)


screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris by Shanto Fucking Mollick")



clock = pygame.time.Clock()
FPS = 60

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 300)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()

			if event.key == pygame.K_w and game.game_over == False and game.pause == False:
				game.reset_high_score

			if event.key == pygame.K_SPACE and game.game_over == False:
				game.rotate
			if event.key == pygame.K_e:
				game.score += 200
			if event.key == pygame.K_LEFT and game.game_over == False and game.pause == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False and game.pause == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False and game.pause == False:
				game.move_down()
				game.update_score(0, 1)
			if event.key == pygame.K_UP and game.game_over == False and game.pause == False:
				game.rotate()
			if event.key == pygame.K_ESCAPE:
				if game.pause:
					game.pause = False
				else:
					game.pause = True
		if event.type == GAME_UPDATE and game.game_over == False and game.pause == False:
			game.move_down()

	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)
	hiscore_value_surface = title_font.render(str(game.highscore), True, Colors.white)

	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 150, 50, 50))
	screen.blit(high_score_surface, (335, 410, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 550, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)

	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, high_score_rect, 0, 10)	
	screen.blit(hiscore_value_surface, hiscore_value_surface.get_rect(centerx = high_score_rect.centerx, 
		centery = high_score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	game.draw(screen)

	pygame.display.update()
	clock.tick(FPS)
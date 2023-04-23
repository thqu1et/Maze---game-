import pygame, sys
from pygame import *
from random import choice, random
from button import Button

WIDTH, HEIGHT = 750, 750
TILE = 50

cols = (WIDTH // TILE + 1) // 2
rows = (HEIGHT // TILE + 1) // 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirint")
clock = pygame.time.Clock()

bg_sound = pygame.mixer.Sound('music/smoke-143172.mp3')
bg_sound.play()

BG = pygame.image.load('image/1600w-F2CyNS5sQdM.webp')



def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    player_speed = 15

    player_x = 30
    player_y = 30
    walk_right = [
        pygame.image.load('image/right.png'),
        pygame.image.load('image/right1.png'),
        pygame.image.load('image/right2.png'),
        pygame.image.load('image/right3.png'),
    ]
    walk_left = [
        pygame.image.load('image/left.png'),
        pygame.image.load('image/left1.png'),
        pygame.image.load('image/left2.png'),
        pygame.image.load('image/left3.png'),
    ]

    player_anim_count = 0
    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False

        def draw(self):
            x = 2 * self.x * TILE
            y = 2 * self.y * TILE

            if self.visited:
                pygame.draw.rect(screen, pygame.Color('red'), (x, y, TILE, TILE))

            if not self.walls['top']:
                pygame.draw.rect(screen, pygame.Color('red'), (x, y - TILE, TILE, TILE))
            if not self.walls['right']:
                pygame.draw.rect(screen, pygame.Color('red'), (x + TILE, y, TILE, TILE))
            if not self.walls['bottom']:
                pygame.draw.rect(screen, pygame.Color('red'), (x, y + TILE, TILE, TILE))
            if not self.walls['left']:
                pygame.draw.rect(screen, pygame.Color('red'), (x - TILE, y, TILE, TILE))

        def check_cell(self, x, y):
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cell[x + y * cols]

        def check_neighbours(self):
            neighbours = []

            top = self.check_cell(self.x, self.y - 1)
            right = self.check_cell(self.x + 1, self.y)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)

            if top and not top.visited:
                neighbours.append(top)
            if right and not right.visited:
                neighbours.append(right)
            if bottom and not bottom.visited:
                neighbours.append(bottom)
            if left and not left.visited:
                neighbours.append(left)

            return choice(neighbours) if neighbours else False

    def remove_walls(current_cell, next_cell):
        dx = current_cell.x - next_cell.x
        dy = current_cell.y - next_cell.y

        if dx == 1:
            current_cell.walls['left'] = False
            next_cell.walls['right'] = False
        if dx == -1:
            current_cell.walls['right'] = False
            next_cell.walls['left'] = False
        if dy == 1:
            current_cell.walls['top'] = False
            next_cell.walls['bottom'] = False
        if dy == -1:
            current_cell.walls['bottom'] = False
            next_cell.walls['top'] = False

    def check_wall(grid_cell, x, y):
        if x % 2 == 0 and y % 2 == 0:
            return False
        if x % 2 == 1 and y % 2 == 1:
            return True

        if x % 2 == 0:
            grid_x = x // 2
            grid_y = (y - 1) // 2
            return grid_cell[grid_x + grid_y * cols].walls['bottom']
        else:
            grid_x = (x - 1) // 2
            grid_y = y // 2
            return grid_cell[grid_x + grid_y * cols].walls['right']

    # class Player(pygame.sprite.Sprite):
    #     def __init__(self):
    #         super().__init__()
    #         self.image = pygame.Surface((50, 50))
    #         self.image.fill((0, 0, 255))
    #         self.rect = self.image.get_rect()
    #         self.rect.center = (WIDTH / 2, HEIGHT / 2)
    #         self.speed = 0.5
    #
    #     def update(self):
    #
    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_LEFT]:
    #             self.rect.x -= self.speed
    #         if keys[pygame.K_RIGHT]:
    #             self.rect.x += self.speed
    #         if keys[pygame.K_UP]:
    #             self.rect.y -= self.speed
    #         if keys[pygame.K_DOWN]:
    #             self.rect.y += self.speed
    #
    #
    #         if self.rect.left < 0:
    #             self.rect.left = 0
    #         elif self.rect.right > WIDTH:
    #             self.rect.right = WIDTH
    #         if self.rect.top < 0:
    #             self.rect.top = 0
    #         elif self.rect.bottom > HEIGHT:
    #             self.rect.bottom = HEIGHT

    grid_cell = [Cell(x, y) for y in range(rows) for x in range(cols)]
    current_cell = grid_cell[0]
    current_cell.visited = True
    stack = []

    # player = Player()
    # all_sprites = pygame.sprite.Group()
    # all_sprites.add(player)

    while True:
        screen.blit(BG, (0, 0))
        screen.blit(walk_right[player_anim_count] , (player_x ,player_y))

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x-=player_speed

        elif keys[pygame.K_RIGHT]:
            player_x+=player_speed

        if keys[pygame.K_UP]:
            player_y-=player_speed
        elif keys[pygame.K_DOWN]:
            player_y+=player_speed

        if player_anim_count==3:
            player_anim_count=0
        else:
            player_anim_count+=1

        # screen.blit(player,(0,0))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()



        # screen.fill("white")

        PLAY_BACK = Button(image=None, pos=(700, 720),
                           text_input="BACK", font=get_font(25), base_color="Black", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)



        for cell in grid_cell:
            cell.draw()

        next_cell = current_cell.check_neighbours()
        if next_cell:
            next_cell.visited = True
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
            stack.append(current_cell)
        elif stack:
            current_cell = stack.pop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                map_cell = [check_wall(grid_cell, x, y) for y in range(rows * 2 - 1) for x in range(cols * 2 - 1)]
                for y in range(rows * 2 - 1):
                    for x in range(cols * 2 - 1):
                        if map_cell[x + y * (cols * 2 - 1)]:
                            print(" ", end="")
                        else:
                            print("#", end="")
                    print()


        pygame.display.flip()
        clock.tick(20)
        display.update()
        # all_sprites.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(20).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(375, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(375, 460),
                              text_input="BACK", font=get_font(25), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(35).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(375, 80))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(375, 170),
                             text_input="PLAY", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(375, 300),
                                text_input="OPTIONS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(375, 430),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

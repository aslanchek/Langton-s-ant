import pygame, pygame.locals, pygame.draw
import constants

class Button():
    pass

class Ant:
    def __init__(self, color, start_x, start_y, start_direction, game):
        self.game = game
        self.x = start_x
        self.y = start_y
        self.color = color
        self.direction = start_direction
    

    def move(self):
        current_cell = self.game.grid[self.x][self.y]
        if current_cell:
            self.direction = (self.direction + 4 - 1) % 4 # angle: 1 for right, -1 for left
        else:
            self.direction = (self.direction + 4 + 1) % 4 # angle: 1 for right, -1 for left
        self.game.grid[self.x][self.y] = not current_cell
        self.x += constants.DIRECTIONS[self.direction][0]
        self.y += constants.DIRECTIONS[self.direction][1]

    def render(self):
        pygame.draw.rect(self.game.screen, constants.RED, (self.x * constants.SIZE, self.y * constants.SIZE, constants.SIZE, constants.SIZE))
        


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.fps = constants.FPS_DEFAULT
        self.running = True
        self.pause = False
        self.selected_color = constants.BLACK
        self.selected_direction = 0 
        self.mode = 0
        self.epoch = 1

        self.ants = []

        self.grid = {}
        for i in range(W):
            self.grid[i] = {}
            for j in range(H):
                self.grid[i][j] = 0

    def next_epoch(self):
        for ant in self.ants:
            ant.move()
        self.epoch += 1
        
    def draw(self):
        if pygame.mouse.get_pressed()[0]:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            x = x // constants.SIZE
            y = y // constants.SIZE
            current_cell = self.grid[x][y]
            if not current_cell:
                self.grid[x][y] = 1
           

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                    self.stop() 
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    self.stop()
                if event.key == pygame.locals.K_w: # speed up simulation speed
                    self.fps += 10
                if event.key == pygame.locals.K_s: # slow down simulation speed
                    self.fps -= 10
                if event.key == pygame.locals.K_SPACE: # pause
                    self.pause = not self.pause
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    x = pygame.mouse.get_pos()[0] // constants.SIZE
                    y = pygame.mouse.get_pos()[1] // constants.SIZE
                    self.ants.append(Ant(self.selected_color, x, y, self.selected_direction, self))
                    print(f'ants: {len(self.ants)}')
            elif event.type == pygame.locals.MOUSEBUTTONUP:
                pass
    
    def render(self):
        self.screen.fill(constants.WHITE)

        for x in self.grid:
            for y in self.grid[x]:
                if self.grid[x][y]:
                    pygame.draw.rect(self.screen, constants.BLACK, (x * constants.SIZE, y * constants.SIZE, constants.SIZE, constants.SIZE))

        for ant in self.ants:
            ant.render()

        pygame.display.update()


    def stop(self):
        self.running = False

    def start(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(self.fps)
            self.render()
            self.draw()
            self.handle_events()
            if not self.pause:
                self.next_epoch()
                
            pygame.display.set_caption(f'FPS: {int(clock.get_fps())}')


pygame.init()

monitor = pygame.display.Info()

## Constants
WIDTH = int(monitor.current_w * 2/3)  # initial window size
HEIGHT = int(monitor.current_h * 2/3) #
W = WIDTH // constants.SIZE
H = HEIGHT // constants.SIZE
FONT_SIZE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) 

main = Game(screen)
main.start()

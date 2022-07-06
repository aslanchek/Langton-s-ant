import pygame, pygame.locals, pygame.draw
import constants

class Button():
    pass

class Ant:
    def __init__(self, color, start_x, start_y, start_direction, game):
        self.color = color
        self.x = start_x
        self.y = start_y
        self.game = game
        self.direction = start_direction
    
    def move(self):
        position = (self.x, self.y)
        if position in self.game.filled_dots:
            self.direction = (self.direction + 4 - 1) % 4 # angle: 1 for right, -1 for left
            del self.game.filled_dots[position] # turn <color> in white
        else:
            self.direction = (self.direction + 4 + 1) % 4 
            self.game.filled_dots[position] = self.color # turns white in <color>

        self.x += constants.DIRECTIONS[self.direction][0]
        self.y += constants.DIRECTIONS[self.direction][1]
    def render(self):
        pygame.draw.rect(self.game.screen, constants.RED, (self.x, self.y, constants.SIZE, constants.SIZE))
        


class Game:
    def __init__(self, screen):
        self.running = True
        self.screen = screen
        self.fps = constants.FPS_DEFAULT
        self.selected_color = constants.BLACK
        self.selected_direction = 0
        self.filled_dots = {}
        self.epoch = 1
        self.ants = []

    def next_epoch(self):
        for ant in self.ants:
            ant.move()
        self.epoch += 1
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                    self.stop() 
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_q:
                    self.stop()
                if event.key == pygame.locals.K_w:
                    self.fps += 10
                if event.key == pygame.locals.K_s:
                    self.fps -= 10
                if event.key == pygame.locals.K_d:
                    print("=========DEBUG INFO==========")
                    print() 
                    print("=============================")
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                x = (x // 4 + int(x % 4 >= 2)) * 4
                y = (y // 4 + int(y % 4 >= 2)) * 4
                self.ants.append(Ant(self.selected_color, x, y, self.selected_direction, self))
    
    def render(self):
        self.screen.fill(constants.WHITE)
        for dot in self.filled_dots:
            pygame.draw.rect(self.screen, self.filled_dots[dot], (dot[0], dot[1], constants.SIZE, constants.SIZE))
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
            self.handle_events()
            self.next_epoch()

            pygame.display.set_caption(f'FPS: {int(clock.get_fps())}, EPOCH: {self.epoch}')

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.SCALED) 

main = Game(screen)
main.start()

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
        self.game.grid[self.x][self.y] = not self.game.grid[self.x][self.y] 
        self.x += constants.DIRECTIONS[self.direction][0]
        self.y += constants.DIRECTIONS[self.direction][1]

    def render(self):
        pygame.draw.rect(self.game.screen, constants.RED, (self.x, self.y, constants.SIZE, constants.SIZE))
        


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.fps = constants.FPS_DEFAULT
        self.running = True
        self.pause = False
        self.myfont = pygame.font.SysFont('Comic Sans MS', 25)
        self.selected_color = constants.BLACK
        self.mode = 0
        self.epoch = 1

        self.ants = []
        self.ants.append(Ant(constants.BLACK, 30, 30, 0, self))
        self.grid = [[0 for i in range(constants.W)] for i in range(constants.H)]


    def next_epoch(self):
        for ant in self.ants:
            ant.move()
        self.epoch += 1
        
    def draw(self):
        if pygame.mouse.get_pressed()[0]:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            x = (x // constants.SIZE) * constants.SIZE
            y = (y // constants.SIZE) * constants.SIZE
            position = (x, y)
            if not self.mode:
                if not position in self.filled_dots:
                    self.filled_dots[(x, y)] = self.selected_color
            else:
                if position in self.filled_dots:
                    del self.filled_dots[(x, y)]
            
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
                if event.key == pygame.locals.K_m: # switch mode: drawing or appeding the ants
                    self.mode = not self.mode
                if event.key == pygame.locals.K_SPACE: # pause
                    self.pause = not self.pause
                if event.key == pygame.locals.K_d:
                    print("=========DEBUG INFO==========")
                    print(pygame.mouse.get_pressed())
                    print("=============================")
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    x = (x // constants.SIZE) * constants.SIZE
                    y = (y // constants.SIZE) * constants.SIZE
                    self.ants.append(Ant(self.selected_color, x, y, self.selected_direction, self))
            elif event.type == pygame.locals.MOUSEBUTTONUP:
                pass
    
    def render(self):
        self.screen.fill(constants.WHITE)
        for dot in self.filled_dots:
            pygame.draw.rect(self.screen, self.filled_dots[dot], (dot[0], dot[1], constants.SIZE, constants.SIZE))
        for ant in self.ants:
            ant.render()
        screen.blit(self.myfont.render(f'MODE: {constants.MODE[self.mode]}', False, (0, 0, 0)) ,(10,10))
        screen.blit(self.myfont.render('RIGHT CLICK: add new ant', False, (0, 0, 0)) ,(constants.WIDTH - 230,10))
        screen.blit(self.myfont.render('LEFT CLICK: drawing', False, (0, 0, 0)) ,(constants.WIDTH - 230,30))
        screen.blit(self.myfont.render('M: switch pen/erase', False, (0, 0, 0)) ,(constants.WIDTH - 230,50))
        screen.blit(self.myfont.render('W/S: speed up/ slow down', False, (0, 0, 0)) ,(constants.WIDTH - 230,70))
        screen.blit(self.myfont.render('SPACE: pause', False, (0, 0, 0)) ,(constants.WIDTH - 230,90))
        if self.pause:
            screen.blit(self.myfont.render('PAUSE', False, (0, 0, 0)) ,(constants.WIDTH / 2 , constants.HEIGHT - 20))
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

            pygame.display.set_caption(f'FPS: {int(clock.get_fps())}, EPOCH: {self.epoch}')

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.SCALED) 

main = Game(screen)
main.start()

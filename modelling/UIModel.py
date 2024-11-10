import pygame
from final.configs import tab_Colour, tab_selectColour, tab_outerColour
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

run = True
t_WIDTH = 100
t_HEIGHT = 30


def shutdown():
    global run
    run = False


def main_menu():
    play = tab(screen, tab_Colour, tab_selectColour, tab_outerColour, 10, 10, t_WIDTH, t_HEIGHT, None, "play")
    next = tab(screen, tab_Colour, tab_selectColour, tab_outerColour, 10, 60, t_WIDTH, t_HEIGHT, None, "options")
    exit = tab(screen, tab_Colour, tab_selectColour, tab_outerColour, 10, 110, t_WIDTH, t_HEIGHT, shutdown, "exit")
    tabs = [play, next, exit]
    current = 0
    screen.fill("black")
    global run

    while run:
        for t in tabs:
            if tabs.index(t) == current:
                t.hover()
            else:
                t.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                if current < 2:
                    current += 1
            if key[pygame.K_UP]:
                if 0 < current:
                    current -= 1
            if key[pygame.K_RETURN] or key[pygame.K_j] or key[pygame.K_SPACE]:
                tabs[current].func()

        pygame.display.update()


class tab:

    def __init__(self, surface, colour, select_colour, outercolour, x, y, width, height, func, message):


        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface
        self.colour = colour
        self.selectColour = select_colour
        self.func = func
        self.message = message

    def hover(self):
        pygame.draw.rect(self.surface, self.selectColour, self.rect)
        self.surface.blit(pygame.font.SysFont("Arial", 25).render(self.message, True, "black"), (self.rect.x + 5, self.rect.y + 5))

    def select(self):
        self.func()

    def draw(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)
        self.surface.blit(pygame.font.SysFont("Arial", 25).render(self.message, True, "black"), (self.rect.x + 5, self.rect.y + 5))


main_menu()
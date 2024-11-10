import pygame

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

image = pygame.Surface()


run = True
while run:
    screen.fill("red")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            run = False
    pygame.display.update()







import pygame

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
clock.tick(60)

class thing:

    def __init__(self, sheet, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.sheet = pygame.image.load(sheet).convert()
        self.width = width
        self.height = height
        self.screen = screen
        self.walking_left_sprites = []
        self.image = None

    def get_sprites(self, num):
        for i in range(0, num):
            image = pygame.Surface((self.width, self.height))
            image.set_colorkey((0, 0, 0))
            image.blit(self.sheet, (0, 0), (i * self.width, 0, self.width, self.height))
            self.walking_left_sprites.append(image)

    def animate(self, frame):
        self.image = self.walking_left_sprites[frame]

    def draw(self):
        self.screen.blit(self.image, (10, 10))


player = thing("sprites/Sprite-0002.png", 10, 20, 80, 100, screen)
frame = 0
player.get_sprites(5)
player.animate(frame)

run = True
while run:
    screen.fill("grey")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if frame < 4:
        player.animate(int(frame))
        frame += 0.005 
    else:
        player.animate(int(frame))
        frame = 0

    key = pygame.key.get_pressed()
    if key[pygame.K_RETURN]:
        run = False

    player.draw()

    pygame.display.update()


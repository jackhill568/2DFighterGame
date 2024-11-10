import pygame
from final.configs import ACCELERATION, WIDTH, HEIGHT
pygame.init()
pygame.font.init()
display_info = pygame.display.Info()
# WIDTH, HEIGHT = display_info.current_w, display_info.current_h
x_scale_factor = 3*WIDTH/1980
y_scale_factor = 3*HEIGHT/1080
Y_ACCELERATION = ACCELERATION * y_scale_factor
X_ACCELERATION = ACCELERATION * x_scale_factor
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

class player:

    def __init__(self, connection, x, y, surface):
        self.connection = connection
        self.x = x
        self.y = y
        self.surface = surface
        self.sheet = [[6, 0.05, pygame.image.load("../sprites/Sully_idle.png").convert_alpha()], [21, 0.5, pygame.image.load(
            "../sprites/Sully_run-Sheet.png").convert_alpha()], [9, 0.005, pygame.image.load(
            "../sprites/Sully_jump-Sheet.png").convert_alpha()], [1, 0, pygame.image.load(
            "../sprites/Sully_fall-Sheet.png").convert_alpha()], [1, 0, pygame.image.load(
            "../sprites/Sully_fall-Sheet.png").convert_alpha()]]
        self.state = [0, 2, 0, 1, 0, 0]#0:idle, 1: moving, 2: jumping, 3: falling, 4:fast-falling, 5:dashing
        self.image = None
        self.width = 52
        self.offset = 8
        self.height = 45
        self.sprites = []

        for sheet in self.sheet:
            self.get_sprites(sheet[0], sheet[2])

        self.get_flip_sprite(self.sprites[0])
        self.get_flip_sprite(self.sprites[1])
        self.get_flip_sprite(self.sprites[2])
        self.get_flip_sprite(self.sprites[3])
        self.get_flip_sprite(self.sprites[4])

        for i in range(len(self.sprites)):
            self.sprites[i] = self.scale_sprite(self.sprites[i])

        # sprites = [idle, run, jump, fall, fast-fall, re-idle, re-run, re-jump, re-fall, re-fast-fall]

        self.animation_state = [self.sprites[0], 5]
        self.animate(self.animation_state[0], 0)
        self.position = pygame.math.Vector2(80, 80)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = self.acc = self.jump_vel = pygame.math.Vector2(0, 0)
        self.jumps_options = 2
        self.dash_key_down = self.down = self.direction = self.is_dashing = self.jump_key_down = self.active_jump = False
        self.Y_INITIAL = self.X_INITIAL = self.frame = 0


    def get_sprites(self, num, sheet):
        sprites = []
        for i in range(0, num):
            image = pygame.Surface((self.width, self.height)).convert_alpha()
            colourkey = image.get_at((0,0))
            image.set_colorkey(colourkey)
            image.blit(sheet, (0, 0), (i * (self.width+self.offset)+2, 9, self.width, self.height))
            sprites.append(image)
        self.sprites.append(sprites)

    def animate(self, sprites, frame):
        self.image = sprites[frame]

    def get_flip_sprite(self, sprites):
        temp = []
        for img in sprites:
            temp.append(pygame.transform.flip(img, True, False).convert_alpha())
        self.sprites.append(temp)

    def scale_sprite(self, sprites):
        temp = []
        for sprite in sprites:
            temp.append(pygame.transform.scale(sprite, (self.width * x_scale_factor, self.height * y_scale_factor)).convert_alpha())
        return temp
    def wall_collision(self):
        wall_collision = []
        if self.position.x <= 0.5*self.rect.w:
            self.position.x = 0.5*self.rect.w
            self.vel.x = 0
            wall_collision.append("left")
        if self.position.y <= 0.5*self.rect.h:
            self.position.y = 0.5*self.rect.h
            self.vel.y = 0
            wall_collision.append("up")
        if self.position.x >= WIDTH-0.5*self.rect.w:
            self.position.x = WIDTH-0.5*self.rect.w
            self.vel.x = 0
            wall_collision.append("right")
        if self.position.y >= HEIGHT-0.5*self.rect.h:
            self.position.y = HEIGHT-0.5*self.rect.h
            self.vel.y = 0
            wall_collision.append("down")
        return wall_collision

    def movement_input(self, collison):
        # 0:idle, 1: moving, 2: jumping, 3: falling, 4:fast-falling, 5:dashing
        movement = False
        if collison:
            limit = 6
        else:
            limit = 4
        if "down" in collison:
            self.state = [1, 0, self.state[2], 0, 0, 0]
        else:
            self.state = [0, 0, self.state[2], 1, 0, 0]
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_SPACE]:
            if self.vel.y > -1*y_scale_factor and self.jumps_options != 0 and "up" not in collison and not self.jump_key_down:
                self.vel.y = 0
                self.state[2] = 1
                self.state[0] = 0
                self.jump_key_down = True
                self.Y_INITIAL = self.position.y
                self.jumps_options -= 1
            # self.vel.y = -3
            # self.acc.y = -2*ACCELERATION
        if key[pygame.K_s]:
            if self.vel.y < 15*y_scale_factor and "down" not in collison:
                self.acc.y = ACCELERATION
                self.state[4] = 1
                self.state[0] = 0
                self.state[2] = 0

        if key[pygame.K_a]:
            if self.vel.x > -limit*x_scale_factor and "left" not in collison:
                self.acc.x = -ACCELERATION
                self.state[1] = 1
                self.state[0] = 0
                self.direction = False

        if key[pygame.K_d]:
            if self.vel.x < limit*x_scale_factor and "right" not in collison:
                self.acc.x = ACCELERATION
                self.state[1] = 2
                self.state[0] = 0
                self.direction = True

        if key[pygame.K_l]:
            if not self.dash_key_down and ("left" not in collison or "right" not in collison) and "down" in collison and self.state[1] != 0:
                self.state[5] = 1
                self.state[0] = 0
                self.dash_key_down = True
                self.X_INITIAL = self.position.x
                self.INITIAL_direction = self.direction

        if self.state[1] == 0 and self.state[4] == 0:
            if self.vel.x != 0:
                if self.vel.x < 0:
                    self.vel.x += 0.25 * ACCELERATION * x_scale_factor
                else:
                    self.vel.x -= 0.25 * ACCELERATION * x_scale_factor
            if self.vel.y != 0:
                if self.vel.y < 0:
                    self.vel.y += 0.25 * ACCELERATION * y_scale_factor
                else:
                    self.vel.y -= 0.25 * ACCELERATION * y_scale_factor
            self.vel.x = self.vel.x.__round__(1)
            self.vel.y = self.vel.y.__round__(1)

    def gravity(self, collision):
        if self.vel.y < 10 * y_scale_factor and self.state[2] == 0 and "down" not in collision:
            self.acc.y += 0.5 * ACCELERATION * y_scale_factor


    def update(self):

        wall_collision = self.wall_collision()
        self.movement_input(wall_collision)

        if self.state[5] == 1:
            if self.state[1] == 1:
                if self.vel.x < 5:
                    self.acc.x = -10 * X_ACCELERATION
                    if self.X_INITIAL - self.position.x >= 300*x_scale_factor or wall_collision or self.direction:
                        self.state[5] = 0
                        self.vel.x = -2.5*x_scale_factor
            elif self.state[1] == 2:
                if self.vel.x > -5:
                    self.acc.x = 10 * X_ACCELERATION
                    if self.position.x - self.X_INITIAL >= 300*x_scale_factor or wall_collision or not self.direction:
                        self.state[5] = 0
                        self.vel.x = 2.5 * x_scale_factor

        if self.state[2] == 0:

            self.gravity(wall_collision)


        else:
            self.acc.y = -1.5 * Y_ACCELERATION

            if self.Y_INITIAL - self.position.y >= 60*y_scale_factor or "left" in wall_collision or "right" in wall_collision:
                self.state[2] = 0


        self.vel += self.acc
        self.position += self.vel
        self.rect.center = self.position

        if "left" in wall_collision or "right" in wall_collision or "down" in wall_collision:
            self.jumps_options = 2

        self.surface.blit(pygame.font.SysFont("Arial", 25).render(f"Acceleration: {self.acc}", True, "white"), (20, 60))
        self.acc = pygame.math.Vector2(0, 0)
        self.surface.blit(pygame.font.SysFont("Arial", 25).render(f"Velocity: {self.vel}", True, "black"), (20, 20))
        # self.surface.blit(pygame.font.SysFont("Arial", 25).render(f"Jumps:  {self.jumps_options}", True, "white"), (20, 100))
        # self.surface.blit(pygame.font.SysFont("Arial", 25).render(f"Active Jump: {self.active_jump}", True, "white"), (20, 140))
        # self.surface.blit(pygame.font.SysFont("Arial", 25).render(f"Jump_key_down: {self.jump_key_down}", True, "white"), (20, 180))


        # 0:idle, 1: moving, 2: jumping, 3: falling, 4:fast-falling, 5:dashing
        # sprites = [idle, run, jump, fall, fast-fall, re-idle, re-run, re-jump, re-fall, re-fast-fall]
        if self.vel.x == 0:
            if self.direction:
                self.animation_state = [self.sheet[0][0], self.sheet[0][1], self.sprites[0]]
            else:
                self.animation_state = [self.sheet[0][0], self.sheet[0][1], self.sprites[5]]

        if self.state[1] == 2 and "down" in wall_collision:
            self.animation_state = [self.sheet[1][0], self.sheet[1][1], self.sprites[1]]
        if self.state[1] == 1 and "down" in wall_collision:
            self.animation_state = [self.sheet[1][0], self.sheet[1][1], self.sprites[6]]


        if "down" not in wall_collision:
            if round(self.vel.y) >= 15 or self.state[4]:
                if self.direction:
                    self.animation_state = [self.sheet[4][0], self.sheet[4][1], self.sprites[4]]
                else:
                    self.animation_state = [self.sheet[4][0], self.sheet[4][1], self.sprites[9]]
            else:
                if self.direction:
                    self.animation_state = [self.sheet[3][0], self.sheet[3][1], self.sprites[3]]
                else:
                    self.animation_state = [self.sheet[3][0], self.sheet[3][1], self.sprites[8]]

        if self.state[2] == 1:
            self.animation_state = [self.sheet[2][0], self.sheet[2][1], self.sprites[2]]
        # if int(self.acc.x) > 0 and "down" in wall_collision and self.state[1] == 2:
        #     self.animation_state = [self.sheet[3][0], self.sheet[3][1], self.sprites[3]]
        # if int(self.acc.x) < 0 and "down" in wall_collision and not self.state[1] == 1:
        #     self.animation_state = [self.sheet[3][0], self.sheet[3][1], self.sprites[6]]

        # else:
        #     self.animation_state = [self.sheet[1][0], self.sheet[1][1], self.sprites[1]]
        # animation state[0] is number of frames in animation
        # animation state[1] is speed to change the frame at
        # animation state[2] is the list of images

        if self.frame> self.animation_state[0]-1:
            self.frame = 0
        if self.frame < self.animation_state[0]-1:
                self.animate(self.animation_state[2], int((self.frame)))
                self.frame += self.animation_state[1]
        else:
            self.animate(self.animation_state[2], int((self.frame)))
            self.frame = 0


        self.surface.blit(self.image, self.rect)



p = player("cheese", 30, 40, screen)

run = True
while run:
    screen.fill("white")
    clock.tick(60)
    key = pygame.key.get_pressed()
    p.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or pygame.K_w:
                p.jump_key_down = False
            if event.key == pygame.K_a or pygame.K_d:
                p.state[1] = 0
            if event.key == pygame.K_l:
                p.dash_key_down = False


    if key[pygame.K_RETURN]:
        run = False



    pygame.display.update()
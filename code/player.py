from settings import *
from sprites import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'idle', 0

        self.image = pygame.image.load(join('..','images','player', 'down', '0001.png')).convert_alpha()

        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,-80)



        #movement
        self.dumping = 0
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites


    def load_images(self):
        self.frames = {'idle':[],'left':[],'right':[],'up':[],'down':[],'down_left':[],'down_right':[],'up_left':[],'up_right':[]}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk (join('..','images','player', state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)


    def input(self, dt):

        keys = pygame.key.get_pressed()
        input_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        input_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        input_up = keys[pygame.K_UP] or keys[pygame.K_w]
        input_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.fire = keys[pygame.K_SPACE]
        if int(input_left) == 0 and int(input_right) == 0:
            self.direction.x = self.direction.x * self.dumping
            if abs(self.direction.x) < 0.01:
                self.direction.x = int(0)
        else:
            self.direction.x = int(input_right) - int(input_left)

        if int(input_up) == 0 and int(input_down) == 0:
            self.direction.y = self.direction.y * self.dumping
            if abs(self.direction.y) < 0.01:
                self.direction.y = int(0)
        else:
            self.direction.y = int(input_down) - int(input_up)

        self.direction = self.direction.normalize() if (abs(self.direction.x) >= 1 or abs(self.direction.y) >= 1) else self.direction


        #print(self.direction)
    def move(self, dt):

        self.hitbox_rect.x += self.speed * self.direction.x * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.speed * self.direction.y * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center;


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
        pass

    def abduction(self):
        pass

    def shoot(self, dt):
        # self.laser_surf = pygame.Surface((10, 100), pygame.SRCALPHA).convert_alpha()
        # self.laser = Laser(self.rect, self.laser_surf, self.all_sprites)
        pass
    def animate(self, dt):
        #get state
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = 'idle'
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        if self.direction.y < 0 and self.direction.x > 0:
            self.state = 'up_right'
        if self.direction.y > 0 and self.direction.x > 0:
            self.state = 'down_right'
        if self.direction.y < 0 and self.direction.x < 0:
            self.state = 'up_left'
        if self.direction.y > 0 and self.direction.x < 0:
            self.state = 'down_left'


        #animation
        self.frame_index += 60 * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input(dt)
        self.move(dt)
        #self.shoot(dt)
        self.animate(dt)





        # self.rect.center = pygame.mouse.get_pos()





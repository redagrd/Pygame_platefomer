import pygame
import numpy

WIDTH = 1500
HEIGHT = 1000
BACKGROUND = (0, 0, 0)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")
        self.min_jumpspeed = 3
        self.prev_key = pygame.key.get_pressed()
        
        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1, 12)]
        self.animation_index = 0
        self.facing_left = False
        
        self.speed = 5
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0
    
    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def update(self, boxes, ground):
        hsp = 0
        onground = self.check_collision(0,1, boxes) or self.check_collision(0,1, ground)
        
        key = pygame.key.get_pressed()
        if key [pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            self.move(-self.speed, 0, boxes)
        elif key [pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            self.move(self.speed, 0, boxes)
        else:
            self.image = self.stand_image
        
        if key [pygame.K_UP]:
            self.vsp = -self.jumpspeed
        
        # variable jump height
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        
        self.prev_key = key
        
        # gravity    
        if self.vsp < 10 and not onground:
            self.jump_animation()
            self.vsp += self.gravity

        if self.vsp > 0 and onground:
            self.vsp = 0
            
        self.move(hsp, self.vsp, boxes)
        
    # movement
    def move(self, x, y, boxes):
        dx = x
        dy = y
        
        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)
            
        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)
                    
        self.rect.move_ip([dx, dy])
        
    def check_collision(self,x, y, boxes):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, boxes)
        self.rect.move_ip([-x, -y])
        return collide

class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)
    
class Ground(Sprite):
    def __init__(self, startx, starty):
        super().__init__("tile_0121.png", startx, starty)

class Background(Sprite):
    def __init__(self, startx, starty):
        super().__init__("backgrounds.png", startx, starty)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    player = Player(100, 200)
    
    boxes = pygame.sprite.Group()
    ground = pygame.sprite.Group() 
    background = pygame.sprite.Group()
    for gnd in range(0, 500, 70):
        ground.add(Ground(gnd, 700))
    for gnd in range(800, 1500, 70):
        ground.add(Ground(gnd, 700))
    boxes.add(Box(100, 430))
    boxes.add(Box(730, 430))
    
    
    background.add(Background(0, 0))
    
    while True:
        pygame.event.pump()
        player.update(boxes, ground)
        
        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        boxes.draw(screen)
        ground.draw(screen)
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()


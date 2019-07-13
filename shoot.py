import pygame
from pygame.locals import *
import sys
import os
import random

# Define screen
WIDTH = 720
HEIGHT = 720
FPS = 60
# SCORE, example: need 2000 point to level 1 up
LEVEL1_SCORE = 2500
LEVEL2_SCORE = 4500
# Sprites property
# Bullet
BULLET_SPEED = -50
# Ship
SHIP_SPEED = 8
# Meteor
NUMBER_OF_METEOR = 6
# UFO
UFO_SCORE = 400
UFO_HEAL = 5
BOSS_HEAL = 50
BOSS_SPEED = -2
BOSS_SCORE = 2000


# Define colors
BLACK = (  0,   0,   0)
RED =   (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE =  (  0,   0, 255)
WHITE = (255, 255, 255)
GALAXY_COLOR = (0, 144, 133)

# Init
pygame.init()
pygame.mixer.init()
score = 0

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Save Galaxy")
clock = pygame.time.Clock()

#images dir
img_dir = os.path.join(os.path.abspath('.'), 'img')
meteor_dir = os.path.join(img_dir, 'meteor')
spaceship_dir = os.path.join(img_dir, 'spaceship')
explosions_dir = os.path.join(img_dir, 'explosions')
ufo_dir = os.path.join(img_dir, 'ufo')
# Background
background_path = os.path.join(img_dir, 'background.jpg')
# Font
font_path = os.path.join(os.path.abspath('.'), 'font', 'RobotoMono.ttf')
# Sound path
sound_dir = os.path.join(os.path.abspath('.'), 'sound')

# Groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
UFOs = pygame.sprite.Group()
UFOWeapons = pygame.sprite.Group()
Bosses = pygame.sprite.Group()


# LOAD IMAGE
# background
background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# load meteor images
meteor_imgs = []
for img_num in range(1, 9):
    meteor_img = pygame.image.load(os.path.join(meteor_dir, 'meteor{}.png'.format(img_num))).convert()
    meteor_imgs.append(meteor_img)

# load ufo images
ufo_imgs = []
for img_num in range(1, 5):
    ufo_img = pygame.image.load(os.path.join(ufo_dir, 'ufo{}.png'.format(img_num))).convert()
    ufo_imgs.append(ufo_img)

# load ufo_weapon images
ufo_weapons_img = []
for img_num in range(1, 3):
    ufo_weapon = pygame.image.load(os.path.join(ufo_dir, 'ufo_weapon{}.png'.format(img_num))).convert()
    ufo_weapons_img.append(ufo_weapon)

# Explosion frames
explosions_imgs = []
for i in range(9):
    image_path = os.path.join(explosions_dir, 'regularExplosion0{}.png'.format(i))
    frame = pygame.image.load(image_path).convert()
    frame.set_colorkey(BLACK)
    explosions_imgs.append(frame)

# SpaceShip
spaceship_img = pygame.image.load(os.path.join(spaceship_dir, 'ship.png')).convert()
# Bullet
bullet_img = pygame.image.load(os.path.join(spaceship_dir, 'laserBlue.png')).convert()
# BOSS image
boss_img = pygame.image.load(os.path.join(ufo_dir, 'boss.png')).convert()

# Load sound
# shoot sound
shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir, "shoot.wav"))
# Explosion
explosion_sound = pygame.mixer.Sound(os.path.join(sound_dir, "explosion.wav"))

# Define bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = BULLET_SPEED

    def update(self):
        self.shoted()

    def shoted(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Define Meteor
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(meteor_imgs)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -80)
        self.speed_y = random.randrange(1, 9)
        self.speed_x = random.randrange(-1, 2)
        self.score = self.rect.width

    def update(self):
        self.fall()

    def fall(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.top > HEIGHT + self.rect.height
            or self.rect.left > WIDTH + self.rect.width
            or self.rect.right < 0 - self.rect.width):
            self.kill()
            if score < LEVEL1_SCORE:
                create_new_meteor()


# Define ship
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceship_img, (65, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 24
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 0
        self.level = 0
    
    def update(self):
        self.move()

    def move(self):
        self.speed = 0
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.speed = -SHIP_SPEED
        if keys[K_RIGHT]:
            self.speed = SHIP_SPEED
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        #shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def collide(self, group):
        collision = False
        group_crashed = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle)
        if group_crashed:
            for element in group_crashed:
                # Generate explosions
                ship_expl = Explosion(self)
                all_sprites.add(ship_expl)
                element_expl = Explosion(element)
                all_sprites.add(element_expl)
            collision = True
        return collision


class UFO(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(ufo_imgs)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed_y = 1
        self.speed_x = random.randint(-10, 10)
        self.score = UFO_SCORE
        self.heal = UFO_HEAL
        self.delay_attack = random.choice([4000, 5000])
        self.last_attack = pygame.time.get_ticks()

    def update(self):
        self.move()
        now = pygame.time.get_ticks()
        if self.rect.left > 0 and self.rect.right < WIDTH:
            if now - self.last_attack > self.delay_attack:
                self.last_attack = now
                self.attack()

    def move(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0) and score > LEVEL2_SCORE:
            self.kill()
        elif self.rect.top > HEIGHT and self.rect.left < WIDTH and self.rect.right > 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
        elif self.rect.left > WIDTH + self.rect.width:
            self.speed_x = -self.speed_x
            self.rect.y = -self.speed_y
        elif self.rect.right < 0 - self.rect.width:
            self.speed_x = -self.speed_x
            self.rect.y = -self.speed_y
    
    def attack(self):
        weapon = UFOWeapon(self.rect.centerx, self.rect.bottom)
        UFOWeapons.add(weapon)
        all_sprites.add(weapon)
        pass


class UFOWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(ufo_weapons_img), (10, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 3

    def update(self):
        self.shoted()

    def shoted(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class BOSS(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss_img, (800, 400))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 200
        self.rect.centery = 100
        self.radius = 200
        self.stop = False
        self.heal = BOSS_HEAL
        self.delay_attack = random.randrange(400, 500)
        self.last_attack = pygame.time.get_ticks()

    def update(self):
        if self.rect.centerx == WIDTH // 2:
            self.stop = True
        self.move()
        now = pygame.time.get_ticks()
        if self.rect.left > -100 and self.rect.right < WIDTH + 100:
            if now - self.last_attack > self.delay_attack:
                self.last_attack = now
                self.attack()

    def move(self):
        if not self.stop:
            self.rect.x += BOSS_SPEED

    def attack(self):
        x = random.randrange(self.rect.left + 50, self.rect.right - 50)
        y = self.rect.centery
        weapon = UFOWeapon(x, y)
        UFOWeapons.add(weapon)
        all_sprites.add(weapon)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, ThisSprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosions_imgs[0]
        pygame.transform.scale(self.image, (ThisSprite.rect.width, ThisSprite.rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = ThisSprite.rect.center
        self.frame_number = 0
        self.frame_update_delay = 60
        self.last_time_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time_update > self.frame_update_delay:
            self.last_time_update = now
            self.frame_number += 1
            if self.frame_number >= len(explosions_imgs):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosions_imgs[self.frame_number]
                self.rect = self.image.get_rect()
                self.rect.center = position
 

def draw_message(suface, message, size, color, x, y):
    '''
    Draw a message at position: midtop = (x, y), width font size and color on input Suface
    '''
    font_path = os.path.join(os.path.abspath('.'), 'font', 'RobotoMono.ttf')
    font_family = pygame.font.match_font(font_path)
    font = pygame.font.Font(font_family, size)
    message_surf = font.render(message, True, color)
    message_position = message_surf.get_rect()
    message_position.midtop = (x, y)
    suface.blit(message_surf, message_position)


def show_begin_game(screen):
    '''
    Show guild when game's start
    '''
    start_game = False
    screen.blit(background, background_rect)
    # music
    pygame.mixer.music.load(os.path.join(sound_dir, "intro.wav"))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1)
    # Draw
    draw_message(screen, "Save Galaxy", 69, GALAXY_COLOR, WIDTH / 2, 80)
    draw_message(screen, "Press left and right arrow key to move spaceship", 32, WHITE, WIDTH / 2, 350)
    draw_message(screen, "Press <space> to fire", 32, WHITE, WIDTH / 2, 400)
    draw_message(screen, ">>Press any key to start game<<", 24, WHITE, WIDTH / 2, 500)
    draw_message(screen, "Press ESC to quit game", 18, WHITE, WIDTH / 2, 600)
    # Render
    pygame.display.flip()
    # Event processing
    quit_game = False
    while not start_game and not quit_game:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game = True
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                start_game = True
                # Stop intro music when game's start
                pygame.mixer.music.stop()


def show_game_message(message, score):
    '''
    Show a message on screen when game over or game win.
    '''
    screen.blit(background, background_rect)
    draw_message(screen, message, 69, GALAXY_COLOR, WIDTH // 2, 80)
    score_message = "Your score: {}".format(score)
    draw_message(screen, score_message, 50, WHITE, WIDTH // 2, 200)
    draw_message(screen, "<F5> to try again", 32, WHITE, WIDTH // 4, 500)
    draw_message(screen, "<ESC> to quit game", 32, WHITE, 3 * WIDTH // 4, 500)
    pygame.display.flip()
    quit_game = False
    try_again = False
    while not quit_game and not try_again:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit_game = True
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and event.key == K_F5:
                try_again = True


def create_new_meteor():
    '''
    '''
    meteor = Meteor()
    meteors.add(meteor)
    all_sprites.add(meteor)


def main(score):
    level = 0
    ufo_added = False
    boss_added = False
    # Spaceship gen
    ship = SpaceShip()
    all_sprites.add(ship)
    # meteor gen
    for i in range(NUMBER_OF_METEOR):
        meteor = Meteor()
        meteors.add(meteor)
        all_sprites.add(meteor)

    # Game loop
    show_begin_game(screen)
    pygame.time.wait(200)
    running = True
    game_over = False
    game_win = False
    while running:
        # Set FPS
        clock.tick(FPS)
        # Check win game
        if game_win or game_over:
            if game_over:
                # Delay
                pygame.time.wait(400)
                show_game_message("Game Over", score)
                game_over = False
            elif game_win:
                pygame.time.wait(400)
                show_game_message("You Win!", score)
                game_win = False
            # Reset all core variables
            ufo_added = False
            boss_added = False
            score = 0
            # Reset groups
            all_sprites.empty()
            meteors.empty()
            bullets.empty()
            UFOs.empty()
            UFOWeapons.empty()
            Bosses.empty()
            # Re-Generate sprites
            # Spaceship gen
            ship = SpaceShip()
            all_sprites.add(ship)
            # meteor gen
            for i in range(NUMBER_OF_METEOR):
                meteor = Meteor()
                meteors.add(meteor)
                all_sprites.add(meteor)


        # Processing events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LEFT:
                    ship.speed = -8
                if event.key == K_RIGHT:
                    ship.speed = 8
                if event.key == K_SPACE:
                    shoot_sound.play()
                    ship.shoot()

        if score >= LEVEL2_SCORE:
            level = 2
        elif score >= LEVEL1_SCORE:
            level = 1
        else:
            level = 0

        if level == 1:
            if not ufo_added:
                # add ufo
                for i in range(5):
                    ufo = UFO()
                    UFOs.add(ufo)
                    all_sprites.add(ufo)
                ufo_added = True
        elif level == 2:
            if not boss_added:
                # add boss
                B = BOSS()
                Bosses.add(B)
                all_sprites.add(B)
                boss_added = True
        
        # Update
        all_sprites.update()

        # Handling collisions
        # ship hit meteor
        ship_collide_meteor = ship.collide(meteors)
        if ship_collide_meteor:
            explosion_sound.play()
            game_over = True
        
        ship_collide_ufo = ship.collide(UFOs)
        if ship_collide_ufo:
            explosion_sound.play()
            game_over = True

        ship_collide_ufo_weapons = ship.collide(UFOWeapons)
        if ship_collide_ufo_weapons:
            explosion_sound.play()
            game_over = True

        # bullets hit meteor
        bullet_hit_meteor = pygame.sprite.groupcollide(meteors, bullets, True, True)
        for hit in bullet_hit_meteor:
            # increase score
            score += hit.score
            # Generate explosions
            expl = Explosion(hit)
            all_sprites.add(expl)
            explosion_sound.play()
            # Create new meteor
            if score < LEVEL1_SCORE:
                create_new_meteor()

        # bullet hit ufos
        ufo_hit_by_bullet = pygame.sprite.groupcollide(UFOs, bullets, False, True)
        for ufo in ufo_hit_by_bullet:
            if ufo.rect.y > 0:
                if ufo.heal <= 0:
                    # increase score
                    score += ufo.score
                    # Generate explosions
                    expl = Explosion(ufo)
                    all_sprites.add(expl)
                    explosion_sound.play()
                    ufo.kill()
                else:
                    ufo.heal -= 1

        # Checking collusion of bullet and boss
        boss_hit_by_bullets = pygame.sprite.groupcollide(Bosses, bullets, False, True)
        for boss in boss_hit_by_bullets:
            boss.heal -= 1
            if boss.heal <= 0:  # BOSS LOSE
                score += BOSS_SCORE
                boss_expl = Explosion(boss)
                all_sprites.add(boss_expl)
                explosion_sound.play()
                boss.kill()
                game_win = True
            for bullet in boss_hit_by_bullets[boss]:
                bullet_expl = Explosion(bullet)
                all_sprites.add(bullet_expl)
                explosion_sound.play()

        # Draw
        screen.blit(background, background_rect)
        # Print score at center
        draw_message(screen, "score: " + str(score), 30, WHITE, WIDTH // 2, 10)
        # Print level at right corner
        draw_message(screen, "level: " + str(level), 30, WHITE,  5 * WIDTH // 6, 10)
        all_sprites.draw(screen)
        # Render / Flip
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(score)
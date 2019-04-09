# encoding:utf-8
import pygame
import sys
import random

WIDTH = 956
HEIGHT = 560


# define button
def button(screen, position, text):
    btn_width = 310
    btn_height = 65
    left, top = position
    pygame.draw.line(screen, (150, 150, 150), (left, top), (left + btn_width, top), 5)
    pygame.draw.line(screen, (150, 150, 150), (left, top - 2), (left, top + btn_height), 5)
    pygame.draw.line(screen, (50, 50, 50), (left, top + btn_height), (left + btn_width, top + btn_height), 5)
    pygame.draw.line(screen, (50, 50, 50), (left + btn_width, top + btn_height), (left + btn_width, top), 5)
    pygame.draw.rect(screen, (100, 100, 100), (left, top, btn_width, btn_height))
    font = pygame.font.Font('./resources/font/simkai.ttf', 50)
    text_render = font.render(text, 1, (255, 0, 0))
    return screen.blit(text_render, (left + 50, top + 10))


# the initial window
def home(screen):
    clock = pygame.time.Clock()
    while True:
        btn_single = button(screen, (330, 190), '单人模式')
        btn_double = button(screen, (330, 305), '双人模式')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_single.collidepoint(pygame.mouse.get_pos()):
                    return 1
                elif btn_double.collidepoint(pygame.mouse.get_pos()):
                    return 2
        clock.tick(60)
        pygame.display.update()


# define bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, id, position):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = ['./resources/imgs/bullet.png']
        self.img = pygame.image.load(self.imgs[0]).convert_alpha()
        self.img = pygame.transform.scale(self.img, (10, 10))
        # position
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = position
        self.position = position
        # SPEED
        self.speed = 8
        # player id
        self.player_id = id

    # move the bullet
    def move(self):
        self.position = self.position[0], self.position[1] - self.speed
        self.rect.left, self.rect.top = self.position

    # draw the bullet
    def draw(self, screen):
        screen.blit(self.img, self.rect)


# define asteroid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = ['./resources/imgs/asteroid.png']
        self.img = pygame.image.load(self.imgs[0]).convert_alpha()
        # position
        self.rect = self.img.get_rect()
        self.position = (random.randrange(20, WIDTH - 20), -64)
        self.rect.left, self.rect.top = self.position
        self.speed = random.randrange(3, 9)
        self.angle = 0
        self.angular_velocity = random.randrange(1, 5)
        self.rotate_ticks = 3

    # move the asteroid
    def move(self):
        self.position = self.position[0], self.position[1] + self.speed
        self.rect.left, self.rect.top = self.position

    # rotate the asteroid
    def rotate(self):
        self.rotate_ticks -= 1
        if self.rotate_ticks == 0:
            self.angle = (self.angle + self.angular_velocity) % 360
            orig_rect = self.img.get_rect()
            rot_img = pygame.transform.rotate(self.img, self.angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_img.get_rect().center
            rot_img = rot_img.subsurface(rot_rect).copy()
            self.img = rot_img
            self.rotate_ticks = 3

    # draw the asteroid
    def draw(self, screen):
        screen.blit(self.img, self.rect)


# define the ship
class Ship(pygame.sprite.Sprite):
    def __init__(self, id):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = ['./resources/imgs/ship.png', './resources/imgs/ship_exploded.png']
        self.img = pygame.image.load(self.imgs[0]).convert_alpha()
        self.explode_img = pygame.image.load(self.imgs[1]).convert_alpha()
        self.position = {'x': random.randrange(-10, 918), 'y': random.randrange(-10, 520)}
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = self.position['x'], self.position['y']
        self.speed = {'x': 10, 'y': 5}
        self.player_id = id
        self.cooling_time = 0
        self.explode_step = 0

    # if the ship explode
    def explode(self, screen):
        img = self.explode_img.subsurface((48 * (self.explode_step - 1), 0), (48, 48))
        screen.blit(img, (self.position['x'], self.position['y']))
        self.explode_step += 1

    # move the ship
    def move(self, direction):
        if direction == 'left':
            self.position['x'] = max(-self.speed['x'] + self.position['x'], -10)
        elif direction == 'right':
            self.position['x'] = min(self.speed['x'] + self.position['x'], 918)
        elif direction == 'up':
            self.position['y'] = max(-self.speed['y'] + self.position['y'], -10)
        elif direction == 'down':
            self.position['y'] = min(self.speed['y'] + self.position['y'], 520)
        self.rect.left, self.rect.top = self.position['x'], self.position['y']

    # draw the ship
    def draw(self, screen):
        screen.blit(self.img, self.rect)

    # shoot
    def shoot(self):
        return Bullet(self.player_id, (self.rect.center[0] - 5, self.position['y'] - 5))


# game window
def game(num_player, screen):
    pygame.mixer.music.load(("./resources/sounds/Cool Space Music.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    explosion_sound = pygame.mixer.Sound('./resources/sounds/boom.wav')
    fire_sound = pygame.mixer.Sound('./resources/sounds/shoot.ogg')
    font = pygame.font.Font('./resources/font/simkai.ttf', 20)
    # the background
    bg_imgs = ['./resources/imgs/bg_big.png',
               './resources/imgs/seamless_space.png',
               './resources/imgs/space3.jpg']
    bg_move_dis = 0
    bg_1 = pygame.image.load(bg_imgs[0]).convert()
    bg_2 = pygame.image.load(bg_imgs[1]).convert()
    bg_3 = pygame.image.load(bg_imgs[2]).convert()
    # player,bullet,asteroid
    player_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()

    asteroid_ticks = 90
    for i in range(num_player):
        player_group.add(Ship(i + 1))
    clock = pygame.time.Clock()
    # score
    score_1 = 0
    score_2 = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # player1:↑↓←→ :contorl, j :shoot
        # player2:w a s d :contorl,blank space:shoot
        pressed_keys = pygame.key.get_pressed()
        i = -1
        for player in player_group:
            i += 1
            direction = None
            if i == 0:
                if pressed_keys[pygame.K_UP]:
                    direction = 'up'
                elif pressed_keys[pygame.K_DOWN]:
                    direction = 'down'
                elif pressed_keys[pygame.K_LEFT]:
                    direction = 'left'
                elif pressed_keys[pygame.K_RIGHT]:
                    direction = 'right'
                if direction:
                    player.move(direction)
                if pressed_keys[pygame.K_j]:
                    if player.cooling_time == 0:
                        fire_sound.play()
                        bullet_group.add(player.shoot())
                        player.cooling_time = 20
            elif i == 1:
                if pressed_keys[pygame.K_w]:
                    direction = 'up'
                elif pressed_keys[pygame.K_s]:
                    direction = 'down'
                elif pressed_keys[pygame.K_a]:
                    direction = 'left'
                elif pressed_keys[pygame.K_d]:
                    direction = 'right'
                if direction:
                    player.move(direction)
                if pressed_keys[pygame.K_SPACE]:
                    if player.cooling_time == 0:
                        fire_sound.play()
                        bullet_group.add(player.shoot())
                        player.cooling_time = 20
            if player.cooling_time > 0:
                player.cooling_time -= 1
        if (score_1 + score_2) < 50:
            background = bg_1
        elif (score_1 + score_2) < 100:
            background = bg_2
        else:
            background = bg_3
        # move down the bg img,make the ship fly up
        screen.blit(background, (0, -background.get_rect().height + bg_move_dis))
        screen.blit(background, (0, bg_move_dis))
        bg_move_dis = (bg_move_dis + 2) % background.get_rect().height
        # create asteroid
        if asteroid_ticks == 0:
            asteroid_ticks = 90
            asteroid_group.add(Asteroid())
        else:
            asteroid_ticks -= 1
        # draw the ship
        for player in player_group:
            if pygame.sprite.spritecollide(player, asteroid_group, True, None):
                player.explode_step = 1
                explosion_sound.play()
            elif player.explode_step > 0:
                if player.explode_step > 3:
                    player_group.remove(player)
                    if len(player_group) == 0:
                        return
                else:
                    player.explode(screen)
            else:
                player.draw(screen)
        # draw the bullets
        for bullet in bullet_group:
            bullet.move()
            if pygame.sprite.spritecollide(bullet, asteroid_group, True, None):
                bullet_group.remove(bullet)
                if bullet.player_id == 1:
                    score_1 += 1
                else:
                    score_2 += 1
            else:
                bullet.draw(screen)
        # draw asteroid
        for asteroid in asteroid_group:
            asteroid.move()
            asteroid.rotate()
            asteroid.draw(screen)
        # show the score
        score_1_text = '玩家一得分： %s' % score_1
        score_2_text = '玩家二得分： %s' % score_2
        text_1 = font.render(score_1_text, True, (0, 0, 255))
        text_2 = font.render(score_2_text, True, (255, 0, 0))
        screen.blit(text_1, (2, 5))
        screen.blit(text_2, (2, 35))
        pygame.display.update()
        clock.tick(60)


# game over window
def game_over(screen):
    clock = pygame.time.Clock()
    while True:
        btn_1 = button(screen, (330, 190), '重新开始')
        btn_2 = button(screen, (330, 305), '退出游戏')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1.collidepoint(pygame.mouse.get_pos()):
                    return
                elif btn_2.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
        pygame.display.update()


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('飞机大战v1.0 by hb')
    num_player = home(screen)
    if num_player == 1:
        while True:
            game(num_player=1, screen=screen)
            game_over(screen)
    else:
        while True:
            game(num_player=2, screen=screen)
            game_over(screen)


if __name__ == '__main__':
    main()

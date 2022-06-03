# majhols


import pygame
import sys
import random
import time


# start pygame mudule
pygame.init()


# all variabels
display_with = 570
display_height = 730
floor_x = 0
pipe_list = []
game_status = True
bird_list_index = 0
game_font = pygame.font.Font('assets/font/Flappy.TTF', 40)
score = 0
high_score = 0
active_score = True
# jazebe
gravity = 0.25
# harkat parande
bird_movement = 0


#.......userevent........#
create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT+1
# zaman tolid lole :1200 mili secend
pygame.time.set_timer(create_pipe, millis=1200)
pygame.time.set_timer(create_flap, millis=90)
#...............#
#......sound.......#
win_sound = pygame.mixer.Sound('assets/sound/smb_stomp.wav')

game_over_sound = pygame.mixer.Sound('assets/sound/smb_mariodie.wav')

# andaze aks ra 2 barabar kon va beriz dakhel backgrund_image
backgrund_image = pygame.transform.scale2x(
    pygame.image.load('assets/img/bg2.png'))

floor_image = pygame.transform.scale2x(
    pygame.image.load('assets/img/floor.png'))


#..........animation bird...........#
bird_image_down = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_down_flap.png'))
bird_image_mid = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_mid_flap.png'))
bird_image_up = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_up_flap.png'))

bird_list = [bird_image_down, bird_image_mid, bird_image_up]

bird_image = bird_list[bird_list_index]


# ......pipe lole load....
pipe_image = pygame.transform.scale2x(
    pygame.image.load('assets/img/pipe_red.png'))

game_over_image = pygame.transform.scale2x(
    pygame.image.load('assets/img/message.png'))

game_over_image_rect = game_over_image.get_rect(center=(270, 252))


def generate_pipe_rect():
    random_pipe = random.randrange(300, 500)
    # aks pipe bala
    pipe_rect_top = pipe_image.get_rect(midbottom=(700, random_pipe-300))
    # aks pipe paiin
    pipe_rect_bottom = pipe_image.get_rect(midtop=(700, random_pipe))

    return pipe_rect_top, pipe_rect_bottom


def move_pipe_rect(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipe = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipe

# chap lole


def display_pipe(pipes):
    for pipe in pipes:
        # lole paeen
        if pipe.bottom >= 730:
            main_screen.blit(pipe_image, pipe)

        # lole bala ra bar aks kon
        else:
            reversed_pipes = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(reversed_pipes, pipe)
# chek colision barkhord rokh dad


def check_colision(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(3)
            active_score = True

            return (False)

        if bird_image_rect.bottom <= -50 or bird_image_rect.top >= 600:
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return (False)

    return True


def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_image_rect.centery))

    return new_bird, new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(
            str(score), False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(250, 120))
        main_screen.blit(text1, text1_rect)
    if status == 'game_over':
        # score
        text1 = game_font.render(
            f'Score:{score}', False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(250, 120))
        main_screen.blit(text1, text1_rect)
        # highscore
        text2 = game_font.render(
            f'High score {high_score}', False, (255, 255, 255))
        text2_rect = text2.get_rect(center=(270, 550))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0:
                active_score = True
    if score > high_score:
        high_score = score
    return high_score


# keshidan moraba dor aks
bird_image_rect = bird_image.get_rect(center=(100, 365))

# game display

main_screen = pygame.display.set_mode((display_with, display_height))


# game timer
clock = pygame.time.Clock()

# game logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # end pygame majhol
            pygame.quit()
            # end game termanete program
            sys.exit()
        # har key ke feshar dade shod
        if event.type == pygame.KEYDOWN:
            # kelid space ke zad beparad bala be tedad 8
            if event.key == pygame.K_SPACE:
                # aval meghdarash ra reset kon 0 kon
                bird_movement = 0
                bird_movement -= 8
                # bastan barname ba kelid esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r and game_status == False:
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (100, 365)
                bird_movement = 0
                score = 0
                #active_score = True

        # agar user event ma bod ke hamishe true hast in shart
        if event.type == create_pipe:
            # mokhtasat lole hai bala va paeen ra add kon
            pipe_list.extend(generate_pipe_rect())
        # agar user event ma bod ke hamishe true hast in shart
        if event.type == create_flap:
            if bird_list_index < 2:
                # migim index man ra1 adad add kon bad az har 200ms
                bird_list_index += 1
            else:
                bird_list_index = 0

            bird_image, bird_image_rect = bird_animation()
    # agar bazi faal ham nabashad zamin va backgrund ra neshan midahad baz
    # update page speed to ....
    main_screen.blit(backgrund_image, (0, -200))
    # agar bazi faal bod ya nabod:
    if game_status:

        # bird image
        main_screen.blit(bird_image, bird_image_rect)
        # check barkhord
        game_status = check_colision(pipe_list)
        # move pipe list
        pipe_list = move_pipe_rect(pipe_list)
        display_pipe(pipe_list)
        # floor gravity
        bird_movement += gravity
        bird_image_rect.centery += bird_movement

        # show score
        update_score()
        display_score('active')

    else:
        main_screen.blit(game_over_image, game_over_image_rect)
        display_score('game_over')

    # display floor
    floor_x -= 1
    main_screen.blit(floor_image, (floor_x, 600))
    main_screen.blit(floor_image, (floor_x+570, 600))
    if floor_x <= -570:
        floor_x = 0

    pygame.display.update()
    # set game speed
    clock.tick(90)

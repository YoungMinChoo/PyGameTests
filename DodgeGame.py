import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
CHAR_WIDTH, CHAR_HEIGHT = 40, 60
CHAR_VEL = 5
STAR_VEL = 3
STAR_WIDTH, STAR_HEIGHT = 10, 20

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fun Little Dodging Game')
BG = pygame.transform.scale(pygame.image.load("assets/img/space_bg.jpg"), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont('comicsans', 30)

def reset():
    character = pygame.Rect(200,  HEIGHT - CHAR_HEIGHT, CHAR_WIDTH, CHAR_HEIGHT)
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0
    stars = []          
    state = 'running'
    CHAR_VEL = 5
    return character, start_time, elapsed_time, star_add_increment, star_count, stars, state, CHAR_VEL

def draw(character, elapsed_time, stars, best_time, state):
    WIN.blit(BG, (0,0))

    elapsed_time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, 'white')
    WIN.blit(elapsed_time_text, (20, 10))
    pygame.draw.rect(WIN, 'red', character)
    for star in stars:
        pygame.draw.rect(WIN, 'white', star)
    if best_time > 0:
        best_time_text = FONT.render(f"Best Time: {round(best_time)}s", 1, 'white')
        WIN.blit(best_time_text, (20, 40))
        
    if state == 'hit':
        lost_text1 = FONT.render(f"You survived {round(elapsed_time)}s before dying! Try Again?", 1, 'red')
        WIN.blit(lost_text1, (WIDTH/2 - lost_text1.get_width()/2, HEIGHT/2 - lost_text1.get_height()/2))
        lost_text2 = FONT.render("(press f to restart, or q to quit)", 1, 'red')
        WIN.blit(lost_text2, (WIDTH/2 - lost_text2.get_width()/2, HEIGHT/2 - lost_text2.get_height()/2 + 30))
    elif state == 'exit':
        exit_text = FONT.render("Are you sure you want to quit? (press c to continue, or q to quit)", 1, 'red')
        WIN.blit(exit_text, (WIDTH/2 - exit_text.get_width()/2, HEIGHT/2 - exit_text.get_height()/2))
    pygame.display.flip()

def main():
    run = True
    clock = pygame.time.Clock()
    clock.tick(60)
    character, start_time, elapsed_time, star_add_increment, star_count, stars, state, CHAR_VEL = reset()
    best_time = 0
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if state != 'hit' and state != 'exit':
                    state = 'exit'
                else:
                    run = False
                break
        
        if keys[pygame.K_LEFT] and character.x - CHAR_VEL >= 0:
            character.x -= CHAR_VEL
        elif keys[pygame.K_RIGHT] and character.x + CHAR_VEL + character.width <= WIDTH:
            character.x += CHAR_VEL
        elif keys[pygame.K_ESCAPE]:
            if state != 'hit':
                state = 'exit'
            
        if state == 'running':
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time
            if star_count > random.randint(100, star_add_increment):
                for _ in range(random.randint(1,5)):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)
                
                star_add_increment = max(100, star_add_increment - 50)
                star_count = 0
            

            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= character.y and star.colliderect(character):
                    stars.remove(star)
                    state = 'hit'
                    break
        elif state == 'hit':
            CHAR_VEL = 0
            pygame.display.update()
            if keys[pygame.K_q]:
                run = False
                break
            elif keys[pygame.K_f]:
                state = 'running'
                if elapsed_time > best_time:
                    best_time = elapsed_time
                character, start_time, elapsed_time, star_add_increment, star_count, stars, state, CHAR_VEL = reset()
                continue
        elif state == 'exit':
            if keys[pygame.K_q]:
                run = False
                break
            elif keys[pygame.K_c]:
                state = 'running'
                continue
        clock.tick(60)
        draw(character, elapsed_time, stars, best_time, state)
    pygame.quit()

if __name__ == '__main__':
    main()
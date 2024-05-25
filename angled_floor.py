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
pygame.display.set_caption('Fun Little Game')
BG = pygame.transform.scale(pygame.image.load("assets/img/space_bg.jpg"), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont('comicsans', 30)

def draw(character, elapsed_time, stars):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, 'white')
    WIN.blit(time_text, (20, 10))
    pygame.draw.rect(WIN, 'red', character)
    for star in stars:
        pygame.draw.rect(WIN, 'white', star)
    pygame.display.update()

def main():
    run = True
    character = pygame.Rect(200,  HEIGHT - CHAR_HEIGHT, CHAR_WIDTH, CHAR_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []          
    hit = False
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if star_count > random.randint(100, star_add_increment):
            for _ in range(random.randint(1,5)):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            
            star_add_increment = max(100, star_add_increment - 50)
            star_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and character.x - CHAR_VEL >= 0:
            character.x -= CHAR_VEL
        elif keys[pygame.K_RIGHT] and character.x + CHAR_VEL + character.width <= WIDTH:
            character.x += CHAR_VEL
        elif keys[pygame.K_ESCAPE]:
            run = False
            break

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= character.y and star.colliderect(character):
                stars.remove(star)
                hit = True
        if hit:
            lost_text = FONT.render("You Lost!", 1, 'red')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(character, elapsed_time, stars)
    pygame.quit()

if __name__ == '__main__':
    main()
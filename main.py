# NOTE: THIS GAME IS MORE FUN WITH A FRIEND
import pygame

# Initializes font and mixer
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500

# Creates a window using the given dimensions & sets the windows title
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dual of the Fates")
pygame.display.set_icon(pygame.image.load('Assets/icon.jpg'))

# Colors in RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Creates a barrier in the centre of the screen
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Sounds are loaded and put into variables
BACKGROUNDSOUND = pygame.mixer.Sound('Assets/soundfx/background.mp3')
TIE_BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/soundfx/tiehit.mp3')
XWING_BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/soundfx/xwinghit.mp3')
TIE_BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/soundfx/tiefire.mp3')
XWING_BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/soundfx/xwingfire.mp3')

# Custom star wars font for health and win screen are set along with its size
HEALTH_FONT = pygame.font.Font("Assets/Starjedi.ttf", 35)
WINNER_FONT = pygame.font.Font('Assets/Starjedi.ttf', 95)

# Sets the frames per second for game
FPS = 60

# Sets speed of spaceships, bullet velocity and max bullets
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 4

# Sets the width and height of spaceships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 45

# Variables for when either spaceships are hit
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Imports image for left side and scales it in terms of screen resolution
YELLOW_SPACESHIP_IMAGE = pygame.image.load('Assets/tieFighter.png')
YELLOW_SPACESHIP = pygame.transform.flip(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), True, False)

# Imports image for right side and scales it in terms of screen resolution
RED_SPACESHIP_IMAGE = pygame.image.load('Assets/xwing.png')
RED_SPACESHIP = pygame.transform.flip(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), True, False)

# Sets the background image
SPACE = pygame.transform.scale(pygame.image.load('Assets/space.jpg'), (WIDTH, HEIGHT))


# Function for displaying objects on screen
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # Puts background in the center of the screen and draws black border in center
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Variables that store the amount of health of left/right side
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    # Display healths in the top corners for spaceships on their respective sides
    WIN.blit(red_health_text,
             (WIDTH - red_health_text.get_width() - 5, 0))
    WIN.blit(yellow_health_text, (5, 0))

    # Draws both red and yellow spaceships on screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # For loops creates bullets for both sides using rectangles
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

        # Updates the screen for HUD to appear
    pygame.display.update()


# Function creates movement for the left side
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


# Function creates movement for the right side
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


# Function deals with bullets once they had been fired
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # Deletes yellow bullets once hit other spaceship or goes out of bounds
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    # Deletes yellow bullets once hit other spaceship or goes out of bounds
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# Displays image screen for 5 seconds and then next round begins
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, YELLOW)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
                         2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


# Main function that runs the game
def main():
    # Plays the background music indefinitely
    music = pygame.mixer.music.load("Assets/soundfx/background.mp3")
    pygame.mixer.music.play(-1)

    # Sets the size for both spaceships
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # Lists to store all bullets
    red_bullets = []
    yellow_bullets = []

    # Number of health both side have
    red_health = 16
    yellow_health = 16

    # Creates the timer and sets run as true
    clock = pygame.time.Clock()
    run = True

    # Begins the game
    while run:

        # Sets the timer
        clock.tick(FPS)

        # Checks if close button has been clicked and ends game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Looks for any keystrokes
            if event.type == pygame.KEYDOWN:

                # Closes the game if ESCAPE is pressed
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

                # Yellow side shoots if bullets are left and V is pressed
                if event.key == pygame.K_v and len(
                        yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)

                    # Adds bullet to list and sounds effect is played
                    yellow_bullets.append(bullet)
                    TIE_BULLET_FIRE_SOUND.play()

                # Red side shoots if bullets are left and num pad 0 is pressed
                if event.key == pygame.K_KP0 and len(
                        red_bullets) < MAX_BULLETS:
                    XWING_BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

                    # Lowers health by 1 if red is hit
            if event.type == RED_HIT:
                red_health -= 1
                XWING_BULLET_HIT_SOUND.play()

            # Lowers health by 1 if yellow is hit
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                TIE_BULLET_HIT_SOUND.play()

        # Checks if red health is 0 and variable becomes yellow victory
        winner_text = ""
        if red_health <= 0:
            winner_text = "Empire Wins!"

        # Checks if yellow health is 0 and variable becomes red victory
        if yellow_health <= 0:
            winner_text = "Rebels Wins!"

        # Displays the victory screen
        if winner_text != "":
            draw_winner(winner_text)
            break

        # Gets the keys that are pressed and allows movement for both sides
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Allows bullets to work
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Draws all objects on screen
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

main()


# If a specific error shows up, it returns an empty string
try:
    if __name__ == "__main__":
        main()
except pygame.error as e:
    print("")

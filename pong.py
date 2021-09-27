from sys import exit

import pygame
import pygame.freetype

from settings import *
from paddle import Paddle
from ball import Ball

def game_over():

    """
    Displays a "game over" message on the screen.
    Who won, by how much and does the user want to play again ('r') or quit ('q')?
    """

    # Figure out who is the winner
    if(player_score == 5):
        winner_text = f"GAME OVER - PLAYER WINS {player_score}-{opponent_score}"
    else:
        winner_text = f"GAME OVER - OPPONENT WINS {player_score}-{opponent_score}"
    
    # Display the game over text
    text = pygame.freetype.SysFont(pygame.font.get_default_font(), 40)
    text.render_to(screen, (300,SCREEN_HEIGHT//2 + 50), winner_text, WHITE)
    text.render_to(screen, (300,SCREEN_HEIGHT//2 + 100), "Press 'r' to restart or 'q' to quit.", WHITE)
    pygame.display.flip()

    # Wait for user input, play again or quit?
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 1
                if event.key == pygame.K_q:
                    return 0

def reset_player_objects():

    """
    After a player scores all game objects must be reset
    to their starting positions before another round can ensue.
    """

    global player_paddle, opponent_paddle, ball

    # Recreate the player's paddle
    player_paddle = Paddle(10,(SCREEN_HEIGHT-PADDLE_HEIGHT)//2)

    # Recreate the opponent's (ai) paddle
    opponent_paddle = Paddle(SCREEN_WIDTH-PADDLE_WIDTH-10,(SCREEN_HEIGHT-PADDLE_HEIGHT)//2)

    # Recreate the ball
    ball = Ball()

def update_score():

    """
    Updates the player scores on the screen
    """

    # Update PLAYER's score
    GAME_FONT.render_to(screen, (SCREEN_WIDTH/2 - 80,50), str(player_score), WHITE)

    # Update OPPONENT's score
    GAME_FONT.render_to(screen, (SCREEN_WIDTH/2 + 40,50), str(opponent_score), WHITE)

def ai_movement():

    """
    Handles the logic behind the movement of the opponent, which
    is a basic AI (as much as you can call the below if statements an "AI") in my implementation.
    """

    global opponent_paddle

    # Paddle below ball? Move up
    if opponent_paddle.y < ball.y:
        opponent_paddle.y += MAX_PADDLE_SPEED - 5 # AI moves slower, else unbeatable

    # Paddle above ball? Move down.
    if opponent_paddle.y > ball.y:
        opponent_paddle.y -= MAX_PADDLE_SPEED - 5 # AI moves slower, else unbeatable

    # Hitting roof?
    if opponent_paddle.y <= 0:
        opponent_paddle.y = 0

    # Hitting floor?
    if opponent_paddle.y >= SCREEN_HEIGHT - PADDLE_HEIGHT:
        opponent_paddle.y = SCREEN_HEIGHT - PADDLE_HEIGHT

def AABB(ball,paddle):

    """
    Uses Axis-Aligned Bounding Box to detect a collision
    between the ball and a paddle.
    """

    if(ball.x < paddle.x + PADDLE_WIDTH and
       ball.x + BALL_RADIUS > paddle.x and
       ball.y < paddle.y + PADDLE_HEIGHT and
       ball.y+ BALL_RADIUS > paddle.y):
        return 1
    return 0

def check_collisions():

    """
    Checks if the ball and/or paddle(s) collides with anything.
    """

    global opponent_score, player_score, ball

    # Bouncing on roof or floor
    if ball.y < 0 or ball.y > SCREEN_HEIGHT - BALL_RADIUS:
        ball.dy *= -1
            
    # Bouncing on left or right wall
    if ball.x < 0:
        reset_player_objects()
        opponent_score += 1
        return
        
    if ball.x > SCREEN_WIDTH - BALL_RADIUS:
        reset_player_objects()
        player_score += 1
        return
            
    # Bouncing on paddle
    if AABB(ball,player_paddle) or AABB(ball,opponent_paddle):
        ball.dx *= -1
        BOUNCE_SOUND.play()
    
    # Paddle going through the roof
    if player_paddle.y < 0:
        player_paddle.y = 0
    
    # Paddle going through the floor
    if player_paddle.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
        player_paddle.y = SCREEN_HEIGHT - PADDLE_HEIGHT

def draw_game_objects():

    """
    Draws the game objects on the screen.
    """

    # Clear screen
    screen.fill(BLACK)

    update_score()
    
    # Redraw the game objects
    player_paddle.draw(screen)
    opponent_paddle.draw(screen)
    ball.draw(screen)
    
    # Redraw the middle line
    pygame.draw.aaline(
        screen, 
        WHITE, 
        (SCREEN_WIDTH/2,0), 
        (SCREEN_WIDTH/2,SCREEN_HEIGHT)
    )

if __name__ == "__main__":

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Pong")
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    GAME_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 80)
    BOUNCE_SOUND = pygame.mixer.Sound('assets/audio/bounce.wav')
    BOUNCE_SOUND.set_volume(0.3)

    running = True
    while running:

        game_objects = []

        # Create the player's paddle
        player_paddle = Paddle(10,(SCREEN_HEIGHT-PADDLE_HEIGHT)//2)

        # Create the opponent's (ai) paddle
        opponent_paddle = Paddle(SCREEN_WIDTH-PADDLE_WIDTH-10,(SCREEN_HEIGHT-PADDLE_HEIGHT)//2)

        # Create the ball
        ball = Ball()

        player_score = 0
        opponent_score = 0

        ##### GAMELOOP #####
        while True:

            # Eventlistener
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        player_paddle.updateSpeed(0, MAX_PADDLE_SPEED)
                    if event.key == pygame.K_UP:
                        player_paddle.updateSpeed(0, -MAX_PADDLE_SPEED)
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player_paddle.updateSpeed(0, -MAX_PADDLE_SPEED)
                    if event.key == pygame.K_UP:
                        player_paddle.updateSpeed(0, MAX_PADDLE_SPEED)
            
            # Update player objects positions
            player_paddle.step()
            ai_movement() # "step function" for the opponent's (AI's) movement
            ball.step()
            
            # Check for collisions
            check_collisions()

            # Update visuals
            draw_game_objects()

            # Check for winner
            if player_score == 5 or opponent_score == 5:
                play_again = game_over()
                if not play_again:
                    running = False
                break

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()
    exit()

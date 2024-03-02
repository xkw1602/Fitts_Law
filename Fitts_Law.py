import pygame
import random
import time
import math

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
BACKGROUND_COLOR = (192,192,192)
ACTIVE_COLOR = (255, 0, 0)
INACTIVE_COLOR = (0, 0, 0)
TRIAL_WD = (60, 180, 20, 60, 100, 300,
            50, 350, 30, 210, 40, 280,
            50, 750, 25, 375, 40, 600,
            20, 620, 25, 775, 30, 930,
            15, 945, 10, 630, 12, 756)
# Enumeration for different game states
class GameState:
    START_MENU = 0
    INSTRUCTIONS = 1
    TEST = 2
    TRIAL_COMPLETE = 3
    TEST_COMPLETE = 4

# Function to display text on the screen
def display_text(screen, text, font, color, height):
    text_surface = font.render(text, True, color)
    position = text_surface.get_rect(center=(SCREEN_WIDTH/2, height))
    screen.blit(text_surface, position)

# Function to display start menu
def display_start_menu(screen, font):
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Fitt's Law Test", font, (0, 0, 0), 225)
    display_text(screen, "Click Anywhere to Start", font, (0, 0, 0), 450)

# Function to display instructions
def display_instructions(screen, font):
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Instructions", font, (0, 0, 0), 100)
    display_text(screen, "Click on the leftmost box to start timing, then click", font, (0, 0, 0), 250)
    display_text(screen, "back and forth between the boxes as fast as you can.", font, (0, 0, 0), 300)
    display_text(screen, "After hitting 10 targets, the targets will change distance/size.", font, (0, 0, 0), 425)
    display_text(screen, "Click anywhere to Start the Test", font, (0, 0, 0), 550)

# Function to display trial complete screen
def display_trial_complete(screen, font, trial):
    screen.fill(BACKGROUND_COLOR)
    text = "Trial " + str(trial) + " of 15 complete!"
    display_text(screen, text, font, (0,0,0), SCREEN_HEIGHT/3)
    display_text(screen, "Click to start next trial", font, (0,0,0), SCREEN_HEIGHT*2/3)

# Function to display test complete screen
def display_test_complete(screen, font):
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Test Complete!", font, (0,0,0), SCREEN_HEIGHT/3)
    display_text(screen, "Click anywhere to return to the start menu", font, (0,0,0), SCREEN_HEIGHT*2/3)

# Function to run the Fitts's Law test
def run_test(screen, font, trial):
    times = []
    targets_hit = 0
    start_time = None
    target_size = TRIAL_WD[trial*2]
    target1_x = 300
    target_y = SCREEN_HEIGHT/2
    target2_x = target1_x + target_size + TRIAL_WD[trial*2+1]
    while True:
        screen.fill(BACKGROUND_COLOR)
        rect1=(target1_x, target_y, target_size, target_size)
        rect2=(target2_x, target_y, target_size, target_size)
        pygame.draw.rect(screen, ACTIVE_COLOR, rect1)
        pygame.draw.rect(screen, INACTIVE_COLOR, rect2)

        if start_time is None and targets_hit > 0: # start timer after first target is hit
            start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (target1_x <= mouse_x <= target1_x + target_size) and \
                (target_y <= mouse_y <= target_y + target_size):    # hit detection
                    targets_hit += 1
                    if targets_hit > 1: # record time
                        time_elapsed = round(time.time() - start_time, 2)
                        times.append(time_elapsed)
                    temp = target1_x # swap targets
                    target1_x = target2_x
                    target2_x = temp
                    start_time = None
                
        if targets_hit == 11: # end the trial after 10 + 1 target hits
            return times

        pygame.display.flip()

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fitts's Law Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    difficulty = 2
    stage = 1
    trial = 0
    current_state = GameState.START_MENU

    while True:
        if current_state == GameState.START_MENU:
            difficulty = 2
            stage = 1
            trial = 0
            display_start_menu(screen, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_state = GameState.INSTRUCTIONS

        elif current_state == GameState.INSTRUCTIONS:
            display_instructions(screen, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_state = GameState.TEST

        elif current_state == GameState.TEST:
            times = run_test(screen, font, trial)
            print("Difficulty:", difficulty, "Stage:", stage)
            print("Times:", times) #change to time
            average_time = 0
            sum = 0
            for x in times:
                sum += x
            average_time = sum/10
            print("Average time:", average_time)
            stage += 1
            trial += 1
            if stage == 4:
                stage = 1
                difficulty += 1
            if trial == 15:
                current_state = GameState.TEST_COMPLETE
            else:
                current_state = GameState.TRIAL_COMPLETE

        elif current_state == GameState.TRIAL_COMPLETE:
            display_trial_complete(screen, font, trial)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_state = GameState.TEST
        
        elif current_state == GameState.TEST_COMPLETE:
            display_test_complete(screen, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_state = GameState.START_MENU

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

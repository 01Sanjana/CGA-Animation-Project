
import pygame
import imageio.v2 as imageio
import numpy as np
import os
import math

# -----------------------------
# INITIAL SETTINGS
# -----------------------------
pygame.init()

WIDTH = 800
HEIGHT = 450
FPS = 20
DURATION = 35

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Small Act of Kindness")
clock = pygame.time.Clock()

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "kindness_story.mp4"
)

# Colors
SKY = (135, 206, 235)
GRASS = (105, 175, 95)
DARK_GREEN = (38, 110, 65)
WHITE = (255, 255, 255)
BLACK = (35, 35, 45)
BLUE = (55, 125, 220)
SKIN = (245, 190, 145)
BROWN = (125, 75, 45)
YELLOW = (255, 210, 65)
ORANGE = (240, 145, 45)

font = pygame.font.SysFont("arial", 25, bold=True)
small_font = pygame.font.SysFont("arial", 18)
title_font = pygame.font.SysFont("arial", 36, bold=True)


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def draw_text(text, y, color=WHITE, font_type=font):
    image = font_type.render(text, True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))

    # Dark background makes the text easy to read
    bg = pygame.Surface((rect.width + 24, rect.height + 14))
    bg.set_alpha(190)
    bg.fill((25, 45, 55))

    screen.blit(bg, (rect.x - 12, rect.y - 7))
    screen.blit(image, rect)


def draw_cloud(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 18)
    pygame.draw.circle(screen, WHITE, (x + 20, y - 8), 23)
    pygame.draw.circle(screen, WHITE, (x + 43, y), 18)
    pygame.draw.rect(screen, WHITE, (x - 2, y, 47, 16))


def draw_tree(x, y):
    pygame.draw.rect(screen, BROWN, (x - 9, y, 18, 85))
    pygame.draw.circle(screen, DARK_GREEN, (x, y - 12), 34)
    pygame.draw.circle(screen, (55, 140, 75), (x - 20, y), 24)
    pygame.draw.circle(screen, (65, 150, 80), (x + 20, y), 24)


def draw_boy(x, y, walking=True, frame=0):
    # Head
    pygame.draw.circle(screen, SKIN, (int(x), int(y)), 18)

    # Hair
    pygame.draw.arc(
        screen, BLACK,
        (x - 18, y - 19, 36, 26),
        0, math.pi, 5
    )
    pygame.draw.circle(screen, BLACK, (int(x + 7), int(y - 3)), 2)

    # Body
    pygame.draw.rect(
        screen, BLUE,
        (int(x - 15), int(y + 18), 30, 43),
        border_radius=7
    )

    # Arms move while walking
    swing = int(8 * math.sin(frame * 0.3)) if walking else 0

    pygame.draw.line(
        screen, SKIN,
        (int(x - 12), int(y + 28)),
        (int(x - 24), int(y + 43 + swing)), 7
    )
    pygame.draw.line(
        screen, SKIN,
        (int(x + 12), int(y + 28)),
        (int(x + 24), int(y + 43 - swing)), 7
    )

    # Legs
    pygame.draw.line(
        screen, BLACK,
        (int(x - 7), int(y + 59)),
        (int(x - 10 + swing), int(y + 82)), 8
    )
    pygame.draw.line(
        screen, BLACK,
        (int(x + 7), int(y + 59)),
        (int(x + 10 - swing), int(y + 82)), 8
    )

    # Shoes
    pygame.draw.line(
        screen, BLACK,
        (int(x - 10 + swing), int(y + 82)),
        (int(x - 20 + swing), int(y + 82)), 6
    )
    pygame.draw.line(
        screen, BLACK,
        (int(x + 10 - swing), int(y + 82)),
        (int(x + 20 - swing), int(y + 82)), 6
    )


def draw_bird(x, y, frame, flying=False):
    # Small bird body
    pygame.draw.ellipse(
        screen, YELLOW,
        (int(x - 17), int(y - 10), 34, 22)
    )

    # Head
    pygame.draw.circle(screen, YELLOW, (int(x + 13), int(y - 9)), 11)

    # Eye and beak
    pygame.draw.circle(screen, BLACK, (int(x + 16), int(y - 12)), 2)
    pygame.draw.polygon(
        screen, ORANGE,
        [(x + 23, y - 9), (x + 32, y - 5), (x + 23, y - 2)]
    )

    # Moving wings
    wing_move = int(9 * math.sin(frame * 0.7)) if flying else 3

    pygame.draw.ellipse(
        screen, (255, 230, 100),
        (int(x - 8), int(y - 17 - wing_move), 18, 15)
    )

    # Tail
    pygame.draw.polygon(
        screen, ORANGE,
        [(x - 15, y), (x - 28, y - 8), (x - 25, y + 5)]
    )


def draw_background():
    screen.fill(SKY)

    # Sun
    pygame.draw.circle(screen, YELLOW, (700, 70), 34)

    # Clouds
    draw_cloud(90, 75)
    draw_cloud(360, 100)

    # Distant trees
    draw_tree(80, 245)
    draw_tree(710, 245)

    # Park grass
    pygame.draw.rect(screen, GRASS, (0, 280, WIDTH, 170))

    # Path
    pygame.draw.polygon(
        screen, (210, 190, 150),
        [(270, 280), (530, 280), (680, 450), (120, 450)]
    )

    # Grass details
    for i in range(30, WIDTH, 55):
        pygame.draw.line(
            screen, DARK_GREEN,
            (i, 330 + (i % 45)),
            (i - 5, 320 + (i % 45)), 2
        )


def draw_water_bottle(x, y):
    # Blue water bottle
    pygame.draw.rect(
        screen, (80, 180, 240),
        (int(x), int(y), 18, 38),
        border_radius=4
    )
    pygame.draw.rect(
        screen, BLUE,
        (int(x + 4), int(y - 5), 10, 7)
    )
    pygame.draw.line(
        screen, WHITE,
        (int(x + 5), int(y + 7)),
        (int(x + 5), int(y + 25)), 2
    )


# -----------------------------
# ANIMATION AND VIDEO RECORDING
# -----------------------------
writer = None
frame_number = 0
total_frames = DURATION * FPS

print("Recording animation...")
print("A window will open. Please wait for the full video to finish.")

try:
    writer = imageio.get_writer(
        OUTPUT_FILE,
        fps=FPS,
        codec="libx264",
        macro_block_size=None
    )

    running = True

    while running and frame_number < total_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        t = frame_number / FPS

        # Draw the park scene
        draw_background()

        # Scene 1: Introduction
        if t < 4:
            draw_text("A SMALL ACT OF KINDNESS", 175, YELLOW, title_font)
            draw_text("A short animated story", 215, WHITE, small_font)

            draw_boy(175, 275, True, frame_number)

        # Scene 2: Boy walks through the park
        elif t < 11:
            boy_x = 100 + int((t - 4) * 43)
            draw_boy(boy_x, 275, True, frame_number)

            draw_text("It was a beautiful day in the park.", 35)

        # Scene 3: Boy notices a little bird
        elif t < 17:
            draw_boy(390, 275, False, frame_number)
            draw_bird(500, 355, frame_number, False)

            draw_text("He noticed a thirsty little bird.", 35)

            # Thought bubble
            pygame.draw.ellipse(
                screen, WHITE,
                (425, 295, 130, 40)
            )
            thought = small_font.render("Poor bird!", True, BLACK)
            screen.blit(thought, (450, 307))

        # Scene 4: Boy helps the bird with water
        elif t < 25:
            draw_boy(390, 275, False, frame_number)
            draw_bird(500, 355, frame_number, False)

            # Bottle moves towards the bird
            bottle_y = 350 - int(min(t - 17, 3) * 8)
            draw_water_bottle(450, bottle_y)

            draw_text("He offered the bird some water.", 35)

            # Water drops
            for i in range(3):
                drop_x = 493 + i * 9
                drop_y = 370 + int((frame_number % 12) * 0.6)
                pygame.draw.circle(
                    screen, (80, 180, 255),
                    (drop_x, drop_y), 3
                )

        # Scene 5: Bird becomes happy and flies away
        elif t < 31:
            draw_boy(390, 275, False, frame_number)

            bird_x = 500 + int((t - 25) * 38)
            bird_y = 350 - int((t - 25) * 30)

            draw_bird(bird_x, bird_y, frame_number, True)
            draw_text("The little bird felt better!", 35)

        # Scene 6: Moral of the story
        else:
            draw_boy(390, 275, False, frame_number)

            bird_x = 720 + int(15 * math.sin(frame_number * 0.2))
            bird_y = 150 + int(12 * math.sin(frame_number * 0.3))
            draw_bird(bird_x, bird_y, frame_number, True)

            draw_text("Kindness makes the world better!", 90, YELLOW)
            draw_text("Even a small act can make a big difference.", 130, WHITE, small_font)

        # Show current frame
        pygame.display.flip()

        # Save frame for the MP4 video
        frame_rgb = pygame.surfarray.array3d(screen)
        frame_rgb = np.transpose(frame_rgb, (1, 0, 2))
        writer.append_data(frame_rgb)

        frame_number += 1
        clock.tick(FPS)

finally:
    if writer is not None:
        writer.close()

    pygame.quit()

if frame_number > 0:
    print("Video saved successfully!")
    print("Location:", OUTPUT_FILE)
else:
    print("No frames were recorded. Run the program again.")

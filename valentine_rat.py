import pygame
import sys
import os
import random
from PIL import Image

# --- CONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NUM_RATS = 50
SPIN_SPEED_MULTIPLIER = 1.0
BACKGROUND_COLOR = (20, 20, 20)

TIMELINE = {
    1.0: "TEST",
    3.0: "TEST",
    5.0: "TEST",
    8.0: "TEST",
    12.0: "TEST",
    16.0: "TEST",
    19.0: "TEST",
}


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_gif_frames(gif_path, target_size=(150, 150)):
    pil_image = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = pil_image.convert("RGBA")
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)
            py_image = pygame.transform.scale(py_image, target_size)
            frames.append(py_image)
            pil_image.seek(pil_image.tell() + 1)
    except EOFError:
        pass
    return frames


# --- SETUP ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spinning Rat Valentine")
clock = pygame.time.Clock()

# --- ASSETS ---
try:
    gif_path = resource_path("rat.gif")
    rat_frames = load_gif_frames(gif_path, target_size=(150, 150))
    song_path = resource_path("song.mp3")
    pygame.mixer.music.load(song_path)
except Exception as e:
    print(f"Error loading assets: {e}")
    sys.exit()


# --- RAT CLASS ---
class Rat:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.frame_index = random.randint(0, len(rat_frames) - 1)
        self.anim_speed = random.uniform(0.8, 1.2) * SPIN_SPEED_MULTIPLIER

    def draw(self, surface, should_animate):
        if should_animate:
            self.frame_index += self.anim_speed

        current_frame_idx = int(self.frame_index) % len(rat_frames)
        current_image = rat_frames[current_frame_idx]
        rect = current_image.get_rect(center=(self.x, self.y))
        surface.blit(current_image, rect)


# --- MAIN LOOP ---
rats = [Rat() for _ in range(NUM_RATS)]
running = True
music_is_playing = False
hold_time = 0.0

font_large = pygame.font.SysFont("Arial", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

# Pre-load music
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.pause()

while running:
    dt = clock.tick(60) / 1000.0

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    keys = pygame.key.get_pressed()

    # --- RESET LOGIC (R key) ---
    if keys[pygame.K_r]:
        hold_time = 0.0
        # Optional: Reset rat positions too?
        # rats = [Rat() for _ in range(NUM_RATS)]

    # --- INPUT STATE CHECK ---
    is_holding_space = keys[pygame.K_SPACE]

    # --- MUSIC CONTROL ---
    if is_holding_space and not music_is_playing:
        pygame.mixer.music.unpause()
        music_is_playing = True
    elif not is_holding_space and music_is_playing:
        pygame.mixer.music.pause()
        music_is_playing = False

    # --- DRAWING LOGIC ---

    # 1. Update Timer
    if is_holding_space:
        hold_time += dt

    # 2. Draw Rats (Pass 'is_holding_space' to freeze them if not holding)
    # If hold_time is 0, we hide them to show the intro text cleanly
    if hold_time > 0.1:
        for rat in rats:
            rat.draw(screen, should_animate=is_holding_space)

    # 3. Draw Text
    if hold_time < 0.1:
        # INTRO SCREEN (Before she presses anything)
        # Show one static rat
        static_rat = rat_frames[0]
        rect = static_rat.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(static_rat, rect)

        msg = font_large.render("Hold SPACE to Spin", True, (255, 255, 255))
        rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(msg, rect)
    else:
        # DURING THE SHOW (Or Paused)
        current_text = ""
        for timestamp, msg in sorted(TIMELINE.items()):
            if hold_time >= timestamp:
                current_text = msg

        if current_text:
            txt_surf = font_large.render(current_text, True, (255, 255, 255))
            outline = font_large.render(current_text, True, (0, 0, 0))
            cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            screen.blit(outline, (cx - txt_surf.get_width() // 2 + 2, cy - txt_surf.get_height() // 2 + 2))
            screen.blit(txt_surf, (cx - txt_surf.get_width() // 2, cy - txt_surf.get_height() // 2))

        # Optional: Show "Paused" text if let go?
        if not is_holding_space:
            pause_msg = font_small.render("(Paused - Hold SPACE to continue)", True, (200, 200, 200))
            screen.blit(pause_msg, (SCREEN_WIDTH // 2 - pause_msg.get_width() // 2, SCREEN_HEIGHT - 50))

    pygame.display.flip()

pygame.quit()
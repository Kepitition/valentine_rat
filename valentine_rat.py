import pygame
import sys
import os
import random
from PIL import Image

# --- CONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NUM_RATS = 80
SPIN_SPEED_MULTIPLIER = 1.0
BACKGROUND_COLOR = (20, 20, 20)

TIMELINE = {
    6.0: "Fareler yeterli sayida dondugune gore\n artik mesaj kismina baslayabilirim sanirim?",
    10.0: "Mesaj kismina da gecmeden kucuk bir edit yapmam gerekiyor buraya",
    12.0: "Aslinda bunu hazirlamaya basladigimda bu kisim yoktu",
    14.0: "Ama sen surekli hediyeyle ilgili sorular sorduktan sonra eklemek istedim",
    16.0: "Biz tartismadan once bunu yapma karari almistim",
    18.0: "Her ne kadar basta inanmasan da burada not olarak kalsin istedim",
    20.0: "Ipucu verme konusunda da tereddutte kaldim cunku surprizi bozulsun istemedim.",
    22.0: "Neyse kucuk update bitti 3-4 saniye de bos dinle bakalim bari",
    26.0: "Hatirliyor musun bunu bu meme populerken yapmak istiyordum",
    28.0: "Cok delayli olsa da sana ulastirmak istedim",
    30.0: "",
    32.0: "TEST",
    34.0: "TEST",
    36.0: "TEST",
    38.0: "TEST",
    40.0: "OEST",
    42.0: "YEST",
    44.0: "KEST",
    46.0: "UEST",
    48.0: "TEST",
    50.0: "TEST",
    52.0: "Bir sene sonra okullarin aciklandiktan sonra ne yapacagimizi ben de bilmiyorum",
    54.0: "Keza Mart Nisanda orada oldugumda ne olacagimizi da bilmiyorum",
    56.0: "Fakat en azindan bu 1 senelik surecte",
    58.0: "Hayat bizi zoraki ayirana kadar seni cok sevmek istiyorum",
    60.0: "Bari Son kismini ingilizce yaziyim havali olsun",
    62.0: "Will you be my valentine ?",
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



def draw_multiline_text(surface, text, font, center_x, center_y,
                        text_color=(255, 255, 255),
                        outline_color=(0, 0, 0)):

    lines = text.split("\n")
    line_height = font.get_height()
    total_height = len(lines) * line_height
    start_y = center_y - total_height // 2

    for i, line in enumerate(lines):
        txt_surf = font.render(line, True, text_color)
        outline = font.render(line, True, outline_color)

        x = center_x - txt_surf.get_width() // 2
        y = start_y + i * line_height

        surface.blit(outline, (x + 2, y + 2))
        surface.blit(txt_surf, (x, y))


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

pygame.mixer.music.play(loops=-1)
pygame.mixer.music.pause()

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    keys = pygame.key.get_pressed()

    # RESET
    if keys[pygame.K_r]:
        hold_time = 0.0

    is_holding_space = keys[pygame.K_SPACE]

    # MUSIC CONTROL
    if is_holding_space and not music_is_playing:
        pygame.mixer.music.unpause()
        music_is_playing = True
    elif not is_holding_space and music_is_playing:
        pygame.mixer.music.pause()
        music_is_playing = False

    # TIMER
    if is_holding_space:
        hold_time += dt

    # DRAW RATS
    if hold_time > 0.1:
        for rat in rats:
            rat.draw(screen, should_animate=is_holding_space)

    # TEXT
    if hold_time < 0.1:
        static_rat = rat_frames[0]
        rect = static_rat.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(static_rat, rect)

        draw_multiline_text(
            screen,
            "Hold SPACE to Spin",
            font_large,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100
        )
    else:
        current_text = ""
        for timestamp, msg in sorted(TIMELINE.items()):
            if hold_time >= timestamp:
                current_text = msg

        if current_text:
            draw_multiline_text(
                screen,
                current_text,
                font_large,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )

        if not is_holding_space:
            pause_msg = font_small.render("(Paused - Hold SPACE to continue)", True, (200, 200, 200))
            screen.blit(pause_msg, (SCREEN_WIDTH // 2 - pause_msg.get_width() // 2, SCREEN_HEIGHT - 50))

    pygame.display.flip()

pygame.quit()

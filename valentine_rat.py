import pygame
import sys
import os
import random
import math
from PIL import Image

# --- CONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NUM_RATS = 80
SPIN_SPEED_MULTIPLIER = 1.0
BACKGROUND_COLOR = (20, 20, 20)
PARTY_TRIGGER_TIME = 64.0
PARTY_FADEOUT_MS = 2000

TIMELINE = {
    6.0: "Fareler yeterli sayida dondugune gore\n artik mesaj kismina baslayabilirim sanirim?",
    10.0: "Mesaj kismina da gecmeden kucuk bir edit yapmam gerekiyor buraya",
    12.0: "Aslinda bunu hazirlamaya basladigimda bu kisim yoktu",
    14.0: "Ama sen surekli hediyeyle ilgili sorular sorduktan sonra eklemek istedim",
    16.0: "Biz tartismadan once bunu yapma karari almistim",
    18.0: "Her ne kadar basta inanmasan da burada not olarak kalsin istedim",
    20.0: "Ipucu verme konusunda da tereddutte kaldim \n cunku surprizi bozulsun istemedim.",
    22.0: "Neyse kucuk update bitti 3-4 saniye de bos dinle bakalim bari",
    26.0: "Hatirliyor musun bunu bu meme populerken yapmak istiyordum",
    28.0: "Cok delayli olsa da sana ulastirmak istedim",
    30.0: "Aslinda paylasmak, soylemek istedigim cok sey oluyor",
    32.0: "Bazen mesafeden dolayi\n bazense birbirimizi yanlis anlasak da",
    34.0: "Gercekten seni kirmak en son istedigim sey",
    36.0: "Cunku seni kaybetmekten endise duyuyorum",
    38.0: "Bu oyunu, videoyu hazirlarken fark ettim",
    40.0: "Seninle / senin icin ugrasmayi ozlemisim",
    42.0: "Suanda yaninda olup birlikte izlemek de keyifli olurdu",
    44.0: "Maalesef yapamiyoruz tabii ki suan",
    46.0: "Her sey mukemmel gitmek zorunda degil",
    48.0: "Gelecegi dusunup dertlenmek yerine",
    50.0: "Su anin tadini cikaralim istiyorum",
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


# --- CONFETTI CLASS ---
class Confetti:
    def __init__(self):
        self.reset()
        self.y = random.randint(-SCREEN_HEIGHT, 0)

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, -10)
        self.size = random.randint(4, 10)
        self.speed = random.uniform(100, 300)
        self.drift = random.uniform(-30, 30)
        self.color = random.choice([
            (255, 0, 100), (255, 50, 200), (255, 200, 0),
            (0, 255, 150), (100, 200, 255), (255, 100, 50),
            (200, 50, 255), (255, 255, 100), (255, 255, 255),
        ])
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-200, 200)

    def update(self, dt):
        self.y += self.speed * dt
        self.x += self.drift * dt
        self.rotation += self.rot_speed * dt
        if self.y > SCREEN_HEIGHT + 20:
            self.reset()

    def draw(self, surface):
        w = self.size
        h = self.size * 0.6
        angle_rad = math.radians(self.rotation)
        cos_a = math.cos(angle_rad)
        apparent_w = max(2, int(abs(w * cos_a)))
        rect = pygame.Rect(0, 0, apparent_w, int(h))
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surface, self.color, rect)


# --- BOUNCING ROSE CLASS ---
class BouncingRose:
    def __init__(self, frames):
        self.frames = frames
        self.x = float(SCREEN_WIDTH // 2)
        self.y = float(SCREEN_HEIGHT // 2)
        angle = random.uniform(0.5, 1.2)
        speed = 250
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.frame_index = 0.0
        self.anim_speed = 1.0

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        half_w = self.frames[0].get_width() // 2
        half_h = self.frames[0].get_height() // 2
        if self.x - half_w <= 0 or self.x + half_w >= SCREEN_WIDTH:
            self.vx *= -1
            self.x = max(half_w, min(SCREEN_WIDTH - half_w, self.x))
        if self.y - half_h <= 0 or self.y + half_h >= SCREEN_HEIGHT:
            self.vy *= -1
            self.y = max(half_h, min(SCREEN_HEIGHT - half_h, self.y))
        self.frame_index += self.anim_speed

    def draw(self, surface):
        idx = int(self.frame_index) % len(self.frames)
        img = self.frames[idx]
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(img, rect)


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
    rose_path = resource_path("rose.gif")
    rose_frames = load_gif_frames(rose_path, target_size=(220, 220))
    joke_song_path = resource_path("joke_song.mp3")
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
party_mode = False
party_fade_started = False
party_song_started = False
disco_timer = 0.0
disco_color = BACKGROUND_COLOR

confetti_particles = [Confetti() for _ in range(120)]
bouncing_roses = [BouncingRose(rose_frames) for _ in range(15)]

font_large = pygame.font.SysFont("Arial", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

pygame.mixer.music.play(loops=-1)
pygame.mixer.music.pause()

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # RESET
    if keys[pygame.K_r]:
        hold_time = 0.0

    is_holding_space = keys[pygame.K_SPACE]

    # MUSIC CONTROL (skip pause/unpause once party mode is handling music)
    if not party_fade_started:
        if is_holding_space and not music_is_playing:
            pygame.mixer.music.unpause()
            music_is_playing = True
        elif not is_holding_space and music_is_playing:
            pygame.mixer.music.pause()
            music_is_playing = False
    elif party_mode:
        if is_holding_space and not music_is_playing:
            pygame.mixer.music.unpause()
            music_is_playing = True
        elif not is_holding_space and music_is_playing:
            pygame.mixer.music.pause()
            music_is_playing = False

    # TIMER
    if is_holding_space:
        hold_time += dt

    # PARTY MODE TRIGGER
    if hold_time >= PARTY_TRIGGER_TIME and not party_fade_started:
        party_fade_started = True
        pygame.mixer.music.fadeout(PARTY_FADEOUT_MS)

    if party_fade_started and not party_song_started and not pygame.mixer.music.get_busy():
        party_song_started = True
        party_mode = True
        pygame.mixer.music.load(joke_song_path)
        pygame.mixer.music.play(loops=-1)

    # DISCO BACKGROUND
    if party_mode and is_holding_space:
        disco_timer += dt
        if disco_timer > 0.1:
            disco_timer = 0.0
            disco_color = (
                random.randint(100, 255),
                random.randint(50, 255),
                random.randint(100, 255),
            )
        screen.fill(disco_color)
    else:
        screen.fill(BACKGROUND_COLOR)

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

    # PARTY MODE EFFECTS
    if party_mode and is_holding_space:
        for c in confetti_particles:
            c.update(dt)
            c.draw(screen)
        for rose in bouncing_roses:
            rose.update(dt)
            rose.draw(screen)

    pygame.display.flip()

pygame.quit()
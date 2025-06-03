import pygame
import pandas as pd
import random
import os
import sys
import subprocess
import shutil
import math

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHIER_EXCEL = os.path.join(BASE_DIR, "participants.xlsx")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
FRAME_DIR = os.path.join(BASE_DIR, "frames")
PRIX = [
    ("1er Prix", 150, (255, 215, 0)),    # Or plus vif
    ("2e Prix", 100, (230, 230, 230)),   # Argent plus clair
    ("3e Prix",  50, (205, 127, 50))     # Bronze (déjà bien)
]
FPS = 30
INTRO_DURATION = 5  # en secondes, affichera aussi un compte à rebours
TIRAGE_DURATION = 10  # en secondes
GAGNANT_DURATION = 5  # en secondes pour afficher le gagnant
NOM_AFFICHAGE_DUREE = 0.1  # durée d'affichage de chaque nom en secondes

# --- INITIALISATION ---
WIDTH, HEIGHT = 480, 800
pygame.init()
pygame.display.set_mode((1, 1))  # Nécessaire pour .convert_alpha()
screen = pygame.Surface((WIDTH, HEIGHT))
font_title = pygame.font.SysFont("Arial", 36)
font_name = pygame.font.SysFont("Arial", 42, bold=True)
font_button = pygame.font.SysFont("Arial", 28)

# --- PRÉPARATION ---
if os.path.exists(FRAME_DIR):
    for f in os.listdir(FRAME_DIR):
        os.remove(os.path.join(FRAME_DIR, f))
else:
    os.makedirs(FRAME_DIR)

# --- DONNÉES ---
df = pd.read_excel(FICHIER_EXCEL)
entries = []
participants_uniques = []
for _, row in df.iterrows():
    entries.extend([row['Nom']] * int(row['Participations']))
    if row['Nom'] not in participants_uniques:
        participants_uniques.append(row['Nom'])

# --- LOGO ---
def load_logo():
    if not os.path.exists(LOGO_PATH):
        print("Logo non trouvé. Placez 'logo.png' dans le dossier.")
        sys.exit()
    logo = pygame.image.load(LOGO_PATH).convert_alpha()
    logo = pygame.transform.smoothscale(logo, (WIDTH, HEIGHT // 2))
    logo.set_alpha(100)  # transparence
    return logo

logo = load_logo()

# --- UTILITAIRES ---
def draw_background():
    screen.fill((0, 0, 0))
    screen.blit(logo, (0, 0))
    screen.blit(logo, (0, HEIGHT // 2))

def draw_text_center(surface, text, y, size=32, color=(255, 255, 255), outline=False):
    font = pygame.font.SysFont(None, size)
    
    if outline:
        outline_color = (0, 0, 0)
        # Dessiner le contour en 8 directions
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    outline_surf = font.render(text, True, outline_color)
                    outline_rect = outline_surf.get_rect(center=(WIDTH // 2 + dx, y + dy))
                    surface.blit(outline_surf, outline_rect)

    # Texte principal au centre
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surf, text_rect)

def draw_confetti():
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])
        pygame.draw.circle(screen, color, (x, y), 3)

def draw_rounded_rect(surface, rect, color, radius=10):
    shape_surf = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, rect[2], rect[3]), border_radius=radius)
    surface.blit(shape_surf, (rect[0], rect[1]))

def save_frame(frame_count):
    path = os.path.join(FRAME_DIR, f"frame_{frame_count:04d}.png")
    pygame.image.save(screen, path)

# --- TIRAGE ET ENREGISTREMENT ---
def intro_screen(frame_count):
    for frame in range(FPS * INTRO_DURATION):
        draw_background()

        # Titre principal avec contour noir
        draw_text_center(screen, "Concours de Lancement", HEIGHT // 2 - 250, size=50, color=(255, 255, 255), outline=True)

        # Affichage des lots
        for index, (titre, montant, couleur) in enumerate(PRIX):
            draw_text_center(screen, f"{titre} : {montant}€", HEIGHT // 2 - 60 + index * 60, size=40 - index*2, color=couleur)

        # Compte à rebours dynamique avec fond
        secondes_restantes = INTRO_DURATION - (frame // FPS)
        texte = f"Début dans {secondes_restantes} seconde{'s' if secondes_restantes > 1 else ''}..."

        # Calcul pour position et rectangle
        box_y = HEIGHT // 2 + 180
        draw_rounded_rect(screen, (WIDTH//2 - 160, box_y - 25, 320, 50), (0, 0, 0, 180), radius=12)
        draw_text_center(screen, texte, box_y, size=30, color=(255, 255, 255), outline=True)

        save_frame(frame_count)
        frame_count += 1
    return frame_count

def tirer_nom(entries, frame_count, titre, montant, couleur=(255, 255, 255)):
    affichage_par_nom = int(NOM_AFFICHAGE_DUREE * FPS)
    total_frames = int(TIRAGE_DURATION * FPS)
    total_noms = total_frames // affichage_par_nom

    noms_affiches = []
    while len(noms_affiches) < total_noms:
        temp = participants_uniques.copy()
        random.shuffle(temp)
        noms_affiches.extend(temp)
    noms_affiches = noms_affiches[:total_noms]

    for nom in noms_affiches:
        for _ in range(affichage_par_nom):
            draw_background()
            draw_text_center(screen, f"{titre} - {montant}€", 200, size=60, color=couleur, outline=True)
            draw_text_center(screen, "Tirage en cours...", HEIGHT // 2, size=45)
            draw_text_center(screen, nom, HEIGHT // 2 + 200, size=60)
            save_frame(frame_count)
            frame_count += 1

    gagnant = random.choice(entries)
    return gagnant, frame_count

def show_gagnant(nom, prix, couleur, frame_count):
    for _ in range(FPS * GAGNANT_DURATION):
        draw_background()
        draw_confetti()
        draw_text_center(screen, f"{nom} gagne {prix}€ !", HEIGHT // 2, size=40, color=couleur, outline=True)
        save_frame(frame_count)
        frame_count += 1
    return frame_count

def draw_gagnants_liste(gagnants):
    draw_text_center(screen, "GAGNANTS DU TIRAGE", HEIGHT // 2 - 250, size=50, outline=True)
    start_y = HEIGHT // 2 - 60
    for i, (nom, montant, couleur) in enumerate(gagnants):
        rect_width, rect_height = 360, 40
        rect_x = (WIDTH - rect_width) // 2
        rect_y = start_y + i * 50 - rect_height // 2
        draw_rounded_rect(screen, (rect_x, rect_y, rect_width, rect_height), (30, 30, 30, 200), radius=12)
        draw_text_center(screen, f"{i+1}. {nom} - {montant}€", rect_y + rect_height // 2, size=28, color=couleur)
        
def draw_remerciements():
    # Texte multi-lignes
    lignes = [
        ("Merci à tous les participants !", 30, (200, 200, 200)),
        ("Vous avez tous gagné", 23, (200, 200, 200)),
        ("5% de réduction avec le code", 23, (200, 200, 200)),
        ("TIRAGE2025", 30, (255, 255, 0)),
        ("Valable jusqu'au 31/12/2025", 20, (200, 200, 200))
    ]

    # Calcul de la hauteur dynamique du bloc
    line_height = 30
    total_height = len(lignes) * line_height
    rect_width = WIDTH - 60
    rect_x = (WIDTH - rect_width) // 2
    rect_y = HEIGHT - total_height - 40  # espace depuis bas

    # Dessin du fond
    draw_rounded_rect(screen, (rect_x, rect_y, rect_width, total_height), (30, 30, 30, 200), radius=12)

    # Dessin du texte
    for i, (text, size, color) in enumerate(lignes):
        draw_text_center(screen, text, rect_y + 20 + i * line_height, size=size, color=color)
 
def show_liste_finale(gagnants, frame_count):
    for _ in range(FPS * 10):  # 5 secondes d'affichage
        draw_background()
        draw_gagnants_liste(gagnants)
        draw_remerciements()
        save_frame(frame_count)
        frame_count += 1
    return frame_count

# --- PIPELINE ---
frame_count = 0
frame_count = intro_screen(frame_count)
gagnants = []
for i, (titre, montant, couleur) in enumerate(PRIX):
    nom, frame_count = tirer_nom(entries, frame_count, titre, montant, couleur)
    gagnants.append((nom, montant, couleur))
    entries = [e for e in entries if e != nom]
    frame_count = show_gagnant(nom, montant, couleur, frame_count)

frame_count = show_liste_finale(gagnants, frame_count)

# --- GÉNÉRATION VIDÉO ---
print("Génération de la vidéo...")
output_file = os.path.join(BASE_DIR, "tirage.mp4")
subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS), "-i",
    os.path.join(FRAME_DIR, "frame_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", output_file
])
print(f"Vidéo générée : {output_file}")

# --- SUPPRESSION DES FRAMES ---
shutil.rmtree(FRAME_DIR)
print("Dossier de frames supprimé.")
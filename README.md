# Tirage Vidéo Automatisé 🎥🎉

Ce projet permet de générer une vidéo animée à partir d'un fichier Excel contenant les participants à un tirage au sort.

## Fonctionnalités

- Affichage animé des noms avec effets visuels
- Sélection aléatoire de gagnants
- Génération d'une vidéo finale avec musique et animation
- Utilisation d'un logo personnalisé

## Installation

1. Clone ou télécharge ce repo :
```bash
git clone https://github.com/ton-compte/Tirage.git
cd Tirage
```

2. Crée un environnement virtuel :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Installe les dépendances :
```bash
pip install -r requirements.txt
```

4. Assure-toi que `ffmpeg` est installé :
```bash
brew install ffmpeg
```

## Utilisation

Place ton fichier `.xlsx` dans le dossier. Puis lance :
```bash
python3 tirage_generate_video.py
```

La vidéo sera générée dans le fichier `tirage_final.mp4`.

---

Créé avec ❤️ pour les tirages plein de suspense !

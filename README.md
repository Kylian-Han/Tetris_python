# Tetris Python

**Auteur :** Haniquet Kylian

## Description du projet

Un jeu Tetris développé en Python utilisant la bibliothèque Pygame.

Ce code est basé sur le travail de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du langage".

## Installation et lancement

### Prérequis
- Python 3.x
- Pygame

### Installation des dépendances
```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur Linux/Mac :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer le jeu
```bash
python tetris.py
```

## Comment jouer

### Contrôles
- **Flèche Gauche** : Déplacer la pièce vers la gauche
- **Flèche Droite** : Déplacer la pièce vers la droite
- **Flèche Bas** : Accélérer la chute de la pièce
- **Flèche Haut** : Faire tourner la pièce
- **Espace** : Faire chuter instantanément la pièce
- **P** : Mettre en pause / Reprendre le jeu
- **Échap** : Quitter le jeu

### Système de score
- **Points par ligne** : Score = Nombre de lignes × Niveau
- **Bonus Tetris** : Score supplémentaire = Niveau × Nombre de Tetris
- **Progression** : Nouveau niveau tous les 10 lignes

## Historique des modifications

### Formatage avec YAPF
YAPF a formaté le code en le rendant plus 'respirable' :
- Ajout d'espaces entre les opérateurs
- Ajout de lignes vides à la fin de chaque fonction
- Correction des indentations
- Évitement des lignes trop longues pour améliorer la lisibilité


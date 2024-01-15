# README - MarkoXCA


## Introduction

Ce projet vise à faciliter le chiffrement et le déchiffrement de fichiers à l'aide de l'algorithme AES-256. Il comprend un script Python principal qui permet de traiter les fichiers en toute sécurité.

## Prérequis

Avant de pouvoir exécuter le script principal, assurez-vous de suivre les étapes suivantes pour configurer l'environnement :

1. **Installer les dépendances** : Exécutez le fichier `dependencies.bat` pour installer toutes les dépendances nécessaires au projet. Ceci est nécessaire pour que le script fonctionne correctement.

2. **Gérer les clés** : Le dossier `key` est utilisé pour gérer les clés de chiffrement. Vous pouvez définir une clé de chiffrement à l'aide du script ou en éditant directement le fichier `encryption_key.key`. Assurez-vous que la clé est en format base64.

## Utilisation

Pour lancer le script Python plus facilement, utilisez le fichier `quick_launch.bat`. Vous pouvez également exécuter le script manuellement en utilisant Python avec la commande :

```bash
python crypter.pyw

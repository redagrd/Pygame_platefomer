# ouvrir un environnement .venv

```python
py -m venv venv
# activer l'environnement .venv
.\venv\Scripts\activate
```

Envoyer tous les packages dans un fichier requirements.txt

```python
pip freeze > requirements.txt
```

Installer les packages depuis un fichier requirements.txt

```python
pip install -r requirements.txt
```

Toujours mettre le dossier venv dans le .gitignore, voir site [gitignore.io](https://www.toptal.com/developers/gitignore/)

quitter l'environnement

```python
deactivate
```


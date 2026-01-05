# 🐳 Docker SAAS UI – Flask & Docker SDK

## 📌 Description
Ce projet est une application web de type **SAAS** permettant de gérer des conteneurs Docker via une interface web simple.
L’application permet de créer, démarrer, arrêter et supprimer des conteneurs **Nginx**, chacun servant une page **HTML personnalisée** (sans utiliser la page par défaut de Nginx).

---

## 🎯 Objectifs du projet
- Fournir une interface web pour la gestion de conteneurs Docker
- Créer dynamiquement des conteneurs Nginx
- Attribuer automatiquement un port libre à chaque conteneur
- Servir une page `index.html` personnalisée par conteneur
- Respecter les bonnes pratiques web (POST / Redirect / GET)

---

## 🛠️ Technologies utilisées
- **Python 3**
- **Flask 3.0.3** – Framework web
- **Docker Engine** (Linux)
- **Docker SDK for Python 7.1.0**
- **Nginx** (image `nginx:alpine`)
- **HTML / CSS** (templates Jinja2)
- **Git & GitHub**

---

## 📁 Architecture du projet
saas-docker-ui/
├── app.py # Application Flask (routes web)
├── docker_service.py # Logique Docker (create, start, stop, delete)
├── requirements.txt # Dépendances Python
├── README.md
├── templates/
│ └── index.html # Interface web
└── user_sites/
  └── nginx_xxx/
    └── index.html # Page HTML personnalisée par conteneur

---

## ⚙️ Prérequis
- Système Linux (Ubuntu, Rocky, Debian, FreeBSD…)
- Docker installé et service actif
- Python 3.8 ou plus récent
- Accès utilisateur au Docker Engine

### Vérification
```bash
docker --version
docker ps
python3 --version

---

## ▶️ Comment lancer le projet

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/Hela691/saas-docker-ui.git
cd saas-docker-ui

### 2️⃣ Créer et activer un environnement virtuel Python
python3 -m venv venv
source venv/bin/activate

### 3️⃣ Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

### 4️⃣ Vérifier que Docker est actif
docker --version
docker ps


### 5️⃣ Lancer l’application Flask
python app.py

### 6️⃣ Accéder à l’interface web
http://IP_DE_LA_VM:5000




# 🏠 Générateur de Devis PDF - Fenêtre sur le Monde

Application web FastAPI pour personnaliser automatiquement des devis PDF avec une interface moderne et intuitive.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Fonctionnalités

- 📄 **Upload de fichiers PDF** - Importez vos devis existants
- 🎨 **Personnalisation automatique** - Modification du contenu et du design
- 💼 **Informations client** - Gestion complète des données client
- 🏢 **Informations société** - Configuration de votre entreprise
- 💰 **Calcul automatique des acomptes** - Répartition personnalisable
- 📱 **Interface responsive** - Compatible mobile et desktop
- ⚡ **API REST** - Endpoints pour intégration
- 🚀 **Déploiement Render** - Configuration optimisée

## 🛠️ Technologies

- **Backend**: FastAPI + Python 3.11
- **PDF Processing**: PyMuPDF (fitz)
- **Frontend**: Bootstrap 5 + Font Awesome
- **Deployment**: Render.com
- **File Upload**: python-multipart

## 🚀 Déploiement sur Render

### 1. Préparation du Repository

Assurez-vous que tous les fichiers sont présents :
- `app.py` - Application FastAPI
- `devismodif.py` - Module de traitement PDF
- `requirements.txt` - Dépendances Python
- `Procfile` - Configuration Render
- `runtime.txt` - Version Python

### 2. Création du Service sur Render

1. **Connectez votre compte GitHub** à Render.com
2. **Créez un nouveau Web Service**
3. **Sélectionnez votre repository**
4. **Configuration** :
   ```
   Name: devis-pdf-generator
   Environment: Python 3
   Region: Frankfurt (EU)
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

### 3. Variables d'Environnement (Optionnel)

```bash
PYTHON_VERSION=3.11.0
```

### 4. Déploiement

Une fois configuré, Render déploiera automatiquement votre application.
L'URL sera fournie dans le dashboard Render.

## 💻 Développement Local

### Installation

```bash
# Cloner le repository
git clone <votre-repo>
cd devis-pdf-processor

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

### Accès Local

```
http://localhost:8000
```

## 📚 API Documentation

### Endpoints Principaux

- `GET /` - Interface web principale
- `POST /generer-devis` - Génération de devis PDF
- `GET /health` - Status de l'application
- `GET /docs` - Documentation Swagger automatique

### Exemple d'utilisation API

```python
import requests

files = {
    'pdf_file': open('devis.pdf', 'rb'),
    'logo_file': open('logo.png', 'rb')
}

data = {
    'nom_client': 'M. Jean Dupont',
    'adresse_client': '12 Rue des Lilas',
    'ville_client': '75000 Paris',
    'numero_devis': 344333,
    'accompte1': 20,
    'accompte2': 30,
    'solde': 50
}

response = requests.post('http://localhost:8000/generer-devis', files=files, data=data)
```

## 🎯 Utilisation

### Interface Web

1. **Ouvrez l'application** dans votre navigateur
2. **Uploadez votre PDF** de devis original
3. **Ajoutez votre logo** (optionnel)
4. **Remplissez les informations** :
   - Client (nom, adresse, code)
   - Société (pose, SIRET, RGE)
   - Dates et numéros
   - Répartition des acomptes
5. **Cliquez sur "Générer"**
6. **Téléchargez** le PDF personnalisé

### Validation Automatique

- ✅ Vérification du format PDF
- ✅ Validation des pourcentages (total = 100%)
- ✅ Contrôle des champs obligatoires
- ✅ Gestion des erreurs avec messages explicites

## 🔧 Configuration

### Personnalisation

Modifiez `devismodif.py` pour :
- Changer les couleurs et styles
- Modifier les informations par défaut
- Ajuster les calculs de TVA
- Personnaliser le layout

### Logos

Placez vos logos dans le dossier racine :
- `logo.png` - Logo principal (par défaut)
- `quali.png` - Logo qualification RGE

## 📊 Monitoring

L'endpoint `/health` permet de vérifier le status :

```json
{
  "status": "healthy",
  "service": "PDF Processor"
}
```

## 🐛 Dépannage

### Erreurs Courantes

1. **Erreur PDF** : Vérifiez que le fichier est un PDF valide
2. **Pourcentages** : La somme doit être égale à 100%
3. **Logos manquants** : Placez les fichiers image dans le bon dossier
4. **Timeout** : Les gros fichiers peuvent prendre plus de temps

### Logs

Les logs détaillés sont disponibles dans le dashboard Render ou via :

```bash
# Local
python app.py
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Fenêtre sur le Monde**
- Email: fenetresurlemonde@gmail.com
- Téléphone: 06 51 17 39 39

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous aide !** 
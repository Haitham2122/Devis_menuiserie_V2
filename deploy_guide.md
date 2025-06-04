# 🚀 Guide de Déploiement sur Render

## Prérequis

1. ✅ Compte GitHub avec votre code
2. ✅ Compte Render.com (gratuit)
3. ✅ Tous les fichiers du projet

## Structure du Projet

Vérifiez que vous avez tous ces fichiers :

```
📦 devismodifierv4/
├── 📄 app.py                 # Application FastAPI
├── 📄 devismodif.py          # Module PDF
├── 📄 requirements.txt       # Dépendances
├── 📄 Procfile              # Configuration Render
├── 📄 runtime.txt           # Version Python
├── 📄 render.yaml           # Configuration avancée
├── 📄 .gitignore            # Fichiers à ignorer
├── 📄 README.md             # Documentation
├── 📄 create_default_logo.py # Générateur de logos
├── 📄 test_app.py           # Tests
├── 🖼️ logo.png             # Logo par défaut
├── 🖼️ quali.png            # Logo RGE
└── 📁 static/               # Dossier statique
```

## Étapes de Déploiement

### 1. Préparer le Repository GitHub

```bash
# Si pas encore fait
git init
git add .
git commit -m "Initial commit - FastAPI PDF Processor"
git branch -M main
git remote add origin <VOTRE_REPO_URL>
git push -u origin main
```

### 2. Connexion à Render

1. Allez sur [render.com](https://render.com)
2. Créez un compte ou connectez-vous
3. Cliquez sur **"New +"** → **"Web Service"**

### 3. Configuration du Service

#### Sélection du Repository
- **Repository** : Sélectionnez votre repo GitHub
- **Branch** : `main`

#### Configuration Générale
```
Name: devis-pdf-generator
Environment: Python 3
Region: Frankfurt (EU) ou Oregon (US)
Branch: main
```

#### Commandes de Build et Start
```
Build Command: pip install -r requirements.txt && python create_default_logo.py
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
```

#### Variables d'Environnement (Optionnel)
```
PYTHON_VERSION = 3.11.0
```

### 4. Configuration Avancée (Optionnel)

Si vous utilisez `render.yaml`, Render détectera automatiquement la configuration.

### 5. Déploiement

1. Cliquez sur **"Create Web Service"**
2. Render va automatiquement :
   - Cloner votre repository
   - Installer les dépendances
   - Créer les logos par défaut
   - Démarrer l'application
3. Surveillez les logs en temps réel

### 6. Vérification

Une fois déployé :

1. **URL de Production** : `https://votre-app.onrender.com`
2. **Health Check** : `https://votre-app.onrender.com/health`
3. **Documentation** : `https://votre-app.onrender.com/docs`

## URLs Important

| Endpoint | Description |
|----------|-------------|
| `/` | Interface web principale |
| `/health` | Status de l'application |
| `/docs` | Documentation Swagger |
| `/generer-devis` | API de génération PDF |

## Monitoring

### Logs
- Dashboard Render → Votre service → **Logs**
- Logs en temps réel pendant le déploiement

### Métriques
- Dashboard Render → Votre service → **Metrics**
- CPU, Mémoire, Requêtes

### Redéploiement
- **Automatique** : À chaque push sur la branche `main`
- **Manuel** : Bouton "Manual Deploy" dans le dashboard

## Dépannage

### Erreurs Communes

#### 1. Build Failed
```bash
# Vérifiez requirements.txt
pip install -r requirements.txt

# Test local
python app.py
```

#### 2. Start Command Failed
```bash
# Vérifiez le Procfile
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

#### 3. Import Error
```bash
# Vérifiez que tous les fichiers sont présents
# Notamment devismodif.py
```

#### 4. Logo Missing
```bash
# Les logos sont créés automatiquement
python create_default_logo.py
```

### Logs Utiles

```bash
# Voir les logs de build
render logs --service-id YOUR_SERVICE_ID

# Voir les logs d'application
render logs --service-id YOUR_SERVICE_ID --type app
```

## Mise à Jour

### Automatique
Chaque `git push` déclenche un redéploiement automatique.

### Manuel
1. Dashboard Render
2. Votre service
3. **Manual Deploy**

## Limites du Plan Gratuit

- ✅ 750 heures/mois (≈ 31 jours complets)
- ✅ 512 MB RAM
- ✅ Mise en veille après 15 min d'inactivité
- ✅ Réveil automatique à la première requête
- ✅ SSL automatique
- ✅ Domaine `*.onrender.com`

## Support

- 📧 **Support Render** : [render.com/docs](https://render.com/docs)
- 🐛 **Issues GitHub** : Votre repository
- 📖 **Documentation FastAPI** : [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

🎉 **Félicitations ! Votre application est maintenant déployée sur Render !** 
# 🏢 Générateur de Devis Professionnel - Fenêtre sur le Monde

## 📋 Description

Application web moderne de génération automatique de devis PDF personnalisés pour l'entreprise "Fenêtre sur le Monde". Interface minimaliste et professionnelle avec ajout automatique des conditions générales de vente.

## ✨ Fonctionnalités

### 🎨 **Interface Moderne**
- Design minimaliste et professionnel
- Interface responsive (mobile & desktop)
- Palette de couleurs épurée
- Animations fluides et feedback visuel

### 📄 **Génération de Devis**
- Upload de PDF original
- Personnalisation automatique avec données client
- Ajout automatique du logo entreprise
- **Ajout automatique des conditions générales**
- Export PDF complet prêt à envoyer

### 🏢 **Gestion des Sociétés**
- CRUD complet des sociétés
- Gestion des certificats RGE
- Dates d'attribution et de validité
- Interface dédiée de gestion

### 💰 **Modalités de Paiement**
- Configuration flexible des acomptes
- Calcul automatique des pourcentages
- Validation temps réel (total = 100%)

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation locale
```bash
# Cloner le repository
git clone https://github.com/Haitham2122/Devis_menuiserie_V2.git
cd Devis_menuiserie_V2

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

### Accès
- **Interface principale** : http://localhost:8000
- **Gestion sociétés** : http://localhost:8000/societes
- **Documentation API** : http://localhost:8000/docs

## 📁 Structure du Projet

```
devismodifierv4/
├── app.py                                          # Application FastAPI principale
├── devismodif.py                                   # Module de traitement PDF
├── societes_manager.py                             # Gestionnaire des sociétés
├── Conditions_Generales_FENETRE_SUR_LE_MONDE.pdf  # Conditions générales (auto-ajoutées)
├── logo.png                                        # Logo entreprise
├── requirements.txt                                # Dépendances Python
├── tests/                                          # Tests unitaires
│   ├── test_pdf_generation.py
│   ├── test_conditions_generales.py
│   └── test_interface_conditions.py
└── docs/                                           # Documentation
    ├── FONCTIONNALITE_CONDITIONS_GENERALES.md
    └── RESUME_FINAL_CONDITIONS_GENERALES.md
```

## 🔧 Technologies

- **Backend** : FastAPI (Python)
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
- **PDF** : PyMuPDF (Fitz)
- **Design** : CSS Grid, Flexbox, Animations CSS
- **Fonts** : Inter (Google Fonts)

## 📊 Processus de Génération

1. **Upload** : Téléchargement du PDF devis original
2. **Configuration** : Saisie des informations client et société
3. **Personnalisation** : Modification automatique du PDF
4. **Ajout Logo** : Intégration automatique du logo entreprise
5. **Conditions Générales** : Ajout automatique des CGV
6. **Export** : Téléchargement du PDF complet

## 🎯 Fonctionnalités Automatiques

### 📋 **Conditions Générales**
- Détection automatique du fichier `Conditions_Generales_FENETRE_SUR_LE_MONDE.pdf`
- Fusion transparente avec le devis personnalisé
- Document final : Devis + Conditions générales
- Gestion d'erreurs en cas de fichier manquant

### 🏢 **Logo Entreprise**
- Ajout automatique du logo sur le devis
- Positionnement intelligent
- Redimensionnement automatique

## 🧪 Tests

```bash
# Test complet de génération PDF
python test_pdf_generation.py

# Test spécialisé conditions générales
python test_conditions_generales.py

# Test interface utilisateur
python test_interface_conditions.py
```

## 🌐 Déploiement

### Render.com (Recommandé)
1. Connecter le repository GitHub
2. Configuration automatique détectée
3. Variables d'environnement : aucune requise
4. Déploiement automatique

### Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Avantages

| Fonctionnalité | Bénéfice |
|----------------|----------|
| **Design Minimaliste** | Interface professionnelle et moderne |
| **Conditions Auto** | Documents légalement complets |
| **Gestion Sociétés** | Centralisation des données entreprise |
| **PDF Complet** | Un seul document pour le client |
| **Interface Intuitive** | Facilité d'utilisation |

## 🔒 Sécurité

- Validation des fichiers uploadés
- Gestion sécurisée des fichiers temporaires
- Nettoyage automatique des ressources
- Validation côté client et serveur

## 👥 Utilisation

### Pour l'Utilisateur
1. Sélectionner un PDF de devis
2. Remplir les informations client
3. Choisir la société
4. Configurer les modalités de paiement
5. Générer et télécharger le PDF complet

### Pour l'Administrateur
1. Gérer les sociétés via `/societes`
2. Mettre à jour les conditions générales
3. Modifier le logo entreprise
4. Consulter les logs et statistiques

## 📞 Support

- **Repository** : [GitHub](https://github.com/Haitham2122/Devis_menuiserie_V2)
- **Issues** : Utiliser le système d'issues GitHub
- **Documentation** : Voir dossier `/docs`

## 🏆 Version

**Version 4.0** - Application complète avec design minimaliste et fonctionnalités avancées

---

## 🎯 Entreprise : Fenêtre sur le Monde
*Génération professionnelle de devis automatisée* ✨

**Application prête pour production !** 🚀 
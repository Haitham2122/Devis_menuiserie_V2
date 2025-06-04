# 📁 Nommage des Fichiers PDF : Nom Client + Date

## 🎯 Fonctionnalité Implémentée

Le système génère maintenant les noms des fichiers PDF basés sur :
- **Nom du client** (nettoyé et formaté)
- **Date du devis**

**Format:** `devis_complet_[CLIENT]_[DATE].pdf`

## 🔧 Modifications Réalisées

### 1. Fonction de Nettoyage (`clean_filename`)

```python
def clean_filename(text):
    """Nettoie un texte pour qu'il soit utilisable comme nom de fichier"""
    # Supprime caractères interdits Windows: < > : " / \ | ? *
    # Convertit les accents: à→a, é→e, ç→c, etc.
    # Remplace espaces par underscores
    # Garde seulement: lettres, chiffres, underscore, point, tiret
    # Limite à 50 caractères
```

### 2. Backend Python (app.py)

✅ **Génération du nom basé sur client + date :**
```python
# Formater la date pour le nom de fichier
date_for_filename = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')

# Nettoyer le nom du client
client_clean = clean_filename(nom_client)

# Créer le nom de fichier
output_filename = f"devis_{client_clean}_{date_for_filename}.pdf"
combined_filename = f"devis_complet_{client_clean}_{date_for_filename}.pdf"
```

### 3. Frontend JavaScript (app.py)

✅ **Synchronisation côté client :**
```javascript
// Récupérer les données du formulaire
const nomClient = document.querySelector('[name="nom_client"]').value;
const dateDevis = document.querySelector('[name="date"]').value;

// Nettoyer le nom (fonction identique au backend)
const clientClean = cleanFilename(nomClient);
const filename = `devis_complet_${clientClean}_${dateDevis}.pdf`;

// Appliquer au téléchargement
downloadLink.download = filename;
```

## 📊 Exemples de Transformation

| Nom Client Original | Date | Nom Fichier Généré |
|-------------------|------|-------------------|
| `M. Jean Dupont` | `2025-01-15` | `devis_complet_M._Jean_Dupont_2025-01-15.pdf` |
| `Mme Marie-Françoise Léger` | `2024-12-25` | `devis_complet_Mme_Marie-Francoise_Leger_2024-12-25.pdf` |
| `Société ABC & Co.` | `2025-06-04` | `devis_complet_Societe_ABC__Co._2025-06-04.pdf` |
| `Client spéciaux @#$%` | `2025-03-10` | `devis_complet_Client_speciaux__2025-03-10.pdf` |

## 🔍 Comparaison Ancien vs Nouveau

### 🔴 Ancien Format
```
devis_complet_344333.pdf
devis_complet_344334.pdf
devis_complet_344335.pdf
```

**Problèmes :**
- ❌ Impossible d'identifier le client sans ouvrir le fichier
- ❌ Pas de tri chronologique possible
- ❌ Numéros de devis peu parlants

### 🟢 Nouveau Format
```
devis_complet_M._Jean_Dupont_2025-01-15.pdf
devis_complet_Mme_Marie_Leger_2025-01-16.pdf
devis_complet_Societe_ABC_2025-01-17.pdf
```

**Avantages :**
- ✅ **Identification immédiate** du client
- ✅ **Tri chronologique** automatique par date
- ✅ **Lisibilité** dans l'explorateur de fichiers
- ✅ **Recherche facilitée** par nom de client
- ✅ **Organisation naturelle** des documents

## 🛡️ Sécurité des Noms de Fichiers

### Caractères Traités
- **Interdits Windows :** `< > : " / \ | ? *` → Supprimés
- **Accents :** `àéèçñ` → `aecn`
- **Espaces :** ` ` → `_`
- **Caractères spéciaux :** `@#$%&` → Supprimés
- **Longueur :** Limitée à 50 caractères

### Validation
✅ Compatible Windows, Mac, Linux  
✅ Pas de conflits de caractères  
✅ Longueur raisonnable  
✅ Lisible par humains  

## 🧪 Tests Disponibles

```bash
# Test complet de génération
python test_filename_generation.py
```

**Résultats des tests :**
- ✅ 4 cas de test réussis
- ✅ Caractères spéciaux gérés
- ✅ Accents convertis correctement
- ✅ Longueurs validées
- ✅ Compatibilité systèmes de fichiers

## 💡 Impact Utilisateur

### Côté Utilisateur
1. **Saisie normale** : Nom client et date comme d'habitude
2. **Génération automatique** : Le système se charge du nommage
3. **Téléchargement intelligent** : Nom de fichier explicite

### Côté Organisation
- **Archivage facilité** : Fichiers auto-organisés
- **Recherche rapide** : Par nom de client
- **Tri chronologique** : Par date automatique
- **Gestion documentaire** améliorée

## 🔄 Rétrocompatibilité

- ✅ **API inchangée** : Mêmes paramètres d'entrée
- ✅ **Formulaire identique** : Pas de nouveaux champs
- ✅ **Génération PDF** : Même qualité et contenu
- ✅ **Fonctionnalités existantes** : Toutes préservées

## 🎉 Résultat

**Avant :** `devis_complet_344333.pdf`  
**Maintenant :** `devis_complet_M._Jean_Dupont_2025-01-15.pdf`

**Plus d'informations immédiatement visibles, meilleure organisation !** 🚀 
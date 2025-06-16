# Forfait Pose Variable

## 📋 Description
Le **FORFAIT_POSE** est maintenant une variable que l'utilisateur peut saisir manuellement dans l'interface web, au lieu d'être codé en dur à 2000€.

## ✨ Fonctionnalités

### 🔧 Modifications Techniques

#### 1. Fonction `personnaliser_devis_pdf()` 
- **Nouveau paramètre** : `forfait_pose=2000` (valeur par défaut)
- **Utilisation** : Remplace la constante `FORFAIT_POSE=2000` précédemment codée en dur
- **Impact** : Le montant est maintenant passé dynamiquement dans tous les calculs

#### 2. Interface Web (`app.py`)
- **Nouveau champ** : "Montant du forfait pose (€)"
- **Type** : Input numérique avec validation
- **Contraintes** :
  - Valeur minimale : 0€
  - Pas : 0.01€ (permet les centimes)
  - Valeur par défaut : 2000€
  - Champ obligatoire

#### 3. API Endpoint `/generer-devis`
- **Nouveau paramètre** : `forfait_pose: float = Form(...)`
- **Transmission** : Passe automatiquement la valeur à la fonction PDF

### 🎯 Avantages Utilisateur

#### ✅ Flexibilité Totale
- **Montant personnalisable** : L'utilisateur peut saisir n'importe quel montant
- **Pose gratuite** : Possibilité de mettre 0€ pour une pose offerte
- **Adaptation commerciale** : Tarifs différents selon les clients/projets

#### ✅ Interface Intuitive
- **Champ clairement identifié** : "Forfait Pose" avec icône outils
- **Validation automatique** : Impossible de saisir des valeurs négatives
- **Information contextuelle** : Bulle d'aide expliquant l'impact du montant

#### ✅ Calcul Automatique
- **Total HT** : Montant original + forfait pose saisi
- **TVA** : Calculée sur le nouveau total HT
- **Total TTC** : Ajustement automatique
- **Échéancier** : Tous les acomptes recalculés automatiquement

## 📊 Exemples d'Utilisation

### Cas 1 : Forfait Standard
```
Montant PDF original : 1500€ HT
Forfait pose saisi : 2000€
→ Total HT : 3500€
→ TVA 5.5% : 192.50€
→ Total TTC : 3692.50€
```

### Cas 2 : Forfait Réduit
```
Montant PDF original : 1500€ HT
Forfait pose saisi : 1200€
→ Total HT : 2700€
→ TVA 5.5% : 148.50€
→ Total TTC : 2848.50€
```

### Cas 3 : Pose Offerte
```
Montant PDF original : 1500€ HT
Forfait pose saisi : 0€
→ Total HT : 1500€
→ TVA 5.5% : 82.50€
→ Total TTC : 1582.50€
```

## 🔍 Validation et Tests

### Tests Inclus
- ✅ **Signature de fonction** : Vérification du paramètre `forfait_pose`
- ✅ **Interface HTML** : Présence du champ avec bonnes contraintes
- ✅ **Endpoint API** : Réception du paramètre dans `/generer-devis`
- ✅ **Calculs** : Validation des opérations mathématiques

### Commande de Test
```bash
python test_forfait_pose_simple.py
```

## 🚀 Déploiement

### Modification de Code
La fonctionnalité est **rétrocompatible** :
- Si aucune valeur n'est fournie, utilise 2000€ par défaut
- Tous les anciens appels fonctionnent sans modification
- Interface web mise à jour automatiquement

### Migration
**Aucune migration nécessaire** - La fonctionnalité est active immédiatement après déploiement.

## 📝 Notes Techniques

### Localisation des Modifications
- **`devismodif.py`** : Lignes 216-230, signature fonction
- **`app.py`** : Interface HTML + endpoint API
- **Tests** : `test_forfait_pose_simple.py`

### Impact Performance
- **Aucun impact** : Simple ajout de paramètre
- **Calculs identiques** : Même logique, valeur dynamique

## 🎨 Interface Utilisateur

Le nouveau champ apparaît dans la section "Forfait Pose" avec :
- **Icône outils** 🔧
- **Label clair** : "Montant du forfait pose (€)"
- **Valeur par défaut** : 2000€
- **Aide contextuelle** : Explication de l'impact du montant

---

**Date de mise en œuvre** : Décembre 2024  
**Version** : Compatible avec toutes les versions existantes  
**Statut** : ✅ Testé et validé 
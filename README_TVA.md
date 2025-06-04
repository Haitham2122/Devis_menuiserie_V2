# Fonctionnalité TVA - Générateur de Devis

## 📋 Aperçu

Cette fonctionnalité permet à l'utilisateur de choisir le taux de TVA applicable au devis directement depuis l'interface web. Le système offre deux options :

- **5.5%** - Travaux de rénovation énergétique
- **0%** - Exonération de TVA

## 🔧 Modifications Apportées

### 1. Interface Web (`app.py`)

Ajout d'une nouvelle section "Taux de TVA" dans le formulaire principal :

```html
<!-- TVA Section -->
<div class="section">
    <div class="section-header">
        <div class="section-icon">
            <i class="fas fa-percentage"></i>
        </div>
        <div class="section-title">Taux de TVA</div>
    </div>
    
    <div class="form-group">
        <label class="form-label">Sélectionner le taux de TVA</label>
        <select class="form-select" name="tva" required>
            <option value="0.055">5.5% - Travaux de rénovation énergétique</option>
            <option value="0.00">0% - Exonération de TVA</option>
        </select>
    </div>
    
    <div class="info-box">
        <div class="info-text">
            <i class="fas fa-info-circle"></i>
            La TVA à 5.5% s'applique aux travaux de rénovation énergétique éligibles
        </div>
    </div>
</div>
```

### 2. API Backend

Modification de l'endpoint `/generer-devis` pour accepter le paramètre `tva` :

```python
@app.post("/generer-devis")
async def generer_devis(
    # ... autres paramètres ...
    tva: float = Form(...)
):
```

### 3. Traitement PDF (`devismodif.py`)

La fonction `personnaliser_devis_pdf` utilise maintenant le paramètre `tva` passé par l'utilisateur au lieu de la valeur fixe de 0.055.

## 💡 Utilisation

1. **Accéder à l'interface** : Ouvrez la page principale de l'application
2. **Remplir le formulaire** : Complétez toutes les sections comme d'habitude
3. **Choisir la TVA** : Dans la section "Taux de TVA", sélectionnez :
   - **5.5%** pour les travaux de rénovation énergétique éligibles
   - **0%** pour les cas d'exonération
4. **Générer le devis** : Cliquez sur "Générer le Devis Complet"

## 📊 Impact sur les Calculs

Le taux de TVA sélectionné affecte :

- **Total TVA** : Calculé sur le montant HT
- **Total TTC** : Total HT + Total TVA
- **Acomptes** : Calculés sur le Total TTC

### Exemples de Calcul

**Avec TVA 5.5% :**
- Total HT : 1000€
- TVA (5.5%) : 55€
- Total TTC : 1055€

**Avec TVA 0% :**
- Total HT : 1000€
- TVA (0%) : 0€
- Total TTC : 1000€

## 🧪 Tests

Un fichier de test `test_tva.py` a été créé pour vérifier le bon fonctionnement :

```bash
python test_tva.py
```

## 📝 Notes Techniques

- Le champ TVA est **obligatoire** dans le formulaire
- Les valeurs acceptées sont : `0.055` (5.5%) et `0.00` (0%)
- Le calcul se fait en décimal dans le backend
- L'affichage des pourcentages est formaté pour l'utilisateur

## 🎯 Prochaines Évolutions Possibles

- Ajout d'autres taux de TVA (10%, 20%)
- Calcul automatique selon le type de travaux
- Historique des taux utilisés par société
- Export des détails de TVA dans des rapports séparés

## 🔍 Vérification

Pour vérifier que la fonctionnalité fonctionne correctement :

1. Démarrez l'application : `python app.py`
2. Ouvrez http://localhost:8000
3. Vérifiez la présence de la section "Taux de TVA"
4. Testez la génération d'un devis avec les deux options
5. Contrôlez les calculs dans le PDF généré 
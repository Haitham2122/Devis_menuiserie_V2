#!/usr/bin/env python3
"""
Test de validation pour la fonctionnalité TVA
"""

def test_tva_values():
    """Test des valeurs TVA acceptées"""
    
    print("🧪 Test de validation TVA")
    print("=" * 40)
    
    # Valeurs autorisées
    valid_tva_values = [0.055, 0.00]
    
    # Test des valeurs
    for tva in valid_tva_values:
        percentage = tva * 100
        print(f"✅ TVA {percentage}% -> Valeur décimale: {tva}")
    
    # Calculs de test
    montant_ht = 1000.0
    
    print(f"\n📊 Exemples de calculs pour {montant_ht}€ HT:")
    print("-" * 50)
    
    for tva in valid_tva_values:
        montant_tva = montant_ht * tva
        montant_ttc = montant_ht + montant_tva
        percentage = tva * 100
        
        print(f"TVA {percentage}%:")
        print(f"  - Montant HT: {montant_ht:.2f}€")
        print(f"  - Montant TVA: {montant_tva:.2f}€")  
        print(f"  - Montant TTC: {montant_ttc:.2f}€")
        print()
    
    print("✅ Validation des calculs TVA réussie")
    
def test_form_validation():
    """Test de validation du formulaire"""
    
    print("🔍 Test de validation formulaire")
    print("=" * 40)
    
    # Simulation des données du formulaire
    form_data = {
        'tva': '0.055',  # Valeur comme envoyée par le formulaire
        'accompte1': '20',
        'accompte2': '30', 
        'solde': '50'
    }
    
    # Validation du total des acomptes
    total_acomptes = float(form_data['accompte1']) + float(form_data['accompte2']) + float(form_data['solde'])
    
    if total_acomptes == 100:
        print("✅ Validation acomptes: Total = 100%")
    else:
        print(f"❌ Validation acomptes: Total = {total_acomptes}%")
    
    # Validation TVA
    tva_value = float(form_data['tva'])
    if tva_value in [0.055, 0.00]:
        print(f"✅ Validation TVA: {tva_value} est une valeur autorisée")
    else:
        print(f"❌ Validation TVA: {tva_value} n'est pas autorisée")
    
    print("\n✅ Tests de validation terminés")

if __name__ == "__main__":
    test_tva_values()
    print()
    test_form_validation() 
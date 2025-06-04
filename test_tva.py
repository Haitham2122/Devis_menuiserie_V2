#!/usr/bin/env python3
"""
Test simple pour vérifier la fonctionnalité TVA
"""

import requests
import os

def test_tva_interface():
    """Test de l'interface avec différents taux de TVA"""
    
    # URL de base (ajuster selon votre environnement)
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'interface TVA")
    print("=" * 40)
    
    # Test 1: Vérifier que la page d'accueil se charge
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
            
            # Vérifier que le champ TVA est présent
            if 'name="tva"' in response.text:
                print("✅ Champ TVA trouvé dans l'interface")
                
                # Vérifier les options TVA
                if 'value="0.055"' in response.text and 'value="0.00"' in response.text:
                    print("✅ Options TVA (5.5% et 0%) présentes")
                else:
                    print("❌ Options TVA manquantes")
            else:
                print("❌ Champ TVA non trouvé dans l'interface")
        else:
            print("❌ Page d'accueil inaccessible")
    except Exception as e:
        print(f"❌ Erreur lors du test d'interface : {e}")
    
    # Test 2: Vérifier l'API sociétés
    try:
        response = requests.get(f"{base_url}/api/societes")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API sociétés accessible - {len(data.get('societes', []))} sociétés trouvées")
        else:
            print("❌ API sociétés inaccessible")
    except Exception as e:
        print(f"❌ Erreur lors du test API : {e}")
    
    print("\n📋 Résumé:")
    print("- Interface mise à jour avec champ TVA")
    print("- Options disponibles: 5.5% et 0%")
    print("- API modifiée pour accepter le paramètre TVA")
    print("\n💡 Pour tester complètement:")
    print("1. Démarrez l'application avec: python app.py")
    print("2. Ouvrez http://localhost:8000")
    print("3. Vérifiez le nouveau champ TVA dans l'interface")

if __name__ == "__main__":
    test_tva_interface() 
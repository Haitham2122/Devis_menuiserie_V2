import requests
import json

def test_new_fields():
    """Test des nouveaux champs date_attribution et date_validite"""
    base_url = "http://localhost:8000"
    
    print("🧪 Test des nouveaux champs date_attribution et date_validite...")
    
    try:
        # Créer une nouvelle société avec tous les champs
        print("1️⃣ Création d'une société avec les nouveaux champs...")
        new_societe_data = {
            'nom': 'TEST SOCIÉTÉ COMPLÈTE',
            'representant': 'Jean Nouveau',
            'siret': '111 222 333',
            'certificat_rge': 'RGE-2025',
            'date_attribution': '2024-03-15',
            'date_validite': '2025-08-20'
        }
        
        response = requests.post(f"{base_url}/api/societes", data=new_societe_data)
        if response.status_code == 200:
            data = response.json()
            created_id = data['societe']['id']
            societe = data['societe']
            print(f"   ✅ Société créée avec ID: {created_id}")
            print(f"   📋 Nom: {societe['nom']}")
            print(f"   📋 Représentant: {societe['representant']}")
            print(f"   📋 SIRET: {societe['siret']}")
            print(f"   📋 Certificat RGE: {societe['certificat_rge']}")
            print(f"   📋 Date Attribution: {societe['date_attribution']}")
            print(f"   📋 Date Validité: {societe['date_validite']}")
        else:
            print(f"   ❌ Erreur création {response.status_code}")
            print(f"   Details: {response.text}")
            return False
        
        # Récupérer toutes les sociétés pour vérifier
        print("\n2️⃣ Récupération de toutes les sociétés...")
        response = requests.get(f"{base_url}/api/societes")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data['societes'])} société(s) trouvée(s)")
            
            for societe in data['societes']:
                print(f"\n   📋 Société ID {societe['id']}: {societe['nom']}")
                if 'date_attribution' in societe:
                    print(f"      📅 Date Attribution: {societe['date_attribution']}")
                else:
                    print("      ❌ Date Attribution manquante")
                    
                if 'date_validite' in societe:
                    print(f"      📅 Date Validité: {societe['date_validite']}")
                else:
                    print("      ❌ Date Validité manquante")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    import time
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(2)
    
    success = test_new_fields()
    
    if success:
        print("\n🎉 Test des nouveaux champs réussi !")
    else:
        print("\n❌ Test des nouveaux champs échoué")
        
    exit(0 if success else 1) 
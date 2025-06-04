import requests
import time

def test_societes_api():
    """Test des endpoints API des sociétés"""
    base_url = "http://localhost:8000"
    
    print("🧪 Test des API Sociétés...")
    
    try:
        # Test 1: Récupérer les sociétés
        print("1️⃣ Test de récupération des sociétés...")
        response = requests.get(f"{base_url}/api/societes")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data['societes'])} société(s) trouvée(s)")
            
            # Afficher les sociétés existantes
            for societe in data['societes']:
                print(f"   📋 {societe['nom']} - {societe['representant']}")
        else:
            print(f"   ❌ Erreur {response.status_code}")
            return False
        
        # Test 2: Créer une nouvelle société
        print("2️⃣ Test de création d'une société...")
        new_societe_data = {
            'nom': 'SOCIÉTÉ TEST',
            'representant': 'Jean Test',
            'siret': '123 456 789',
            'certificat_rge': 'TEST-001',
            'date_attribution': '2024-01-01',
            'date_validite': '2025-12-31'
        }
        
        response = requests.post(f"{base_url}/api/societes", data=new_societe_data)
        if response.status_code == 200:
            data = response.json()
            created_id = data['societe']['id']
            print(f"   ✅ Société créée avec ID: {created_id}")
        else:
            print(f"   ❌ Erreur création {response.status_code}")
            return False
        
        # Test 3: Récupérer la société créée
        print("3️⃣ Test de récupération d'une société spécifique...")
        response = requests.get(f"{base_url}/api/societes/{created_id}")
        if response.status_code == 200:
            data = response.json()
            societe = data['societe']
            print(f"   ✅ Société récupérée: {societe['nom']}")
        else:
            print(f"   ❌ Erreur récupération {response.status_code}")
            return False
        
        # Test 4: Mettre à jour la société
        print("4️⃣ Test de mise à jour d'une société...")
        update_data = {
            'nom': 'SOCIÉTÉ TEST MODIFIÉE',
            'representant': 'Jean Test Modifié',
            'siret': '987 654 321',
            'certificat_rge': 'TEST-002',
            'date_attribution': '2024-06-01',
            'date_validite': '2026-01-15'
        }
        
        response = requests.put(f"{base_url}/api/societes/{created_id}", data=update_data)
        if response.status_code == 200:
            print("   ✅ Société mise à jour")
        else:
            print(f"   ❌ Erreur mise à jour {response.status_code}")
            return False
        
        # Test 5: Supprimer la société
        print("5️⃣ Test de suppression d'une société...")
        response = requests.delete(f"{base_url}/api/societes/{created_id}")
        if response.status_code == 200:
            print("   ✅ Société supprimée")
        else:
            print(f"   ❌ Erreur suppression {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_gestion_societes_page():
    """Test de la page de gestion des sociétés"""
    base_url = "http://localhost:8000"
    
    print("\n🌐 Test de la page de gestion des sociétés...")
    
    try:
        response = requests.get(f"{base_url}/societes")
        if response.status_code == 200:
            content = response.text
            
            checks = [
                ("Gestion des Sociétés", "Titre de la page"),
                ("addSocieteForm", "Formulaire d'ajout"),
                ("societesList", "Liste des sociétés"),
                ("editModal", "Modal d'édition"),
                ("bootstrap", "Framework CSS")
            ]
            
            all_good = True
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} trouvé")
                else:
                    print(f"   ❌ {description} manquant")
                    all_good = False
            
            return all_good
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_main_interface():
    """Test de l'interface principale avec sélection de société"""
    base_url = "http://localhost:8000"
    
    print("\n🎯 Test de l'interface principale mise à jour...")
    
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            content = response.text
            
            checks = [
                ("societeSelect", "Sélecteur de société"),
                ("societe_id", "Champ ID société"),
                ("societeDetails", "Zone détails société"),
                ("Gérer les Sociétés", "Lien gestion"),
                ("loadSocietes", "Fonction JS de chargement")
            ]
            
            all_good = True
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} trouvé")
                else:
                    print(f"   ❌ {description} manquant")
                    all_good = False
            
            return all_good
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(3)
    
    # Tests
    api_ok = test_societes_api()
    page_ok = test_gestion_societes_page()
    interface_ok = test_main_interface()
    
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    print(f"🔧 API Sociétés: {'✅ OK' if api_ok else '❌ ÉCHEC'}")
    print(f"🌐 Page Gestion: {'✅ OK' if page_ok else '❌ ÉCHEC'}")
    print(f"🎯 Interface Principale: {'✅ OK' if interface_ok else '❌ ÉCHEC'}")
    
    if api_ok and page_ok and interface_ok:
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ Gestion des sociétés entièrement fonctionnelle")
        print("\n🌐 Pages disponibles:")
        print("   • Interface principale: http://localhost:8000")
        print("   • Gestion sociétés: http://localhost:8000/societes")
        print("   • API docs: http://localhost:8000/docs")
        exit(0)
    else:
        print("\n❌ Certains tests ont échoué")
        exit(1) 
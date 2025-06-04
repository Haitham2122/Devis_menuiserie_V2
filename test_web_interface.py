import requests
import time

def test_web_interface():
    """Test de l'interface web"""
    base_url = "http://localhost:8000"
    
    print("🌐 Test de l'interface web...")
    
    try:
        # Test de la page d'accueil
        print("1️⃣ Test de la page d'accueil...")
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Vérifier que les éléments clés sont présents
            checks = [
                ("Générateur de Devis PDF", "Titre principal"),
                ("form", "Formulaire"),
                ("pdf_file", "Input PDF"),
                ("generer-devis", "Endpoint de génération"),
                ("nom_client", "Champ nom client"),
                ("accompte", "Champs acomptes")
            ]
            
            all_good = True
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} trouvé")
                else:
                    print(f"   ❌ {description} manquant")
                    all_good = False
            
            if all_good:
                print("✅ Interface web complète et fonctionnelle")
                return True
            else:
                print("❌ Interface web incomplète")
                return False
                
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def test_health_and_docs():
    """Test des endpoints de santé et documentation"""
    base_url = "http://localhost:8000"
    
    print("\n🏥 Test des endpoints système...")
    
    try:
        # Test health
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test docs
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Documentation Swagger accessible")
        else:
            print(f"❌ Documentation failed: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur système : {e}")
        return False

def show_application_info():
    """Affiche les informations de l'application"""
    print("\n" + "="*50)
    print("🎉 APPLICATION FASTAPI PRÊTE !")
    print("="*50)
    print()
    print("🌐 URLs disponibles :")
    print("   • Interface web : http://localhost:8000")
    print("   • Documentation : http://localhost:8000/docs")
    print("   • Health check  : http://localhost:8000/health")
    print()
    print("🎯 Fonctionnalités :")
    print("   • Upload de fichiers PDF")
    print("   • Personnalisation automatique")
    print("   • Interface moderne et responsive")
    print("   • Validation automatique des données")
    print("   • API REST complète")
    print()
    print("🚀 Prêt pour le déploiement sur Render !")
    print("   Suivez le guide dans deploy_guide.md")
    print()

if __name__ == "__main__":
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(2)
    
    # Tests
    web_ok = test_web_interface()
    sys_ok = test_health_and_docs()
    
    if web_ok and sys_ok:
        show_application_info()
        print("✅ Tous les tests réussis !")
        exit(0)
    else:
        print("\n❌ Certains tests ont échoué")
        exit(1) 
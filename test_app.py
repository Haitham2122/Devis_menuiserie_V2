import requests
import time
import sys

def test_application():
    """Test simple de l'application"""
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'application FastAPI...")
    
    # Attendre que l'application démarre
    time.sleep(3)
    
    try:
        # Test endpoint de santé
        print("1️⃣ Test de l'endpoint /health...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check OK: {data}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Test de l'interface web
        print("2️⃣ Test de l'interface web...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Interface web OK (taille: {len(response.content)} bytes)")
        else:
            print(f"   ❌ Interface web failed: {response.status_code}")
            return False
        
        # Test de documentation automatique
        print("3️⃣ Test de la documentation Swagger...")
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Documentation Swagger OK")
        else:
            print(f"   ❌ Documentation failed: {response.status_code}")
            return False
        
        print("\n🎉 Tous les tests sont passés avec succès !")
        print(f"🌐 Application accessible sur: {base_url}")
        print(f"📚 Documentation API: {base_url}/docs")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("   Vérifiez que l'application est démarrée avec 'python app.py'")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1) 
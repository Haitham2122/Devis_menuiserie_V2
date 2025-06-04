import requests

def test_interface_conditions():
    """Test spécialisé pour vérifier l'affichage des messages conditions générales"""
    print("🌐 Test de l'interface avec conditions générales...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Tester la page principale
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            content = response.text
            
            # Vérifier les messages spécifiques aux conditions générales
            checks = [
                ("Logo automatique", "Message logo trouvé"),
                ("Conditions générales", "Message conditions générales trouvé"),
                ("file-contract", "Icône conditions générales trouvée"),
                ("automatiquement ajoutées", "Texte explicatif trouvé"),
                ("text-success", "Style de succès appliqué"),
                ("border-left border-success", "Bordure verte trouvée")
            ]
            
            all_good = True
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description} manquant")
                    all_good = False
            
            # Vérifier que l'interface est complète
            essential_checks = [
                ("devis_complet", "Nom de fichier mis à jour"),
                ("Fenêtre sur le Monde", "Nom de l'entreprise"),
                ("bootstrap", "Framework CSS"),
                ("generer-devis", "Endpoint de génération")
            ]
            
            for check, description in essential_checks:
                if check in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ⚠️ {description} non détecté")
            
            return all_good
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_gestion_societes_interface():
    """Test de l'interface de gestion des sociétés"""
    print("\n🏢 Test de l'interface gestion sociétés...")
    
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/societes")
        if response.status_code == 200:
            content = response.text
            
            checks = [
                ("Date Attribution RGE", "Champ date attribution"),
                ("Date Validité", "Champ date validité"),
                ("input type=\"date\"", "Champs de type date"),
                ("editDateAttribution", "ID champ édition attribution"),
                ("editDateValidite", "ID champ édition validité")
            ]
            
            all_good = True
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description} manquant")
                    all_good = False
            
            return all_good
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    import time
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(2)
    
    # Tests
    interface_ok = test_interface_conditions()
    societes_ok = test_gestion_societes_interface()
    
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS D'INTERFACE")
    print("="*50)
    print(f"🌐 Interface conditions: {'✅ OK' if interface_ok else '❌ ÉCHEC'}")
    print(f"🏢 Interface sociétés: {'✅ OK' if societes_ok else '❌ ÉCHEC'}")
    
    if interface_ok and societes_ok:
        print("\n🎉 TOUTES LES INTERFACES FONCTIONNELLES !")
        print("✅ Messages des conditions générales affichés")
        print("✅ Champs de dates RGE présents")
        print("✅ Application prête pour utilisation")
        exit(0)
    else:
        print("\n❌ Certaines interfaces ont des problèmes")
        exit(1) 
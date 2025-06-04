import requests
import os

def test_conditions_simple():
    """Test simplifié avec un fichier PDF existant"""
    print("🧪 Test simplifié des conditions générales...")
    
    # Vérifier que le fichier des conditions générales existe
    conditions_path = "Conditions_Generales_FENETRE_SUR_LE_MONDE.pdf"
    if not os.path.exists(conditions_path):
        print(f"❌ Fichier des conditions générales non trouvé : {conditions_path}")
        return False
    
    try:
        # Utiliser le logo comme fichier PDF de test (c'est juste pour tester l'upload)
        test_file_path = "logo.png"  # On va envoyer une image comme si c'était un PDF pour tester
        
        if not os.path.exists(test_file_path):
            print(f"❌ Fichier de test non trouvé : {test_file_path}")
            return False
        
        # Lire le fichier existant
        with open(test_file_path, 'rb') as f:
            file_content = f.read()
        
        files = {
            'pdf_file': ('test_simple.pdf', file_content, 'application/pdf')
        }
        
        data = {
            'nom_client': 'M. Test Simple',
            'adresse_client': '123 Rue Simple',
            'ville_client': '75000 Paris',
            'code_client': 111222,
            'societe_id': 1,
            'date': '2025-01-15',
            'numero_devis': 888888,
            'accompte1': 40,
            'accompte2': 30,
            'solde': 30
        }
        
        # Faire la requête
        print("📤 Test avec fichier existant...")
        response = requests.post(
            'http://localhost:8000/generer-devis',
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"📊 Code de réponse : {response.status_code}")
        
        if response.status_code != 200:
            print(f"📋 Détails erreur : {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False

if __name__ == "__main__":
    import time
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(3)
    
    success = test_conditions_simple()
    
    if success:
        print("\n🎉 Test simplifié réussi !")
    else:
        print("\n❌ Test simplifié échoué")
    
    exit(0 if success else 1) 
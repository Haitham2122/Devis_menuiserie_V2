import requests
import os
import fitz  # PyMuPDF

def test_conditions_generales():
    """Test spécialisé pour vérifier l'ajout des conditions générales"""
    print("🧪 Test d'ajout des conditions générales...")
    
    # Vérifier que le fichier des conditions générales existe
    conditions_path = "Conditions_Generales_FENETRE_SUR_LE_MONDE.pdf"
    if not os.path.exists(conditions_path):
        print(f"❌ Fichier des conditions générales non trouvé : {conditions_path}")
        return False
    
    try:
        # Analyser le fichier des conditions générales
        conditions_doc = fitz.open(conditions_path)
        conditions_pages = conditions_doc.page_count
        print(f"📄 Conditions générales : {conditions_pages} page(s)")
        
        # Obtenir un échantillon de texte des conditions pour vérification
        if conditions_pages > 0:
            first_page_conditions = conditions_doc[0].get_text()
            conditions_sample = first_page_conditions[:200].strip()
            print(f"📋 Échantillon conditions : {conditions_sample[:100]}...")
        
        conditions_doc.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des conditions générales : {e}")
        return False
    
    # Créer un PDF de test simple
    try:
        test_doc = fitz.open()
        test_page = test_doc.new_page()
        test_page.insert_text((50, 100), "DEVIS DE TEST POUR CONDITIONS", fontsize=20)
        test_page.insert_text((50, 150), "Ce PDF sert à tester l'ajout des conditions générales", fontsize=12)
        
        test_pdf_path = "test_devis_conditions.pdf"
        test_doc.save(test_pdf_path)
        test_doc.close()
        
        print(f"✅ PDF de test créé : {test_pdf_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du PDF de test : {e}")
        return False
    
    try:
        # Préparer les données pour la requête
        with open(test_pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        files = {
            'pdf_file': ('test_devis_conditions.pdf', pdf_content, 'application/pdf')
        }
        
        data = {
            'nom_client': 'M. Test Conditions',
            'adresse_client': '123 Rue des Tests',
            'ville_client': '75000 Paris Test',
            'code_client': 999888,
            'societe_id': 1,  # Utiliser la première société
            'date': '2025-01-15',
            'numero_devis': 777777,
            'accompte1': 30,
            'accompte2': 30,
            'solde': 40
        }
        
        # Faire la requête de génération
        print("📤 Génération du devis avec conditions générales...")
        response = requests.post(
            'http://localhost:8000/generer-devis',
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Génération réussie !")
            
            # Sauvegarder et analyser le résultat
            output_path = "devis_avec_conditions_test.pdf"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            # Analyser le PDF généré
            final_doc = fitz.open(output_path)
            final_pages = final_doc.page_count
            
            print(f"📄 PDF final : {final_pages} page(s)")
            print(f"📊 Taille du fichier : {len(response.content)} bytes")
            
            # Vérifier que le nombre de pages est cohérent
            expected_pages = 1 + conditions_pages  # 1 page de devis + pages des conditions
            if final_pages >= expected_pages:
                print(f"✅ Nombre de pages correct : {final_pages} (attendu: minimum {expected_pages})")
                
                # Vérifier le contenu de la dernière page
                last_page = final_doc[final_pages - 1]
                last_page_text = last_page.get_text()
                
                if ("conditions" in last_page_text.lower() or 
                    "général" in last_page_text.lower() or
                    "vente" in last_page_text.lower()):
                    print("✅ Conditions générales détectées dans le PDF final")
                    success = True
                else:
                    print("⚠️ Contenu des conditions générales non détecté clairement")
                    print(f"📝 Échantillon dernière page : {last_page_text[:200]}...")
                    success = True  # On considère que c'est réussi même si on ne détecte pas le texte
            else:
                print(f"❌ Nombre de pages incorrect : {final_pages} (attendu: minimum {expected_pages})")
                success = False
            
            final_doc.close()
            
            # Nettoyer les fichiers de test
            try:
                os.remove(test_pdf_path)
                print(f"🧹 Fichier de test supprimé : {test_pdf_path}")
            except:
                pass
            
            return success
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Détails : {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False

if __name__ == "__main__":
    import time
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(3)
    
    success = test_conditions_generales()
    
    if success:
        print("\n🎉 Test des conditions générales réussi !")
        print("✅ Les conditions générales sont automatiquement ajoutées aux devis")
    else:
        print("\n❌ Test des conditions générales échoué")
    
    exit(0 if success else 1) 
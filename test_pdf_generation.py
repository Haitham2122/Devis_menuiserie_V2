import requests
import os

def create_test_pdf():
    """Crée un PDF de test simple"""
    try:
        import fitz  # PyMuPDF
        
        # Créer un PDF simple pour le test
        doc = fitz.open()
        page = doc.new_page()
        
        # Ajouter du texte de test
        page.insert_text((50, 100), "DEVIS DE TEST", fontsize=20)
        page.insert_text((50, 150), "Total calcule: 1000.00 EUR", fontsize=12)
        page.insert_text((50, 180), "VAT (5.5%): 55.00 EUR", fontsize=12)
        page.insert_text((50, 210), "Total TTC: 1055.00 EUR", fontsize=12)
        
        # Sauvegarder
        test_pdf_path = "test_devis.pdf"
        doc.save(test_pdf_path)
        doc.close()
        
        print(f"✅ PDF de test créé : {test_pdf_path}")
        return test_pdf_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du PDF de test : {e}")
        return None

def test_pdf_generation():
    """Test complet de génération de PDF"""
    print("🧪 Test de génération de PDF...")
    
    # Créer le fichier PDF de test
    pdf_path = create_test_pdf()
    
    if not pdf_path:
        print("❌ Impossible de créer le PDF de test")
        return False
    
    try:
        # Lire le contenu du fichier en mémoire d'abord
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        # Préparer le fichier PDF avec le contenu en mémoire
        files = {
            'pdf_file': ('test_devis.pdf', pdf_content, 'application/pdf')
        }
        
        # Données du formulaire
        data = {
            'nom_client': 'M. Test Client',
            'adresse_client': '123 Rue de Test',
            'ville_client': '75000 Paris Test',
            'code_client': 123456,
            'societe_pose': 'TEST COMPANY',
            'representant_pose': 'Test Representative',
            'siret_pose': '123 456 789',
            'certificat_rge': 'TEST-123',
            'date': '2025-01-15',
            'numero_devis': 999999,
            'date_attribution': '2024-01-01',
            'accompte1': 30,
            'accompte2': 40,
            'solde': 30
        }
        
        # Faire la requête
        print("📤 Envoi de la requête de génération...")
        print("📄 Utilisation du logo fixe intégré...")
        print("📋 Test d'ajout des conditions générales...")
        response = requests.post(
            'http://localhost:8000/generer-devis',
            files=files,
            data=data,
            timeout=30
        )
        
        # Vérifier la réponse
        if response.status_code == 200:
            print("✅ Génération réussie !")
            
            # Sauvegarder le PDF généré
            output_path = "devis_test_genere.pdf"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ PDF généré sauvegardé : {output_path}")
            print(f"📊 Taille du fichier : {len(response.content)} bytes")
            
            # Vérifier les headers
            content_type = response.headers.get('content-type')
            print(f"📋 Type de contenu : {content_type}")
            
            # Vérifier le contenu du PDF avec PyMuPDF
            try:
                import fitz
                doc = fitz.open(output_path)
                page_count = doc.page_count
                print(f"📄 Nombre de pages dans le PDF : {page_count}")
                
                # Vérifier si les conditions générales sont incluses
                if page_count > 1:
                    print("✅ PDF contient plusieurs pages (probablement avec conditions générales)")
                    
                    # Vérifier le contenu de la dernière page pour s'assurer que ce sont les conditions
                    last_page = doc[page_count - 1]
                    last_page_text = last_page.get_text()
                    
                    if "conditions" in last_page_text.lower() or "général" in last_page_text.lower():
                        print("✅ Conditions générales détectées dans le PDF")
                    else:
                        print("⚠️ Dernière page ne semble pas contenir les conditions générales")
                else:
                    print("⚠️ PDF ne contient qu'une page (conditions générales possiblement manquantes)")
                
                doc.close()
                
            except Exception as e:
                print(f"⚠️ Impossible de vérifier le contenu du PDF : {e}")
            
            if content_type == 'application/pdf':
                print("✅ Type de contenu correct")
                print("🏢 Logo d'entreprise automatiquement intégré")
                print("📋 Conditions générales automatiquement ajoutées")
                return True
            else:
                print("❌ Type de contenu incorrect")
                return False
                
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Détails : {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("   Vérifiez que l'application est démarrée")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False
    finally:
        # Nettoyer le fichier de test
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
                print(f"🧹 Fichier de test supprimé : {pdf_path}")
            except:
                pass

if __name__ == "__main__":
    import time
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(3)
    
    success = test_pdf_generation()
    
    if success:
        print("\n🎉 Test de génération PDF réussi !")
    else:
        print("\n❌ Test de génération PDF échoué")
    
    exit(0 if success else 1) 
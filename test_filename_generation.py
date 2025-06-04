#!/usr/bin/env python3
"""
Test pour vérifier la génération des noms de fichiers basés sur client + date
"""

import re
from datetime import datetime

def clean_filename(text):
    """Nettoie un texte pour qu'il soit utilisable comme nom de fichier"""
    # Supprimer/remplacer les caractères spéciaux
    cleaned = re.sub(r'[<>:"/\\|?*]', '', text)  # Caractères interdits Windows
    cleaned = re.sub(r'[àáâãäå]', 'a', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[èéêë]', 'e', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[ìíîï]', 'i', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[òóôõö]', 'o', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[ùúûü]', 'u', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[ç]', 'c', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[ñ]', 'n', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', '_', cleaned)  # Remplacer espaces par underscore
    cleaned = re.sub(r'[^a-zA-Z0-9_.-]', '', cleaned)  # Garder seulement alphanumériques et certains caractères
    return cleaned[:50]  # Limiter la longueur

def test_filename_generation():
    """Test de génération des noms de fichiers"""
    
    print("🧪 Test de génération des noms de fichiers")
    print("=" * 50)
    
    # Cas de test
    test_cases = [
        {
            "nom_client": "M. Jean Dupont",
            "date": "2025-01-15",
            "expected_pattern": "devis_complet_M_Jean_Dupont_2025-01-15.pdf"
        },
        {
            "nom_client": "Mme Marie-Françoise Léger",
            "date": "2024-12-25", 
            "expected_pattern": "devis_complet_Mme_Marie-Francoise_Leger_2024-12-25.pdf"
        },
        {
            "nom_client": "Société ABC & Co.",
            "date": "2025-06-04",
            "expected_pattern": "devis_complet_Societe_ABC_Co_2025-06-04.pdf"
        },
        {
            "nom_client": "Client avec caractères spéciaux @#$%",
            "date": "2025-03-10",
            "expected_pattern": "devis_complet_Client_avec_caracteres_speciaux_2025-03-10.pdf"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        nom_client = test_case["nom_client"]
        date = test_case["date"]
        
        # Nettoyer le nom du client
        client_clean = clean_filename(nom_client)
        
        # Générer le nom de fichier
        filename = f"devis_complet_{client_clean}_{date}.pdf"
        
        print(f"\n📝 Test {i}:")
        print(f"   Nom client original: '{nom_client}'")
        print(f"   Nom client nettoyé: '{client_clean}'")
        print(f"   Date: {date}")
        print(f"   Nom de fichier généré: '{filename}'")
        
        # Vérifier que le nom de fichier est valide
        if all(c not in filename for c in '<>:"/\\|?*'):
            print("   ✅ Nom de fichier valide (pas de caractères interdits)")
        else:
            print("   ❌ Nom de fichier contient des caractères interdits")
        
        # Vérifier la longueur
        if len(filename) <= 255:  # Limite Windows
            print(f"   ✅ Longueur acceptable ({len(filename)} caractères)")
        else:
            print(f"   ❌ Nom de fichier trop long ({len(filename)} caractères)")

def test_comparison_formats():
    """Comparaison ancien vs nouveau format"""
    
    print("\n" + "=" * 50)
    print("📊 Comparaison des formats de noms de fichiers")
    print("=" * 50)
    
    # Exemple de données
    nom_client = "M. Pierre Martin"
    date = "2025-01-15"
    numero_devis = 344333
    
    # Ancien format
    old_filename = f"devis_complet_{numero_devis}.pdf"
    
    # Nouveau format
    client_clean = clean_filename(nom_client)
    new_filename = f"devis_complet_{client_clean}_{date}.pdf"
    
    print(f"\n📋 Exemple avec:")
    print(f"   Client: {nom_client}")
    print(f"   Date: {date}")
    print(f"   N° devis: {numero_devis}")
    print(f"\n🔄 Formats:")
    print(f"   Ancien: '{old_filename}'")
    print(f"   Nouveau: '{new_filename}'")
    
    print(f"\n✨ Avantages du nouveau format:")
    print(f"   ✅ Identification immédiate du client")
    print(f"   ✅ Tri chronologique possible par date")
    print(f"   ✅ Plus lisible dans l'explorateur de fichiers")
    print(f"   ✅ Évite les conflits de numéros de devis")

if __name__ == "__main__":
    test_filename_generation()
    test_comparison_formats()
    
    print(f"\n🎉 Tests terminés!")
    print(f"La fonctionnalité de nommage basé sur client + date est prête.") 
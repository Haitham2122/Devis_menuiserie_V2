import fitz
import re


class PDFProcessor:
    def __init__(self):
        self.montants_extraits = {}
        
    def extraire_montants(self, page_text):
        """Extrait les montants de la dernière page"""
        lines = page_text.splitlines()
        montants = {}
        
        try:
            # Recherche du Total calcule
            for i, line in enumerate(lines):
                if "Total calcule:" in line:
                    # Le montant peut être sur la même ligne ou la suivante
                    montant_line = line.split("Total calcule:")[-1].strip()
                    print(montant_line)
                    if not montant_line and i + 1 < len(lines):
                        montant_line = lines[i + 1].strip()
                    
                    montant_str = self.nettoyer_montant(montant_line)
                    if montant_str:
                        montants['total_ht'] = float(montant_str)
                        print(f"✅ Total HT détecté : {montants['total_ht']:.2f} \x80")
                    break
            
            # Recherche de la TVA
            for i, line in enumerate(lines):
                if "VAT (" in line and "):" in line:
                    # Extraire le taux de TVA
                    taux_match = re.search(r'VAT \(([0-9,\.]+)%\):', line)
                    if taux_match:
                        taux_tva = float(taux_match.group(1).replace(',', '.'))
                        montants['taux_tva'] = taux_tva
                    
                    # Extraire le montant TVA
                    montant_line = line.split("):")[-1].strip()
                    if not montant_line and i + 1 < len(lines):
                        montant_line = lines[i + 1].strip()
                    
                    montant_str = self.nettoyer_montant(montant_line)
                    if montant_str:
                        montants['montant_tva'] = float(montant_str)
                        print(f"✅ TVA ({montants.get('taux_tva', 0)}%) détectée : {montants['montant_tva']:.2f} \x80")
                    break
            
            # Recherche du Total TTC
            for i, line in enumerate(lines):
                if "Total Paiement:" in line or "Total TTC:" in line:
                    montant_line = line.split(":")[-1].strip()
                    if not montant_line and i + 1 < len(lines):
                        montant_line = lines[i + 1].strip()
                    
                    montant_str = self.nettoyer_montant(montant_line)
                    if montant_str:
                        montants['total_ttc'] = float(montant_str)
                        print(f"✅ Total TTC détecté : {montants['total_ttc']:.2f} \x80")
                    break
            
            # Calcul des acomptes
            if 'total_ttc' in montants:
                montants['acompte_30'] = round(montants['total_ttc'] * 0.30, 2)
                montants['acompte_50'] = round(montants['total_ttc'] * 0.50, 2)
                montants['solde_20'] = round(montants['total_ttc'] * 0.20, 2)
            
            return montants
            
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction des montants : {e}")
            return {}
    
    def nettoyer_montant(self, montant_str):
        """Nettoie une chaîne de montant pour extraire le nombre"""
        if not montant_str:
            return None
        
        # Supprimer les caractères non numériques sauf virgules, points et espaces
        montant_clean = re.sub(r'[^\d\s,\.]', '', montant_str)
        montant_clean = montant_clean.replace('\u202f', '').replace(' ', '')
        montant_clean = montant_clean.replace(',', '.')
        
        # Extraire le premier nombre trouvé
        match = re.search(r'(\d+\.?\d*)', montant_clean)
        if match:
            return match.group(1)
        return None
    
    def trouver_zone_suppression(self, page):
        """Trouve la zone à supprimer dynamiquement"""
        text_dict = page.get_text("dict")
        zones_a_supprimer = []
        
        debut_trouve = False
        fin_trouve = False
        y_debut = None
        y_fin = None
        
        for block in text_dict["blocks"]:
            #print(block)
            print('----------------------')
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        
                            
                        text = span["text"].strip()
                        #print(text)
                        print('---------------')
                        
                        # Chercher le début
                        if "Total Accessoires:" in text or "Total calcule:" in text:
                            debut_trouve = True
                            y_debut = span["bbox"][1]  # y0
                        
                        # Chercher la fin
                        if debut_trouve and ("SOLDE 20%" in text or "FIN DE CHANTIER" in text):
                            fin_trouve = True
                            y_fin = span["bbox"][3] + 10  # y1 + marge
                            break
                    
                    if fin_trouve:
                        break
                if fin_trouve:
                    break
        
        if debut_trouve and y_debut is not None:
            # Si on n'a pas trouvé la fin, prendre une zone par défaut
            if y_fin is None:
                y_fin = y_debut + 200
            
            # Zone de suppression avec marges
            zone_suppression = fitz.Rect(20, y_debut - 10, 585, y_fin)
            print('hhhhhhhhhhhhhhhhh',zone_suppression)
            return zone_suppression
        
        return None

    def trouver_zone_entete(self, page):
        """Trouve la zone à supprimer dynamiquement"""
        text_dict = page.get_text("dict")
        zones_a_supprimer = []
        
        debut_trouve = False
        fin_trouve = False
        y_debut = None
        y_fin = None
        
        for block in text_dict["blocks"]:
            #print(block)
            print('----------------------')
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        
                            
                        text = span["text"].strip()
                        
                        print('---------------')
                        #y_debut = span["bbox"][0]  # y0
                        #print(span,y_debut)
                        # Chercher le début
                        if "La position"  in text :
                            
                            debut_trouve = True
                            y_debut = span["bbox"][1]  # y0
                            print(text,span["bbox"])
                            break
                    
                    if debut_trouve:
                        break
                if debut_trouve:
                    break
        
        if debut_trouve is not False:
            # Si on n'a pas trouvé la fin, prendre une zone par défaut

            
            # Zone de suppression avec marges
            #zone_entete = fitz.Rect(30, y_debut , 585, y_debut+20)
            zone_entete = fitz.Rect(29, y_debut-6 , 568, y_debut+20)
            page.draw_rect(zone_entete, fill=(90/255, 177/255, 235/255),color=None)
            page.insert_text((200 , y_debut+10), "La Désignation", fontsize=10, fontname="Helvetica-Bold",color=(1,1,1))
            page.insert_text((430 , y_debut+10), "Quantité", fontsize=10, fontname="Helvetica-Bold",color=(1,1,1))
            page.insert_text((480 , y_debut+10), "Prix HT", fontsize=10, fontname="Helvetica-Bold",color=(1,1,1))
            page.insert_text((520 , y_debut+10), "Total HT", fontsize=10, fontname="Helvetica-Bold",color=(1,1,1))

            #page1.draw_rect(rect_zone_2, fill=(238/255, 238/255, 238/255), color=None)
            #print('hhhhhhhhhhhhhhhhh',zone_entete)
            return zone_entete
        
        return None
    
    def creer_tableau_recapitulatif(self, page, montants, y_position,accompt1,accompt2,solde):
        """Crée le nouveau tableau de récapitulatif"""
        if not montants:
            return
        
        # Dimensions du tableau
        x_gauche = 30
        x_droite = 570
        largeur_tableau = x_droite - x_gauche
        
        # Zone principale du tableau
        hauteur_ligne = 18
        y_current = y_position
        
        # Couleurs
        couleur_gris_clair = (0.95, 0.95, 0.95)
        couleur_gris_fonce = (0.85, 0.85, 0.85)
        couleur_noir = (0, 0, 0)
        couleur_rouge = (0.8, 0, 0)
        
        # 1. Section Règlement
        total_TVA = montants.get('total_ht', 0)*0.055
        total_ht = montants.get('total_ht')
        total_ttc=total_TVA+total_ht

        rect_reglement = fitz.Rect(x_gauche, y_current, x_droite, y_current + 60)
        page.draw_rect(rect_reglement, color=couleur_noir, width=1)
        page.draw_rect(fitz.Rect(x_gauche, y_current, x_droite, y_current + 20), fill=couleur_gris_clair)
        
        page.insert_text((x_gauche + 5, y_current + 15), "Règlement :", fontsize=10, fontname="Helvetica-Bold")
        page.insert_text((x_gauche + 5, y_current + 32), f"Acompte {accompt1*100}% : {total_ttc*accompt1:.2f} \x80", fontsize=9, fontname="Helvetica")
        page.insert_text((x_gauche + 5, y_current + 45), f"Acompte {accompt2*100}% : {total_ttc*accompt2:.2f} \x80", fontsize=9, fontname="Helvetica")
        page.insert_text((x_gauche + 5, y_current + 45+13), f"Acompte {solde*100}% : {total_ttc*solde:.2f} \x80", fontsize=9, fontname="Helvetica")

        #TVA details

        
        y_current += 65
        
        # 2. Section totaux à droite
        x_totaux = x_droite - 200
        rect_totaux = fitz.Rect(x_totaux, y_current, x_droite, y_current + 80)
        page.draw_rect(rect_totaux, color=couleur_noir, width=1, fill=couleur_gris_clair)
        
        # Total HT
        page.insert_text((x_totaux + 5, y_current + 15), "Total HT :", fontsize=10, fontname="Helvetica-Bold")
        
        page.insert_text((x_totaux + 120, y_current + 15), f"{total_ht:.2f} \x80", fontsize=10, fontname="Helvetica-Bold")
        
        # Total TVA
        page.insert_text((x_totaux + 5, y_current + 35), "Total TVA :", fontsize=10, fontname="Helvetica-Bold")

        page.insert_text((x_totaux + 120, y_current + 35), f"{total_TVA:.2f} \x80", fontsize=10, fontname="Helvetica-Bold")
        
        # Total TTC
        rect_ttc = fitz.Rect(x_totaux, y_current + 50, x_droite, y_current + 80)
        page.draw_rect(rect_ttc, fill=couleur_gris_fonce)
        page.insert_text((x_totaux + 5, y_current + 65), "Total TTC :", fontsize=12, fontname="Helvetica-Bold")
        page.insert_text((x_totaux + 120, y_current + 65), f"{total_TVA+total_ht:.2f} \x80", fontsize=12, fontname="Helvetica-Bold")
        
        y_current += 90
        
        # 3. Informations complémentaires
        rect_info = fitz.Rect(x_gauche, y_current, x_droite, y_current + 40)
        page.draw_rect(rect_info, color=couleur_noir, width=1, fill=(1, 0.9, 0.9))
        
        page.insert_text((x_gauche + 5, y_current + 15), "Images et photos non contractuelles - ce devis est valable 10 jours.", 
                        fontsize=10, fontname="Helvetica-Bold", color=couleur_rouge)
        page.insert_text((x_gauche + 5, y_current + 30), "/* Devis sous réserve de visite technique */", 
                        fontsize=9, fontname="Helvetica-Oblique", color=couleur_rouge)
    
        y_current += 50
        
        # 4. Coordonnées bancaires
        rect_bancaire = fitz.Rect(x_gauche, y_current, x_droite, y_current + 35)
        page.draw_rect(rect_bancaire, color=couleur_noir, width=1)
        
        page.insert_text((x_gauche + 5, y_current + 15), "COORDONNÉES BANCAIRES : CR NORD DE FRANCE", 
                        fontsize=10, fontname="Helvetica-Bold")
        page.insert_text((x_gauche + 5, y_current + 30), "IBAN : FR76 1670 6000 6053 9267 1036 936 - BIC : AGRIFRPP867", 
                        fontsize=9, fontname="Helvetica")
        
        y_current += 40
        
        # 5. Section signature
        rect_signature = fitz.Rect(x_gauche, y_current, x_droite, y_current + 40)
        page.draw_rect(rect_signature, color=couleur_noir, width=1)
        
        # Diviser en 3 colonnes
        col_width = largeur_tableau / 3
        
        page.insert_text((x_gauche + 5, y_current + 15), "Bon pour accord", fontsize=10, fontname="Helvetica-Bold")
        page.insert_text((x_gauche + col_width + 5, y_current + 15), "Fait à :", fontsize=10, fontname="Helvetica-Bold")
        page.insert_text((x_gauche + 2*col_width + 5, y_current + 15), "Signature client :", fontsize=10, fontname="Helvetica-Bold")
        
        # Lignes de séparation verticales
        page.draw_line(fitz.Point(x_gauche + col_width, y_current), 
                      fitz.Point(x_gauche + col_width, y_current + 40), width=1)
        page.draw_line(fitz.Point(x_gauche + 2*col_width, y_current), 
                      fitz.Point(x_gauche + 2*col_width, y_current + 40), width=1)
#

def personnaliser_devis_pdf(
    input_pdf_path,
    output_pdf_path,
    logo_path,
    nom_client="Nom prénom",
    adresse_client="885 BOULEVARD DES PRINCES",
    ville_client="06210 MANDELIEU-LA-NAPOULE",
    societe_pose="FERMETURE SABOT",
    representant_pose="Boufedji selim",
    siret_pose="934 496 985",
    certificat_rge="E-E210179",
    date_attribution="19/11/2024",
    date_validite="16/06/2025",
    accompte1=0.2,
    accompte2=0.3,
    solde=0.5,
    Date="04/06/2025",
    numero_devis=344333,
    code_client=7658765
):
    processor = PDFProcessor()
    logo_quali = "quali.png"
    
    texte_pose_sous_traite = (
        f"Pose sous traité mis en place par la société {societe_pose}\n"
        f"représentée par {representant_pose}, SIRET {siret_pose}, Certificat RGE\n"
        f"Numéro {certificat_rge} attribué le {date_attribution} valable jusqu'au {date_validite}"
    )
    
    doc = fitz.open(input_pdf_path)
    page1 = doc[0]
    last_page = doc[-1]
    
    # 1. Extraire les montants de la dernière page
    texte_derniere_page = last_page.get_text()
    montants = processor.extraire_montants(texte_derniere_page)
    processor.montants_extraits = montants
    
    # 2. Nettoyage en-tête et pied de toutes les pages
    page1.add_redact_annot(fitz.Rect(30, 20, 570, 120), fill=(1, 1, 1))
    page1.add_redact_annot(fitz.Rect(30, 125, 570, 200), fill=(1, 1, 1))
    page1.add_redact_annot(fitz.Rect(20, 170, 300, 210), fill=(1, 1, 1))
    
    for page in doc:
        # Pied de page standard
        page.add_redact_annot(fitz.Rect(20, 760, 570, 800), fill=(1, 1, 1))
        page.apply_redactions()
        
        # Footer personnalisé
        ligne_zone = fitz.Rect(30, 760, 570, 804)
        page.draw_rect(ligne_zone, fill=(238/255, 238/255, 238/255), color=None)
        page.insert_text((38, 785), "SIRET : 94366500000015", fontsize=8, fontname="Helvetica", color=(0, 0, 0))
        page.insert_text((140, 785), "Adresse : 885 BOULEVARD DES PRINCES, 06210 MANDELIEU-LA-NAPOULE", fontsize=8, fontname="Helvetica", color=(0, 0, 0))
        
        ligne_zone_1 = fitz.Rect(30, 804, 570, 805)
        page.draw_rect(ligne_zone_1, fill=(90/255, 177/255, 235/255), color=None)
        page.insert_image(fitz.Rect(30, 753, 1066, 803), filename=logo_quali)
        
        ligne_zone_certificat = fitz.Rect(430, 789, 525, 801)
        page.draw_rect(ligne_zone_certificat, fill=(4/255, 138/255, 211/255), color=None)
        page.insert_text((430, 797), f"Certificat N° {certificat_rge} ", fontsize=8, fontname="Helvetica", color=(1, 1, 1))
        #trouver_zone_entete(page)
        processor.trouver_zone_entete(page)
        
    
    # 3. En-tête personnalisé première page
    page1.insert_image(fitz.Rect(30, 20, 130, 100), filename=logo_path)
    
    # Zone entreprise
    rect_zone_2 = fitz.Rect(30, 120, 570, 190)
    page1.draw_rect(rect_zone_2, fill=(238/255, 238/255, 238/255), color=None)
    
    #page1.insert_text((32, 110), "Fenêtre sur le monde", fontsize=14, fontname="Helvetica-Bold", color=(0, 0, 0))
    page1.insert_text((32, 135), "885 BOULEVARD DES PRINCES", fontsize=10, fontname="Helvetica-Bold")
    page1.insert_text((32, 150), "06210 MANDELIEU-LA-NAPOULE", fontsize=10, fontname="Helvetica-Bold")
    page1.insert_text((32, 165), "Tél. : 06 51 17 39 39", fontsize=10, fontname="Helvetica-Bold")
    page1.insert_text((32, 180), "E-mail : fenetresurlemonde@gmail.com", fontsize=10, fontname="Helvetica-Bold")
    rect_info = fitz.Rect(30, 120, 570, 190)
    page1.draw_rect(rect_info, color=(0, 0, 0), width=1)
    # Infos client
    page1.insert_text((400, 135), nom_client, fontsize=10, fontname="Helvetica-Bold")
    page1.insert_text((400, 150), adresse_client, fontsize=10, fontname="Helvetica-Bold")
    page1.insert_text((400, 165), ville_client, fontsize=10, fontname="Helvetica-Bold")
    
    # Bloc à droite
    page1.draw_rect(fitz.Rect(400, 30, 570, 85), fill=(90/255, 177/255, 235/255), color=None)
    page1.draw_rect(fitz.Rect(400, 87, 570, 88), fill=(90/255, 177/255, 235/255), color=None)
    
    # Section poseur
    page1.draw_rect(fitz.Rect(30, 325, 570, 390), fill=(1, 1, 1), color=None)
    page1.draw_rect(fitz.Rect(30, 330, 570, 390), fill=(238/255, 238/255, 238/255), color=None)
    page1.insert_text((33, 350), texte_pose_sous_traite, fontsize=12, fontname="Helvetica-Bold", color=(0, 0, 0))
    
    rect_poseur = fitz.Rect(30, 330, 570, 390)
    page1.draw_rect(rect_poseur, color=(0, 0, 0), width=1)
    
    rect_d = fitz.Rect(30, 210, 570, 325)
    page1.draw_rect(rect_d, color=(0, 0, 0), width=1)

    
    page1.insert_text((415, 45), f"Date : {Date}", fontsize=11, fontname="Helvetica-Bold", color=(1, 1, 1))
    page1.insert_text((415, 60), f"DEVIS N° : {numero_devis}", fontsize=11, fontname="Helvetica-Bold", color=(1, 1, 1))
    page1.insert_text((415, 75), f"Code Client :{code_client}", fontsize=11, fontname="Helvetica-Bold", color=(1, 1, 1))
    #page1.draw_rect(fitz.Rect(30, 193, 570, 194), fill=(116/255, 185/255, 250/255), color=None)
    
    # 4. Traitement de la dernière page - suppression et nouveau tableau
    zone_a_supprimer = processor.trouver_zone_suppression(last_page)
    
    if zone_a_supprimer:
        # Supprimer l'ancienne zone
        last_page.add_redact_annot(zone_a_supprimer, fill=(1, 1, 1))
        last_page.apply_redactions()
        
        # Créer le nouveau tableau
        y_position = zone_a_supprimer.y0 + 10
        processor.creer_tableau_recapitulatif(last_page, montants, y_position,accompte1,accompte2,solde)
    else:
        print("⚠️ Zone de suppression non trouvée, création du tableau en bas de page")
        processor.creer_tableau_recapitulatif(last_page, montants, 500,accompte1,accompte2,solde)
    
    # Enregistrement
    doc.save(output_pdf_path)
    doc.close()
    print(f"✅ PDF sauvegardé : {output_pdf_path}")
    
    return processor.montants_extraits


# Exemple d'utilisation
if __name__ == "__main__":
    montants_detectes = personnaliser_devis_pdf(
        input_pdf_path="VISCOGLIOSI DevisHAITEM.pdf",
        output_pdf_path="devis_nettoye.pdf",
        logo_path="logo.png",
        nom_client="M. Jean Dupont",
        adresse_client="12 Rue des Lilas",
        ville_client="75000 Paris",
        societe_pose="FERMETURE SABOT",
        representant_pose="Boufedji selim",
        siret_pose="934 496 985",
        certificat_rge="E-E210179",
        date_attribution="19/11/2024",
        date_validite="16/06/2025",
        Date="04/06/2025",
        numero_devis=344333,
        code_client=7658765
    )
    
    print("\n=== RÉSUMÉ DES MONTANTS DÉTECTÉS ===")
    for cle, valeur in montants_detectes.items():
        print(f"{cle}: {valeur}")
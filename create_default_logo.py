from PIL import Image, ImageDraw, ImageFont
import os

def create_default_logos():
    """Crée des logos par défaut si ils n'existent pas"""
    
    # Logo principal avec le nom de l'entreprise
    if not os.path.exists("logo.png"):
        # Créer une image avec le nom de l'entreprise
        width, height = 300, 120
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Essayer d'utiliser une police, sinon police par défaut
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            subtitle_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Texte principal
        main_text = "Fenêtre sur le Monde"
        subtitle_text = "Menuiserie - Fermeture"
        
        # Calculer la position du titre
        bbox = draw.textbbox((0, 0), main_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x_main = (width - text_width) // 2
        y_main = 30
        
        # Calculer la position du sous-titre
        bbox_sub = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        sub_width = bbox_sub[2] - bbox_sub[0]
        x_sub = (width - sub_width) // 2
        y_sub = y_main + text_height + 10
        
        # Dessiner le texte principal en bleu
        draw.text((x_main, y_main), main_text, fill=(0, 102, 204), font=title_font)
        
        # Dessiner le sous-titre en gris
        draw.text((x_sub, y_sub), subtitle_text, fill=(100, 100, 100), font=subtitle_font)
        
        # Bordure élégante
        draw.rectangle([5, 5, width-6, height-6], outline=(0, 102, 204), width=3)
        
        # Petite ligne décorative sous le titre
        line_start_x = x_main
        line_end_x = x_main + text_width
        line_y = y_main + text_height + 5
        draw.line([(line_start_x, line_y), (line_end_x, line_y)], fill=(0, 102, 204), width=2)
        
        image.save("logo.png")
        print("✅ Logo professionnel créé : logo.png")
    
    # Logo qualification RGE
    if not os.path.exists("quali.png"):
        width, height = 120, 60
        image = Image.new('RGB', (width, height), color=(0, 150, 0))  # Vert pour RGE
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 14)
            small_font = ImageFont.truetype("arial.ttf", 10)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Texte RGE
        text = "RGE"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = 15
        
        draw.text((x, y), text, fill='white', font=font)
        
        # Sous-texte
        subtext = "Qualité"
        bbox_sub = draw.textbbox((0, 0), subtext, font=small_font)
        sub_width = bbox_sub[2] - bbox_sub[0]
        x_sub = (width - sub_width) // 2
        
        draw.text((x_sub, y + text_height + 5), subtext, fill='white', font=small_font)
        
        # Bordure blanche
        draw.rectangle([2, 2, width-3, height-3], outline='white', width=2)
        
        image.save("quali.png")
        print("✅ Logo qualification RGE créé : quali.png")

if __name__ == "__main__":
    create_default_logos() 
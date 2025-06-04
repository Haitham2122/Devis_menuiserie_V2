import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class SocietesManager:
    def __init__(self, data_file: str = "societes.json"):
        self.data_file = data_file
        self.societes = self._load_societes()
    
    def _load_societes(self) -> List[Dict]:
        """Charge les sociétés depuis le fichier JSON"""
        if not os.path.exists(self.data_file):
            # Créer avec des données par défaut
            default_societes = [
                {
                    "id": 1,
                    "nom": "FERMETURE SABOT",
                    "representant": "Boufedji selim",
                    "siret": "934 496 985",
                    "certificat_rge": "E-E210179",
                    "date_attribution": "2024-11-19",
                    "date_validite": "2025-06-16",
                    "date_creation": datetime.now().isoformat(),
                    "actif": True
                }
            ]
            self._save_societes(default_societes)
            return default_societes
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_societes(self, societes: List[Dict]):
        """Sauvegarde les sociétés dans le fichier JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(societes, f, ensure_ascii=False, indent=2)
        self.societes = societes
    
    def _get_next_id(self) -> int:
        """Génère le prochain ID disponible"""
        if not self.societes:
            return 1
        return max(s.get('id', 0) for s in self.societes) + 1
    
    def get_all_societes(self, actives_only: bool = True) -> List[Dict]:
        """Récupère toutes les sociétés"""
        if actives_only:
            return [s for s in self.societes if s.get('actif', True)]
        return self.societes.copy()
    
    def get_societe_by_id(self, societe_id: int) -> Optional[Dict]:
        """Récupère une société par son ID"""
        for societe in self.societes:
            if societe.get('id') == societe_id:
                return societe.copy()
        return None
    
    def add_societe(self, nom: str, representant: str, siret: str, certificat_rge: str, date_attribution: str, date_validite: str) -> Dict:
        """Ajoute une nouvelle société"""
        nouvelle_societe = {
            "id": self._get_next_id(),
            "nom": nom.strip(),
            "representant": representant.strip(),
            "siret": siret.strip(),
            "certificat_rge": certificat_rge.strip(),
            "date_attribution": date_attribution.strip(),
            "date_validite": date_validite.strip(),
            "date_creation": datetime.now().isoformat(),
            "actif": True
        }
        
        self.societes.append(nouvelle_societe)
        self._save_societes(self.societes)
        
        return nouvelle_societe.copy()
    
    def update_societe(self, societe_id: int, nom: str, representant: str, siret: str, certificat_rge: str, date_attribution: str, date_validite: str) -> Optional[Dict]:
        """Met à jour une société existante"""
        for i, societe in enumerate(self.societes):
            if societe.get('id') == societe_id:
                self.societes[i].update({
                    "nom": nom.strip(),
                    "representant": representant.strip(),
                    "siret": siret.strip(),
                    "certificat_rge": certificat_rge.strip(),
                    "date_attribution": date_attribution.strip(),
                    "date_validite": date_validite.strip(),
                    "date_modification": datetime.now().isoformat()
                })
                self._save_societes(self.societes)
                return self.societes[i].copy()
        return None
    
    def delete_societe(self, societe_id: int) -> bool:
        """Supprime une société (soft delete)"""
        for i, societe in enumerate(self.societes):
            if societe.get('id') == societe_id:
                self.societes[i]['actif'] = False
                self.societes[i]['date_suppression'] = datetime.now().isoformat()
                self._save_societes(self.societes)
                return True
        return False
    
    def restore_societe(self, societe_id: int) -> bool:
        """Restaure une société supprimée"""
        for i, societe in enumerate(self.societes):
            if societe.get('id') == societe_id:
                self.societes[i]['actif'] = True
                if 'date_suppression' in self.societes[i]:
                    del self.societes[i]['date_suppression']
                self._save_societes(self.societes)
                return True
        return False
    
    def search_societes(self, query: str) -> List[Dict]:
        """Recherche des sociétés par nom ou représentant"""
        query = query.lower().strip()
        if not query:
            return self.get_all_societes()
        
        results = []
        for societe in self.get_all_societes():
            if (query in societe.get('nom', '').lower() or 
                query in societe.get('representant', '').lower()):
                results.append(societe)
        
        return results

# Instance globale du gestionnaire
societes_manager = SocietesManager() 
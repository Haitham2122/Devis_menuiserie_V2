import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import csv
import io
import urllib.request

class SocietesManager:
    def __init__(self, data_file: str = "societes.json"):
        self.data_file = data_file
        # Configuration Google Sheet (si présente, on privilégie la feuille)
        self.google_sheet_id = os.environ.get(
            "GOOGLE_SHEET_ID",
            "1ekE0STldHnW3zruG8_G8VKn7xwEOsdNqvpPc-tbWwKw"  # par défaut: l'ID fourni
        )
        self.google_sheet_gid = os.environ.get("GOOGLE_SHEET_GID", "0")
        # Activer la feuille Google uniquement si l'ID est défini explicitement (ou laissé au défaut)
        self.source = "google" if self.google_sheet_id else "json"
        self.societes = self._load_societes()
    
    def _load_societes(self) -> List[Dict]:
        """Charge les sociétés depuis Google Sheet (si configuré), sinon depuis le JSON local."""
        # 1) Essayer la feuille Google (CSV public)
        if self.source == "google":
            try:
                url = (
                    f"https://docs.google.com/spreadsheets/d/{self.google_sheet_id}/export?format=csv&gid={self.google_sheet_gid}"
                )
                with urllib.request.urlopen(url, timeout=10) as resp:
                    csv_bytes = resp.read()
                csv_text = csv_bytes.decode("utf-8", errors="replace")
                reader = csv.DictReader(io.StringIO(csv_text))
                societes: List[Dict] = []
                for row in reader:
                    if not any(row.values()):
                        continue
                    try:
                        sid = int(row.get("id", "").strip() or 0)
                    except Exception:
                        sid = 0
                    nom = (row.get("nom", "") or "").strip()
                    representant = (row.get("representant", "") or "").strip()
                    siret = (row.get("siret", "") or "").strip()
                    certificat_rge = (row.get("certificat_rge", "") or "").strip()
                    date_attribution = (row.get("date_attribution", "") or "").strip()
                    date_validite = (row.get("date_validite", "") or "").strip()
                    if not nom:
                        continue
                    societes.append({
                        "id": sid if sid > 0 else None,
                        "nom": nom,
                        "representant": representant,
                        "siret": siret,
                        "certificat_rge": certificat_rge,
                        "date_attribution": date_attribution,
                        "date_validite": date_validite,
                        "date_creation": datetime.now().isoformat(),
                        "actif": True
                    })
                # Donner des IDs si manquants en gardant l'ordre
                next_id = 1
                for s in societes:
                    if s["id"] is None:
                        s["id"] = next_id
                        next_id += 1
                    else:
                        next_id = max(next_id, s["id"] + 1)
                return societes
            except Exception:
                # En cas d'échec on tombe sur le JSON local
                pass

        # 2) JSON local (fallback)
        if not os.path.exists(self.data_file):
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
        # Si Google Sheet est la source, rafraîchir à chaque appel pour récupérer les nouvelles lignes
        if self.source == "google":
            self.societes = self._load_societes()
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
        if self.source == "google":
            raise RuntimeError("Ajout via API désactivé: modifiez la Google Sheet pour ajouter des sociétés.")
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
        if self.source == "google":
            raise RuntimeError("Mise à jour via API désactivée: modifiez la Google Sheet pour mettre à jour.")
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
        if self.source == "google":
            raise RuntimeError("Suppression via API désactivée: supprimez la ligne dans la Google Sheet.")
        for i, societe in enumerate(self.societes):
            if societe.get('id') == societe_id:
                self.societes[i]['actif'] = False
                self.societes[i]['date_suppression'] = datetime.now().isoformat()
                self._save_societes(self.societes)
                return True
        return False
    
    def restore_societe(self, societe_id: int) -> bool:
        """Restaure une société supprimée"""
        if self.source == "google":
            raise RuntimeError("Restauration via API désactivée: gérez l'état dans la Google Sheet.")
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
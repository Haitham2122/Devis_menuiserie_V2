from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import uuid
from datetime import datetime
from devismodif import personnaliser_devis_pdf
import shutil
from societes_manager import societes_manager
import re

app = FastAPI(
    title="Processeur de Devis PDF", 
    description="API pour personnaliser des devis PDF",
    version="1.0.0"
)

# Configuration CORS pour Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer le dossier static s'il n'existe pas
os.makedirs("static", exist_ok=True)

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health_check():
    """Endpoint de santé pour Render"""
    return {"status": "healthy", "service": "PDF Processor"}

# ==================== ENDPOINTS SOCIÉTÉS ====================

@app.get("/api/societes")
async def get_societes():
    """Récupère toutes les sociétés actives"""
    return {"societes": societes_manager.get_all_societes()}

@app.get("/api/societes/{societe_id}")
async def get_societe(societe_id: int):
    """Récupère une société par son ID"""
    societe = societes_manager.get_societe_by_id(societe_id)
    if not societe:
        raise HTTPException(status_code=404, detail="Société non trouvée")
    return {"societe": societe}

@app.post("/api/societes")
async def create_societe(
    nom: str = Form(...),
    representant: str = Form(...),
    siret: str = Form(...),
    certificat_rge: str = Form(...),
    date_attribution: str = Form(...),
    date_validite: str = Form(...)
):
    """Crée une nouvelle société"""
    try:
        nouvelle_societe = societes_manager.add_societe(nom, representant, siret, certificat_rge, date_attribution, date_validite)
        return {"success": True, "societe": nouvelle_societe, "message": "Société créée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création : {str(e)}")

@app.put("/api/societes/{societe_id}")
async def update_societe(
    societe_id: int,
    nom: str = Form(...),
    representant: str = Form(...),
    siret: str = Form(...),
    certificat_rge: str = Form(...),
    date_attribution: str = Form(...),
    date_validite: str = Form(...)
):
    """Met à jour une société"""
    societe_updated = societes_manager.update_societe(societe_id, nom, representant, siret, certificat_rge, date_attribution, date_validite)
    if not societe_updated:
        raise HTTPException(status_code=404, detail="Société non trouvée")
    return {"success": True, "societe": societe_updated, "message": "Société mise à jour avec succès"}

@app.delete("/api/societes/{societe_id}")
async def delete_societe(societe_id: int):
    """Supprime une société"""
    success = societes_manager.delete_societe(societe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Société non trouvée")
    return {"success": True, "message": "Société supprimée avec succès"}

@app.get("/societes", response_class=HTMLResponse)
async def gestion_societes():
    """Page de gestion des sociétés"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestion des Sociétés - Fenêtre sur le Monde</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { background: white; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin: 2rem auto; padding: 2rem; }
            .header-title { color: #2c3e50; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
            .societe-card { border: 1px solid #dee2e6; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; background: #f8f9fa; }
            .btn-edit { background: #28a745; border: none; }
            .btn-delete { background: #dc3545; border: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1 class="header-title"><i class="fas fa-building"></i> Gestion des Sociétés</h1>
                <a href="/" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Retour</a>
            </div>

            <!-- Formulaire d'ajout -->
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5><i class="fas fa-plus"></i> Ajouter une Société</h5>
                </div>
                <div class="card-body">
                    <form id="addSocieteForm">
                        <div class="row">
                            <div class="col-md-6">
                                <label class="form-label">Nom de la Société :</label>
                                <input type="text" class="form-control" name="nom" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Représentant :</label>
                                <input type="text" class="form-control" name="representant" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">SIRET :</label>
                                <input type="text" class="form-control" name="siret" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Certificat RGE :</label>
                                <input type="text" class="form-control" name="certificat_rge" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Date Attribution RGE :</label>
                                <input type="date" class="form-control" name="date_attribution" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Date Validité :</label>
                                <input type="date" class="form-control" name="date_validite" required>
                            </div>
                        </div>
                        <div class="mt-3">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Ajouter la Société
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Liste des sociétés -->
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5><i class="fas fa-list"></i> Sociétés Enregistrées</h5>
                </div>
                <div class="card-body">
                    <div id="societesList"></div>
                </div>
            </div>
        </div>

        <!-- Modal d'édition -->
        <div class="modal fade" id="editModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Modifier la Société</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="editSocieteForm">
                            <input type="hidden" id="editSocieteId">
                            <div class="mb-3">
                                <label class="form-label">Nom de la Société :</label>
                                <input type="text" class="form-control" id="editNom" name="nom" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Représentant :</label>
                                <input type="text" class="form-control" id="editRepresentant" name="representant" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">SIRET :</label>
                                <input type="text" class="form-control" id="editSiret" name="siret" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Certificat RGE :</label>
                                <input type="text" class="form-control" id="editCertificat" name="certificat_rge" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Date Attribution RGE :</label>
                                <input type="date" class="form-control" id="editDateAttribution" name="date_attribution" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Date Validité :</label>
                                <input type="date" class="form-control" id="editDateValidite" name="date_validite" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-primary" onclick="updateSociete()">Sauvegarder</button>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Charger les sociétés au démarrage
            loadSocietes();

            // Formulaire d'ajout
            document.getElementById('addSocieteForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                
                try {
                    const response = await fetch('/api/societes', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        this.reset();
                        loadSocietes();
                        alert('Société ajoutée avec succès !');
                    } else {
                        alert('Erreur lors de l\\'ajout');
                    }
                } catch (error) {
                    alert('Erreur: ' + error.message);
                }
            });

            async function loadSocietes() {
                try {
                    const response = await fetch('/api/societes');
                    const data = await response.json();
                    
                    const list = document.getElementById('societesList');
                    list.innerHTML = '';
                    
                    if (data.societes.length === 0) {
                        list.innerHTML = '<p class="text-muted">Aucune société enregistrée.</p>';
                        return;
                    }
                    
                    data.societes.forEach(societe => {
                        const card = document.createElement('div');
                        card.className = 'societe-card';
                        card.innerHTML = `
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="text-primary">${societe.nom}</h6>
                                    <p class="mb-1"><strong>Représentant:</strong> ${societe.representant}</p>
                                    <p class="mb-1"><strong>SIRET:</strong> ${societe.siret}</p>
                                    <p class="mb-1"><strong>RGE:</strong> ${societe.certificat_rge}</p>
                                    <p class="mb-1"><strong>Date Attribution:</strong> ${societe.date_attribution}</p>
                                    <p class="mb-0"><strong>Date Validité:</strong> ${societe.date_validite}</p>
                                </div>
                                <div>
                                    <button class="btn btn-sm btn-edit me-2" onclick="editSociete(${societe.id})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="btn btn-sm btn-delete" onclick="deleteSociete(${societe.id})">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                        `;
                        list.appendChild(card);
                    });
                } catch (error) {
                    console.error('Erreur:', error);
                }
            }

            async function editSociete(id) {
                try {
                    const response = await fetch(`/api/societes/${id}`);
                    const data = await response.json();
                    const societe = data.societe;
                    
                    document.getElementById('editSocieteId').value = id;
                    document.getElementById('editNom').value = societe.nom;
                    document.getElementById('editRepresentant').value = societe.representant;
                    document.getElementById('editSiret').value = societe.siret;
                    document.getElementById('editCertificat').value = societe.certificat_rge;
                    document.getElementById('editDateAttribution').value = societe.date_attribution;
                    document.getElementById('editDateValidite').value = societe.date_validite;
                    
                    new bootstrap.Modal(document.getElementById('editModal')).show();
                } catch (error) {
                    alert('Erreur lors du chargement: ' + error.message);
                }
            }

            async function updateSociete() {
                const id = document.getElementById('editSocieteId').value;
                const formData = new FormData(document.getElementById('editSocieteForm'));
                
                try {
                    const response = await fetch(`/api/societes/${id}`, {
                        method: 'PUT',
                        body: formData
                    });
                    
                    if (response.ok) {
                        bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
                        loadSocietes();
                        alert('Société mise à jour avec succès !');
                    } else {
                        alert('Erreur lors de la mise à jour');
                    }
                } catch (error) {
                    alert('Erreur: ' + error.message);
                }
            }

            async function deleteSociete(id) {
                if (!confirm('Êtes-vous sûr de vouloir supprimer cette société ?')) {
                    return;
                }
                
                try {
                    const response = await fetch(`/api/societes/${id}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        loadSocietes();
                        alert('Société supprimée avec succès !');
                    } else {
                        alert('Erreur lors de la suppression');
                    }
                } catch (error) {
                    alert('Erreur: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def interface_principale():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Générateur de Devis - Fenêtre sur le Monde</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: #f8fafc;
                color: #1e293b;
                line-height: 1.6;
                min-height: 100vh;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem 1rem;
            }
            
            .header {
                text-align: center;
                margin-bottom: 3rem;
                padding-top: 2rem;
            }
            
            .logo {
                width: 64px;
                height: 64px;
                background: linear-gradient(135deg, #3b82f6, #1e40af);
                border-radius: 16px;
                margin: 0 auto 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                font-weight: 600;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            }
            
            .title {
                font-size: 2.25rem;
                font-weight: 600;
                color: #0f172a;
                margin-bottom: 0.75rem;
                letter-spacing: -0.025em;
            }
            
            .subtitle {
                font-size: 1.125rem;
                color: #64748b;
                font-weight: 400;
            }
            
            .form-card {
                background: white;
                border-radius: 20px;
                box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
                padding: 2.5rem;
                margin-bottom: 2rem;
                border: 1px solid #e2e8f0;
            }
            
            .section {
                margin-bottom: 2rem;
            }
            
            .section:last-child {
                margin-bottom: 0;
            }
            
            .section-header {
                display: flex;
                align-items: center;
                margin-bottom: 1.5rem;
            }
            
            .section-icon {
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: #f1f5f9;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
                color: #3b82f6;
                font-size: 18px;
            }
            
            .section-title {
                font-size: 1.25rem;
                font-weight: 600;
                color: #0f172a;
                flex: 1;
            }
            
            .section-link {
                color: #3b82f6;
                text-decoration: none;
                font-size: 0.875rem;
                font-weight: 500;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                transition: all 0.2s;
            }
            
            .section-link:hover {
                background: #f8fafc;
                border-color: #3b82f6;
            }
            
            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
            }
            
            .form-group {
                display: flex;
                flex-direction: column;
            }
            
            .form-group.full-width {
                grid-column: 1 / -1;
            }
            
            .form-label {
                font-size: 0.875rem;
                font-weight: 500;
                color: #374151;
                margin-bottom: 0.5rem;
            }
            
            .form-input, .form-select {
                padding: 0.75rem 1rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 10px;
                font-size: 0.875rem;
                background: white;
                transition: all 0.2s;
                outline: none;
            }
            
            .form-input:focus, .form-select:focus {
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1);
            }
            
            .form-file {
                padding: 1.5rem;
                border: 2px dashed #cbd5e1;
                border-radius: 12px;
                text-align: center;
                background: #f8fafc;
                transition: all 0.2s;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }
            
            .form-file:hover {
                border-color: #3b82f6;
                background: #f0f9ff;
            }
            
            .form-file.file-selected {
                border-color: #059669;
                background: #f0fdf4;
            }
            
            .form-file.file-selected .file-icon {
                color: #059669;
            }
            
            .form-file.file-selected .file-text {
                color: #047857;
                font-weight: 600;
            }
            
            .form-file input {
                position: absolute;
                inset: 0;
                opacity: 0;
                cursor: pointer;
            }
            
            .file-icon {
                font-size: 2rem;
                color: #64748b;
                margin-bottom: 0.75rem;
            }
            
            .file-text {
                font-weight: 500;
                color: #1e293b;
                margin-bottom: 0.25rem;
            }
            
            .file-subtext {
                font-size: 0.875rem;
                color: #64748b;
            }
            
            .info-box {
                background: #f0f9ff;
                border: 1px solid #bfdbfe;
                border-radius: 10px;
                padding: 1rem;
                margin-top: 1rem;
            }
            
            .info-box.success {
                background: #f0fdf4;
                border-color: #bbf7d0;
            }
            
            .info-text {
                font-size: 0.875rem;
                color: #0369a1;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .info-text.success {
                color: #166534;
            }
            
            .details-box {
                background: #f8fafc;
                border-radius: 10px;
                padding: 1.25rem;
                margin-top: 1rem;
                border: 1px solid #e2e8f0;
                display: none;
            }
            
            .details-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            
            .detail-item {
                font-size: 0.875rem;
            }
            
            .detail-label {
                font-weight: 500;
                color: #374151;
            }
            
            .detail-value {
                color: #6b7280;
            }
            
            .percentage-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
            }
            
            .percentage-total {
                text-align: center;
                padding: 1rem;
                background: #f8fafc;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
                margin-top: 1rem;
            }
            
            .total-label {
                font-size: 0.875rem;
                color: #6b7280;
                margin-bottom: 0.25rem;
            }
            
            .total-value {
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            .total-success {
                color: #059669;
            }
            
            .total-warning {
                color: #d97706;
            }
            
            .submit-button {
                width: 100%;
                background: linear-gradient(135deg, #3b82f6, #1e40af);
                color: white;
                border: none;
                padding: 1rem 2rem;
                border-radius: 12px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                margin-top: 2rem;
            }
            
            .submit-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 15px -3px rgb(0 0 0 / 0.1);
            }
            
            .submit-button:active {
                transform: translateY(0);
            }
            
            .status-card {
                background: white;
                border-radius: 16px;
                box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
                padding: 2rem;
                margin-top: 2rem;
                border: 1px solid #e2e8f0;
                text-align: center;
                display: none;
            }
            
            .status-success {
                border-color: #bbf7d0;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            }
            
            .status-error {
                border-color: #fecaca;
                background: linear-gradient(135deg, #fef2f2, #fee2e2);
            }
            
            .status-loading {
                border-color: #bfdbfe;
                background: linear-gradient(135deg, #f0f9ff, #dbeafe);
            }
            
            .loading-spinner {
                width: 40px;
                height: 40px;
                border: 3px solid #e2e8f0;
                border-top: 3px solid #3b82f6;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .download-button {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: #059669;
                color: white;
                text-decoration: none;
                padding: 1rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.2s;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                margin-top: 1rem;
            }
            
            .download-button:hover {
                background: #047857;
                transform: translateY(-2px);
                box-shadow: 0 8px 15px -3px rgb(0 0 0 / 0.1);
            }
            
            @media (max-width: 768px) {
                .container {
                    padding: 1rem;
                }
                
                .form-card {
                    padding: 1.5rem;
                }
                
                .title {
                    font-size: 1.875rem;
                }
                
                .form-grid {
                    grid-template-columns: 1fr;
                }
                
                .percentage-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <div class="logo">FM</div>
                <h1 class="title">Générateur de Devis</h1>
                <p class="subtitle">Fenêtre sur le Monde • Personnalisation professionnelle</p>
            </div>

            <!-- Form -->
            <div class="form-card">
                <form id="devisForm" enctype="multipart/form-data">
                    
                    <!-- Upload Section -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-file-upload"></i>
                            </div>
                            <div class="section-title">Document PDF</div>
                        </div>
                        
                        <div class="form-file" id="fileDropZone">
                            <input type="file" name="pdf_file" accept=".pdf" required id="pdfFileInput">
                            <div class="file-icon" id="fileIcon">
                                <i class="fas fa-file-pdf"></i>
                            </div>
                            <div class="file-text" id="fileText">Sélectionner le devis PDF</div>
                            <div class="file-subtext" id="fileSubtext">Glissez-déposez ou cliquez pour parcourir</div>
                        </div>
                        
                        <div class="info-box">
                            <div class="info-text">
                                <i class="fas fa-info-circle"></i>
                                Le logo sera automatiquement ajouté au document
                            </div>
                        </div>
                        
                        <div class="info-box success">
                            <div class="info-text success">
                                <i class="fas fa-file-contract"></i>
                                Les conditions générales seront ajoutées automatiquement
                            </div>
                        </div>
                    </div>

                    <!-- Client Information -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-user"></i>
                            </div>
                            <div class="section-title">Informations Client</div>
                        </div>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Nom du client</label>
                                <input type="text" class="form-input" name="nom_client" value="M. Jean Dupont" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Code client</label>
                                <input type="number" class="form-input" name="code_client" value="7658765" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Adresse</label>
                                <input type="text" class="form-input" name="adresse_client" value="12 Rue des Lilas" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Ville</label>
                                <input type="text" class="form-input" name="ville_client" value="75000 Paris" required>
                            </div>
                        </div>
                    </div>

                    <!-- Company Information -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-building"></i>
                            </div>
                            <div class="section-title">Société</div>
                            <a href="/societes" class="section-link" target="_blank">
                                <i class="fas fa-cog"></i> Gérer
                            </a>
                        </div>
                        
                        <div class="form-group full-width">
                            <label class="form-label">Sélectionner une société</label>
                            <select class="form-select" name="societe_id" id="societeSelect" required>
                                <option value="">Chargement...</option>
                            </select>
                        </div>
                        
                        <div class="details-box" id="societeDetails">
                            <div class="details-grid">
                                <div class="detail-item">
                                    <div class="detail-label">Représentant</div>
                                    <div class="detail-value" id="detailRepresentant">-</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">SIRET</div>
                                    <div class="detail-value" id="detailSiret">-</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Certificat RGE</div>
                                    <div class="detail-value" id="detailCertificat">-</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Date Attribution</div>
                                    <div class="detail-value" id="detailDateAttribution">-</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Date Validité</div>
                                    <div class="detail-value" id="detailDateValidite">-</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Date & Numbers -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-calendar"></i>
                            </div>
                            <div class="section-title">Date & Numéro</div>
                        </div>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Date du devis</label>
                                <input type="date" class="form-input" name="date" value="2025-06-04" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Numéro de devis</label>
                                <input type="number" class="form-input" name="numero_devis" value="344333" required>
                            </div>
                        </div>
                        
                        <div class="info-box">
                            <div class="info-text">
                                <i class="fas fa-clock"></i>
                                Les dates RGE sont automatiquement prises de la société sélectionnée
                            </div>
                        </div>
                    </div>

                    <!-- Payment Terms -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-euro-sign"></i>
                            </div>
                            <div class="section-title">Modalités de Paiement</div>
                        </div>
                        
                        <div class="percentage-grid">
                            <div class="form-group">
                                <label class="form-label">Acompte 1 (%)</label>
                                <input type="number" class="form-input" name="accompte1" value="20" min="0" max="100" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Acompte 2 (%)</label>
                                <input type="number" class="form-input" name="accompte2" value="30" min="0" max="100" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Solde (%)</label>
                                <input type="number" class="form-input" name="solde" value="50" min="0" max="100" required>
                            </div>
                        </div>
                        
                        <div class="percentage-total">
                            <div class="total-label">Total</div>
                            <div class="total-value" id="totalPourcentage">100%</div>
                        </div>
                    </div>

                    <!-- TVA Section -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-percentage"></i>
                            </div>
                            <div class="section-title">Taux de TVA</div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Sélectionner le taux de TVA</label>
                            <select class="form-select" name="tva" required>
                                <option value="0.055">5.5% - Travaux de rénovation énergétique</option>
                                <option value="0.00">0% - Exonération de TVA</option>
                            </select>
                        </div>
                        
                        <div class="info-box">
                            <div class="info-text">
                                <i class="fas fa-info-circle"></i>
                                La TVA à 5.5% s'applique aux travaux de rénovation énergétique éligibles
                            </div>
                        </div>
                    </div>

                    <!-- Forfait Pose Section -->
                    <div class="section">
                        <div class="section-header">
                            <div class="section-icon">
                                <i class="fas fa-tools"></i>
                            </div>
                            <div class="section-title">Forfait Pose</div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Montant du forfait pose (€)</label>
                            <input type="number" class="form-input" name="forfait_pose" value="2000" min="0" step="0.01" required>
                        </div>
                        
                        <div class="info-box">
                            <div class="info-text">
                                <i class="fas fa-info-circle"></i>
                                Ce montant sera ajouté au total HT pour calculer le coût total avec la pose
                            </div>
                        </div>
                    </div>

                    <button type="submit" class="submit-button">
                        <i class="fas fa-magic"></i>
                        Générer le Devis Complet
                    </button>
                </form>
            </div>

            <!-- Status Cards -->
            <div id="loadingCard" class="status-card status-loading">
                <div class="loading-spinner"></div>
                <h3>Génération en cours...</h3>
                <p>Personnalisation et ajout des conditions générales</p>
            </div>

            <div id="successCard" class="status-card status-success">
                <div style="font-size: 3rem; color: #059669; margin-bottom: 1rem;">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h3>Devis généré avec succès !</h3>
                <p>Votre document complet est prêt à télécharger</p>
                <a href="#" id="downloadLink" class="download-button">
                    <i class="fas fa-download"></i>
                    Télécharger le PDF
                </a>
            </div>

            <div id="errorCard" class="status-card status-error">
                <div style="font-size: 3rem; color: #dc2626; margin-bottom: 1rem;">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3>Erreur lors de la génération</h3>
                <p id="errorMessage">Une erreur s'est produite</p>
            </div>
        </div>

        <script>
            // Load companies on startup
            loadSocietes();

            // Calculate percentage total
            function updateTotal() {
                const accompte1 = parseInt(document.querySelector('[name="accompte1"]').value) || 0;
                const accompte2 = parseInt(document.querySelector('[name="accompte2"]').value) || 0;
                const solde = parseInt(document.querySelector('[name="solde"]').value) || 0;
                const total = accompte1 + accompte2 + solde;
                
                const totalElement = document.getElementById('totalPourcentage');
                totalElement.textContent = total + '%';
                
                // Update styling based on total
                totalElement.className = 'total-value ' + (total === 100 ? 'total-success' : 'total-warning');
            }

            // Load companies
            async function loadSocietes() {
                try {
                    const response = await fetch('/api/societes');
                    const data = await response.json();
                    
                    const select = document.getElementById('societeSelect');
                    select.innerHTML = '<option value="">Sélectionner une société...</option>';
                    
                    data.societes.forEach(societe => {
                        const option = document.createElement('option');
                        option.value = societe.id;
                        option.textContent = societe.nom;
                        option.dataset.representant = societe.representant;
                        option.dataset.siret = societe.siret;
                        option.dataset.certificat = societe.certificat_rge;
                        option.dataset.dateAttribution = societe.date_attribution;
                        option.dataset.dateValidite = societe.date_validite;
                        select.appendChild(option);
                    });
                    
                    if (data.societes.length === 0) {
                        select.innerHTML = '<option value="">Aucune société disponible</option>';
                    }
                } catch (error) {
                    console.error('Erreur:', error);
                    document.getElementById('societeSelect').innerHTML = '<option value="">Erreur de chargement</option>';
                }
            }

            // Handle company selection
            document.getElementById('societeSelect').addEventListener('change', function() {
                const selectedOption = this.options[this.selectedIndex];
                const detailsDiv = document.getElementById('societeDetails');
                
                if (selectedOption.value) {
                    document.getElementById('detailRepresentant').textContent = selectedOption.dataset.representant || '-';
                    document.getElementById('detailSiret').textContent = selectedOption.dataset.siret || '-';
                    document.getElementById('detailCertificat').textContent = selectedOption.dataset.certificat || '-';
                    document.getElementById('detailDateAttribution').textContent = selectedOption.dataset.dateAttribution || '-';
                    document.getElementById('detailDateValidite').textContent = selectedOption.dataset.dateValidite || '-';
                    detailsDiv.style.display = 'block';
                } else {
                    detailsDiv.style.display = 'none';
                }
            });

            // Add event listeners for percentages
            ['accompte1', 'accompte2', 'solde'].forEach(name => {
                document.querySelector(`[name="${name}"]`).addEventListener('input', updateTotal);
            });

            // Handle form submission
            document.getElementById('devisForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                // Validate percentages
                const accompte1 = parseInt(document.querySelector('[name="accompte1"]').value) || 0;
                const accompte2 = parseInt(document.querySelector('[name="accompte2"]').value) || 0;
                const solde = parseInt(document.querySelector('[name="solde"]').value) || 0;
                
                if (accompte1 + accompte2 + solde !== 100) {
                    alert('La somme des acomptes doit être égale à 100%');
                    return;
                }

                // Validate company selection
                const societeId = document.querySelector('[name="societe_id"]').value;
                if (!societeId) {
                    alert('Veuillez sélectionner une société');
                    return;
                }
                
                const formData = new FormData(this);
                
                // Show loading
                hideAllStatusCards();
                document.getElementById('loadingCard').style.display = 'block';
                
                try {
                    const response = await fetch('/generer-devis', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const downloadLink = document.getElementById('downloadLink');
                        
                        // Générer le nom de fichier basé sur le client et la date
                        const nomClient = document.querySelector('[name="nom_client"]').value;
                        const dateDevis = document.querySelector('[name="date"]').value;
                        
                        // Fonction pour nettoyer le nom du client (similaire au backend)
                        function cleanFilename(text) {
                            let cleaned = text.replace(/[<>:"/\\|?*]/g, ''); // Caractères interdits
                            cleaned = cleaned.replace(/[àáâãäå]/gi, 'a');
                            cleaned = cleaned.replace(/[èéêë]/gi, 'e');
                            cleaned = cleaned.replace(/[ìíîï]/gi, 'i');
                            cleaned = cleaned.replace(/[òóôõö]/gi, 'o');
                            cleaned = cleaned.replace(/[ùúûü]/gi, 'u');
                            cleaned = cleaned.replace(/[ç]/gi, 'c');
                            cleaned = cleaned.replace(/[ñ]/gi, 'n');
                            cleaned = cleaned.replace(/\s+/g, '_'); // Espaces par underscore
                            cleaned = cleaned.replace(/[^a-zA-Z0-9_.-]/g, ''); // Caractères autorisés seulement
                            return cleaned.substring(0, 50); // Limiter longueur
                        }
                        
                        const clientClean = cleanFilename(nomClient);
                        const filename = `devis_complet_${clientClean}_${dateDevis}.pdf`;
                        
                        downloadLink.href = url;
                        downloadLink.download = filename;
                        
                        hideAllStatusCards();
                        document.getElementById('successCard').style.display = 'block';
                    } else {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Erreur lors de la génération');
                    }
                } catch (error) {
                    document.getElementById('errorMessage').textContent = error.message;
                    hideAllStatusCards();
                    document.getElementById('errorCard').style.display = 'block';
                }
            });

            function hideAllStatusCards() {
                document.getElementById('loadingCard').style.display = 'none';
                document.getElementById('successCard').style.display = 'none';
                document.getElementById('errorCard').style.display = 'none';
            }

            // Handle file selection and drag & drop
            const fileInput = document.getElementById('pdfFileInput');
            const dropZone = document.getElementById('fileDropZone');
            const fileIcon = document.getElementById('fileIcon');
            const fileText = document.getElementById('fileText');
            const fileSubtext = document.getElementById('fileSubtext');

            // Handle file selection
            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    updateFileDisplay(file);
                }
            });

            // Handle drag and drop
            dropZone.addEventListener('dragover', function(e) {
                e.preventDefault();
                dropZone.style.borderColor = '#3b82f6';
                dropZone.style.background = '#f0f9ff';
            });

            dropZone.addEventListener('dragleave', function(e) {
                e.preventDefault();
                if (!dropZone.classList.contains('file-selected')) {
                    dropZone.style.borderColor = '#cbd5e1';
                    dropZone.style.background = '#f8fafc';
                }
            });

            dropZone.addEventListener('drop', function(e) {
                e.preventDefault();
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const file = files[0];
                    if (file.type === 'application/pdf') {
                        fileInput.files = files;
                        updateFileDisplay(file);
                    } else {
                        alert('Veuillez sélectionner un fichier PDF');
                    }
                }
            });

            function updateFileDisplay(file) {
                // Ajouter la classe pour l'état sélectionné
                dropZone.classList.add('file-selected');
                
                // Mettre à jour l'icône
                fileIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
                
                // Afficher le nom du fichier
                fileText.textContent = file.name;
                
                // Afficher la taille du fichier
                const fileSize = (file.size / 1024 / 1024).toFixed(2); // en MB
                fileSubtext.innerHTML = `<i class="fas fa-check"></i> Fichier sélectionné (${fileSize} MB)`;
            }

            // Initialize
            updateTotal();
        </script>
    </body>
    </html>
    """

@app.post("/generer-devis")
async def generer_devis(
    pdf_file: UploadFile = File(...),
    nom_client: str = Form(...),
    adresse_client: str = Form(...),
    ville_client: str = Form(...),
    societe_id: int = Form(...),
    date: str = Form(...),
    numero_devis: int = Form(...),
    code_client: int = Form(...),
    accompte1: float = Form(...),
    accompte2: float = Form(...),
    solde: float = Form(...),
    tva: float = Form(...),
    forfait_pose: float = Form(...)
):
    """Génère un devis PDF personnalisé"""
    
    # Validation des entrées
    if not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")
    
    if accompte1 + accompte2 + solde != 100:
        raise HTTPException(status_code=400, detail="La somme des acomptes doit être égale à 100%")
    
    # Récupérer les informations de la société
    societe = societes_manager.get_societe_by_id(societe_id)
    if not societe:
        raise HTTPException(status_code=404, detail="Société non trouvée")
    
    try:
        # Créer un dossier temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            # Lire le contenu du PDF uploadé en mémoire d'abord
            pdf_content = await pdf_file.read()
            
            # Créer un nom de fichier unique pour éviter les conflits
            unique_filename = f"input_{uuid.uuid4().hex[:8]}_{pdf_file.filename}"
            pdf_path = os.path.join(temp_dir, unique_filename)
            
            # Écrire le contenu dans le fichier temporaire et fermer explicitement
            with open(pdf_path, "wb") as f:
                f.write(pdf_content)
            # Le fichier est maintenant fermé et disponible pour d'autres processus
            
            # Utiliser toujours le logo par défaut
            logo_path = "logo.png"
            
            # Vérifier que le logo par défaut existe
            if not os.path.exists(logo_path):
                print("⚠️ Logo par défaut manquant, création en cours...")
                from create_default_logo import create_default_logos
                create_default_logos()
            
            # Formater les dates
            try:
                date_formatted = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
                date_for_filename = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
                # Utiliser les dates de la société
                date_attribution_formatted = datetime.strptime(societe['date_attribution'], '%Y-%m-%d').strftime('%d/%m/%Y')
                date_validite_formatted = datetime.strptime(societe['date_validite'], '%Y-%m-%d').strftime('%d/%m/%Y')
            except ValueError:
                # Si le format est déjà bon
                date_formatted = date
                date_for_filename = date
                date_attribution_formatted = societe['date_attribution']
                date_validite_formatted = societe['date_validite']
            
            # Créer un nom de fichier basé sur le client et la date
            client_clean = clean_filename(nom_client)
            output_filename = f"devis_{client_clean}_{date_for_filename}.pdf"
            output_path = os.path.join(temp_dir, output_filename)
            
            # Convertir les pourcentages en décimales
            accompte1_decimal = accompte1 / 100
            accompte2_decimal = accompte2 / 100
            solde_decimal = solde / 100
            
            # Appeler la fonction de traitement PDF avec les données de la société
            montants = personnaliser_devis_pdf(
                input_pdf_path=pdf_path,
                output_pdf_path=output_path,
                logo_path=logo_path,
                nom_client=nom_client,
                adresse_client=adresse_client,
                ville_client=ville_client,
                societe_pose=societe['nom'],
                representant_pose=societe['representant'],
                siret_pose=societe['siret'],
                certificat_rge=societe['certificat_rge'],
                date_attribution=date_attribution_formatted,
                date_validite=date_validite_formatted,
                accompte1=accompte1_decimal,
                accompte2=accompte2_decimal,
                solde=solde_decimal,
                Date=date_formatted,
                numero_devis=numero_devis,
                code_client=code_client,
                tva=tva,
                forfait_pose=forfait_pose
            )
            
            # Vérifier que le fichier a été créé
            if not os.path.exists(output_path):
                raise HTTPException(status_code=500, detail="Le fichier PDF n'a pas pu être généré")
            
            # Combiner avec les conditions générales de vente
            conditions_generales_path = "Conditions_Generales_FENETRE_SUR_LE_MONDE.pdf"
            if os.path.exists(conditions_generales_path):
                print("📄 Ajout des conditions générales de vente...")
                # Nom du fichier complet avec client et date
                combined_filename = f"devis_complet_{client_clean}_{date_for_filename}.pdf"
                combined_output_path = os.path.join(temp_dir, combined_filename)
                
                try:
                    import fitz  # PyMuPDF
                    
                    # Créer un nouveau document combiné
                    combined_doc = fitz.open()
                    
                    # Ouvrir et ajouter le devis généré
                    with fitz.open(output_path) as devis_doc:
                        combined_doc.insert_pdf(devis_doc)
                    
                    # Ouvrir et ajouter les conditions générales
                    with fitz.open(conditions_generales_path) as conditions_doc:
                        combined_doc.insert_pdf(conditions_doc)
                    
                    # Sauvegarder le document combiné
                    combined_doc.save(combined_output_path)
                    combined_doc.close()
                    
                    # Utiliser le fichier combiné
                    output_path = combined_output_path
                    output_filename = combined_filename
                    
                    print("✅ Conditions générales ajoutées avec succès")
                    
                except Exception as e:
                    print(f"⚠️ Erreur lors de l'ajout des conditions générales : {e}")
                    print("📄 Utilisation du devis sans conditions générales")
            else:
                print("⚠️ Fichier des conditions générales non trouvé, devis généré sans conditions")
            
            # Lire le fichier en mémoire avant que le dossier temporaire soit supprimé
            with open(output_path, "rb") as pdf_buffer:
                pdf_output = pdf_buffer.read()
            
            # Retourner le contenu du fichier directement
            return Response(
                content=pdf_output,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={output_filename}",
                    "Content-Length": str(len(pdf_output))
                }
            )
            
    except Exception as e:
        print(f"Erreur lors de la génération : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération : {str(e)}")

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

if __name__ == "__main__":
    # Configuration pour le développement local
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
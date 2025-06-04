"""
Point d'entrée principal pour le déploiement Render.
Importe l'application FastAPI depuis app.py
"""

from app import app

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
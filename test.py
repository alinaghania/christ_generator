#!/usr/bin/env python3
"""
Test simple avec le code officiel BFL exact
"""

import os
import base64
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_bfl_finetune():
    """Test avec le code exact de BFL"""
    
    # Paramètres
    zip_path = "christian.zip"
    finetune_comment = "Test Christian portraits"
    trigger_word = "christian_ton_1234"
    mode = "character"
    api_key = os.environ.get("BFL_API_KEY")
    
    print(f"🧪 Test BFL Fine-tuning")
    print(f"   - Fichier: {zip_path}")
    print(f"   - API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'MISSING'}")
    
    if not api_key:
        print("❌ BFL_API_KEY manquante dans .env")
        return
    
    if not os.path.exists(zip_path):
        print(f"❌ Fichier {zip_path} non trouvé")
        return
    
    # CODE EXACT DE BFL (copié du document officiel)
    with open(zip_path, "rb") as file:
        encoded_zip = base64.b64encode(file.read()).decode("utf-8")
    
    url = "https://api.us1.bfl.ai/v1/finetune"
    headers = {
        "Content-Type": "application/json",
        "X-Key": api_key,
    }
    payload = {
        "finetune_comment": finetune_comment,
        "trigger_word": trigger_word,
        "file_data": encoded_zip,
        "iterations": 300,
        "mode": mode,
        "learning_rate": 0.00001,
        "captioning": True,
        "priority": "quality",
        "lora_rank": 32,
        "finetune_type": "full",
    }
    
    print(f"🚀 Envoi de la requête...")
    print(f"   - URL: {url}")
    print(f"   - Headers: {headers}")
    print(f"   - Payload keys: {list(payload.keys())}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"📡 Réponse:")
    print(f"   - Status: {response.status_code}")
    print(f"   - Headers: {dict(response.headers)}")
    print(f"   - Body: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Succès! ID: {result.get('id')}")
        return result
    else:
        print(f"❌ Erreur {response.status_code}")
        try:
            error_detail = response.json()
            print(f"   - Détail: {error_detail}")
        except:
            print(f"   - Raw: {response.text}")
        return None

if __name__ == "__main__":
    test_bfl_finetune()
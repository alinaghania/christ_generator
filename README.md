📊 COMPARAISON DES ENDPOINTS FINETUNED :
1. 🥇 /flux-pro-1.1-ultra-finetuned (NOTRE CHOIX)

Modèle : FLUX 1.1 Pro Ultra (le plus récent/puissant)
Résolution : 4x (jusqu'à 4MP)
Vitesse : <10 secondes
Modes : Ultra + Raw disponibles
Usage : Text-to-image avec votre modèle Christian
Qualité : 🏆 MAXIMALE

2. 🥈 /flux-pro-finetuned (Version standard)

Modèle : FLUX Pro 1.0 (ancien)
Résolution : Standard (1MP)
Vitesse : ~15-20 secondes
Usage : Text-to-image basique avec fine-tune
Qualité : Bonne mais dépassée

3. 🔧 /flux-pro-1.0-depth-finetuned (Contrôle de profondeur)

Spécialité : Génération avec contrôle de la profondeur/structure
Input : Prompt + image de depth map
Usage : Respecter la structure 3D d'une image de référence
Exemple : "Transforme cette pose en Christian"

4. 🎨 /flux-pro-1.0-canny-finetuned (Contrôle des contours)

Spécialité : Génération avec détection des contours
Input : Prompt + image Canny (contours)
Usage : Respecter les contours/formes d'une image
Exemple : "Christian dans cette pose exacte"

5. 🖼️ /flux-pro-1.0-fill-finetuned (Inpainting/Outpainting)

Spécialité : Remplir/étendre des zones d'image
Input : Prompt + image + masque
Usage : Compléter/modifier des parties d'image
Exemple : "Remplace le fond par Christian"


(venv) (base) alina.ghani@AMALQH0F43CY3 FINETUNE-FLUX % curl --request GET \
  --url 'https://api.us1.bfl.ai/v1/get_result?id=17547232-bbdf-409b-91c9-a8a510286857' \
  --header 'X-Key: ea0de23e-18a1-4a64-9673-f73c860c15bd'
{"id":"17547232-bbdf-409b-91c9-a8a510286857","status":"Ready","result":{"finetune_id":"17547232-bbdf-409b-91c9-a8a510286857"},"progress":null,"details":null}%                 


````
curl --request POST \
  --url 'https://api.us1.bfl.ai/v1/flux-pro-1.1-ultra-finetuned' \
  --header 'Content-Type: application/json' \
  --header 'X-Key: ea0de23e-18a1-4a64-9673-f73c860c15bd' \
  --data '{
    "prompt": "christian, professional portrait, natural lighting, confident expression",
    "finetune_id": "17547232-bbdf-409b-91c9-a8a510286857",
    "finetune_strength": 1.2,
    "width": 1024,
    "height": 1024,
    "raw": true
  }'


````



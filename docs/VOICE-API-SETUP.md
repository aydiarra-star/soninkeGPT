# Backend vocal SoninkeGPT (première étape)

Cette API ajoute la reconnaissance vocale serveur sans remplacer le corpus, les audios historiques ni le moteur de réponse existant.

## Ce qui est livré

- `GET /health` : vérification de disponibilité.
- `POST /api/process-voice` : reçoit un fichier audio et retourne une transcription.
- La clé fournisseur reste côté serveur dans `OPENAI_API_KEY`.
- Le frontend utilise la transcription comme texte utilisateur ; la réponse reste produite par le moteur linguistique local et les audios validés continuent d'être prioritaires.

**Limite linguistique :** la reconnaissance automatique du soninké n'est pas garantie. Le prompt fournit quelques termes comme indices, mais ne rend pas le modèle fiable par magie. L'utilisateur doit pouvoir corriger la transcription avant envoi. La synthèse vocale de phrases nouvelles n'est pas activée par cette première étape.

## Déploiement Render

1. Ouvrir le dépôt GitHub `aydiarra-star/soninkeGPT` dans Render et choisir le blueprint `render.yaml`.
2. Créer le service `soninkegpt-voice-api`.
3. Dans les variables d'environnement du service, renseigner `OPENAI_API_KEY` avec une clé valide. Ne jamais mettre cette clé dans `app.js`, `index.html` ou un fichier public.
4. Attendre que le service soit disponible puis vérifier `https://<URL-DU-SERVICE>/health`.
5. Copier l'URL HTTPS attribuée par Render dans `voice-config.js` sous la forme `window.SONINKEGPT_API_BASE = "https://<URL-DU-SERVICE>";`, puis valider ce changement dans GitHub.
6. Vérifier le microphone sur le site publié et tester d'abord une phrase française, puis une phrase soninkée courte. Corriger la transcription avant l'envoi si nécessaire.

Le domaine du service Render n'est pas connu avant sa création ; aucune URL de service fictive n'est préconfigurée.

## Tester en local

Depuis le dossier `voice_api` :

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="votre-clé"
uvicorn main:app --reload --port 8000
```

Puis envoyer un fichier audio à `POST http://127.0.0.1:8000/api/process-voice` avec le champ multipart `file`.

## Sécurité et coûts

- Les enregistrements sont traités en mémoire et ne sont pas enregistrés sur disque par cette API.
- L'API externe de transcription peut facturer l'utilisation selon le compte fournisseur.
- La limite par défaut est de 20 Mo par enregistrement.
- Le service de production doit être configuré avec des limites de débit et un suivi d'utilisation avant une diffusion publique importante.

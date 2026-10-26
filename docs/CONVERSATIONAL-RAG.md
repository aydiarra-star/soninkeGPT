# Architecture conversationnelle — SoninkeGPT

## État vérifié de l'implémentation

Le dépôt utilise une interface statique (HTML/CSS/JavaScript) et un service FastAPI existant sous `voice_api/`. Le service Render `soninkegpt-voice-api` déploie la branche `main`; cette branche de travail n'est donc pas en production tant qu'elle n'est pas fusionnée et déployée.

Dans cette branche `feature/conversational-rag-foundation` :
- `POST /api/chat` est ajouté à `voice_api/main.py`.
- Les trois modes `translation_vocabulary`, `culture_history` et `general` sont validés par le schéma d'entrée.
- L'historique, le message et le contexte fourni par le corpus sont limités en taille.
- Les clés restent côté serveur.
- Des tests de contrat sont ajoutés dans `voice_api/tests/test_chat.py`.

**Limite essentielle :** l'interface n'appelle pas encore `/api/chat`. Le endpoint ne recherche pas lui-même le lexique du navigateur : le client doit lui transmettre le contexte récupéré et les références réelles. Il ne s'agit donc pas encore d'un RAG complet ni d'une fonctionnalité activée dans l'application publique.

## Modes

1. **Traduction & Vocabulaire** — le contexte du corpus est prioritaire. Les formes non confirmées doivent rester signalées. Sans contexte, le service prévient que les formes ne sont pas validées.
2. **Culture & Histoire** — sépare les informations appuyées par le contexte des connaissances incertaines ; les références ne doivent jamais être inventées.
3. **Assistant général** — réponses générales, sans présenter une forme soninkée non vérifiée comme attestée.

## Contrat API actuellement ajouté

`POST /api/chat`

Exemple de requête :
```json
{
  "message": "Que signifie cette forme ?",
  "mode": "translation_vocabulary",
  "history": [{"role": "user", "content": "Question précédente"}],
  "corpus_context": "Entrée, traduction, provenance et statut issus du corpus local",
  "sources": [{"title": "Corpus local", "id": "identifiant-de-la-source"}]
}
```

Le champ `corpus_context` doit provenir d'une recherche réelle côté client ou d'un service de récupération ajouté ultérieurement. Les champs `sources` doivent désigner des sources effectivement consultées. Les transmettre arbitrairement ne rend pas la recherche réelle.

Réponse : `answer`, `mode`, `sources`, `corpus_context_used`, `degraded` et `warning`.

## Pipeline à terminer

1. Ajouter dans l'interface un sélecteur de mode accessible.
2. Rechercher dans le lexique et les phrases attestées du corpus déjà chargé.
3. Transmettre au backend les résultats pertinents, leur statut, leur provenance et les références réelles.
4. Afficher les sources et statuts dans les réponses, sans modifier les fonctions vocales ni les favoris.
5. N'ajouter Supabase/pgvector ou une recherche externe qu'après configuration explicite, vérification des licences et tests de repli.
6. Tester les trois modes, les champs invalides, les erreurs du fournisseur et l'absence de clé API.
7. Vérifier l'expérience mobile, la confidentialité, les quotas et les contrôles d'accès avant l'ouverture publique.

## Configuration et sécurité

- Définir `OPENAI_API_KEY` côté serveur et, si nécessaire, `OPENAI_CHAT_MODEL`. Ne jamais exposer ces variables au navigateur.
- `OPENAI_TRANSCRIPTION_MODEL` reste utilisé pour la transcription vocale.
- Les requêtes sont bornées par `MAX_CHAT_MESSAGE_CHARS`, `MAX_CHAT_HISTORY_MESSAGES` et `MAX_CORPUS_CONTEXT_CHARS`.
- Le service ne doit pas journaliser le contenu des conversations ou des secrets.
- Avant la production, ajouter quotas/rate limiting et une protection contre les abus. L'endpoint actuel ne remplace pas ces contrôles.

## Validation

Commandes à exécuter depuis `voice_api/` :
```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Ces tests vérifient le contrat HTTP et les appels simulés au fournisseur ; ils ne prouvent pas que la clé API, le réseau ou le fournisseur distant fonctionnent réellement. La branche doit passer les tests avant fusion et déploiement.

## Hors périmètre actuel

Aucune migration vers Next.js, aucun entraînement de modèle, aucun embedding ou index pgvector, aucune connexion Supabase et aucune recherche Web ne sont implémentés par ce changement. La priorité est d'intégrer le endpoint au frontend et de préserver l'intégrité du corpus soninké.

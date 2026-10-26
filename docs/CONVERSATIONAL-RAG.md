# Architecture conversationnelle — SoninkeGPT

## État vérifié de l'implémentation

Le dépôt utilise une interface statique (HTML/CSS/JavaScript) et un service FastAPI existant sous `voice_api/`. Le service Render `soninkegpt-voice-api` déploie la branche `main`; cette branche de travail n'est donc pas en production tant qu'elle n'est pas fusionnée et déployée.

Dans cette branche `feature/conversational-rag-foundation` :
- `POST /api/chat` est ajouté à `voice_api/main.py`.
- Les trois modes `translation_vocabulary`, `culture_history` et `general` sont validés par le schéma d'entrée.
- L'historique, le message et le contexte fourni par le corpus sont limités en taille.
- Les clés restent côté serveur.
- Des tests de contrat sont ajoutés dans `voice_api/tests/test_chat.py`.

**État actuel :** le frontend de cette branche appelle maintenant `/api/chat` pour les demandes explicatives, grammaticales et culturelles reconnues par des règles simples. Il construit un contexte borné à partir des entrées déjà chargées en mémoire, du livret d'expressions et des exemples locaux, en conservant le statut et la provenance lorsqu'ils existent. Les demandes ordinaires de traduction/vocabulaire restent sur le moteur local existant. Si l'API distante échoue, l'application revient au moteur local et l'indique. Le service Render public ne sert pas ce code tant que la branche n'est pas fusionnée puis déployée.

**Limites restantes :** la sélection du mode est heuristique, il n'y a pas encore de sélecteur de mode dans l'interface, et les références retournées par le backend ne sont pas encore affichées comme fiches de sources. Ce n'est pas un index sémantique complet : la récupération locale repose sur le recouvrement des mots de la demande avec les champs lexicaux chargés.

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

Le frontend de cette branche remplit `corpus_context` depuis les résultats locaux calculés à partir des entrées, expressions et exemples réellement chargés. Le contexte est tronqué à une taille bornée. Les champs `sources` sont des métadonnées des résultats récupérés ; l'interface n'affiche pas encore une liste de références consultables. Les transmettre ne remplace pas une évaluation de la qualité de récupération.

Réponse : `answer`, `mode`, `sources`, `corpus_context_used`, `degraded` et `warning`.

## Pipeline à terminer

1. Ajouter un sélecteur de mode accessible et explicite, si souhaité, en complément de la détection heuristique.
2. Améliorer la récupération locale au-delà du recouvrement lexical et mesurer la pertinence sur des questions de test.
3. Afficher les sources et statuts retournés par le backend, sans modifier les fonctions vocales ni les favoris.
4. Tester l'intégration frontend avec une API déployée, y compris le repli local lorsque le service est indisponible.
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

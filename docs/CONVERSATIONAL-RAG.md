# Architecture conversationnelle — SoninkeGPT

## Statut réel

Cette branche prépare l'intégration conversationnelle. Au moment de sa création, le dépôt `main` ne contient pas `docs/CONVERSATIONAL-RAG.md`, et les recherches dans le code n'ont pas permis de confirmer la présence d'un endpoint `/api/chat` ni d'une implémentation FastAPI. Ce document ne prétend donc pas que ces fonctions sont déjà opérationnelles.

La priorité est de préserver l'application actuelle, le lexique et les enregistrements audio validés. Toute intégration doit être adaptée aux fichiers réellement présents après inspection du dépôt.

## Objectifs fonctionnels

1. **Traduction & Vocabulaire** — donner la priorité aux phrases et entrées attestées du corpus SoninkeGPT. Préserver graphies, variantes, sens multiples, exemples, provenance et statut de validation. Signaler les assemblages indicatifs et ne pas présenter une phrase construite comme attestée.
2. **Culture & Histoire** — fournir des explications contextualisées et distinguer les faits sourcés des hypothèses.
3. **Assistant général** — conversation générale avec indication explicite de l'incertitude.
4. **Voix** — réutiliser les fichiers audio du corpus et leurs métadonnées de validation ; ne jamais remplacer un enregistrement validé par une synthèse non approuvée.
5. **Références** — retourner les sources consultées lorsque des services de recherche externes sont utilisés.

## Pipeline proposé

1. Valider et normaliser la requête et le mode choisi.
2. Chercher d'abord dans le lexique et les phrases locales.
3. Si Supabase/pgvector est configuré, lancer une recherche sémantique sur les données dont la provenance et les droits sont connus.
4. En mode culture ou assistant général, consulter des fournisseurs externes uniquement s'ils sont configurés.
5. Générer une réponse à partir des éléments récupérés, en conservant les statuts linguistiques et les références.
6. Si un fournisseur échoue, répondre à partir des données locales lorsque possible et signaler la limite ; ne jamais inventer une source ni un résultat de recherche.
7. Journaliser les métadonnées minimales nécessaires au diagnostic, sans enregistrer inutilement les conversations ou secrets.

## Contrat API proposé

`POST /api/chat`

Requête JSON :
- `message` : texte non vide.
- `mode` : `translation_vocabulary`, `culture_history` ou `general`.
- `history` : historique borné et validé côté serveur, facultatif.

Réponse JSON :
- `answer` : texte de réponse.
- `mode` : mode retenu.
- `sources` : liste de références consultées, éventuellement vide.
- `linguistic_status` : statut(s) des formes soninké affichées.
- `degraded` : indique qu'un fournisseur optionnel était indisponible.

Ce contrat est une proposition et ne doit être considéré comme actif qu'après implémentation et tests.

## Configuration et sécurité

- Les clés des fournisseurs doivent rester côté serveur, dans les variables d'environnement ; jamais dans le JavaScript livré au navigateur.
- Supabase et les fournisseurs de recherche sont facultatifs. L'application doit fonctionner avec la recherche locale sans eux.
- Appliquer une limite de taille à la requête et à l'historique, des délais d'attente, une gestion explicite des erreurs, des quotas et une protection d'accès avant ouverture publique.
- Ne jamais inclure de clé API, jeton, URL de connexion contenant un secret ou donnée personnelle dans les journaux.
- Les données externes ne doivent être importées qu'après vérification de la provenance et des droits de réutilisation.

## Plan de livraison et critères de validation

- [ ] Inspecter les points d'entrée réels du backend et de l'interface avant de choisir les fichiers à modifier.
- [ ] Implémenter le contrat API dans le framework déjà utilisé par le dépôt.
- [ ] Tester les trois modes, les champs invalides, l'historique trop long et l'absence de configuration externe.
- [ ] Tester l'échec de chaque fournisseur optionnel et vérifier que le repli local fonctionne.
- [ ] Vérifier que le lexique, les favoris, les fonctions micro/audio et les statuts de validation restent inchangés.
- [ ] Exécuter la suite de tests du dépôt et documenter les résultats observés.
- [ ] Configurer secrets, quotas et authentification avant le déploiement public.

## Limites connues

Aucune migration de framework, génération d'embeddings, migration pgvector, connexion réelle à un fournisseur externe ni modification de production n'est attestée par ce document. Ces étapes nécessitent une implémentation et des vérifications séparées.

# Protection du patrimoine SoninkeGPT : droits, provenance et sauvegardes

Dernière mise à jour : 2026-10-25

> **Document de gouvernance, pas un avis juridique.** Il consigne les précautions et les points à vérifier. Il ne crée aucun droit sur les ressources de tiers et ne remplace pas une autorisation écrite.

## 1. Règle essentielle : distinguer logiciel, données et enregistrements

Le fichier `/LICENSE` contient une licence MIT pour le logiciel. **Ne pas présenter cette licence comme couvrant automatiquement le dictionnaire, les traductions, les corpus, les audios, les polices ou les ressources de tiers.** Chaque élément conserve sa provenance et sa licence propre.

Le code original, les outils de validation, les scripts, les schémas, les annotations originales et les enregistrements produits par l'équipe doivent être inventoriés séparément. Leur titulaire exact et les conditions applicables doivent être documentés, notamment lorsque des contributeurs ou des services tiers ont participé.

## 2. Règles de publication jusqu'à confirmation des droits

- Ne pas importer davantage de contenu substantiel du dictionnaire SIL/IPS dans les artefacts publics ou commerciaux tant que le titulaire et les conditions de réutilisation ne sont pas établis.
- Ne pas déclarer que SIL/IPS a autorisé SoninkeGPT sans accord écrit ou licence applicable retrouvée et archivée.
- Ne pas supprimer les données existantes à titre préventif : préserver les commits, les fichiers, les audios et leurs manifestes. Si une ressource doit être retirée de la diffusion publique, préparer une migration contrôlée, avec inventaire, sauvegarde et tests, plutôt qu'une suppression improvisée.
- La validation linguistique par un référent confirme la forme linguistique selon ce référent ; elle ne prouve ni la propriété des données ni l'autorisation de redistribution de la source.
- Conserver les citations, les identifiants de source, les dates, les lignes/entrées d'origine, les variantes, les traductions et le statut de validation. Ne pas effacer les variantes ou les sens multiples pour dédupliquer.
- Les données dont la licence est inconnue ne doivent pas être présentées comme « libres », « propriété de SoninkeGPT » ou « autorisées à un usage commercial ».

## 3. Dossier SIL/IPS : autorisation à obtenir

Source utilisée dans les audits L–Y : https://media.ipsapps.org/snk/oda/index-french/index.htm

La consultation publique d'un dictionnaire n'établit pas, à elle seule, une permission de copier, d'extraire systématiquement, de republier, d'intégrer dans une application, d'utiliser pour entraîner un modèle ou de commercialiser le contenu. La licence d'un logiciel SIL n'est pas automatiquement celle des données lexicales qui y sont affichées.

Avant de réutiliser le contenu SIL/IPS dans une version distribuée, obtenir une réponse écrite du détenteur des droits précisant :
1. le titulaire et l'édition exacte du dictionnaire ;
2. les droits de reproduction, extraction, adaptation et redistribution des entrées, définitions, exemples, prononciations et médias ;
3. l'autorisation d'intégration dans un service web/app et dans un assistant IA ;
4. l'usage commercial, les abonnements et la monétisation éventuelle ;
5. les territoires, la durée, les obligations d'attribution et la possibilité de redistribuer les exports ;
6. la licence exacte et la personne habilitée à accorder l'autorisation.

Archiver l'URL, une copie datée des conditions/licences, les courriels d'autorisation et les limites convenues. En l'absence de réponse, le statut reste **À CLARIFIER — NE PAS CONSIDÉRER COMME AUTORISÉ POUR REDISTRIBUTION OU USAGE COMMERCIAL**.

## 4. Registre de provenance

Le fichier `data/source/registre-provenance-licences.csv` est le registre de suivi. Toute nouvelle source doit y être ajoutée avant intégration. Chaque ligne doit indiquer le propriétaire/source, la licence exacte et son URL, les permissions connues, les obligations d'attribution, le statut de vérification et les restrictions.

Statuts autorisés :
- `CONFIRMEE` : licence ou permission écrite consultée et archivée ;
- `PARTIELLE` : certains usages seulement sont autorisés ;
- `A_CLARIFIER` : licence/titulaire/périmètre non établi ;
- `INTERNE_A_DOCUMENTER` : travail produit pour le projet mais auteurs/conditions à consigner ;
- `NON_AUTORISE_POUR_PUBLICATION` : ne pas distribuer tant que la situation n'est pas résolue.

## 5. Sauvegardes et prévention de la casse

- GitHub est l'historique de développement, mais ne doit pas être l'unique sauvegarde.
- Maintenir au moins une archive complète indépendante du compte GitHub, incluant le code, les fichiers de données autorisés, les audios, les manifestes, les rapports, les scripts et l'historique Git.
- Garder deux copies de sauvegarde distinctes, dont une hors ligne ou sous un compte séparé ; vérifier périodiquement les archives en les ouvrant et en comparant les sommes SHA-256.
- Avant chaque migration du lexique : exporter la base complète, compter les entrées, contrôler les doublons/IDs, vérifier que tous les chemins d'audio référencés existent, comparer le diff et tester la recherche/traduction avant de fusionner.
- Ne jamais remplacer le lexique canonique par un export partiel ou un fichier récupéré de manière incomplète. Une importation doit être additive ou faire l'objet d'une comparaison explicite, avec possibilité de retour arrière.
- Conserver les fichiers audio et leurs manifestes comme artefacts distincts ; aucune régénération ne doit écraser un audio déjà validé sans sauvegarde et autorisation explicite.
- Préparer une version de référence datée et, lorsque l'inventaire est fiable, une archive de release avec somme de contrôle. Une archive GitHub ne remplace pas une sauvegarde indépendante.
- Enregistrer les décisions de validation linguistique séparément de la validation technique et des droits de redistribution.

## 6. Protection de l'antériorité

Conserver les commits Git, les PR, les rapports de validation, les journaux de génération et les exports datés. Pour les éléments originaux importants (corpus créé, structure, scripts, audios et documentation), envisager un dépôt e-Soleau auprès de l'INPI et/ou un accompagnement juridique. Un dépôt de preuve date un contenu ; il ne confère pas, à lui seul, de droits sur le contenu d'un tiers.

## 7. Contrôle avant une publication ou une monétisation

- [ ] Les licences et autorisations sont archivées pour chaque source substantielle.
- [ ] Les attributions exigées sont affichées.
- [ ] Les données sous licence inconnue sont isolées de l'export public/commercial, sans destruction de l'archive interne.
- [ ] Les droits sur les voix/enregistrements, les outils TTS/STT, les modèles et les voix de synthèse sont vérifiés.
- [ ] Le fichier de licence du logiciel ne prétend pas couvrir les données.
- [ ] L'archive indépendante est créée et son intégrité vérifiée.
- [ ] Les tests, le diff et le plan de retour arrière sont prêts.

## Références de départ

- Dictionnaire consulté : https://media.ipsapps.org/snk/oda/index-french/index.htm
- Licence de Dictionary App Builder (SIL) : https://software.sil.org/fr/dictionaryappbuilder/license/ — elle précise que l'utilisateur doit posséder les données ou avoir l'autorisation de les distribuer.
- INPI, droit d'auteur et preuve de création : https://www.inpi.fr/ressources/propriete-intellectuelle/droit-dauteur
- INPI, préparation d'un dépôt e-Soleau : https://www.inpi.fr/realiser-demarches/propriete-intellectuelle/se-preparer-au-depot-dune-e-soleau
- Commission européenne, protection des bases de données : https://digital-strategy.ec.europa.eu/fr/policies/protection-databases

# CLAUDE.md

Ce dépôt (`yaya`) est une base de connaissances sur **SIXT** (Sixt SE) : contexte d'entreprise, offres, stratégie de croissance et guide de style. Il ne contient pas de code applicatif (pas de build, de lint ni de tests). Le travail consiste à lire, synthétiser et rédiger du contenu en s'appuyant sur les documents de `docs/sixt/`.

## Documents de référence

Lire le fichier pertinent avant de répondre ou de rédiger. Ne pas répondre de mémoire sur SIXT.

| Fichier | Contenu | À consulter pour |
|---|---|---|
| `docs/sixt/SIXT_Contexte_Complet.md` | Identité, gouvernance, actionnariat, chiffres 2025 et S1 2026, financement, concurrence, risques | Chiffres financiers, gouvernance, bourse, guidance |
| `docs/sixt/SIXT_Offres_Produits_et_Strategie_Commerciale.md` | Les 11 produits (rent, van & truck, SIXT+, share, ride, charge, ONE, Business, carhub, franchises), prix d'appel, canaux B2C/B2P/B2B, partenariats | Fiches produit, prix, messages par segment |
| `docs/sixt/SIXT_Strategie_Croissance_Marketing_et_Digital.md` | Piliers de l'Equity Story, parts de marché, digital, IA, unit economics, playbook de croissance | Stratégie, marketing, digital, KPI à suivre |
| `docs/sixt/SIXT_Style_Ton_et_Voix.md` | ADN de marque, règles d'écriture, gabarits, lexique, checklist, brief de prompt | Toute rédaction « à la manière de SIXT » |

Les quatre documents sont datés du **8 octobre 2026**. Prochaine publication financière : résultats T3 2026 le **12 novembre 2026**.

## Légende de fiabilité (à respecter dans toute réponse)

Les documents taguent chaque information. Reprendre ces tags quand on cite un chiffre.

- **[S]** source officielle SIXT (sites, rapport annuel 2025, communiqués, Equity Story)
- **[P]** presse ou site tiers rapportant une info SIXT
- **[A]** source secondaire ou analyse de l'auteur, à vérifier
- **[D]** donnée dérivée, calculée à partir de chiffres [S]
- **[I]** standards internes d'écriture SIXT (Confluence) ; en cas de conflit, ils priment sur le guide de style
- **[E]** exemple original écrit « à la manière de SIXT », non officiel
- **[U]** document fourni par l'utilisateur

Règles :
- Ne jamais présenter un chiffre [A], [D] ou [P] comme officiel.
- Ne pas inventer ce que les documents déclarent non public (part du canal direct, coût d'acquisition, budgets par canal).
- Les prix sont des photographies datées, parfois d'un autre pays (Allemagne, Royaume-Uni). Les signaler comme tels.
- Si deux documents divergent, le dire plutôt que choisir en silence (exemples connus : 27 % vs 28 % de notoriété aux États-Unis ; 72 % vs 73 % de CA retail ; 222 000 véhicules annoncés vs 365 900 en flotte moyenne avec franchises).

## Faits à ne pas se tromper

- Entité : **Sixt SE**, siège à Pullach (Munich), SDAX, famille Sixt = 58,3 % des droits de vote. Fondée en 1912.
- Direction : co-CEO Alexander Sixt et Konstantin Sixt ; CFO Dr Franz Weinberger.
- 13 pays corporate, environ 100 marchés en franchise, plus de 2 300 agences (juin 2026).
- 2025 : CA 4 283 M€, EBT 400,5 M€ (marge 9,4 %). S1 2026 : CA 2 118,2 M€, EBT 125,1 M€. Guidance 2026 : CA 4,45 à 4,60 Md€, marge EBT environ 10 %.
- Signature de marque : « Bold, Fun, Premium » ; promesse « premium à un prix qu'on aime ».
- Les documents ne comparent pas SIXT à d'autres loueurs, hors le point de vigilance signalé. Ne pas ajouter de comparaisons concurrentielles non demandées.

## Règles de rédaction (français, ton SIXT)

Synthèse de `SIXT_Style_Ton_et_Voix.md`. Le guide complet fait foi.

- Français, **vouvoiement** par défaut (tutoiement uniquement si demandé pour un canal social jeune).
- Conversationnel, voix active, phrases courtes. **Bénéfice dans les 5 à 7 premiers mots.**
- Une seule action (CTA) par texte ; le bouton dit ce que le client obtient (« Voir les offres », pas « Rechercher »).
- **Pas de tirets longs** (« — » ou « – ») dans les textes destinés à SIXT : remplacer par un point, une virgule ou deux-points.
- Casse de phrase. Pas de titres ni de boutons en majuscules.
- Pas de remplissage : *simple, facile, rapide, fluide, sans souci, large gamme*. Pas de jargon d'assurance (LDW, CDW).
- Pas de ton administratif (*veuillez, afin de*), pas d'alarmisme (*Important :*), pas de « Félicitations ! » creux.
- Ne jamais accuser le client. S'excuser uniquement si l'erreur vient de SIXT.
- Humour permis (confirmations, états vides, réseaux sociaux), jamais au milieu d'une tâche ni au détriment de la clarté.
- Sujets interdits : politique et personnalités nommées, religion, accidents, sexualité explicite, discrimination, témoignages ou athlètes sans accord.
- **B2B : pas d'upsell.** B2C : upsell possible. B2P : pas d'upsell avant la location.
- Réseaux sociaux : titre-choc très court, chute dans le petit texte, lien produit.

### Noms de produits (jamais traduits, casse exacte)

`SIXT rent`, `SIXT share`, `SIXT ride`, `SIXT+`, `SIXT van & truck`, `SIXT charge`, `SIXT carhub`, `SIXT Business`, `SIXT unlimited`, et **`SIXT ONE`** (seule exception, tout en majuscules). Erreurs à corriger : « SIXT Ride », « SIXT one », « Sixt rent ».

### Identité visuelle

Orange `#FF5000` (l'ancien `#FF5F00` n'est plus utilisé), noir `#1A1A1A`, blanc `#FFFFFF`. L'orange est le seul accent de marque. Police HelveticaNow (repli Helvetica, Roboto, Arial).

## Conventions pour ce dépôt

- Les documents de `docs/sixt/` sont des sources : ne les modifier que sur demande explicite, et conserver la légende de fiabilité.
- Tout nouveau document de synthèse suit le même format : objectif, légende des tags, limites, sections numérotées, chiffres avec tags, section « À vérifier », sources, date de génération.
- Textes rédigés « à la manière de SIXT » : les marquer [E] et rappeler qu'ils sont à valider avant publication (promesses factuelles, délais, mentions légales).
- Écrire en français, sauf demande contraire.

## Git

- Développer sur la branche `claude/fichier-claude-mmd-mtcmp6`.
- Ne pas créer de pull request sans demande explicite.

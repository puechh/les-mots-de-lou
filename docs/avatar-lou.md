# Avatar de Lou : méthode pour un visage unique, réaliste et constant (02/11/2026)

## En bref
- **Visage gardé : la version C** (rousse, chignon bas, yeux gris-bleu, ≈ 28 ans). Aucun test n'a donné de visage nettement plus
  réaliste. En revanche, **le rendu de la peau a été nettement amélioré** (taches de rousseur, pores, rougeurs, sans effet lissé).
- **Méthode retenue (gratuite en plus de l'existant) : OpenAI `gpt-image-2.5-flare` en mode « retouche »** (endpoint d'édition),
  en envoyant **toujours 2 images de référence** : `contenu/lou/reference/01-face.png` (+ une 2e de la planche selon l'angle voulu).
  Résultat : même visage sur face, trois-quarts, profil et sourire. ≈ 11-15 s par image en qualité medium, **sans erreur 502**.
- **Planche de référence validée par Claude (à faire valider par l'utilisateur)** : `contenu/lou/reference/`
  (`planche-lou.jpg` = les 5 images côte à côte ; chaque image a son prompt dans un `.txt`).
- Plan B / vidéos : clé **fal.ai** (une clé pour Kling, Veo, Flux, Nano Banana, entraînement LoRA). Voir plus bas.

## Tests réalisés (8 images, qualité medium)
Même prompt « photo iPhone prise par une amie, peau non retouchée » à partir de `reference-visage.png` (dossier `contenu/lou/essais/`) :

| Essai | Modèle | Visage gardé | Réalisme de la peau | Temps |
|---|---|---|---|---|
| 01 | gpt-image-2 | ✅ très fidèle | bon, encore un peu lisse | 26 s |
| 02 | **gpt-image-2.5-flare** | ✅ très fidèle | **le plus naturel** (taches de rousseur, rougeurs, décor crédible) | **11 s** |
| 03 | gpt-image-2.5-sunburst | ✅ très fidèle | très bon, proche de flare | 16 s |

Puis planche (5 images) avec flare, références = essai 02 + `reference-visage.png` : `01-face`, `02-trois-quarts`, `03-profil`,
`04-sourire`, `05-mains`. Toutes cohérentes. Limites : le « profil » est un trois-quarts très tourné (pas un profil strict) ; les
mains n'ont volontairement pas de bijou (on ajoutera le vrai bijou à partir de la photo fournisseur, sans le modifier).

Leçons techniques :
- `gpt-image-2` / `2.5` **n'acceptent pas** le paramètre `input_fidelity` (erreur 400) : la fidélité est déjà élevée par défaut.
- Mots qui aident le réalisme : « candid photo taken on an iPhone », « unretouched skin, visible pores, peach fuzz, faint freckles,
  slight redness, natural asymmetry », « no beauty filter, no airbrushing, no plastic skin », « slight sensor grain », lumière de fenêtre.
- **Toujours repartir des images de la planche** (jamais d'une image elle-même dérivée de dérivée), sinon le visage dérive peu à peu.
- Outil : `python3 contenu/lou/generer_lou.py modifier "<prompt>" contenu/lou/reference/01-face.png contenu/lou/reference/02-trois-quarts.png --nom <nom> --dossier <dossier> --modele gpt-image-2.5-flare --fidelite aucune`
  (attente de 10 min, nouvel essai automatique en cas de 502). Pour les images de la boutique, ranger la sortie selon les règles
  de la session principale.

Modèle de prompt pour une scène :
> The exact same woman as in the reference photos (Lou, fictional character): same face shape, same nose, same lips, same
> blue-grey eyes, same eyebrows, same faint freckles, same copper auburn hair in a loose low messy bun. [SCÈNE]. Candid photo taken
> on an iPhone, natural daylight, realistic unretouched skin, visible pores, faint freckles, no beauty filter, no plastic skin,
> slight sensor grain, true-to-life colors. No text, no watermark.

## Recherche web (nov. 2026) : résumé
Prix indicatifs, souvent tirés de revendeurs/blogs (à vérifier avant de payer). Sources détaillées en bas.

| Outil | Points forts | Prix indicatif | Accès depuis notre environnement |
|---|---|---|---|
| **OpenAI gpt-image-2 / 2.5** (2.5 sorti le 08/09/2026) | Très bon réalisme, bonne fidélité avec références | ≈ 0,01-0,2 $/image | ✅ **déjà connecté** |
| Google Nano Banana Pro / Nano Banana 2 | Souvent cité n° 1 pour garder un visage | 0,07-0,13 $/image | clé Google AI Studio (`generativelanguage.googleapis.com`) |
| Flux.2 (Black Forest Labs) | Très réaliste, multi-référence, meilleure base pour un LoRA | ≈ 0,03-0,07 $/image | `api.bfl.ai` ou fal.ai |
| Seedream 5.0 (ByteDance) | Jusqu'à 14 références | ≈ 0,03-0,07 $/image | via fal.ai |
| Midjourney v8 | Très esthétique | abonnement ≈ 10 $/mois | ❌ pas d'API officielle |
| Higgsfield (Soul ID) | Visage entraîné + vidéo, tout en interface web | 9-49 $/mois | site web (hors conteneur) |
| **LoRA Flux** (entraîné sur 15-30 images de Lou) | Le plus stable sur des centaines d'images | ≈ 2 $ l'entraînement | fal.ai / Replicate |
| Face swap | — | — | ❌ à éviter (rendu artificiel, risques juridiques) |

Vidéo (animer une photo de Lou) :
| Outil | Prix indicatif | Remarque |
|---|---|---|
| **Kling 3.0** | ≈ 0,08-0,22 $/s | bonne fidélité au visage de l'image de départ, via fal.ai |
| **Google Veo 3.1** Lite/Fast | ≈ 0,05-0,12 $/s | même clé que Nano Banana ; clip 8 s ≈ 1 $ |
| Seedance 2.0, Runway Gen-4.5 | ≈ 0,05-0,30 $/s | alternatives |
| HeyGen / Hedra | ≈ 3-4 $/min | seulement si Lou doit **parler** face caméra |
| OpenAI Sora 2 | — | ❌ refuse les visages humains en image de départ ; API annoncée fermée (sept. 2026), non vérifié |

## Recommandation
1. **Maintenant (0 € de plus)** : toutes les images de Lou avec `gpt-image-2.5-flare` + 2 images de la planche. Quelques euros
   pour 50 à 100 images.
2. **Pour les vidéos (≈ 10-15 € pour 10 clips de 5-8 s)** : créer un compte **fal.ai**, puis animer les photos de Lou avec
   **Kling 3.0** (ou Veo 3.1 Fast). Le même compte permet, si le visage dérive un jour, de tester Nano Banana Pro / Flux.2 ou
   d'entraîner un **LoRA** (≈ 2 $, avec 20 images validées de Lou).
3. **Plan B** : clé **Google AI Studio** (Nano Banana Pro pour les images + Veo pour la vidéo, une seule clé). Ou, pour cliquer
   sans API, Higgsfield (abonnement, en dehors de Claude).

## Ce que l'utilisateur doit faire (seulement pour la vidéo)
1. Créer un compte sur **fal.ai** → ajouter ≈ 10-20 € de crédit → menu **API Keys** → créer une clé (ne pas la coller dans le chat).
2. Sur claude.ai → environnement cloud **« Les Mots de Lou »** → paramètres → **Network secrets / domaines autorisés** : ajouter
   `fal.run`, `queue.fal.run` et `fal.media` (téléchargement des fichiers) avec la clé dans l'en-tête `Authorization` au format
   `Key <la clé>`. Puis ouvrir une nouvelle session.
3. Dire à Claude : « la clé fal est ajoutée, on fait les vidéos de Lou ».

## ⚖️ Rappels légaux
- Lou est **fictive** et ne doit ressembler à aucune personne réelle connue : visage créé de zéro par prompt, jamais à partir de
  la photo d'une vraie personne (pas de face swap).
- Contenus commerciaux montrant Lou : mention **« image virtuelle »** (loi n° 2023-451 art. 5 ; décret n° 2026-233 du 30/03/2026
  sur les modalités, **à vérifier sur Légifrance** → `docs/veille-legale.md`) + étiquettes IA des plateformes (Meta « Infos IA »,
  TikTok AIGC, Pinterest « AI modified »). **AI Act art. 50** applicable depuis le 02/08/2026 (obligation de signaler les
  « deepfakes » non repoussée). L'utilisateur ajoute ces mentions lui-même en publiant.
- Ne jamais faire croire que Lou existe, qu'elle fabrique les bijoux, ni lui faire « recommander » un produit comme une vraie cliente.
- Bijoux portés par Lou : partir des photos fournisseur, ne jamais changer forme, couleur, taille ou gravure.

## Sources
gpt-image-2.5 : jopr.org/news/detail/openai-launches-chatgpt-images-25 · eesel.ai/blog/chatgpt-images-2-5-pricing —
Nano Banana : benchlm.ai/media-pricing/nano-banana · apatero.com/blog/nano-banana-pro-vs-gpt-image-2-100-prompt-test —
Flux.2 : help.bfl.ai/articles/7686530342-flux-2-pricing-guide · fal.ai/models/fal-ai/flux-2-trainer-v2/edit —
Kling : aireiter.com/blog/kling-3-api-pricing-guide-2026 — Veo : benchlm.ai/media-pricing/veo —
Sora : community.openai.com/t/is-the-sora2-api-still-working/1379946 — Higgsfield : creatify.ai/blog/higgsfield-pricing-(2026)-plans-and-what-you-ll-actually-pay —
AI Act : cpduk.co.uk/news/deadline-moved-and-duty-did-not-ai-act-transparency-obligations-after-digital-omnibus —
Loi influenceurs : dalloz-actualite.fr/document/ord-n-2024-978-6-nov-2024-jo-7-nov —
Plateformes : auditsocials.com/blog/pinterest-ai-modified-ad-label-2026-iptc-metadata-synthetic-content-disclosure-advertiser-appeals ·
cinerads.com/blog/tiktok-ai-content-policy · commonthreadco.com/blogs/coachs-corner/meta-ai-ad-labels-mandatory-disclosure-ecommerce-2026

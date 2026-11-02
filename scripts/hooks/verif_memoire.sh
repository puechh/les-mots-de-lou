#!/usr/bin/env bash
# Hook Stop : empêche Claude de terminer tant que la mémoire du dépôt n'est pas sauvegardée sur GitHub.
cd "$(dirname "$0")/../.." || exit 0

# Deuxième passage après un blocage : on laisse finir pour éviter une boucle infinie
grep -q '"stop_hook_active" *: *true' && exit 0

modifs=$(git status --porcelain 2>/dev/null)
non_pousses=$(git rev-list --count '@{u}..HEAD' 2>/dev/null || echo 0)
[ -z "$modifs" ] && [ "$non_pousses" = "0" ] && exit 0

raison="Mémoire du dépôt pas à jour"
[ -n "$modifs" ] && raison="$raison : fichiers modifiés non commités ($(echo "$modifs" | wc -l | tr -d ' '))"
[ "$non_pousses" != "0" ] && raison="$raison : $non_pousses commit(s) non poussé(s)"
raison="$raison. Applique la règle « Mémoire » de CLAUDE.md : mets à jour docs/journal.md (et CLAUDE.md si le contexte a changé), lance python3 scripts/sauvegarde.py si la boutique a été modifiée, vérifie qu'aucun secret n'est inclus, puis commit et push sur main."
printf '{"decision":"block","reason":"%s"}\n' "$raison"

#!/bin/bash
# Pubblica il sito di RaceKart su GitHub Pages, e VERIFICA che sia arrivato tutto.
#
#   ./pubblica.sh
#
# ⚠️ **Non si carica a mano da «Add file → Upload files».** Su LookAt, il 14 ago 2026, quel
# trascinamento si è fermato a metà senza dire niente: 20 pagine su 39, e mancava anche `.nojekyll`
# perché il browser scarta i file che iniziano con un punto. Nessun errore a schermo, sito
# apparentemente online. Un push git o arriva tutto o fallisce dicendolo.
#
# ⚠️ **Questo repository contiene SOLO il sito.** `git init` gira dentro `website/`, che è una
# sottocartella: il gioco resta fuori, e RaceKart non è un repo git (vedi `CLAUDE.md`).
set -euo pipefail
cd "$(dirname "$0")"

# ⚠️ Maiuscole come le scrive GitHub: con `angelosassoit` il push funziona lo stesso ma risponde
# «This repository moved», perché il nome canonico dell'account è AngeloSassoIT. L'indirizzo del
# sito resta invece minuscolo nell'host — ma ⚠️ **il PERCORSO è sensibile alle maiuscole**:
# `/RaceKart/` e `/racekart/` non sono la stessa pagina, e gli URL scritti su App Store Connect
# usano la prima forma.
REPO="https://github.com/AngeloSassoIT/RaceKart.git"
RAMO="main"
SITO="https://angelosassoit.github.io/RaceKart"

command -v git >/dev/null || { echo "git non installato"; exit 1; }

# ── 1. il sito dev'essere quello rigenerato, non uno stato intermedio
python3 _sorgenti/genera-sito.py --base-url "$SITO"

# ⚠️ Senza `.nojekyll`, GitHub Pages passa il sito da Jekyll, che **ignora le cartelle che iniziano
# con un underscore**: `_sorgenti/` sparirebbe. Non è grave in sé, ma è la stessa regola che
# altrove fa sparire pagine vere.
touch .nojekyll

# ── 2. repository locale, allineato al remoto
if [ ! -d .git ]; then
  git init -b "$RAMO" >/dev/null
  git remote add origin "$REPO"
fi
git remote set-url origin "$REPO"

# `git reset` (mixed) porta HEAD e indice al commit remoto SENZA toccare i file: subito dopo,
# `git add -A` mette in stagione esattamente la differenza fra ciò che è online e ciò che c'è qui —
# file mancanti compresi.
git fetch origin "$RAMO" >/dev/null 2>&1 || true
git reset "origin/$RAMO" >/dev/null 2>&1 || true

git add -A
if git diff --cached --quiet; then
  echo "· niente da pubblicare: il repository è già allineato"
else
  git -c user.name="SimpleBuild" -c user.email="support@simplebuild.it" \
      commit -q -m "Sito RaceKart: privacy, assistenza e vetrina in sei localizzazioni"
  git push -u origin "$RAMO"
  echo "· push eseguito — GitHub Pages ricostruisce in un minuto circa"
fi

# ── 3. controllo vero: ogni pagina deve rispondere **ed essere quella nuova**
#
# ⚠️ **Non basta il 200.** Su LookAt il sito era già aggiornato e la CDN di GitHub Pages continuava
# a servire la versione precedente: tutte le pagine rispondevano 200 con dentro un testo appena
# tolto. Quindi si confronta l'impronta del file servito con quella del file locale, e la richiesta
# porta un parametro variabile per non ripescare la stessa cache.
echo "· attendo la ricostruzione di GitHub Pages…"
LINGUE=("" "en-us/" "it/" "es-es/" "fr/" "de/")
TOTALE=$(( ${#LINGUE[@]} * 3 ))
for tentativo in $(seq 1 12); do
  rotte=0; vecchie=0; ultima=""
  for L in "${LINGUE[@]}"; do
    for P in index privacy support; do
      atteso=$(shasum -a 256 "$L$P.html" | cut -d' ' -f1)
      servito=$(curl -s -m 20 -H "Cache-Control: no-cache" \
                "$SITO/$L$P.html?v=$(date +%s)$RANDOM" | shasum -a 256 | cut -d' ' -f1)
      c=$(curl -s -o /dev/null -w "%{http_code}" -m 20 "$SITO/$L$P.html" || echo 000)
      if [ "$c" != "200" ]; then
        rotte=$((rotte + 1)); ultima="$L$P.html (HTTP $c)"
      elif [ "$atteso" != "$servito" ]; then
        vecchie=$((vecchie + 1)); ultima="$L$P.html (versione vecchia)"
      fi
    done
  done
  if [ "$rotte" -eq 0 ] && [ "$vecchie" -eq 0 ]; then
    echo "✓ $TOTALE pagine su $TOTALE rispondono 200 e sono identiche ai file locali"
    break
  fi
  echo "  $rotte non servite · $vecchie non aggiornate (ultima: $ultima) — riprovo fra 30 s [$tentativo/12]"
  sleep 30
done

if [ $(( rotte + vecchie )) -ne 0 ]; then
  echo "⛔ mancano ancora $(( rotte + vecchie )) pagine su $TOTALE."
  echo "   Controlla Settings → Pages (ramo $RAMO, cartella /) e la scheda Actions del repo."
  exit 1
fi

echo
echo "Ora gli indirizzi si possono caricare sulla scheda App Store:"
echo "   cd ../AppStoreConnect_Resource"
echo "   ./prepara-deliver.sh --con-url && fastlane ios schede force:true && fastlane ios urls"

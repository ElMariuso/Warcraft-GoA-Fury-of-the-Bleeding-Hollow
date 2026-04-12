.PHONY: help install install-wiki test \
	lint lint-loc lint-effects lint-all lint-rules lint-loc-rules lint-effects-rules \
	tiger tiger-install \
	logs logs-errors logs-filter logs-level logs-start \
	watch watch-filter \
	dev dev-bh dev-horde dev-all dev-filter dev-trace \
	errors-bh errors-horde errors-clear \
	symbols generate inject \
	hansel

PYTHON := python

help:
	@echo "CK3 Mod — Outils Python"
	@echo ""
	@echo "Setup"
	@echo "  make install                         Installer les dépendances (pip)"
	@echo "  make install-wiki                    + navigateur Playwright (scraping wiki, ~130 MB)"
	@echo "  make test                            Lancer les tests pytest"
	@echo ""
	@echo "Référence (lire, chercher) — via ./hansel"
	@echo "  ./hansel doc <topic>                 Doc complète d'un topic (ex: triggers, lists)"
	@echo "  ./hansel doc                         Lister tous les topics disponibles"
	@echo "  ./hansel search <query>              Rechercher dans la doc CK3/Paradox"
	@echo "  make lint-rules                      Lister les règles events"
	@echo "  make lint-loc-rules                  Lister les règles localisation"
	@echo "  make lint-effects-rules              Lister les règles effects"
	@echo ""
	@echo "Écriture (générer, scaffolding)"
	@echo "  make generate T=hansel-tools/templates/event_unique.yaml  Générer stubs event"
	@echo "  make inject S='character:10005 = { add_prestige = 500 }'"
	@echo "  make symbols                         Extraire symbols.json depuis GoA2"
	@echo ""
	@echo "Validation (lint, tiger)"
	@echo "  make lint-all                        Tout linter (Python — rapide)"
	@echo "  make lint          [F=fichier.txt]   Events (.txt)"
	@echo "  make lint-loc      [F=fichier.yml]   Localisation (.yml)"
	@echo "  make lint-effects  [F=fichier.txt]   Scripted effects (.txt)"
	@echo "  make tiger                           Validation CK3 complète (scopes, refs, loc)"
	@echo "  make tiger-install                   Installer ck3-tiger (cargo)"
	@echo ""
	@echo "Runtime (surveiller le jeu)"
	@echo "  make dev-bh                          wc_bleeding_hollow seulement"
	@echo "  make dev-horde                       wc_horde_invasion seulement"
	@echo "  make dev                             Filtrer namespaces wc_* (défaut)"
	@echo "  make dev-trace                       Résumé des events wc_* déclenchés"
	@echo "  make dev-filter F=kilrogg            Regex custom sur game.log"
	@echo "  make dev-all                         Aucun filtre (tout game.log)"
	@echo ""
	@echo "Logs (accumuler, filtrer)"
	@echo "  make errors-bh                       wc_bleeding_hollow — accumule dans logs/errors-bh.log"
	@echo "  make errors-horde                    wc_horde_invasion  — accumule dans logs/errors-horde.log"
	@echo "  make errors-clear                    Vider les logs d'erreurs accumulés"
	@echo "  make logs                            Surveiller game.log en temps réel"
	@echo "  make logs-errors                     Erreurs seulement"
	@echo "  make logs-filter F=wc_bleeding       Filtrer par regex"
	@echo "  make logs-level L=WARN               Niveau minimum (DEBUG/INFO/WARN/ERROR)"

# ── Setup ────────────────────────────────────────────────────────────────────

install:
	$(PYTHON) -m pip install -r hansel-tools/requirements.txt
	chmod +x hansel

install-wiki:
	$(PYTHON) -m playwright install --with-deps chromium

test:
	$(PYTHON) -m pytest tests/ -v

# ── Dev watch unifié ─────────────────────────────────────────────────────────

dev:
	$(PYTHON) hansel-tools/watchers/dev_watch.py

dev-bh:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --namespace bh

dev-horde:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --namespace horde

dev-all:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --namespace all

dev-filter:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --filter "$(F)"

dev-trace:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --event-trace

# ── Accumulation d'erreurs (set persistant, sans doublons) ───────────────────

ERRORS_PATTERN := wc_bleeding_hollow|wc_horde_invasion|Fury|Bleeding

errors-bh:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --namespace bh 2>&1 | \
		$(PYTHON) hansel-tools/watchers/error_accumulator.py --out logs/errors-bh.log --pattern "$(ERRORS_PATTERN)"

errors-horde:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --namespace horde 2>&1 | \
		$(PYTHON) hansel-tools/watchers/error_accumulator.py --out logs/errors-horde.log --pattern "$(ERRORS_PATTERN)"

errors-clear:
	@rm -f logs/errors-bh.log logs/errors-horde.log
	@echo "Logs d'erreurs supprimés."

# ── Logs structurés (log_viewer) ─────────────────────────────────────────────

logs:
	$(PYTHON) hansel-tools/watchers/log_viewer.py

logs-errors:
	$(PYTHON) hansel-tools/watchers/log_viewer.py --errors-only

logs-filter:
	$(PYTHON) hansel-tools/watchers/log_viewer.py --filter "$(F)"

logs-level:
	$(PYTHON) hansel-tools/watchers/log_viewer.py --level "$(L)"

logs-start:
	$(PYTHON) hansel-tools/watchers/log_viewer.py --from-start

# ── Watch simple (watch_logs) ─────────────────────────────────────────────────

watch:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --namespace all

watch-filter:
	$(PYTHON) hansel-tools/watchers/dev_watch.py --filter "$(F)"

# ── Tiger ────────────────────────────────────────────────────────────────────
# Pré-requis : cargo install ck3-tiger
# Pré-requis : copier ck3-tiger.conf.example → ck3-tiger.conf et renseigner ck3-dir

tiger:
	ck3-tiger .

tiger-install:
	cargo install ck3-tiger

# ── Lint ─────────────────────────────────────────────────────────────────────

lint:
	$(PYTHON) hansel-tools/linters/lint_events.py $(if $(F),$(F),events/story_cycles/)

lint-loc:
	$(PYTHON) hansel-tools/linters/lint_localization.py $(if $(F),$(F),localization/english/)

lint-effects:
	$(PYTHON) hansel-tools/linters/lint_effects.py $(if $(F),$(F),common/scripted_effects/)

lint-all: lint lint-loc lint-effects

lint-rules:
	$(PYTHON) hansel-tools/linters/lint_events.py --rules

lint-loc-rules:
	$(PYTHON) hansel-tools/linters/lint_localization.py --rules

lint-effects-rules:
	$(PYTHON) hansel-tools/linters/lint_effects.py --rules

# ── Développement ────────────────────────────────────────────────────────────

symbols:
	$(PYTHON) hansel-tools/extract_symbols.py

generate:
	$(PYTHON) hansel-tools/generate_events.py $(T)

inject:
	$(PYTHON) hansel-tools/inject_run.py --inline "$(S)"

# ── Hansel CLI ───────────────────────────────────────────────────────────────

hansel:
	$(PYTHON) hansel-tools/cli.py $(ARGS)

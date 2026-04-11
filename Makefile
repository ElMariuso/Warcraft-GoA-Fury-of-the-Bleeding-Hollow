.PHONY: help install test \
	lint lint-loc lint-effects lint-all lint-rules lint-loc-rules lint-effects-rules \
	tiger tiger-install \
	logs logs-errors logs-filter logs-level logs-start \
	watch watch-filter \
	dev dev-bh dev-horde dev-all dev-filter dev-trace \
	errors-bh errors-horde errors-clear \
	symbols generate inject

PYTHON := python

help:
	@echo "CK3 Mod — Outils Python"
	@echo ""
	@echo "Setup"
	@echo "  make install                         Installer les dépendances (pip)"
	@echo "  make test                            Lancer les tests pytest"
	@echo ""
	@echo "Accumulation d'erreurs (set persistant, sans doublons)"
	@echo "  make errors-bh                       wc_bleeding_hollow — accumule dans logs/errors-bh.log"
	@echo "  make errors-horde                    wc_horde_invasion  — accumule dans logs/errors-horde.log"
	@echo "  make errors-clear                    Vider les logs d'erreurs accumulés"
	@echo ""
	@echo "Dev watch unifié (game.log + error.log)"
	@echo "  make dev                             Filtrer namespaces wc_* (défaut)"
	@echo "  make dev-bh                          wc_bleeding_hollow seulement"
	@echo "  make dev-horde                       wc_horde_invasion seulement"
	@echo "  make dev-all                         Aucun filtre (tout game.log)"
	@echo "  make dev-filter F=kilrogg            Regex custom sur game.log"
	@echo "  make dev-trace                       Résumé des events wc_* déclenchés"
	@echo ""
	@echo "Logs CK3 (game.log structuré)"
	@echo "  make logs                            Surveiller en temps réel"
	@echo "  make logs-errors                     Erreurs seulement"
	@echo "  make logs-filter F=wc_bleeding       Filtrer par regex"
	@echo "  make logs-level L=WARN               Niveau minimum (DEBUG/INFO/WARN/ERROR)"
	@echo "  make logs-start                      Lire depuis le début du fichier"
	@echo ""
	@echo "Watch simple"
	@echo "  make watch                           Surveiller game.log (mode simple)"
	@echo "  make watch-filter F=wc_bleeding      Filtrer par namespace"
	@echo ""
	@echo "Lint (Python — checks internes)"
	@echo "  make lint          [F=fichier.txt]   Events (.txt)"
	@echo "  make lint-loc      [F=fichier.yml]   Localisation (.yml)"
	@echo "  make lint-effects  [F=fichier.txt]   Scripted effects (.txt)"
	@echo "  make lint-all                        Tout linter (Python)"
	@echo "  make lint-rules                      Lister les règles events"
	@echo "  make lint-loc-rules                  Lister les règles localisation"
	@echo "  make lint-effects-rules              Lister les règles effects"
	@echo ""
	@echo "Tiger (validation CK3 complète — scopes, refs, loc)"
	@echo "  make tiger                           Lancer ck3-tiger sur le mod"
	@echo "  make tiger-install                   Installer ck3-tiger (cargo)"
	@echo ""
	@echo "Développement"
	@echo "  make symbols                         Extraire symbols.json depuis GoA2"
	@echo "  make generate T=tools/templates/event_stub.yaml  Générer stubs event"
	@echo "  make inject S='character:10005 = { add_prestige = 500 }'"

# ── Setup ────────────────────────────────────────────────────────────────────

install:
	$(PYTHON) -m pip install -r tools/requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v

# ── Dev watch unifié ─────────────────────────────────────────────────────────

dev:
	$(PYTHON) tools/dev_watch.py

dev-bh:
	$(PYTHON) tools/dev_watch.py --namespace bh

dev-horde:
	$(PYTHON) tools/dev_watch.py --namespace horde

dev-all:
	$(PYTHON) tools/dev_watch.py --namespace all

dev-filter:
	$(PYTHON) tools/dev_watch.py --filter "$(F)"

dev-trace:
	$(PYTHON) tools/dev_watch.py --event-trace

# ── Accumulation d'erreurs (set persistant, sans doublons) ───────────────────

ERRORS_PATTERN := wc_bleeding_hollow|wc_horde_invasion|Fury|Bleeding

errors-bh:
	$(PYTHON) tools/dev_watch.py --namespace bh 2>&1 | \
		$(PYTHON) tools/error_accumulator.py --out logs/errors-bh.log --pattern "$(ERRORS_PATTERN)"

errors-horde:
	$(PYTHON) tools/dev_watch.py --namespace horde 2>&1 | \
		$(PYTHON) tools/error_accumulator.py --out logs/errors-horde.log --pattern "$(ERRORS_PATTERN)"

errors-clear:
	@rm -f logs/errors-bh.log logs/errors-horde.log
	@echo "Logs d'erreurs supprimés."

# ── Logs structurés (log_viewer) ─────────────────────────────────────────────

logs:
	$(PYTHON) tools/log_viewer.py

logs-errors:
	$(PYTHON) tools/log_viewer.py --errors-only

logs-filter:
	$(PYTHON) tools/log_viewer.py --filter "$(F)"

logs-level:
	$(PYTHON) tools/log_viewer.py --level "$(L)"

logs-start:
	$(PYTHON) tools/log_viewer.py --from-start

# ── Watch simple (watch_logs) ─────────────────────────────────────────────────

watch:
	$(PYTHON) tools/watch_logs.py

watch-filter:
	$(PYTHON) tools/watch_logs.py --filter "$(F)"

# ── Tiger ────────────────────────────────────────────────────────────────────
# Pré-requis : cargo install ck3-tiger
# Pré-requis : copier ck3-tiger.conf.example → ck3-tiger.conf et renseigner ck3-dir

tiger:
	ck3-tiger .

tiger-install:
	cargo install ck3-tiger

# ── Lint ─────────────────────────────────────────────────────────────────────

lint:
	$(PYTHON) tools/lint_events.py $(if $(F),$(F),events/story_cycles/)

lint-loc:
	$(PYTHON) tools/lint_localization.py $(if $(F),$(F),localization/english/)

lint-effects:
	$(PYTHON) tools/lint_effects.py $(if $(F),$(F),common/scripted_effects/)

lint-all: lint lint-loc lint-effects

lint-rules:
	$(PYTHON) tools/lint_events.py --rules

lint-loc-rules:
	$(PYTHON) tools/lint_localization.py --rules

lint-effects-rules:
	$(PYTHON) tools/lint_effects.py --rules

# ── Développement ────────────────────────────────────────────────────────────

symbols:
	$(PYTHON) tools/extract_symbols.py

generate:
	$(PYTHON) tools/generate_events.py $(T)

inject:
	$(PYTHON) tools/inject_run.py --inline "$(S)"

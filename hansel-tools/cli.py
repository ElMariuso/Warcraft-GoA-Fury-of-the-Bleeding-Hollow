"""hansel-tools/cli.py — CLI unifié pour le tooling du mod CK3.

Usage:
    python hansel-tools/cli.py --help

    # Référence
    python hansel-tools/cli.py search <query> [--max N] [--docs PATH] [--no-color]
    python hansel-tools/cli.py doc [topic]

    # Écriture
    python hansel-tools/cli.py generate <template>

    # Validation
    python hansel-tools/cli.py lint [mode] [path]

    # Runtime (surveiller le jeu)
    python hansel-tools/cli.py logs [--errors-only] [--filter F] [--level L] [--from-start]
    python hansel-tools/cli.py watch [bh|horde|all] [--filter F] [--event-trace]
"""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory

from doc_search import SearchResult, _tokenize, search_docs
from ui import BLUE, BOLD, CYAN, DIM, RESET, YELLOW

HANSEL_DIR = Path(__file__).parent
PROJECT_ROOT = HANSEL_DIR.parent
DOCS_DIR = HANSEL_DIR / "docs"
TEMPLATES_DIR = HANSEL_DIR / "templates"


def _highlight(text: str, tokens: list[str], use_color: bool) -> str:
    """Met en évidence les tokens de la requête dans text."""
    if not use_color or not tokens:
        return text
    for token in tokens:
        text = re.sub(
            re.escape(token),
            lambda m: f"{BOLD}{YELLOW}{m.group()}{RESET}",
            text,
            flags=re.IGNORECASE,
        )
    return text


def _get_file_label(filename: str) -> str:
    """Retourne un label lisible depuis le basename d'un fichier .md."""
    return filename.removesuffix(".md").replace("_", " ").replace("-", " ").title()


def _c(text: str, code: str, use_color: bool) -> str:
    """Applique un code ANSI si use_color est vrai."""
    return f"{code}{text}{RESET}" if use_color else text


def _truncate(text: str, width: int = 90) -> str:
    """Tronque à width caractères avec '…'."""
    return text if len(text) <= width else text[: width - 1] + "…"


def cmd_search(args: argparse.Namespace) -> int:
    docs_dir = Path(args.docs) if args.docs else DOCS_DIR
    results = search_docs(args.query, docs_dir, max_results=args.max)
    use_color = sys.stdout.isatty() and not args.no_color

    if not results:
        print(_c(f"Aucun résultat pour : {args.query!r}", DIM, use_color))
        return 0

    # Regrouper par fichier (les résultats sont déjà triés score DESC)
    # Au sein de chaque fichier, trier par numéro de ligne pour lecture naturelle
    by_file: dict[str, list[SearchResult]] = {}
    for r in results:
        by_file.setdefault(r.file, []).append(r)

    total = len(results)
    query_tokens = _tokenize(args.query)

    for filename, file_results in by_file.items():
        file_results.sort(key=lambda r: r.line)
        label = _get_file_label(filename)

        # ── En-tête de fichier ──────────────────────────────────────────
        header_text = f"  {label}  "
        suffix = f" {filename} "
        pad = max(0, 72 - len(header_text) - len(suffix))
        header = _c("━━", BOLD + BLUE, use_color)
        header += _c(header_text, BOLD + BLUE, use_color)
        header += _c("─" * pad, DIM, use_color)
        header += _c(suffix, DIM, use_color)
        print()
        print(header)

        cur_section: str | None | object = object()  # sentinel distinct de None
        for r in file_results:
            # ── Séparateur de section ───────────────────────────────────
            if r.section != cur_section:
                cur_section = r.section
                if r.section:
                    print()
                    section_display = r.section if len(r.section) <= 70 else r.section[:69] + "…"
                    section_line = f"  § {section_display}"
                    print(_c(section_line, CYAN + DIM, use_color))

            # ── Ligne de résultat ───────────────────────────────────────
            lineno = _c(f"{r.line:>5}", DIM, use_color)
            bar = _c("│", DIM, use_color)
            excerpt = _highlight(_truncate(r.excerpt), query_tokens, use_color)
            print(f"  {lineno} {bar} {excerpt}")

    # ── Résumé bas de page ──────────────────────────────────────────────
    print()
    summary = f"  {total} résultat{'s' if total > 1 else ''}"
    if total == args.max:
        summary += f" (limite {args.max} — utilisez --max N pour en voir plus)"
    print(_c(summary, DIM, use_color))
    return 0


def _template_files() -> list[Path]:
    return sorted(TEMPLATES_DIR.glob("*.yaml"))


def cmd_generate(args: argparse.Namespace) -> int:
    template = getattr(args, "template", None)

    # Sans argument : lister les templates disponibles
    if not template:
        files = _template_files()
        if not files:
            print(f"Aucun template .yaml dans {TEMPLATES_DIR}")
            return 1
        use_color = sys.stdout.isatty()
        print(_c("Templates disponibles\n", BOLD + BLUE, use_color))
        for i, f in enumerate(files, 1):
            # Lire la première ligne de commentaire comme description
            desc = ""
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("# ") and "Template" in line:
                    desc = line.lstrip("# ").strip()
                    break
            print(f"  {i}.  {f.name:<32} {_c(desc, DIM, use_color)}")
        print(_c("\nUsage : generate <nom ou numéro>", DIM, use_color))
        return 0

    # Sélection par numéro
    if template.isdigit():
        files = _template_files()
        idx = int(template) - 1
        if idx < 0 or idx >= len(files):
            print(f"Numéro invalide : {template} (1–{len(files)})", file=sys.stderr)
            return 1
        template = str(files[idx])

    # Résolution du nom partiel (sans chemin complet)
    resolved = Path(template)
    if not resolved.exists():
        candidate = TEMPLATES_DIR / resolved.name
        if candidate.exists():
            resolved = candidate
        else:
            print(f"Template introuvable : {template}", file=sys.stderr)
            return 1

    return subprocess.run(
        [sys.executable, str(HANSEL_DIR / "generate_events.py"), str(resolved)],
        cwd=str(PROJECT_ROOT),
    ).returncode


# Modes de lint disponibles dans l'ordre d'affichage
_LINT_MODES: list[tuple[str, str, str, str]] = [
    ("events",  "events/story_cycles/",      "linters/lint_events.py",        "events .txt"),
    ("loc",     "localization/english/",     "linters/lint_localization.py",  "localisation .yml"),
    ("effects", "common/scripted_effects/",  "linters/lint_effects.py",       "scripted effects .txt"),
]


def _run_lint(script: str, path: str) -> int:
    return subprocess.run(
        [sys.executable, str(HANSEL_DIR / script), path],
        cwd=str(PROJECT_ROOT),
    ).returncode


def cmd_lint(args: argparse.Namespace) -> int:
    mode = getattr(args, "mode", None)

    # Sans argument : afficher le listing numéroté
    if not mode:
        use_color = sys.stdout.isatty()
        print(_c("Lint — que veux-tu valider ?\n", BOLD + BLUE, use_color))
        for i, (name, _, _, desc) in enumerate(_LINT_MODES, 1):
            print(f"  {i}.  {name:<10} {_c(desc, DIM, use_color)}")
        print(f"  4.  all        {_c('lint-all (3 passes)', DIM, use_color)}")
        print(_c("\nUsage : lint <numéro ou nom>  [path]", DIM, use_color))
        return 0

    # Sélection par numéro
    if mode.isdigit():
        idx = int(mode) - 1
        if idx == 3:  # "all"
            mode = "all"
        elif 0 <= idx < len(_LINT_MODES):
            mode = _LINT_MODES[idx][0]
        else:
            print(f"Numéro invalide : {mode} (1–4)", file=sys.stderr)
            return 1

    path = getattr(args, "path", None)

    if mode == "all":
        rc = 0
        for name, default_path, script, _ in _LINT_MODES:
            print(_c(f"\n── {name} ──", BOLD, sys.stdout.isatty()))
            rc |= _run_lint(script, path or str(PROJECT_ROOT / default_path))
        return rc

    # Résolution par nom
    matches = [m for m in _LINT_MODES if m[0] == mode]
    if not matches:
        # Chemin direct passé comme mode (compat)
        return _run_lint("linters/lint_events.py", mode)
    _, default_path, script, _ = matches[0]
    return _run_lint(script, path or str(PROJECT_ROOT / default_path))


def cmd_tiger(args: argparse.Namespace) -> int:
    """Lance ck3-tiger pour validation CK3 complète."""
    try:
        return subprocess.run(["ck3-tiger", "."], cwd=str(PROJECT_ROOT)).returncode
    except FileNotFoundError:
        print("ck3-tiger introuvable — installe avec : cargo install ck3-tiger", file=sys.stderr)
        return 1


def cmd_logs(args: argparse.Namespace) -> int:
    """Surveille game.log en temps réel (délègue à log_viewer.py)."""
    cmd: list[str] = [sys.executable, str(HANSEL_DIR / "watchers" / "log_viewer.py")]
    if getattr(args, "errors_only", False):
        cmd.append("--errors-only")
    if getattr(args, "filter", None):
        cmd += ["--filter", args.filter]
    if getattr(args, "level", None):
        cmd += ["--level", args.level]
    if getattr(args, "from_start", False):
        cmd.append("--from-start")
    try:
        return subprocess.run(cmd, cwd=str(PROJECT_ROOT)).returncode
    except KeyboardInterrupt:
        return 0


# Namespaces disponibles pour `watch`, dans l'ordre d'affichage
_WATCH_NAMESPACES: list[tuple[str | None, str, str]] = [
    (None,    "wc_*",  "tous les namespaces du mod (défaut)"),
    ("bh",    "bh",    "wc_bleeding_hollow seulement"),
    ("horde", "horde", "wc_horde_invasion seulement"),
    ("all",   "all",   "tout game.log (aucun filtre)"),
]


def cmd_watch(args: argparse.Namespace) -> int:
    """Surveille game.log + error.log filtré par namespace (délègue à dev_watch.py)."""
    namespace = getattr(args, "namespace", None)

    # Sans argument : afficher le listing numéroté
    if namespace is None and not getattr(args, "_run_default", False):
        use_color = sys.stdout.isatty()
        print(_c("Namespaces disponibles\n", BOLD + BLUE, use_color))
        for i, (_, short, desc) in enumerate(_WATCH_NAMESPACES, 1):
            print(f"  {i}.  {short:<8} {_c(desc, DIM, use_color)}")
        print(_c("\nUsage : watch <numéro ou nom>  [--filter F] [--event-trace]", DIM, use_color))
        return 0

    cmd_list: list[str] = [sys.executable, str(HANSEL_DIR / "watchers" / "dev_watch.py")]
    if namespace:
        cmd_list += ["--namespace", namespace]
    if getattr(args, "filter", None):
        cmd_list += ["--filter", args.filter]
    if getattr(args, "event_trace", False):
        cmd_list.append("--event-trace")
    try:
        return subprocess.run(cmd_list, cwd=str(PROJECT_ROOT)).returncode
    except KeyboardInterrupt:
        return 0


def _match_doc_files(topic: str, docs_dir: Path) -> list[Path]:
    """Fuzzy-match du topic contre les stems de fichiers .md."""
    needle = topic.lower().replace("-", "").replace("_", "").replace(" ", "")
    files = sorted(docs_dir.glob("*.md"))
    exact = [f for f in files if f.stem.lower().replace("_", "") == needle]
    if exact:
        return exact
    return [f for f in files if needle in f.stem.lower().replace("_", "")]


def _is_ref(f: Path) -> bool:
    """Vrai si le fichier est une liste de référence (non un guide)."""
    return f.stem.lower().endswith("_list") or f.stem.lower() == "console_commands"


def _doc_index(docs_dir: Path) -> list[Path]:
    """Retourne la liste ordonnée : refs d'abord, puis guides."""
    files = sorted(docs_dir.glob("*.md"))
    refs = [f for f in files if _is_ref(f)]
    guides = [f for f in files if not _is_ref(f)]
    return refs + guides


def _doc_show_listing(docs_dir: Path, use_color: bool) -> int:
    """Show the numbered doc menu."""
    index = _doc_index(docs_dir)
    if not index:
        print(f"No doc files found in {docs_dir}", file=sys.stderr)
        return 1

    refs = [f for f in index if _is_ref(f)]
    guides = [f for f in index if not _is_ref(f)]

    try:
        from rich.console import Console
        from rich.padding import Padding
        from rich.table import Table
        from rich.text import Text

        console = Console()
        counter = 0

        def _rich_group(icon: str, title: str, group: list[Path]) -> None:
            nonlocal counter
            console.print(f"\n [bright_blue]{icon}[/]  [bold white]{title}[/]")
            t = Table.grid(padding=(0, 2))
            t.add_column(style="dim", no_wrap=True, min_width=4, justify="right")
            t.add_column(style="bold cyan", no_wrap=True, min_width=28)
            t.add_column(style="dim")
            for f in group:
                counter += 1
                label = f.stem.replace("_", " ").lower()
                t.add_row(f"{counter}.", label, f.name)
            console.print(Padding(t, (0, 0, 0, 4)))

        _rich_group("󰈙", "Reference", refs)
        _rich_group("󰈮", "Guides & Concepts", guides)
        console.print(
            Padding(Text("doc <topic or number>", style="dim italic"), (1, 0, 0, 4))
        )
    except ImportError:
        counter = 0

        def _plain_group(title: str, group: list[Path]) -> None:
            nonlocal counter
            print(_c(title, BOLD + BLUE, use_color))
            for f in group:
                counter += 1
                label = f.stem.replace("_", " ").lower()
                print(f"  {counter:>2}.  {label:<28} {_c(f.name, DIM, use_color)}")
            print()

        _plain_group("Reference", refs)
        _plain_group("Guides & Concepts", guides)
        print(_c("doc <topic or number>", DIM, use_color))

    return 0


def _doc_render_content(f: Path) -> int:
    """Affiche le contenu d'un fichier doc avec rich (fallback texte brut)."""
    content = f.read_text(encoding="utf-8")
    try:
        from rich.console import Console
        from rich.markdown import CodeBlock, Markdown
        from rich.panel import Panel
        from rich.rule import Rule
        from rich.syntax import Syntax
        from rich.text import Text

        # Code block sans le Padding(1, 0) que rich ajoute par défaut
        class _CompactCodeBlock(CodeBlock):
            def __rich_console__(self, console, options):  # type: ignore[override]
                code = str(self.text).rstrip()
                yield Syntax(code, self.lexer_name, theme=self.theme, word_wrap=True)

        class _CompactMarkdown(Markdown):
            elements = {**Markdown.elements, "fence": _CompactCodeBlock, "code_block": _CompactCodeBlock}

        content = re.sub(r"^#[^#][^\n]*\n", "", content, count=1).lstrip("\n")
        content = re.sub(r"\n{3,}", "\n\n", content)

        console = Console()
        title = f.stem.replace("_", " ").title()
        console.print()
        console.print(
            Panel(
                Text.assemble(
                    ("󰈙  ", "bright_blue"),
                    (title, "bold white"),
                ),
                subtitle=Text(f.name, style="dim"),
                border_style="bright_blue",
                padding=(0, 3),
            )
        )
        console.print(_CompactMarkdown(content, code_theme="monokai"))
        console.print(Rule(style="dim"))
    except ImportError:
        print(content)
    return 0


def cmd_doc(args: argparse.Namespace) -> int:
    docs_dir = Path(args.docs) if getattr(args, "docs", None) else DOCS_DIR
    use_color = sys.stdout.isatty()
    topic = " ".join(args.topic) if args.topic else None

    if topic and topic.isdigit():
        index = _doc_index(docs_dir)
        idx = int(topic) - 1
        if idx < 0 or idx >= len(index):
            print(f"Invalid number: {topic} (1–{len(index)})", file=sys.stderr)
            return 1
        topic = index[idx].stem.replace("_", " ")

    if not topic:
        return _doc_show_listing(docs_dir, use_color)

    matches = _match_doc_files(topic, docs_dir)
    if not matches:
        print(_c(f"No doc found for: {topic!r}", DIM, use_color), file=sys.stderr)
        print("Type 'doc' to list all available topics.", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(_c(f"Multiple matches for {topic!r}:", BOLD, use_color))
        for f in matches:
            print(f"  {f.stem.lower().replace('_', ' '):<32} {f.name}")
        print(_c("\nBe more specific.", DIM, use_color))
        return 1

    return _doc_render_content(matches[0])


class HanselRepl:
    """REPL interactif pour hansel — lance avec `./hansel` sans arguments."""

    _last_list: str = "doc"  # "doc" | "generate" | "watch" | "lint"

    def _build_completer(self) -> NestedCompleter:
        doc_stems = {f.stem.replace("_", " "): None for f in sorted(DOCS_DIR.glob("*.md"))}
        tmpl_stems = {f.stem: None for f in sorted(TEMPLATES_DIR.glob("*.yaml"))}
        return NestedCompleter.from_nested_dict({
            "search": None,
            "doc": doc_stems,
            "lint": {"events": None, "loc": None, "effects": None, "all": None},
            "watch": {"bh": None, "horde": None, "all": None},
            "generate": tmpl_stems,
            "logs": {
                "--errors-only": None,
                "--filter": None,
                "--level": None,
                "--from-start": None,
            },
            "tiger": None,
            "help": None,
            "ls": None,
            "exit": None,
            "quit": None,
        })

    def run(self) -> None:
        session: PromptSession[str] = PromptSession(
            history=FileHistory(str(Path.home() / ".hansel_history")),
            completer=self._build_completer(),
        )
        self._do_help("")
        prompt_str = ANSI(f"{BLUE}hansel{RESET} {DIM}❯{RESET} ")
        while True:
            try:
                line = session.prompt(prompt_str)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            line = line.strip()
            if not line:
                continue
            if self._dispatch(line):
                break

    def _dispatch(self, line: str) -> bool:
        """Retourne True si l'utilisateur veut quitter."""
        if line.isdigit():
            dispatch = {
                "doc": self._do_doc,
                "generate": self._do_generate,
                "watch": self._do_watch,
                "lint": self._do_lint,
            }
            fn = dispatch.get(self._last_list, self._do_doc)
            fn(line)
            return False
        parts = line.split(None, 1)
        cmd_name = parts[0]
        arg = parts[1] if len(parts) > 1 else ""
        handler = {
            "search": self._do_search,
            "doc": self._do_doc,
            "lint": self._do_lint,
            "tiger": self._do_tiger,
            "logs": self._do_logs,
            "watch": self._do_watch,
            "generate": self._do_generate,
            "help": self._do_help,
            "ls": self._do_help,
            "exit": lambda _: True,
            "quit": lambda _: True,
        }.get(cmd_name)
        if handler is None:
            print(f"Commande inconnue : {cmd_name!r}. Tape 'help'.")
            return False
        result = handler(arg)
        return result is True

    # ── Commandes ────────────────────────────────────────────────────────────

    def _do_search(self, arg: str) -> None:
        """search <query> [--max N]  — Rechercher dans la doc"""
        parts = shlex.split(arg) if arg else []
        if not parts:
            print("Usage : search <query> [--max N]")
            return
        p = argparse.ArgumentParser(prog="search", exit_on_error=False)
        p.add_argument("query")
        p.add_argument("--max", type=int, default=20)
        p.add_argument("--no-color", action="store_true", dest="no_color")
        p.add_argument("--docs", default=None)
        try:
            ns = p.parse_args(parts)
        except (argparse.ArgumentError, SystemExit):
            print("Usage : search <query> [--max N]")
            return
        cmd_search(ns)

    def _do_doc(self, arg: str) -> None:
        """doc [topic]  — Afficher la doc d'un topic (ou lister)"""
        words = shlex.split(arg) if arg else []
        if not words:
            self._last_list = "doc"
        cmd_doc(argparse.Namespace(topic=words, docs=None))

    def _do_lint(self, arg: str) -> None:
        """lint [mode|numéro] [path]  — Linter (events/loc/effects/all)"""
        parts = shlex.split(arg) if arg else []
        if not parts:
            self._last_list = "lint"
            cmd_lint(argparse.Namespace(mode=None, path=None))
            return
        mode = parts[0]
        path = parts[1] if len(parts) > 1 else None
        cmd_lint(argparse.Namespace(mode=mode, path=path))

    def _do_tiger(self, _arg: str) -> None:
        """tiger  — Validation CK3 complète (ck3-tiger)"""
        cmd_tiger(argparse.Namespace())

    def _do_logs(self, arg: str) -> None:
        """logs [--errors-only] [--filter F] [--level L] [--from-start]  — Surveiller game.log"""
        parts = shlex.split(arg) if arg else []
        p = argparse.ArgumentParser(prog="logs", exit_on_error=False)
        p.add_argument("--errors-only", action="store_true", dest="errors_only")
        p.add_argument("--filter", default=None, metavar="F")
        p.add_argument("--level", default=None, metavar="L")
        p.add_argument("--from-start", action="store_true", dest="from_start")
        try:
            ns = p.parse_args(parts)
        except (argparse.ArgumentError, SystemExit):
            print("Usage : logs [--errors-only] [--filter F] [--level DEBUG|INFO|WARN|ERROR]")
            return
        cmd_logs(ns)

    def _do_watch(self, arg: str) -> None:
        """watch [bh|horde|all] [--filter F] [--event-trace]  — Surveiller les namespaces wc_*"""
        parts = shlex.split(arg) if arg else []

        # Sélection par numéro depuis le listing
        if len(parts) == 1 and parts[0].isdigit():
            idx = int(parts[0]) - 1
            if idx < 0 or idx >= len(_WATCH_NAMESPACES):
                print(f"Numéro invalide : {parts[0]} (1–{len(_WATCH_NAMESPACES)})")
                return
            ns_key, _, _ = _WATCH_NAMESPACES[idx]
            cmd_watch(
                argparse.Namespace(namespace=ns_key, filter=None, event_trace=False, _run_default=True)
            )
            return

        p = argparse.ArgumentParser(prog="watch", exit_on_error=False)
        p.add_argument("namespace", nargs="?", choices=["bh", "horde", "all"], default=None)
        p.add_argument("--filter", default=None, metavar="F")
        p.add_argument("--event-trace", action="store_true", dest="event_trace")
        try:
            ns = p.parse_args(parts)
        except (argparse.ArgumentError, SystemExit):
            print("Usage : watch [bh|horde|all] [--filter F] [--event-trace]")
            return

        if not parts:
            self._last_list = "watch"
        else:
            ns._run_default = True
        cmd_watch(ns)

    def _do_generate(self, arg: str) -> None:
        """generate [template]  — Générer un event stub (ou lister les templates)"""
        tmpl = arg.strip() or None
        if not tmpl:
            self._last_list = "generate"
        cmd_generate(argparse.Namespace(template=tmpl))

    def _do_help(self, _arg: str) -> None:
        """Show command reference."""
        try:
            from rich.console import Console
            from rich.padding import Padding
            from rich.table import Table
            from rich.text import Text

            console = Console()

            # icon, title, [(cmd, flags, description, example)]
            sections: list[tuple[str, str, list[tuple[str, str, str, str]]]] = [
                ("󰈙", "Reference", [
                    ("search", "<query> [--max N]",
                     "Search keywords across all CK3/Paradox docs",
                     "search trigger"),
                    ("doc", "[topic]",
                     "Read a full reference topic — no arg lists all topics",
                     "doc events"),
                ]),
                ("󰝰", "Scaffolding", [
                    ("generate", "[template]",
                     "Scaffold a new .txt event file + .yml localization stubs",
                     "generate event_unique"),
                ]),
                ("󰗡", "Validation", [
                    ("lint", "[events|loc|effects|all]",
                     "Static linter — checks content_source, ai_chance, keys…",
                     "lint events"),
                    ("tiger", "",
                     "Full CK3 engine check: scopes, references, localization",
                     "tiger"),
                ]),
                ("󰓅", "Runtime  [CK3 must be running]", [
                    ("logs", "[--errors-only] [--filter F] [--level L]",
                     "Tail game.log — filter by regex, level, or errors only",
                     "logs --errors-only"),
                    ("watch", "[bh|horde|all] [--filter F] [--event-trace]",
                     "game.log + error.log in parallel, filtered to wc_* namespaces",
                     "watch bh"),
                ]),
            ]

            console.print()
            for icon, title, rows in sections:
                console.print(f" [bright_blue]{icon}[/]  [bold white]{title}[/]")
                t = Table.grid(padding=(0, 2))
                t.add_column(style="bold cyan", no_wrap=True, min_width=10)
                t.add_column(style="dim", no_wrap=True, min_width=26)
                t.add_column(style="white")
                t.add_column(style="dim italic")
                for cmd, flags, desc, ex in rows:
                    t.add_row(cmd, flags, desc, f"e.g.  {ex}" if ex else "")
                console.print(Padding(t, (0, 0, 1, 4)))

        except ImportError:
            print(
                f"\n{BOLD}Reference{RESET}\n"
                f"  search <query> [--max N]       Search CK3/Paradox docs\n"
                f"  doc [topic]                    Show a doc topic or list all\n"
                f"\n{BOLD}Scaffolding{RESET}\n"
                f"  generate [template]            Scaffold event stubs from YAML\n"
                f"\n{BOLD}Validation{RESET}\n"
                f"  lint [events|loc|effects|all]  Static linter\n"
                f"  tiger                          Full CK3 validation\n"
                f"\n{BOLD}Runtime{RESET}\n"
                f"  logs  [--errors-only] [--filter F] [--level L]\n"
                f"  watch [bh|horde|all] [--filter F] [--event-trace]\n"
                f"\n{DIM}Tab=autocomplete  ↑↓=history  Ctrl+D=quit{RESET}\n"
            )


def _start_repl() -> None:
    try:
        from rich.console import Console
        from rich.padding import Padding
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text

        console = Console()
        console.print()

        # ── Banner ──────────────────────────────────────────────────────────
        console.print(
            Panel(
                Text.assemble(
                    ("hansel", "bold bright_blue"),
                    ("  ·  v1.0\n", "dim"),
                    ("CK3 modding toolkit for ", "dim"),
                    ("Warcraft-GoA: Fury of the Bleeding Hollow\n\n", "white"),
                    (
                        "Write, validate, and debug CK3 events without\n"
                        "leaving your terminal. Works alongside the game.\n",
                        "dim",
                    ),
                ),
                subtitle=Text("Ctrl-D  ·  exit  ·  quit  —  to quit", style="dim"),
                border_style="bright_blue",
                padding=(1, 3),
            )
        )
        console.print(
            Padding(
                Text.assemble(
                    ("Type ", "dim"),
                    ("help", "bold cyan"),
                    (" for the full command reference  ·  ", "dim"),
                    ("Tab", "bold cyan"),
                    (" to autocomplete  ·  ", "dim"),
                    ("↑/↓", "bold cyan"),
                    (" to navigate history", "dim"),
                ),
                (0, 0, 0, 1),
            )
        )

        # ── Quick-start workflow ─────────────────────────────────────────────
        qs = Table.grid(padding=(0, 2))
        qs.add_column(style="dim", no_wrap=True, min_width=2)   # step number
        qs.add_column(style="bold cyan", no_wrap=True)          # command
        qs.add_column(style="dim")                              # what it does
        qs.add_row("1.", "search <term>", "Look up any trigger, effect, or scope in the CK3/Paradox docs")
        qs.add_row("2.", "generate",      "Scaffold a new event file from a YAML template")
        qs.add_row("3.", "lint events",   "Run the static linter before loading the mod in-game")
        qs.add_row("4.", "watch bh",      "Tail game.log + error.log live while CK3 runs")

        console.print()
        console.print(
            Panel(
                Padding(qs, (0, 1)),
                title=Text("  Typical workflow", style="dim"),
                title_align="left",
                border_style="dim",
                padding=(0, 2),
            )
        )
        console.print()
    except ImportError:
        print("hansel v1.0 — CK3 modding toolkit")
        print("Warcraft-GoA: Fury of the Bleeding Hollow")
        print("Type 'help' for commands.\n")

    HanselRepl().run()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hansel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Tooling CK3 — Warcraft-GoA: Fury of the Bleeding Hollow",
        epilog=textwrap.dedent("""\
          Référence
            search <query>              Rechercher dans la doc CK3/Paradox (occurrences)
            doc [topic]                 Afficher la doc complète d'un topic (ou lister)

          Écriture
            generate <template>         Générer un event stub depuis un YAML

          Validation
            lint [events|loc|effects|all]  Linter (menu numéroté sans arg)
            tiger                       Validation CK3 complète (ck3-tiger)

          Runtime
            logs                        Surveiller game.log en temps réel
            watch [bh|horde|all]        Surveiller les namespaces wc_* (Ctrl-C pour quitter)
        """),
    )
    sub = parser.add_subparsers(dest="command", metavar=" ")
    sub.required = True

    # search
    p_search = sub.add_parser("search", help="Rechercher dans la doc CK3/Paradox")
    p_search.add_argument("query", help="Termes à rechercher")
    p_search.add_argument(
        "--max",
        type=int,
        default=20,
        metavar="N",
        help="Nombre max de résultats (défaut: 20)",
    )
    p_search.add_argument(
        "--docs",
        metavar="PATH",
        help="Répertoire docs (défaut: docs/wiki-paradox/)",
    )
    p_search.add_argument(
        "--no-color",
        action="store_true",
        dest="no_color",
        help="Désactiver les couleurs ANSI",
    )
    p_search.set_defaults(func=cmd_search)

    # generate
    p_gen = sub.add_parser("generate", help="Générer un event stub depuis un template YAML")
    p_gen.add_argument("template", help="Chemin vers le template .yaml")
    p_gen.set_defaults(func=cmd_generate)

    # lint
    p_lint = sub.add_parser("lint", help="Linter events, loc, effects ou tout")
    p_lint.add_argument(
        "mode",
        nargs="?",
        help="events | loc | effects | all (défaut: menu interactif)",
    )
    p_lint.add_argument(
        "path",
        nargs="?",
        help="Fichier ou dossier (surcharge le chemin par défaut du mode)",
    )
    p_lint.set_defaults(func=cmd_lint)

    # tiger
    p_tiger = sub.add_parser("tiger", help="Validation CK3 complète (ck3-tiger)")
    p_tiger.set_defaults(func=cmd_tiger)

    # doc
    p_doc = sub.add_parser("doc", help="Afficher la doc complète d'un topic (ou lister)")
    p_doc.add_argument("topic", nargs="*", help="Topic (ex: lists, effects, story cycles)")
    p_doc.add_argument("--docs", metavar="PATH", help="Répertoire docs")
    p_doc.set_defaults(func=cmd_doc)

    # logs
    p_logs = sub.add_parser("logs", help="Surveiller game.log en temps réel")
    p_logs.add_argument("--errors-only", action="store_true", dest="errors_only", help="Erreurs seulement")
    p_logs.add_argument("--filter", default=None, metavar="F", help="Regex custom sur game.log")
    p_logs.add_argument("--level", default=None, metavar="L", help="Niveau minimum (DEBUG/INFO/WARN/ERROR)")
    p_logs.add_argument("--from-start", action="store_true", dest="from_start", help="Depuis le début du fichier")
    p_logs.set_defaults(func=cmd_logs)

    # dev
    p_watch = sub.add_parser("watch", help="Surveiller les namespaces wc_* (game.log + error.log)")
    p_watch.add_argument(
        "namespace",
        nargs="?",
        choices=["bh", "horde", "all"],
        default=None,
        help="bh = bleeding_hollow, horde = horde_invasion, all = tout (défaut: wc_*)",
    )
    p_watch.add_argument("--filter", default=None, metavar="F", help="Regex custom")
    p_watch.add_argument("--event-trace", action="store_true", dest="event_trace", help="Résumé des events déclenchés")
    p_watch.set_defaults(func=cmd_watch)

    return parser


def main() -> None:
    if len(sys.argv) == 1:
        _start_repl()
        return
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import sys
import textwrap
import time
from datetime import datetime, timezone
from typing import Any

def _get_psycopg2():
    try:
        import psycopg2
        return psycopg2
    except ImportError:
        print("ERROR: psycopg2 is not installed.\n"
              "       Run:  pip install psycopg2-binary", file=sys.stderr)
        sys.exit(1)


from seed.data import (
    CORRIDORS, SACCOS, SACCO_ALIASES, STAGES, STAGE_HOURS,
    ROUTES, ROUTE_PATHS, FARES, PAYMENT_METHODS,
    PUBLIC_HOLIDAYS, OCCUPANCY, APP_SETTINGS,
    STAGE_CBD_GPO, STAGE_MFANGANO,
    ROUTE_45_OUT, ROUTE_45_IN, ROUTE_44_OUT, ROUTE_44_IN,
    ROUTE_LUCKY_OUT, ROUTE_LUCKY_IN, ROUTE_KAS_OUT, ROUTE_KAS_IN,
    ROUTE_MIREMA_OUT, ROUTE_MIREMA_IN, ROUTE_TRM_OUT, ROUTE_TRM_IN,
    ROUTE_CLAY_OUT, ROUTE_CLAY_IN, ROUTE_UMOINER_OUT, ROUTE_UMOINER_IN,
)

_OUTBOUND_ROUTES = {
    ROUTE_45_OUT, ROUTE_44_OUT, ROUTE_LUCKY_OUT, ROUTE_KAS_OUT,
    ROUTE_MIREMA_OUT, ROUTE_TRM_OUT, ROUTE_CLAY_OUT, ROUTE_UMOINER_OUT,
}
_INBOUND_ROUTES = {
    ROUTE_45_IN, ROUTE_44_IN, ROUTE_LUCKY_IN, ROUTE_KAS_IN,
    ROUTE_MIREMA_IN, ROUTE_TRM_IN, ROUTE_CLAY_IN, ROUTE_UMOINER_IN,
}


BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
YELLOW= "\033[33m"
RESET = "\033[0m"

def _h(text: str) -> str:
    return f"{BOLD}{CYAN}{text}{RESET}"

def _ok(text: str) -> str:
    return f"{GREEN}✓{RESET}  {text}"

def _warn(text: str) -> str:
    return f"{YELLOW}!{RESET}  {text}"


def _print_banner() -> None:
    print()
    print(_h("━" * 60))
    print(_h("  Thika Road Corridor – Matatu Database Seeder"))
    print(_h("━" * 60))
    print()


def _ask_direction() -> str:
    print(textwrap.dedent("""\
        Which direction are you travelling?

          [1]  Outbound  –  CBD  →  Githurai / Kasarani / panya routes
          [2]  Inbound   –  Githurai / Kasarani  →  CBD
          [3]  Both      –  seed all directions (default)
    """))
    while True:
        raw = input("  Enter choice [1/2/3]: ").strip()
        if raw in ("", "3"):
            return "both"
        if raw == "1":
            return "outbound"
        if raw == "2":
            return "inbound"
        print("  Please enter 1, 2, or 3.")


def _ask_db_url() -> str:
    print()
    default = "postgresql://postgres:1234@localhost/matatu_db"
    raw = input(
        f"  Database URL [{default}]: "
    ).strip()
    return raw or default


def _print_stage_menu(direction: str) -> None:
    """Display formal and informal stages relevant to the chosen direction."""
    from seed.data import STAGES

    outbound_formal   = []
    outbound_informal = []
    inbound_formal    = []
    inbound_informal  = []

    for s in STAGES:
        row = f"    {'📍' if s['stage_type']=='formal' else '📌'}  " \
              f"{s['name']}  ({s['area']})"
        if s["direction"] == "outbound":
            if s["stage_type"] == "formal":
                outbound_formal.append(row)
            else:
                outbound_informal.append(row)
        else:
            if s["stage_type"] == "formal":
                inbound_formal.append(row)
            else:
                inbound_informal.append(row)

    show_out = direction in ("outbound", "both")
    show_in  = direction in ("inbound",  "both")

    print()
    print(_h("  Stages being seeded"))
    print(_h("  " + "─" * 56))

    if show_out:
        print(f"\n  {BOLD}Outbound (CBD → upcountry) – Formal{RESET}")
        for r in outbound_formal:
            print(r)
        print(f"\n  {BOLD}Outbound – Informal / Panya{RESET}")
        for r in outbound_informal:
            print(r)

    if show_in:
        print(f"\n  {BOLD}Inbound (upcountry → CBD) – Formal{RESET}")
        for r in inbound_formal:
            print(r)

    print()


def _filter_by_direction(direction: str) -> dict[str, list]:
    """Return only the rows relevant to the chosen direction."""
    if direction == "both":
        return {
            "routes":        ROUTES,
            "route_paths":   ROUTE_PATHS,
            "fares":         FARES,
            "payment_methods": PAYMENT_METHODS,
            "occupancy":     OCCUPANCY,
        }

    wanted = _OUTBOUND_ROUTES if direction == "outbound" else _INBOUND_ROUTES

    def filt(rows, key="route_id"):
        return [r for r in rows if r.get(key) in wanted or r.get("id") in wanted]

    return {
        "routes":          [r for r in ROUTES     if r["id"] in wanted],
        "route_paths":     filt(ROUTE_PATHS),
        "fares":           filt(FARES),
        "payment_methods": filt(PAYMENT_METHODS),
        "occupancy":       filt(OCCUPANCY),
    }



def _insert(cur, table: str, rows: list[dict[str, Any]], dry_run: bool) -> int:
    if not rows:
        return 0
    if dry_run:
        return len(rows)
    cols = list(rows[0].keys())
    placeholders = ", ".join(f"%({c})s" for c in cols)
    sql = (
        f"INSERT INTO {table} ({', '.join(cols)}) "
        f"VALUES ({placeholders}) ON CONFLICT DO NOTHING"
    )
    import psycopg2.extras
    psycopg2.extras.execute_batch(cur, sql, rows, page_size=500)
    return len(rows)


def _run_seed(db_url: str, direction: str, dry_run: bool) -> None:
    psycopg2 = _get_psycopg2()

    filtered = _filter_by_direction(direction)

    now_ts = datetime.now(tz=timezone.utc).isoformat()
    for r in filtered["routes"]:
        r.setdefault("fare_last_verified_at", now_ts)
        r.setdefault("last_confirmed_at", now_ts)
        r.setdefault("created_at", now_ts)
    for s in SACCOS:
        s.setdefault("last_confirmed_at", now_ts)
        s.setdefault("created_at", now_ts)

    tables: list[tuple[str, list]] = [
        ("corridors",       CORRIDORS),
        ("saccos",          SACCOS),
        ("sacco_aliases",   SACCO_ALIASES),
        ("stages",          STAGES),
        ("stage_hours",     STAGE_HOURS),
        ("routes",          filtered["routes"]),
        ("route_paths",     filtered["route_paths"]),
        ("fares",           filtered["fares"]),
        ("payment_methods", filtered["payment_methods"]),
        ("public_holidays", PUBLIC_HOLIDAYS),
        ("occupancy",       filtered["occupancy"]),
        ("app_settings",    APP_SETTINGS),
    ]

    print()
    print(_h("  Seeding tables"))
    print(_h("  " + "─" * 56))

    if dry_run:
        print(f"  {YELLOW}DRY RUN – nothing will be written to the DB{RESET}\n")

    conn = cur = None
    if not dry_run:
        conn = psycopg2.connect(db_url)
        conn.autocommit = False
        cur  = conn.cursor()

    total = 0
    for table, rows in tables:
        t0  = time.perf_counter()
        n   = _insert(cur, table, rows, dry_run)
        ms  = (time.perf_counter() - t0) * 1000
        total += n
        print(_ok(f"{table:<22}  {n:>5} rows  ({ms:.0f} ms)"))

    if not dry_run and conn:
        conn.commit()
        cur.close() # type: ignore
        conn.close()

    print()
    print(_h("  " + "─" * 56))
    print(_ok(f"Total rows inserted: {BOLD}{total}{RESET}"))
    print()



def _print_route_summary(direction: str) -> None:
    from seed.data import ROUTES, SACCOS, STAGES

    sacco_name  = {s["id"]: s["name"] for s in SACCOS}
    stage_name  = {s["id"]: s["name"] for s in STAGES}
    wanted = (
        _OUTBOUND_ROUTES | _INBOUND_ROUTES if direction == "both"
        else _OUTBOUND_ROUTES if direction == "outbound"
        else _INBOUND_ROUTES
    )

    print(_h("  Routes seeded"))
    print(_h("  " + "─" * 56))
    for r in ROUTES:
        if r["id"] not in wanted:
            continue
        origin = stage_name.get(r["origin_stage_id"], "?")
        dest   = stage_name.get(r["dest_stage_id"],   "?")
        sacco  = sacco_name.get(r["sacco_id"],        "?")
        express = " [EXPRESS]" if r["is_express"] else ""
        print(f"    {BOLD}{sacco}{RESET}{express}")
        print(f"      {origin}  →  {dest}")
        print(f"      via: {r['via_description']}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m seed",
        description="Interactive Thika Road matatu corridor seeder",
    )
    parser.add_argument(
        "--url", default=None,
        help="PostgreSQL connection URL (will prompt if omitted)",
    )
    parser.add_argument(
        "--direction", choices=["inbound", "outbound", "both"], default=None,
        help="Travel direction to seed (will prompt if omitted)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print counts without writing to the database",
    )
    args = parser.parse_args()

    _print_banner()

    direction = args.direction or _ask_direction()
    _print_stage_menu(direction)
    _print_route_summary(direction)

    db_url = args.url or ("DRY_RUN" if args.dry_run else _ask_db_url())

    _run_seed(db_url, direction, dry_run=args.dry_run)

    if not args.dry_run:
        print(_ok("Done. Run your app and enjoy the matatus! 🚐"))
    else:
        print(_warn("Dry run complete – re-run without --dry-run to commit."))
    print()
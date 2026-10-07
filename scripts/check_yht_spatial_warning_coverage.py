from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.yht_spatial_warning_coverage import write_coverage


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Outcome-firewalled movement-only coverage gate for the frozen "
            "Ya Ha Tinda Love-Otto future-demography protocol."
        )
    )
    parser.add_argument("--movebank-csv", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--official-movebank-utc-semantics",
        action="store_true",
        help=(
            "Interpret timezone-naive timestamp strings as UTC only when the input is the "
            "official Movebank archive, whose documented timestamp semantics are UTC."
        ),
    )
    args = parser.parse_args()
    write_coverage(
        args.movebank_csv,
        args.output,
        movebank_naive_utc=args.official_movebank_utc_semantics,
    )


if __name__ == "__main__":
    main()

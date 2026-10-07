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
        "--timestamp-semantics",
        choices=("explicit_timezone", "movebank_utc"),
        default="explicit_timezone",
    )
    args = parser.parse_args()
    write_coverage(
        args.movebank_csv,
        args.output,
        timestamp_semantics=args.timestamp_semantics,
    )


if __name__ == "__main__":
    main()

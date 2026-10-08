from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.yht_spatial_warning_state import write_summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build frozen Love-Otto annual spatial state from Ya Ha Tinda GPS rows."
    )
    parser.add_argument("--movement-csv", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--timestamp-semantics",
        choices=("explicit_timezone", "movebank_utc"),
        default="explicit_timezone",
    )
    args = parser.parse_args()
    write_summary(
        args.movement_csv,
        args.output,
        timestamp_semantics=args.timestamp_semantics,
    )


if __name__ == "__main__":
    main()

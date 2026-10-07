from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.yht_spatial_warning_forecast import write_result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the frozen Ya Ha Tinda rolling-origin M0/M1 forecast comparison."
    )
    parser.add_argument("--normalized-csv", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    write_result(args.normalized_csv, args.output)


if __name__ == "__main__":
    main()

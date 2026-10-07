from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.svalbard_spatial_warning import write


def main() -> None:
    parser = argparse.ArgumentParser(description="Run frozen Svalbard Love-Otto future-population validation.")
    parser.add_argument("--gps-csv", required=True)
    parser.add_argument("--abundance-xlsx", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    write(args.gps_csv, args.abundance_xlsx, args.output)


if __name__ == "__main__":
    main()

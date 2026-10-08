from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.yht_mirror_sampling_audit import write


def main() -> None:
    p = argparse.ArgumentParser(description="Outcome-free 2004 YHT teaching-mirror sampling stability audit")
    p.add_argument("--source-csv", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    write(args.source_csv, args.output)


if __name__ == "__main__":
    main()

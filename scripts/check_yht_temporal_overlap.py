from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.yht_temporal_overlap_gate import write


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check frozen Ya Ha Tinda year alignment using metadata only; never open GPS or demography rows."
    )
    parser.add_argument(
        "--protocol", default="experiments/yht_spatial_warning_protocol.json"
    )
    parser.add_argument(
        "--output", default="artifacts/yht_spatial_warning/primary_temporal_overlap_stop.json"
    )
    args = parser.parse_args()
    write(args.protocol, args.output)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.headroom_effect_scale import write


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post-hoc descriptive scale audit for the locked generation-20 headroom DID."
    )
    parser.add_argument("--records", required=True, help="Locked workflow artifact records.json")
    parser.add_argument("--output", required=True, help="Destination JSON summary")
    args = parser.parse_args()
    write(args.records, args.output)


if __name__ == "__main__":
    main()

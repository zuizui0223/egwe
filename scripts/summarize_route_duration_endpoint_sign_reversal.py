from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.route_duration_endpoint_posthoc import write


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Post-hoc audit of generation-40 endpoint benefit versus the preregistered "
            "positive-margin route-duration effect in the locked route-margin experiment."
        )
    )
    parser.add_argument("--records", required=True, help="Locked workflow artifact records.json")
    parser.add_argument("--output", required=True, help="Destination JSON summary")
    args = parser.parse_args()
    write(args.records, args.output)


if __name__ == "__main__":
    main()

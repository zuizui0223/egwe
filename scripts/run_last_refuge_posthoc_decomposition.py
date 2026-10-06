from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.last_refuge_posthoc_decomposition import write


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Post-hoc exploratory decomposition of the prospectively locked "
            "last-refuge warning holdout. This does not alter the locked primary analysis."
        )
    )
    parser.add_argument("--summary", required=True)
    parser.add_argument("--records")
    parser.add_argument("--protocol")
    args = parser.parse_args()
    write(
        summary_path=args.summary,
        records_path=args.records,
        protocol_path=args.protocol,
    )


if __name__ == "__main__":
    main()

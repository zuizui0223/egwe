from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.last_refuge_warning_holdout import write


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--records", required=True)
    args = parser.parse_args()
    write(args.summary, args.records)


if __name__ == "__main__":
    main()

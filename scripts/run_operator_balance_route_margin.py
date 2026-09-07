from __future__ import annotations

import argparse
import json
from pathlib import Path

from eco_genetic_warning_extensions.operator_balance_route_margin import initial_matched_marginal_certificate


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the exact opening operator-balance route-margin certificate.")
    parser.add_argument("--output", default="artifacts/operator_balance_route_margin/opening_certificate.json")
    args = parser.parse_args()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(initial_matched_marginal_certificate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

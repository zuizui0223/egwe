from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.headroom_mediation_followup import write


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the prospectively locked sorting-headroom follow-up.")
    parser.add_argument("--summary", default="artifacts/headroom_mediation_followup/summary.json")
    parser.add_argument("--records", default="artifacts/headroom_mediation_followup/records.json")
    args = parser.parse_args()
    write(args.summary, args.records)


if __name__ == "__main__":
    main()

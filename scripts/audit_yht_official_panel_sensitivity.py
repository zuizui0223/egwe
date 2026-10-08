from __future__ import annotations

import argparse

from eco_genetic_warning_extensions.yht_official_panel_sensitivity import write


def main() -> None:
    ap=argparse.ArgumentParser(
        description="Outcome-free official Movebank eight-year Love-Otto GPS panel-sensitivity audit."
    )
    ap.add_argument("--source-csv",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    write(args.source_csv,args.output)


if __name__=="__main__":
    main()

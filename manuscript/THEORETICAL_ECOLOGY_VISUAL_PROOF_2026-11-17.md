# Canonical PDF and figure visual-proof packet — author review adapter

**Goal.** Make the current *Theoretical Ecology* TeX-generated manuscript
reviewable page by page without creating a new scientific analysis or claiming
that an automated renderer has done a human visual inspection.

The existing reproducible paper builder already generates a XeLaTeX PDF,
editable .tex and .docx, four SVG/PNG figures and a checksum manifest.
This adapter runs **after** that build and does not alter those files.

New job outputs in the same GitHub Actions artifact:

1. `theoretical_ecology_visual_proof/all_pages_contact_sheet.jpg` —
   raster thumbnails of every page, in reading order with page numbers.
2. `theoretical_ecology_visual_proof/four_figures_contact_sheet.jpg` —
   all four manuscript figures on one review sheet.
3. `theoretical_ecology_visual_proof/pages/page-NN.jpg` —
   full preview JPEGs for each page.
4. `theoretical_ecology_visual_proof/visual_proof_manifest.json` —
   page count, PDF SHA256, raster nonblank fractions, and source figure SHA256
   plus pixel dimensions.
5. `theoretical_ecology_visual_proof/AUTHOR_REVIEW_REQUIRED.txt` —
   explicit human gating instructions.

The review proof is **separate from** the existing
`theoretical_ecology_review_packet.zip` (its checksums are
unchanged). Both are uploaded to the same GitHub Actions review artifact.
If the PDF cannot be rendered, a page is effectively blank, or an expected
figure is missing/low-resolution, the workflow fails.

**What this does not establish:** proper equation semantics, complete figure
legibility at journal scale, author agreement, permissions, or acceptance by the
publisher portal. The author still needs to view the full PDF at 100% and
approve all four figures, citations, declarations, layout and submission.
No library installation, image rendering, or contact-sheet generation changes
any frozen simulator result or authorship declaration.

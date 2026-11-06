# Binding mockup regression

**Read when:** deriving or reviewing acceptance for a supplied image, especially a conceptual raster.

This worked example models the reported failure: behavior tests and QA passed while the page's theme,
header, filters, cards and footer differed from the selected mockup. Values below illustrate a contract;
they are not claims about dimensions in the unavailable original image.

## Contract before coding

- Source: user-selected `listing-search.png`, frozen revision/hash recorded in the feature UI map.
- Intent: implement the image; binding composition. The user did not call it inspiration.
- Screen/states: `/listings`, populated and filters open at 390×844 and 1440×900; scrolled filters at
  390×844. The raster shows desktop only; record mobile stacking as an inferred adaptation.
- Hierarchy: compact brand/navigation header, title, horizontal desktop filter band, result grid,
  footer. Mobile keeps that order and stacks filter controls without hiding choices.
- Spacing/type: preserve generous section separation, compact filter gaps, prominent serif title,
  smaller sans-serif controls and card metadata; record estimated dimensions from the raster.
- Palette: light warm background, dark text, muted green accents; preserve this theme when the host
  or OS prefers dark mode. Map matching canonical tokens or create a scoped supported variant.
- Cards/media: three desktop columns, one mobile column, landscape media above name and location;
  retain crop proportions and text hierarchy. Footer remains a distinct final region.

| Region/property | Source requirement | Implementation difference | Necessity and authority | Preserved requirement / verification |
| --- | --- | --- | --- | --- |
| Results | sample listings/count | live data/count | runtime truth | card shape, metadata hierarchy and count placement |
| Filter labels | compact low-contrast text | accessible contrast and explicit labels | accessibility | control order and filter-band composition |
| Cards/media | listing photos | neutral placeholder with visible “Photo unavailable” | no verified listing photos | media geometry; no stock/generated photo presented as the listing |
| Mobile filters | desktop row only | stacked controls | inferred responsive rule | same choices, no sticky overlay blocking options |

“Directional; use project tokens” cannot replace these rows or excuse a dark page, different header,
sidebar filters, different card structure or omitted footer. A necessary material redesign goes back
to the user; a raster's uncertain exact pixels do not erase its visible composition.

## Regression walk and verdict

1. Builder captures the full page at both sizes, compares each region beside the source, corrects
   mismatches, and recaptures. Record the source, implementation revision, runtime/scale, fixtures,
   loaded fonts/assets and theme in the existing report.
2. In actual 390×844 and 1440×900 viewports, open filters and exercise choices. Scroll mobile until
   sticky controls activate; verify every choice and focused action remains visible and reachable.
   Capture the viewport in those states. A tall full-page screenshot can hide this occlusion.
3. Check the selected light palette under inherited dark preference, and inspect placeholder labels
   beside card names so media cannot be mistaken for a real listing photograph.
4. Independent Verifier opens the source and paired captures, verifies every declared pair and
   reproduces interactions when needed. Record comparison findings and a visual verdict.

| Observation with functional tests passing | Required result |
| --- | --- |
| Dark theme, replaced header, sidebar filters, redesigned cards or missing footer | FAIL: material visual contradiction |
| Sticky filter bar obscures an option or focused action | FAIL: viewport interaction defect |
| Stock/generated photo implies it shows the named real listing | FAIL: misleading media |
| Only full-page evidence; filters-open viewport uninspected | Unverified; cannot PASS |
| Raster antialiasing differs; recorded composition and permitted adaptations match | PASS after independent inspection |

Put contradictions or missing pairs in the existing binding-source table; retain behavioral results
separately. The `Visual fidelity` report table records Source, Screen/state, Viewport, Captures,
Comparison and Result. The validator rejects missing/blank evidence or non-PASS rows; it cannot judge
pixels or establish that an agent actually inspected an image.

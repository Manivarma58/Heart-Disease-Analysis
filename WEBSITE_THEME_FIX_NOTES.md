# CardioViz unified-shell correction

The D: project is read-only from this sandbox, so apply these changes to app/__init__.py when write access is available:

- Replace Material Symbols ligature names in `links` with short codes: DB, AN, ST, TR, SQL, KN, SP, SE, UP.
- Remove the Google Material Symbols @import from the injected shell style.
- Style `.cv-shell-link-icon` as a fixed 2rem badge so icon text can never overlap labels.
- Add light-theme overrides for `.viz-page`, `.viz-card`, `.viz-kpis article`, `.viz-legend`, `.story-scene`, `.tableau-frame`, `.panel`, and `.patient-card`.

<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Safe data handling and publication

Reviewed 2026-11-01.

This is an operator checklist for local FreeCAD monohull and catamaran guide-geometry experiments, not a claim that these controls
are automatically enforced by the code.

1. Run the generators in a disposable FreeCAD session. Review document names and
   close or save unrelated work before rerunning a generator.
2. Use invented labels and dimensions for public demonstrations. Inspect the document
   property editor and exported metadata before sharing a saved model.
3. Capture only the relevant geometry when taking screenshots. Omit personal paths,
   project tabs, recent-file lists and unrelated proprietary models.
4. Keep local FreeCAD preferences, add-ons and application logs separate from a public
   source archive. Review their own storage and network settings.
5. Inspect the staged diff before publication; a geometrically valid model can still
   contain information that should not be published.

There is no project deletion service or retention timer for local documents and exports.
Removing a local model does not remove copies already published or backed up.

## Review before publishing

Check the complete staged diff and all attachments, not just source extensions. Reject
secrets, real customer records, personal documents and unexplained binary exports.
Use synthetic reproductions in public discussions. If information is already public,
contact AEKR through [the privacy notice](../PRIVACY.md); changing the current file
does not erase Git history or third-party copies. Rotate an exposed credential through
its provider rather than relying on a later Git deletion.

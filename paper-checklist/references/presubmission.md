# Pre-submission Requirements

Take every value from the current venue's template and call for papers. Values differ between venues and between years of one venue.

## Contents

- Page budget
- Statements and checklists
- Anonymous mode
- PDF properties
- Supplementary material
- Final state of the source

## Page budget

- Locate the last page of the main body on the rendered PDF, or read the page of an end-of-body label from the `.aux` file.
- Compare it with the limit. Check what the venue counts: references, statements, appendix, and whether the appendix may sit in the same PDF. When the venue's documents disagree, check against the stricter value and name both.
- A body that ends past the limit is a blocking row owned by paper-typesetting, whose page-budget order decides the fix.

## Statements and checklists

- Find which statements the venue requires, such as ethics, reproducibility, broader impact, limitations or LLM usage, and whether each is mandatory.
- Check where each must sit: after the main body, before the references, or starting on the page after the limit.
- Check whether the venue requires a filled checklist inside the PDF, such as a paper checklist after the appendix, and that every item is answered.
- A missing mandatory statement or checklist is a blocking row.

## Anonymous mode

- The template's anonymous option is on, and the rendered first page shows no names.
- Acknowledgments and funding lines are absent or hidden.
- Self-citations are written in the third person.
- Code and data links point to anonymized hosts or say they will be released.

## PDF properties

```
pdfinfo main.pdf           # Title, Author, Creator, Pages, page size
pdffonts main.pdf          # every font must show "yes" under emb
```

- No author name in metadata for an anonymous submission.
- Every font is embedded. Some venues also reject Type 3 fonts. When the venue says nothing about them, Type 3 fonts pass.
- Page size matches the template, such as US Letter.
- The file is within the venue's size limit. Large raster figures are the usual cause of an oversized file.

## Supplementary material

- The supplement holds only what the venue allows, within its size limit.
- Every file is anonymous, including code comments, notebook outputs, configuration files with user paths, and license headers.
- No `.git` directory, cache directory or credentials file is included.
- Content referenced from the main paper as being in the supplement is actually there.

## Final state of the source

- No undefined references or citations in the final build log, and no `??` on any page. Without a build log, search the PDF text for `??` and `[?]`, and list the log under what was not checked.
- No pending markers, `\todo` notes, comment macros that render visibly, or colored revision marks.
- No draft options such as `draft`, line numbers that the venue does not require, or visible overfull markers.
- The source that will be uploaded, if the venue asks for source, compiles on its own. It contains every included figure and style file, and no local absolute paths.

# Résumé

Run `npm ci` after cloning to install Husky and activate the commit hook.
Commit subjects must use `feat|chore|fix|wip(scope): summary`, for example
`fix(resume): correct employment dates`. Merge commits are allowed.

Edit `resume.html`, then regenerate `resume.pdf`:

```sh
python3 generate_pdf.py
```

Requires Python 3.8+, Chrome/Chromium, and `pdfinfo` (Ubuntu: `poppler-utils`).
Set `CHROME_BIN` to use a specific browser executable. The script works from any
working directory and uses a temporary browser profile.

A4 portrait paper, 10 mm margins, and print layout are defined in `resume.html`.
The generator disables browser headers/footers and checks that the result is
exactly one A4 page before replacing `resume.pdf`.

For restricted environments where Chrome's sandbox cannot run:

```sh
python3 generate_pdf.py --no-sandbox
```

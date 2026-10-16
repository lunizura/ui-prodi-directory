# Contributing to Universitas Indonesia (UI) Study Programs Directory

Thank you for your interest in contributing to the **Universitas Indonesia Study Programs & Accreditation Directory**. We welcome corrections, curriculum updates, and code enhancements from students, researchers, alumni, and academic counselors.

---

## 1. Golden Rules & Code Hygiene

1. **Strict Zero-Emoji Policy:** All source files, comments, markdown documentation, issue templates, and Git commit messages must strictly contain zero emoji characters.
2. **Conventional Commits:** Follow the conventional commit format:
   - `docs:` for documentation, guides, or README updates.
   - `feat:` for new UI capabilities, filters, or dataset attributes.
   - `fix:` for data corrections, broken links, or UI bug fixes.
   - `test:` for test additions or validation assertions.
   - `chore:` for repository maintenance, dependencies, or configuration.
3. **Data Parity:** Any modifications to academic programs must be reflected across all three data formats: `data/ui_prodi.json`, `data/ui_prodi.js`, and `data/ui_prodi.csv`.

---

## 2. Local Development & Testing

Run the automated test suite before opening any pull request:

```bash
# Execute unit tests across dataset integrity, DOM contracts, and zero-emoji compliance
python -m unittest discover tests
```

All 8 test cases must pass with `OK` status.

---

## 3. Pull Request Guidelines

1. Fork the repository and create a descriptive branch:
   ```bash
   git checkout -b docs/add-faculty-profile
   ```
2. Verify changes locally with the test suite.
3. Submit a Pull Request targeting the `main` branch with a clear description of the data source (official UI admission portal or BAN-PT/LAM-PTKes registry).

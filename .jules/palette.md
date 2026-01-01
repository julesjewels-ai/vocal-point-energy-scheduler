## 2024-05-23 - Handle Empty Input Gracefully
**Learning:** Users running CLI apps may accidentally press Enter or input only whitespace. Processing this as valid data (e.g. "Medium" energy) degrades data quality and confuses the user.
**Action:** Always validate input for empty/whitespace content. If empty, provide a friendly, specific error message explaining what is needed and exit gracefully (or prompt again if interactive loop is supported).

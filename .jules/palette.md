## 2024-05-23 - Micro-UX in CLI Applications
**Learning:** Even in simple CLI tools, handling empty input and `KeyboardInterrupt` (Ctrl+C) gracefully transforms the experience from "script-like" to "app-like". Users expect software to anticipate their mistakes (like hitting Enter too early) or their desire to quit without crashing.
**Action:** Always wrap interactive CLI `input()` calls in a try-except block for `KeyboardInterrupt` and validate input immediately, providing clear feedback or a clean exit path.

## 2024-05-23 - Destructive Actions in CLI
**Learning:** Destructive actions (like clearing all data) should never happen immediately upon a flag invocation. Users often explore flags or copy-paste commands without full context. Immediate destruction is a "hostile" UX pattern.
**Action:** Always implement a confirmation prompt (y/N) for destructive CLI operations, defaulting to 'No' (safety first).

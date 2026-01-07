## 2024-05-23 - Micro-UX in CLI Applications
**Learning:** Even in simple CLI tools, handling empty input and `KeyboardInterrupt` (Ctrl+C) gracefully transforms the experience from "script-like" to "app-like". Users expect software to anticipate their mistakes (like hitting Enter too early) or their desire to quit without crashing.
**Action:** Always wrap interactive CLI `input()` calls in a try-except block for `KeyboardInterrupt` and validate input immediately, providing clear feedback or a clean exit path.

## 2024-05-24 - Accessibility in Dynamic Web Interfaces
**Learning:** Dynamic status updates (like "Listening...", "Processing...") are invisible to screen readers unless explicitly marked with `aria-live`. Adding `aria-live="polite"` to status containers and `aria-pressed` to toggle buttons drastically improves the experience for non-visual users without changing the visual design.
**Action:** Always add `aria-live` regions for dynamic status text and ensure toggle buttons use `aria-pressed` to communicate state.

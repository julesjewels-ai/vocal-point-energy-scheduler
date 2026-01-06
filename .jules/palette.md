## 2024-05-23 - Micro-UX in CLI Applications
**Learning:** Even in simple CLI tools, handling empty input and `KeyboardInterrupt` (Ctrl+C) gracefully transforms the experience from "script-like" to "app-like". Users expect software to anticipate their mistakes (like hitting Enter too early) or their desire to quit without crashing.
**Action:** Always wrap interactive CLI `input()` calls in a try-except block for `KeyboardInterrupt` and validate input immediately, providing clear feedback or a clean exit path.

## 2024-05-24 - Accessibility for Dynamic Status
**Learning:** Screen reader users often miss status updates (like "Processing..." or "Error") if they are just text changes. Adding `aria-live="polite"` makes these updates audible without interrupting the user's flow, significantly improving the experience for non-visual users.
**Action:** Identify dynamic status text containers and add `role="status"` and `aria-live="polite"` attributes.

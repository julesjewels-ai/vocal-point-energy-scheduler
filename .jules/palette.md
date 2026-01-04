## 2024-05-23 - Micro-UX in CLI Applications
**Learning:** Even in simple CLI tools, handling empty input and `KeyboardInterrupt` (Ctrl+C) gracefully transforms the experience from "script-like" to "app-like". Users expect software to anticipate their mistakes (like hitting Enter too early) or their desire to quit without crashing.
**Action:** Always wrap interactive CLI `input()` calls in a try-except block for `KeyboardInterrupt` and validate input immediately, providing clear feedback or a clean exit path.

## 2024-05-24 - Accessibility in Simple Web Apps
**Learning:** Even small single-page apps need explicit keyboard navigation support. Adding a simple `:focus-visible` style and "Skip to content" link drastically improves usability for keyboard users without affecting the visual design for mouse users.
**Action:** Always verify `tab` index order and visual focus states, especially when custom styles reset browser defaults.

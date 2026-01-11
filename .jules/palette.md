## 2024-05-23 - Micro-UX in CLI Applications
**Learning:** Even in simple CLI tools, handling empty input and `KeyboardInterrupt` (Ctrl+C) gracefully transforms the experience from "script-like" to "app-like". Users expect software to anticipate their mistakes (like hitting Enter too early) or their desire to quit without crashing.
**Action:** Always wrap interactive CLI `input()` calls in a try-except block for `KeyboardInterrupt` and validate input immediately, providing clear feedback or a clean exit path.

## 2024-05-24 - Focus Indicators on Custom Shapes
**Learning:** Default browser focus rings (usually rectangular) clash visually with custom circular elements like round action buttons, degrading the perceived quality of the interface.
**Action:** Use `:focus-visible` with `outline-offset` and `border-radius` (if using box-shadow) or ensure the outline follows the shape, or use a custom outline style that complements the design system colors.

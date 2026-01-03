# Testing Guide for VocalPoint

VocalPoint uses a combination of automated unit tests and manual CLI-based testing to ensure reliability and accuracy in energy level detection.

## Automated Testing

We use Python's built-in `unittest` framework for automated testing.

> [!IMPORTANT]
> Always ensure your virtual environment is activated before running tests:
> `source .venv/bin/activate`

### Running All Tests
To run all tests in the `tests` directory, execute the following command from the project root:

```bash
python3 -m unittest discover tests
```

### Test Structure
- `tests/test_analyzer.py`: Tests the core energy analysis logic.
- `tests/test_storage.py`: Tests data persistence.
- `tests/test_feedback.py`: Tests the feedback generation logic.
- `tests/test_validation.py`: Tests input validation and security (e.g., massive input, invalid ranges).
- `tests/test_ux_interaction.py`: Tests CLI interaction patterns.

---

## Manual Testing

You can manually test the application by running it in interactive mode or by providing CLI arguments.

### Interactive Mode
Run the application without arguments to start the interactive logger:

```bash
python3 -m src.main
```
Follow the prompts to enter your feelings and see the detected energy level.

### Command Line Arguments
You can simulate specific scenarios using CLI flags:

| Flag | Description | Example |
|------|-------------|---------|
| `--text` | Simulation of audio transcription | `--text "I am feeling very productive"` |
| `--pace` | Words per minute (default 130) | `--pace 160` |
| `--tone` | Tone valence -1.0 to 1.0 (default 0.0) | `--tone 0.5` |
| `--clear` | Clear all stored history | `--clear` |

### Expected Outputs
- **High Energy (⚡)**: Detected when text contains energetic keywords (e.g., "excited", "ready") or pace/tone are high.
- **Medium Energy (🌊)**: Detected for neutral logs or mixed signals.
- **Low Energy (☕)**: Detected when text contains fatigue keywords (e.g., "tired", "exhausted") or pace/tone are low.

---

## Troubleshooting

If you encounter a `ModuleNotFoundError: No module named 'src'`, ensure you are running the application using the `-m` flag from the project root:
`python3 -m src.main`

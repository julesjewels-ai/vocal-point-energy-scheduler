# VocalPoint: AI Energy-Based Scheduler

A privacy-first mobile application that replaces traditional time-blocking with energy-blocking. Users record brief, stream-of-consciousness audio logs throughout their day. The app uses on-device AI to analyze vocal biomarkers (tone, pace, prosody) and semantic context to quantify cognitive load and emotional energy levels. It then connects to calendar APIs to dynamically rearrange task lists and meeting suggestions, ensuring high-focus work is scheduled during peak energy windows and administrative tasks are offloaded to detected low-energy periods.

## Getting Started

### Prerequisites
- Python 3.8 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vocal-point-energy-scheduler
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application in interactive mode:
```bash
python3 -m src.main
```

## Documentation
- [Testing Guide](docs/testing_guide.md)
# ExoWorlds — starter project

A small Streamlit application for exploring confirmed exoplanets and experimenting with hypothetical worlds.

## 1. Requirements

- Python 3.10 or newer
- Internet connection for live NASA data (the app has a small offline fallback)

## 2. Setup

Open a terminal in this project folder.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run Home.py
```

If PowerShell blocks activation, use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run Home.py
```

Streamlit should open the app in your browser, usually at http://localhost:8501.

## 3. Project structure

```text
exoworlds_starter/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── exoplanets_sample.csv
├── src/
│   └── data.py
└── pages/
    ├── 1_Universe_Explorer.py
    ├── 2_Planet_Observatory.py
    └── 3_World_Builder.py
```

## 4. Data source

Live planet data is requested from the NASA Exoplanet Archive TAP service, using the `pscomppars` table. A bundled sample CSV is used if the network request fails.

NASA documentation:
https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html

## 5. Suggested team split

- Person A: `src/data.py` and Universe Explorer data/filtering.
- Person B: page layout, Planet Observatory and World Builder visuals.
- Both: agree before changing shared column names or the selected-planet session-state key.

## 6. Important scientific note

The World Builder score is an explicitly labelled illustrative heuristic. It is not a scientific habitability probability or a NASA metric. Missing archive values are displayed as unavailable, not guessed.

# ExoWorlds
## 1. Requirements
- Python 3.10 or newer
- Internet connection for live NASA data

## 2. Setup

Open a terminal in this project folder.

### Windows PowerShell

```powershell
python -m pip install -r requirements.txt
streamlit run Home.py
```

OR USE the website at https://ewe-space.streamlit.app/


Streamlit should open the app in your browser, usually at http://localhost:8501.

## 4. Data source

Live planet data is requested from the NASA Exoplanet Archive TAP service, using the `pscomppars` table.

NASA documentation:
https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html

## 6. Notes

World Engineer score is a demo only — not a NASA or scientific habitability metric. Missing archive values stay blank; we don't invent them.

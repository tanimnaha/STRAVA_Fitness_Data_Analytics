"""
STRAVA Fitness Data Analytics — Root Entrypoint for Streamlit Cloud Deployment.
Redirects execution to streamlit_app/app.py.
"""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / 'streamlit_app' / 'app.py'
runpy.run_path(str(target), run_name='__main__')

@echo off
python -m streamlit run --server.headless true --browser.gatherUsageStats=false --theme.base="dark" --theme.primaryColor="#4bb6ff" --server.enableXsrfProtection=false set_web.py
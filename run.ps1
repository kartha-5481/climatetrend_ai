Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Starting ClimateTrend AI - Weather Warehouse Dashboard" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "[ERROR] Virtual environment 'venv' not found!" -ForegroundColor Red
    exit 1
}

& ".\venv\Scripts\Activate.ps1"
Write-Host "[INFO] Virtual environment activated." -ForegroundColor Green
Write-Host "[INFO] Launching Streamlit on http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
streamlit run app.py

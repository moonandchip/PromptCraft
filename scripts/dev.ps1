$root = Split-Path -Parent $PSScriptRoot

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; cd backend; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root`"; cd frontend; npm run dev"
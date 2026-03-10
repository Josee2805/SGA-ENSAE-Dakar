# setup.ps1
# Script PowerShell - Installation SGA ENSAE Paris
# Executer : .\setup.ps1

Write-Host ""
Write-Host "  =============================================" -ForegroundColor DarkRed
Write-Host "   SGA ENSAE Paris - Installation du projet   " -ForegroundColor White
Write-Host "  =============================================" -ForegroundColor DarkRed
Write-Host ""

# 1. Structure dossiers
Write-Host "[1/4] Creation de la structure..." -ForegroundColor Yellow
$folders = @("SGA", "SGA\models", "SGA\pages", "SGA\utils", "SGA\data", "SGA\assets")
foreach ($f in $folders) {
    if (-not (Test-Path $f)) { New-Item -ItemType Directory -Path $f | Out-Null }
}
Write-Host "  OK - Structure creee" -ForegroundColor Green

# 2. Python
Write-Host "[2/4] Verification Python..." -ForegroundColor Yellow
try {
    $v = python --version 2>&1
    Write-Host "  OK - $v detecte" -ForegroundColor Green
} catch {
    Write-Host "  ERREUR : Python non installe. Telecharger sur https://python.org" -ForegroundColor Red
    exit 1
}

# 3. Environnement virtuel
Write-Host "[3/4] Creation de l'environnement virtuel..." -ForegroundColor Yellow
if (-not (Test-Path "SGA\venv")) {
    python -m venv SGA\venv
    Write-Host "  OK - venv cree dans SGA\venv" -ForegroundColor Green
} else {
    Write-Host "  OK - venv existant conserve" -ForegroundColor Gray
}

# 4. Dependances
Write-Host "[4/4] Installation des dependances..." -ForegroundColor Yellow
& "SGA\venv\Scripts\Activate.ps1"
pip install -r SGA\requirements.txt -q
Write-Host "  OK - Toutes les dependances installees" -ForegroundColor Green

Write-Host ""
Write-Host "  =============================================" -ForegroundColor DarkRed
Write-Host "   Installation terminee avec succes !" -ForegroundColor White
Write-Host "  =============================================" -ForegroundColor DarkRed
Write-Host ""
Write-Host "  Pour lancer l'application :" -ForegroundColor Cyan
Write-Host ""
Write-Host "    cd SGA" -ForegroundColor White
Write-Host "    ..\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "    python app.py" -ForegroundColor White
Write-Host ""
Write-Host "  Puis ouvrir : http://localhost:8050" -ForegroundColor Green
Write-Host ""
Write-Host "  Comptes de demo :" -ForegroundColor Cyan
Write-Host "    admin / ensae2026" -ForegroundColor White
Write-Host "    papa.tata / sga2025" -ForegroundColor White
Write-Host ""

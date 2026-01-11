@echo off
echo ========================================
echo  Ternarius Atlas - Setup para Windows
echo  Otimizado para NVIDIA RTX 3050
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.10 ou 3.11 de: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante instalacao
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM Create virtual environment
echo [1/5] Criando ambiente virtual...
if exist venv (
    echo Ambiente virtual ja existe, pulando...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado
)
echo.

REM Activate virtual environment
echo [2/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual
    pause
    exit /b 1
)
echo [OK] Ambiente ativado
echo.

REM Upgrade pip
echo [3/5] Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Install PyTorch with CUDA support
echo [4/5] Instalando PyTorch com suporte CUDA para RTX 3050...
echo Isso pode levar alguns minutos...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 (
    echo [ERRO] Falha ao instalar PyTorch
    pause
    exit /b 1
)
echo [OK] PyTorch instalado com suporte CUDA
echo.

REM Install Stable Diffusion and dependencies
echo [5/5] Instalando Stable Diffusion e dependencias...
pip install diffusers transformers accelerate safetensors xformers scipy ftfy
if errorlevel 1 (
    echo [AVISO] Algumas dependencias podem ter falhado, mas vamos continuar...
)
echo.

REM Install project requirements
if exist requirements.txt (
    echo Instalando dependencias do projeto...
    pip install -r requirements.txt
)
echo.

REM Test GPU
echo ========================================
echo  Testando GPU...
echo ========================================
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA disponivel:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Nenhuma')"
echo.

REM Create test script
echo import torch > test_gpu.py
echo import sys >> test_gpu.py
echo. >> test_gpu.py
echo print("="*60) >> test_gpu.py
echo print("DIAGNOSTICO DA GPU") >> test_gpu.py
echo print("="*60) >> test_gpu.py
echo print(f"PyTorch version: {torch.__version__}") >> test_gpu.py
echo print(f"CUDA available: {torch.cuda.is_available()}") >> test_gpu.py
echo if torch.cuda.is_available(): >> test_gpu.py
echo     print(f"CUDA version: {torch.version.cuda}") >> test_gpu.py
echo     print(f"GPU: {torch.cuda.get_device_name(0)}") >> test_gpu.py
echo     print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB") >> test_gpu.py
echo     print(f"") >> test_gpu.py
echo     print("[OK] GPU pronta para usar!") >> test_gpu.py
echo else: >> test_gpu.py
echo     print("[ERRO] CUDA nao disponivel. Verifique drivers NVIDIA.") >> test_gpu.py
echo     sys.exit(1) >> test_gpu.py

echo ========================================
echo  INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Proximos passos:
echo 1. Sempre ative o ambiente antes de usar:
echo    venv\Scripts\activate
echo.
echo 2. Execute o gerador de e-books:
echo    python main.py
echo.
echo 3. Ou teste a GPU:
echo    python test_gpu.py
echo.
echo 4. Documentacao completa: SETUP_LOCAL_WINDOWS.md
echo.
echo Sua RTX 3050 esta pronta para gerar imagens!
echo.
pause

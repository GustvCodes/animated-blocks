@echo off
echo Verificando se o Python está instalado...

:: Verifica se o Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python não encontrado. Por favor, instale o Python primeiro.
    pause
    exit /b
)

echo Python encontrado! Verificando as dependências...

:: Verifica se o Pip está instalado
python -m ensurepip --upgrade >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip não encontrado. Instalando pip...
    python -m ensurepip
)

:: Atualiza o pip para a versão mais recente
echo Atualizando o pip...
python -m pip install --upgrade pip

:: Instalando Pillow e outras dependências
echo Instalando Pillow...
python -m pip install Pillow

echo Instalando imageio...
python -m pip install imageio

echo Instalando moviepy...
python -m pip install moviepy

:: Verifica se as bibliotecas foram instaladas com sucesso
echo Verificando se o Pillow foi instalado corretamente...
python -c "from PIL import Image; print('Pillow está instalado corretamente!')"

IF %ERRORLEVEL% NEQ 0 (
    echo Erro ao instalar o Pillow. Verifique a instalação.
    pause
    exit /b
)

echo Dependências instaladas com sucesso!

:: Agora executa o script Python
echo Executando o script Python...
python ob_animada.py

:: Finaliza
pause

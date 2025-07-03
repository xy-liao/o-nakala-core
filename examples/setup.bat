@echo off
REM Setup script for O-Nakala Core Examples (Windows)

echo Setting up O-Nakala Core Examples environment...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete!
echo.
echo To use the examples:
echo 1. Activate the environment: venv\Scripts\activate.bat
echo 2. Start Jupyter: jupyter lab
echo 3. Open notebooks/workflow_notebook.ipynb
echo.
echo Ready to run O-Nakala Core workflows!
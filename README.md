# co2e-calculator
Calculates Carbon Dioxide equivalent based on Ceva's website

## To run the program
- Create an environment (make sure you are in the directory):
    py venv -m venv
    pip install -r requirements.txt

- Run this in the CLI to create an .exe file in a folder called "dist":
    pyinstaller run_main.py --hidden-import openpyxl.cell._writer --onefile --name co2e-calculator-Executable
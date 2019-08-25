# Bachelorarbeit "Untersuchung von Möglichkeiten zur Datenprofilierung von Open Data im Kontext von Ernährungssicherheit"

Interaktives Jupyter Notebook (voilà Dashboard) als prototypische Implementierung analysierter Data Profiling Möglichkeiten zur Unterstützung der Evaluation von Nützlichkeit und Qualität der in Food Security Portal (foodescurityportal.org/api) enthaltenen Datensätze. 

### Installationsanleitung

-> Anaconda3 muss installiert sein (siehe https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

1. Anaconda Prompt in Terminal starten
2. in Verzeichnis 'Code-BA_DataProfiling_OpenData' navigieren
3. im Terminal virtuelle Anaconda - Umgebung importieren und herstellen mit
    `conda env create -f environment.yaml`
    - Falls Import scheitert, plattformabhängige environment Version importieren (environment_mac.yaml/ environment_windows.yaml/ environment_linux.yaml)
3. conda environment aktivieren mit `conda activate thesis_lisa_koeritz` (bei plattformbhängigen `_mac`/`_windows`/`_linux` anhängen)
4. Voilà Dashboard starten mit `voila DataProfiling_FoodSecurity_Prototype.ipynb`

   Jupyter Notebook starten mit `jupyter notebook DataProfiling_FoodSecurity_Prototype.ipynb`
   --> Dashboard über Voilà Button in Jupyter Notebook startbar

### Test
Testdateien als test_ bezeichnet. Verwendete Mockdaten liegen unter /testdata.
- Alle in virtueller Anacoda-Umgebung ausführbar mit pytest Framework über `pytest`

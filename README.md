# smart_trading_assisstant
## Steps to execute
* use python 3.12 for running app
* in project root, install all the requirements
```bash
pip install -r requirements.txt
```
* run example backtest
```bash
python -m examples.run_backtest_example
```
* set environment variable ```PYTHONPATH``` to project root system path, replace ```project_path``` with the full path to the proect root
```bash
# in powershell
$env:PYTHONPATH="project_path"
# in cmd
set PYTHONPATH=project_path
# in bash
export PYTHONPATH=project_path
```
* run steamlit ui
```bash
streamlit run src/ui_streamlit.py
```

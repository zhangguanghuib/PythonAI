### 1. Create a folder called langgraph
```ps
uv venv venvLangGraph --python 3.13
.\venvLangGraph\Scripts\activate
python --version  
```
### 2. If you use "pip" got the error " No module named pip"
```
(venvLangGraph) PS C:\D\Python\PythonAI\langgraph> .\venvLangGraph\Scripts\python.exe -m pip install -r .\requirements.txt     
C:\D\Python\PythonAI\langgraph\venvLangGraph\Scripts\python.exe: No module named pip
```
Please run this command to install the module
```ps
.\venvLangGraph\Scripts\python.exe -m ensurepip --upgrade  
```
Untill you see<br/>
<img width="442" height="61" alt="image" src="https://github.com/user-attachments/assets/a611927e-aa72-498d-a6e8-021309880493" /><br/>

### 3. Install the packages
```
.\venvLangGraph\Scripts\python.exe -m pip install -r .\requirements.txt
```
Here please make sure you use the python.exe from virtual environment to install all the packages, otherwise the packages will be installed the global python environment

Finally see the package are instalelling:<br/>
<img width="1853" height="1556" alt="image" src="https://github.com/user-attachments/assets/0d27e75e-9972-4d1a-8856-c58a30746372" />

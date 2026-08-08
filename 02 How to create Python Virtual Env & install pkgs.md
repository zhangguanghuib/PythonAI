<img width="1710" height="517" alt="image" src="https://github.com/user-attachments/assets/e0ac0959-f217-49ac-91f8-ef695b8fefbc" />### 1. Create a folder called langgraph
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

Finally see the package are installing:<br/>
<img width="1853" height="1556" alt="image" src="https://github.com/user-attachments/assets/0d27e75e-9972-4d1a-8856-c58a30746372" />

Wait some minutes, you can see the packages are installed:<br/>
<img width="1917" height="1556" alt="image" src="https://github.com/user-attachments/assets/c4b0de65-1d13-4dba-bf15-67a7c310be88" />

### 4.  Test
.env file is:
```
DASHSCOPE_API_KEY=sk-*************************K0
BAILIAN_MODEL=deepseek-v4-flash
BAILIAN_BASE_URL=https://llm-553bcdr8n87xlijd.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```
main.py
```
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    model = ChatOpenAI(
        model=os.getenv("BAILIAN_MODEL", "deepseek-v3.2"),
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url=os.environ["BAILIAN_BASE_URL"],
    )

    response = model.invoke("Explain LangGraph in two sentences.")
    print(response.content)
```

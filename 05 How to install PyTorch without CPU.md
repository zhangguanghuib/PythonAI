# PyTorch

```
.\venvLangGraph\Scripts\python.exe -m pip install torch torchvision torchaudio `
    --index-url https://download.pytorch.org/whl/cpu `
    --extra-index-url https://packagefeedproxy.microsoft.io/pypi/simple/
```
```python
import torch

print("PyTorch version:", torch.__version__)  # Installed: 2.14.1+cpu

x = torch.tensor([1.0, 2.0, 3.0], device="cpu")
print("Device:", x.device)  # cpu
print("Result:", x * 2)     # tensor([2., 4., 6.])
```

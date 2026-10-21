# Instala Wan2GP en el PC NVIDIA. Revisa el README del repo para la version exacta de torch/CUDA.
param([string]$Dir = 'C:\AI\Wan2GP')
git clone https://github.com/deepbeepmeep/Wan2GP $Dir
Set-Location $Dir
# El README recomienda Python 3.10 y torch con CUDA; ajusta segun tu GPU (ver Wan2GP\README.md).
uv venv --python 3.10 venv
& "$Dir\venv\Scripts\python.exe" -m ensurepip
Write-Host "Ahora sigue 'Installation' del README de Wan2GP dentro de $Dir\venv, luego: python wgp.py --help"

✅ This guide is for **developers** who want to contribute or modify NO_ONX. PRs and bug reports are welcome on Telegram group
---
# NO_ONX
**NO_ONX** is a lightweight yet powerful toolkit designed for **analysis**, **investigation**, and **security monitoring** on Windows systems. 
<p align="center">
  <a href="https://github.com/DevStatesSmp/NO_ONX-old">
    <img src="https://github.com/user-attachments/assets/dd3b4b8d-ec74-429b-a629-2c1b1f3d6aac" width="200" alt="NO_ONX Logo" title="NO_ONX - Lightweight Security Tool" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/DevStatesSmp/NO_ONX/releases/tag/beta-v0.3.1">
    <img src="https://img.shields.io/badge/NO_ONX-v0.3.1%20Beta-orange?style=flat-square" alt="Latest Release" />
  </a>
  &nbsp;&nbsp;
  <a href="https://t.me/+-hUpHRhvj9wyYmE1">
    <img src="https://img.shields.io/badge/Telegram-Bug%20report%20and%20feedback-blue?style=flat-square" alt="Telegram" />
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/DevStatesSmp/NO_ONX/blob/main/CHANGELOG.md">
    <img src="https://img.shields.io/badge/Changelog-Click%20me!-red?style=flat-square" alt="Changelog" />
  </a>
</p>

<br/>

---

## 📦 Install NO_ONX

(Make sure that you have installed Python and Git)<br>
Use git clone:

```bash
git clone https://github.com/DevStatesSmp/NO_ONX
```

Go to folder containing NO_ONX file and use this command:

```bash
pip install -r requirements.txt
```

---

## 🛠️ HOW TO BUILD

(Make sure you had installed `PyInstaller` before and `noonx_shell.spec` is not deleted)<br>

```bashrc
pyinstaller --onefile --hidden-import=encodings --icon=...\NO_ONX\noonx.ico src\noonx_shell.py
```

If `noonx_shell.spec` not exists or got deleted then make another one with this code: (named it noonx_shell.spec)
```bashrc
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\noonx_shell.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['encodings'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='noonx_shell',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['...\\NO_ONX\\noonx.ico'], # Change into your NO_ONX icon path
)
```

---

## 🧩 Plugin Development Guide

1. Go to the `plugin/` folder.
2. Create a new file, Ex: `my_plugin.py`.
3. Write the plugin function like this:

```python
def execute(args=None): # execute function is required
    print("Example command")
```

4. Run it via terminal:

```bash
nnx --plugin my_plugin.py
```

# NO_ONX
<a href="https://github.com/DevStatesSmp/NO_ONX">
  <img title="NO_ONX - Investigate and Protect!" src="https://github.com/user-attachments/assets/55d0ce25-e7c7-49e0-a3c8-49d48660179c" width="200" alt="NO_ONX Logo" />
</a>
<br>

<a href="https://github.com/DevStatesSmp/NO_ONX/releases/tag/beta-v0.2.9">
  <img src="https://img.shields.io/badge/NO_ONX-v0.2.9%20Beta-orange?style=flat-square" alt="NO_ONX latest release" title="NO_ONX latest release" />
</a>
<a href="https://github.com/DevStatesSmp/NO_ONX/blob/main/CHANGELOG.md">
  <img src="https://img.shields.io/badge/Changelog-Click me!-blue?style=flat-square" alt="NO_ONX Changelog" title="NO_ONX Changelog" />
</a>



<br>

NO_ONX is a lightweight tool but useful to analysis, investigattion, security monitoring for Window<br>
[WARNING: The v0.2.9 beta is the final update and no more support]

## Requirement
- OS: Window 10+ (can be lower than Window 10)
- Python: 3.1x

## Install NO_ONX
(Make sure that you have installed Python and Git)<br>
Go to .../window-version/ and use this command:
```bash
pip install -r requirement.txt # for window
```

Use git clone:
```bash
git clone https://github.com/DevStatesSmp/NO_ONX
```

Or if you prefer to download a specific version manually, visit the [Releases page](https://github.com/DevStatesSmp/NO_ONX/releases) and download the latest version.

## NO_ONX Command structure (until v0.2.9 Beta)
NO_ONX <br>
├── Main Options <br>
│   ├── --help <br>
│   ├── -h <br>
│   ├── --system_info <br>
│   ├── -si <br> 
│   ├── --version<br>
│   └── -v<br>
│<br>
├── File Information (::modify module)<br>
│   ├── --readfile<br>
│   ├── --file_info<br>
│   ├── --file_hash<br>
│   ├── --dir_info<br>
│   ├── --file_list<br>
│   ├── --symlink_info<br>
│   ├── --extended_info<br>
│   ├── --scan_dir<br>
│   ├── --check_permission<br>
│   └── --hidden_file_info<br>
│<br>
├── Modify (::modify module)<br>
│   ├── --modify_file_permission<br>
│   ├── --modify_file_content<br>
│   ├── --modify_file_name<br>
│   ├── --modify_file_metadata<br>
│   ├── --modify_file_line<br>
│   ├── --modify_file_symlink<br>
│   ├── --modify_directory<br>
│   ├── --modify_directory_permissions<br>
│   └── --modify_file_owner<br>
│<br>
├── Other<br>
│   ├── --compare --mode<br>
│   └── --backup<br>

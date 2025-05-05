# NO_ONX
<a href="https://github.com/DevStatesSmp/NO_ONX">
  <img title="NO_ONX - Investigate and Protect!" src="https://github.com/user-attachments/assets/55d0ce25-e7c7-49e0-a3c8-49d48660179c" width="200" alt="NO_ONX Logo" />
</a>
<br>

<a href="https://github.com/DevStatesSmp/NO_ONX/releases">
  <img src="https://img.shields.io/badge/NO_ONX-v0.2.8%20Beta-orange?style=flat-square" alt="NO_ONX latest release" title="NO_ONX latest release" />
</a>
<a href="https://github.com/DevStatesSmp/NO_ONX/blob/main/CHANGELOG.md">
  <img src="https://img.shields.io/badge/Changelog-Click me!-blue?style=flat-square" alt="NO_ONX Changelog" title="NO_ONX Changelog" />
</a>
<a href="https://t.me/+-hUpHRhvj9wyYmE1">
  <img src="https://img.shields.io/badge/Official%20telegram-Click%20me!-blue?style=flat-square" alt="NO_ONX - Bug report & feedback" title="NO_ONX - Bug report & feedback" />
</a>


<br>

NO_ONX is a lightweight tool but useful to analysis, investigattion, security monitoring for Window

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
NO_ONX
├── Main Options
│   ├── --help
│   ├── -h
│   ├── --system_info
│   ├── -si
│   ├── --version
│   └── -v
│
├── File Info
│   ├── --readfile
│   ├── --file_info
│   ├── --file_hash
│   ├── --dir_info
│   ├── --file_list
│   ├── --symlink_info
│   ├── --extended_info
│   ├── --scan_dir
│   ├── --check_permission
│   └── --hidden_file_info
│
├── Modify (::modify module)
│   ├── --modify_file_permission
│   ├── --modify_file_content
│   ├── --modify_file_name
│   ├── --modify_file_metadata
│   ├── --modify_file_line
│   ├── --modify_file_symlink
│   ├── --modify_directory
│   ├── --modify_directory_permissions
│   └── --modify_file_owner
│
├── Other
│   ├── --compare --mode
│   └── --backup

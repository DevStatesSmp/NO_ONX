# Changelog
> :window: Since **v0.2.4 Beta**, NO_ONX officially supports **Windows only**. Linux support has been **discontinued**.
> 
<p align="center">
  <a href="https://github.com/DevStatesSmp/NO_ONX-old">
    <img src="https://github.com/user-attachments/assets/a5b967f8-bc49-464a-8f89-787f6c972886" width="200" alt="NO_ONX Shell" title="NO_ONX - Lightweight Security Tool" />
  </a>
</p>

---
## [v0.3.3 Beta] - 2025-08-04
### Added
NNX CLI Command

### Fixed
- Optimize code and improve stability
- fix sys_health option cannot be optional
  
### Remove
- remove some annoying loading code lines

## [v0.3.2 Beta] - 2025-07-26
### Added
Add Sandbox command and profile (only work for NNX Private)

### Changed
- config.py split into folder
- New NNX Prompt and NNX Private

### Fixed
- Fixed bug when input the wrong command or the command has an error, you will be kicked out of cmd.
- Fix plugin command error nofication
- Optimized plugin command

### Remove
NNX Plugin Store is cancelled because unstable

## [v0.3.1 Beta] - 2025-05-21
### Experiment:
- v0.3.1.2exp (Telegram version), 2025-06-21: Fix some bug, improve sandbox command and NNX Prompt, NNX Private
- v0.3.1.1exp (Telegram version), 2025-05-30: Added Sandbox (unstable and not working for malware analysis), new NNX prompt and add NNX private, finally add config and fix some bug
### Added
- Add plugin, allowing you to add your own commands
- Add new two commands

### Fixed
- Fully fixed not showing error (or better for your eyes)
- Fixed some bugs

## [v0.3.0 Beta] - 2025-05-16
### Added
- Ported Detective command from Linux to Window
- Added Activity, Security, System Health, Network (Detective)

### Fixed
- Improve stability and optimization
- Fix serious error still exists
- Fix not display error
  
## [v0.2.9 Beta] - 2025-05-05
### Experiment v0.2.10exp (Telegram version): 
Added Detective (which from Linux version and not fully) and fix somebug

### Added
- Minor update with improve stability and fix some bug
- Add file list command
- Modify configuration options.

## [v0.2.8 Beta] - 2025-05-03
### Added
- Add Backup, Compare command
- Add Documents folder

## Changed
- Remove internal command on NO_ONX Shell (Not officially)
- Stop support run [MODULE_NAME].py directly (You can active by editing config.py)

### Fixed
- Fix modification commands
- Improve stability
- Fix some bugs

## [v0.2.4 Beta] - 2025-05-02
### Added
- Integrated all commands from `NO_ONX::modify` (v0.1.2 Beta).
- Experimental CMD Shell for Windows.

### Changed
- Migrated focus from Linux to Windows platform.
- Optimize file structure and commands
- Integrate hidden_file_info command, permission into file_info command

(Note: CMD Shell is still under testing but available in the Windows version)

## [v0.1.2 Beta] - 2025-04-14 (Old Repository)
### Added
- Several commands from `NO_ONX::modify` module.
- Finally support NO_ONX for Window

### Fixed
- Minor bugs related to file operations.


## [v0.0.5 Beta] - 2025-04-12 (Old Repository)
### Fixed
- Bugs in `readfile`, `detective`, and initial command modules.

### Added
- `NO_ONX::modify` module with basic file info and modification commands.
- Added 3 commands to NO_ONX
---

## [v0.0.2 Alpha] - 2025-04-12 (Trial, Not Available)
- Initial implementation of `readfile` and `detective` commands.

---
[Visit old repository here](https://github.com/DevStatesSmp/NO_ONX-old)

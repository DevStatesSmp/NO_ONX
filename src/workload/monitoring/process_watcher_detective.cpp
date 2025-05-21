#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <memory>
#include <iomanip>
#include <sstream>
#include <atomic>
#include <signal.h>

std::atomic<bool> g_running{true};

// Console colors
constexpr int COLOR_RED    = 12;
constexpr int COLOR_GREEN  = 10;
constexpr int COLOR_YELLOW = 14;
constexpr int COLOR_WHITE  = 15;

inline void SetColor(int color) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hConsole == INVALID_HANDLE_VALUE) {
        std::cerr << "Error: Unable to get console handle." << std::endl;
        return;
    }
    if (!SetConsoleTextAttribute(hConsole, color)) {
        std::cerr << "Warning: Unable to set console color." << std::endl;
    }
}

BOOL WINAPI ConsoleHandler(DWORD signal) {
    if (signal == CTRL_C_EVENT) {
        g_running = false;
        SetColor(COLOR_YELLOW);
        std::wcout << L"\nStopping monitor..." << std::endl;
        SetColor(COLOR_WHITE);
        return TRUE;
    }
    return FALSE;
}

inline std::wstring ExtractProcessName(const std::wstring& path) {
    size_t pos = path.find_last_of(L"\\/");
    return (pos != std::wstring::npos) ? path.substr(pos + 1) : path;
}

std::wstring GetProcessImagePath(DWORD pid) {
    std::wstring path = L"<unknown>";
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
    if (hProcess) {
        WCHAR buffer[MAX_PATH];
        DWORD size = MAX_PATH;
        if (QueryFullProcessImageNameW(hProcess, 0, buffer, &size)) {
            path = buffer;
        }
        CloseHandle(hProcess);
    }
    return path;
}

inline std::wstring FileTimeToString(const FILETIME& ft) {
    SYSTEMTIME stUTC, stLocal;
    if (!FileTimeToSystemTime(&ft, &stUTC)) return L"<unknown>";
    if (!SystemTimeToTzSpecificLocalTime(nullptr, &stUTC, &stLocal)) return L"<unknown>";
    std::wstringstream ss;
    ss << std::setfill(L'0') << std::setw(4) << stLocal.wYear << L'-'
       << std::setw(2) << stLocal.wMonth << L'-'
       << std::setw(2) << stLocal.wDay << L' '
       << std::setw(2) << stLocal.wHour << L':'
       << std::setw(2) << stLocal.wMinute << L':'
       << std::setw(2) << stLocal.wSecond;
    return ss.str();
}

struct ProcessInfo {
    DWORD pid;
    DWORD parentPid;
    std::wstring imagePath;
    std::wstring processName;
    std::wstring creationTime;
};

inline void PrintProcessEvent(const ProcessInfo& info, const wchar_t* status, int color) {
    SetColor(color);
    std::wcout << std::setw(8) << status << L" PID: " << std::setw(6) << info.pid
        << L" | Parent: " << std::setw(6) << info.parentPid
        << L" | Created: " << info.creationTime
        << L"\n    Process: " << info.processName
        << L"\n    Path: " << info.imagePath << std::endl;
    SetColor(COLOR_WHITE);
}

std::unordered_map<DWORD, ProcessInfo> SnapshotProcesses() {
    std::unordered_map<DWORD, ProcessInfo> result;
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnap == INVALID_HANDLE_VALUE) return result;
    PROCESSENTRY32W pe;
    pe.dwSize = sizeof(pe);
    if (Process32FirstW(hSnap, &pe)) {
        do {
            ProcessInfo info;
            info.pid = pe.th32ProcessID;
            info.parentPid = pe.th32ParentProcessID;
            info.imagePath = GetProcessImagePath(pe.th32ProcessID);
            info.processName = ExtractProcessName(info.imagePath);
            info.creationTime = L"<unknown>";
            result.emplace(info.pid, std::move(info));
        } while (Process32NextW(hSnap, &pe));
    }
    CloseHandle(hSnap);
    return result;
}

void MonitorProcesses() {
    auto prev = SnapshotProcesses();
    while (g_running) {
        Sleep(1000);
        auto curr = SnapshotProcesses();
        for (const auto& [pid, info] : curr) {
            if (prev.find(pid) == prev.end()) {
                PrintProcessEvent(info, L"[NEW]", COLOR_GREEN);
            }
        }
        for (const auto& [pid, info] : prev) {
            if (curr.find(pid) == curr.end()) {
                PrintProcessEvent(info, L"[EXITED]", COLOR_RED);
            }
        }
        prev = std::move(curr);
    }
}

int main() {
    // Enable Unicode output for console
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCtrlHandler(ConsoleHandler, TRUE);
    SetColor(COLOR_YELLOW);
    std::wcout << L"Press Ctrl+C to exit.\n" << std::endl;
    SetColor(COLOR_WHITE);
    MonitorProcesses();
    std::wcout << L"Monitor stopped." << std::endl;
    return 0;
}

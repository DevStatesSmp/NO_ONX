#include <windows.h>
#include <tlhelp32.h>
#include <iostream>
#include <thread>
#include <psapi.h>
#include <comdef.h>
#include <Wbemidl.h>

#define RED     "\033[91m"
#define GREEN   "\033[92m"
#define YELLOW  "\033[93m"
#define CYAN    "\033[96m"
#define RESET   "\033[0m"

ULONGLONG FileTimeToULL(const FILETIME& ft) {
    return (((ULONGLONG)ft.dwHighDateTime) << 32) + ft.dwLowDateTime;
}

// Get CPU usage percentage of a process over the specified interval (ms)
double GetProcessCpuUsage(DWORD pid, DWORD interval_ms = 1000) {
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    if (!hProcess) return 0.0;

    FILETIME creationTime, exitTime, kernelTime1, userTime1;
    if (!GetProcessTimes(hProcess, &creationTime, &exitTime, &kernelTime1, &userTime1)) {
        CloseHandle(hProcess);
        return 0.0;
    }

    ULONGLONG startKernel = FileTimeToULL(kernelTime1);
    ULONGLONG startUser = FileTimeToULL(userTime1);

    std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));

    FILETIME kernelTime2, userTime2;
    if (!GetProcessTimes(hProcess, &creationTime, &exitTime, &kernelTime2, &userTime2)) {
        CloseHandle(hProcess);
        return 0.0;
    }

    ULONGLONG endKernel = FileTimeToULL(kernelTime2);
    ULONGLONG endUser = FileTimeToULL(userTime2);

    CloseHandle(hProcess);

    ULONGLONG delta = (endKernel + endUser) - (startKernel + startUser);
    double cpuUsage = (double)delta / (interval_ms * 10000.0) * 100.0;

    return cpuUsage;
}

// Get RAM usage in bytes for a given process
SIZE_T GetProcessRamUsage(DWORD pid) {
    SIZE_T ramUsage = 0;
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    if (!hProcess) return 0;

    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(hProcess, &pmc, sizeof(pmc))) {
        ramUsage = pmc.WorkingSetSize;
    }
    CloseHandle(hProcess);
    return ramUsage;
}

// Get average CPU temperature (in Celsius) via WMI, or -1 if error
double GetCpuTemperature() {
    HRESULT hres;

    hres = CoInitializeEx(0, COINIT_MULTITHREADED);
    if (FAILED(hres)) return -1;

    hres = CoInitializeSecurity(
        NULL,
        -1,
        NULL,
        NULL,
        RPC_C_AUTHN_LEVEL_DEFAULT,
        RPC_C_IMP_LEVEL_IMPERSONATE,
        NULL,
        EOAC_NONE,
        NULL);

    if (FAILED(hres)) {
        CoUninitialize();
        return -1;
    }

    IWbemLocator *pLoc = NULL;

    hres = CoCreateInstance(
        CLSID_WbemLocator, 0,
        CLSCTX_INPROC_SERVER,
        IID_IWbemLocator, (LPVOID *)&pLoc);

    if (FAILED(hres)) {
        CoUninitialize();
        return -1;
    }

    IWbemServices *pSvc = NULL;

    hres = pLoc->ConnectServer(
        _bstr_t(L"ROOT\\WMI"),
        NULL,
        NULL,
        NULL,
        0,
        NULL,
        NULL,
        &pSvc);

    if (FAILED(hres)) {
        pLoc->Release();
        CoUninitialize();
        return -1;
    }

    hres = CoSetProxyBlanket(
        pSvc,
        RPC_C_AUTHN_WINNT,
        RPC_C_AUTHZ_NONE,
        NULL,
        RPC_C_AUTHN_LEVEL_CALL,
        RPC_C_IMP_LEVEL_IMPERSONATE,
        NULL,
        EOAC_NONE);

    if (FAILED(hres)) {
        pSvc->Release();
        pLoc->Release();
        CoUninitialize();
        return -1;
    }

    IEnumWbemClassObject* pEnumerator = NULL;
    hres = pSvc->ExecQuery(
        _bstr_t(L"WQL"),
        _bstr_t(L"SELECT CurrentTemperature FROM MSAcpi_ThermalZoneTemperature"),
        WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY,
        NULL,
        &pEnumerator);

    if (FAILED(hres)) {
        pSvc->Release();
        pLoc->Release();
        CoUninitialize();
        return -1;
    }

    IWbemClassObject *pclsObj = NULL;
    ULONG uReturn = 0;

    double avgTempC = 0.0;
    int count = 0;

    while (pEnumerator) {
        HRESULT hr = pEnumerator->Next(WBEM_INFINITE, 1, &pclsObj, &uReturn);
        if (0 == uReturn) break;

        VARIANT vtProp;

        hr = pclsObj->Get(L"CurrentTemperature", 0, &vtProp, 0, 0);
        if (SUCCEEDED(hr) && vtProp.vt == VT_UI4) {
            // Temperature reported in tenths of Kelvin; convert to Celsius:
            double tempC = ((double)vtProp.uintVal / 10.0) - 273.15;
            avgTempC += tempC;
            count++;
        }
        VariantClear(&vtProp);
        pclsObj->Release();
    }

    if (count > 0) {
        avgTempC /= count;
    }
    else {
        avgTempC = -1; // Failed to get temperature
    }

    pEnumerator->Release();
    pSvc->Release();
    pLoc->Release();
    CoUninitialize();

    return avgTempC;
}

void MonitorProcesses(double cpuThreshold, SIZE_T ramThreshold, double tempThreshold) {
    while (true) {
        double cpuTemp = GetCpuTemperature();

        if (cpuTemp >= 0 && cpuTemp > tempThreshold) {
            SYSTEMTIME st;
            GetLocalTime(&st);
            std::wcout << RED << L"[!] " << st.wHour << L":" << st.wMinute << L":" << st.wSecond
                       << L": CPU temperature too high: " << cpuTemp << L"°C (Threshold: " << tempThreshold << L"°C)" << std::endl;
        }

        HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (hSnapshot == INVALID_HANDLE_VALUE) {
            std::cerr << "\033[91m[!]\033[0m Failed to get process list" << std::endl;
            return;
        }

        PROCESSENTRY32 pe;
        pe.dwSize = sizeof(PROCESSENTRY32);

        if (!Process32First(hSnapshot, &pe)) {
            CloseHandle(hSnapshot);
            std::cerr << "\033[91m[!]\033[0m Failed to get first process" << std::endl;
            return;
        }

        while (true) {
            double cpu = GetProcessCpuUsage(pe.th32ProcessID, 500);
            SIZE_T ram = GetProcessRamUsage(pe.th32ProcessID);

            bool warnCpu = (cpu > cpuThreshold);
            bool warnRam = (ramThreshold > 0 && ram > ramThreshold);

            if (warnCpu || warnRam) {
                SYSTEMTIME st;
                GetLocalTime(&st);
                std::wcout << L"\033[91m[!]\033[0m " << st.wHour << L":" << st.wMinute << L":" << st.wSecond
                           << L": Process '" << pe.szExeFile << L"' (PID " << pe.th32ProcessID << L") ";
                if (warnCpu) {
                    std::wcout << L"CPU usage: " << cpu << L"% ";
                }
                if (warnRam) {
                    double ramMB = ram / (1024.0 * 1024.0);
                    double ramGB = ram / (1024.0 * 1024.0 * 1024.0);
                    std::wcout << L"RAM usage: " << ramMB << L" MB (" << ramGB << L" GB) ";
                }
                std::wcout << std::endl;
            }

            if (!Process32Next(hSnapshot, &pe)) break;
        }
        CloseHandle(hSnapshot);

        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
}

int main() {
    std::cout << "Enter CPU usage threshold (%) for warnings: " << std::endl;
    double cpuInput = 0;
    std::cin >> cpuInput;

    std::cout << "Enter RAM usage threshold (GB) for warnings (enter 0 to disable): " << std::endl;
    double ramInput = 0;
    std::cin >> ramInput;
    SIZE_T ramThreshold = static_cast<SIZE_T>(ramInput * 1024 * 1024 * 1024);

    std::cout << "Enter CPU temperature threshold (°C) for warnings (enter 0 to disable): " << std::endl;
    double tempInput = 0;
    std::cin >> tempInput;
    
    std::cout << CYAN << "===[ PROCESS DETECTIVE STARTED ]===\n" << std::endl;
    std::cout << "Starting monitoring with CPU threshold: " << cpuInput << "%, RAM threshold: " << ramInput << " GB, Temperature threshold: " << tempInput << " °C" << std::endl;

    MonitorProcesses(cpuInput, ramThreshold, tempInput);

    return 0;
}

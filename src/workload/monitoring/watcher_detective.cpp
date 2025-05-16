#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <thread>
#include <mutex>
#include <atomic>
#include <filesystem>
#include <csignal>
#include <windows.h>

namespace fs = std::filesystem;

std::map<HANDLE, std::string> watch_map;
std::vector<std::thread> watcher_threads;
std::mutex map_mutex;
std::atomic<bool> running(true);
std::ofstream log_file("watcher.log");

// ANSI color codes
#define RED     "\033[91m"
#define GREEN   "\033[92m"
#define YELLOW  "\033[93m"
#define CYAN    "\033[96m"
#define RESET   "\033[0m"

// Timestamp
std::string current_time() {
    time_t now = time(nullptr);
    char buf[32];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&now));
    return std::string(buf);
}

// Logging
void log_event(const std::string& level, const std::string& event_type, const std::string& path) {
    std::string color;
    if (level == "INFO") color = GREEN;
    else if (level == "WARN") color = YELLOW;
    else if (level == "ALERT" || level == "ERROR") color = RED;
    else color = CYAN;

    std::string time_str = current_time();
    std::string msg = "[" + level + "] [" + time_str + "] " + event_type + " -> " + path;

    std::lock_guard<std::mutex> lock(map_mutex);
    std::cout << color << msg << RESET << std::endl;
    log_file << msg << std::endl;
}

// Recursive watcher
void watch_directory(const std::string& path);

void add_watch(const std::string& path) {
    std::wstring wpath(path.begin(), path.end());
    HANDLE hDir = CreateFileW(wpath.c_str(), FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, NULL, OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS, NULL);

    if (hDir == INVALID_HANDLE_VALUE) {
        log_event("ERROR", "Failed to open directory", path);
        return;
    }

    {
        std::lock_guard<std::mutex> lock(map_mutex);
        watch_map[hDir] = path;
    }

    log_event("INFO", "Watching directory", path);

    watcher_threads.emplace_back([hDir, path]() {
        DWORD bytesReturned;
        char buffer[4096];
        while (running) {
            if (ReadDirectoryChangesW(hDir, buffer, sizeof(buffer), TRUE,
                FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_DIR_NAME | FILE_NOTIFY_CHANGE_SIZE |
                FILE_NOTIFY_CHANGE_LAST_WRITE | FILE_NOTIFY_CHANGE_CREATION,
                &bytesReturned, NULL, NULL)) {

                FILE_NOTIFY_INFORMATION* info = reinterpret_cast<FILE_NOTIFY_INFORMATION*>(buffer);
                do {
                    std::wstring file_name(info->FileName, info->FileNameLength / sizeof(WCHAR));
                    std::string action;
                    std::string file_path = path + "\\" + std::string(file_name.begin(), file_name.end());

                    switch (info->Action) {
                        case FILE_ACTION_ADDED: action = "Created"; break;
                        case FILE_ACTION_REMOVED: action = "Deleted"; break;
                        case FILE_ACTION_MODIFIED: action = "Modified"; break;
                        case FILE_ACTION_RENAMED_OLD_NAME: action = "Moved From"; break;
                        case FILE_ACTION_RENAMED_NEW_NAME: action = "Moved To"; break;
                        default: action = "Unknown Action"; break;
                    }

                    log_event("INFO", action, file_path);

                    if (info->NextEntryOffset == 0) break;
                    info = reinterpret_cast<FILE_NOTIFY_INFORMATION*>(
                        reinterpret_cast<BYTE*>(info) + info->NextEntryOffset);
                } while (true);
            } else {
                log_event("ERROR", "Failed to read changes", path);
                break;
            }
        }
        CloseHandle(hDir);
    });
}

void watch_directory(const std::string& path) {
    add_watch(path);
    for (const auto& entry : fs::directory_iterator(path)) {
        if (entry.is_directory()) {
            watch_directory(entry.path().string());
        }
    }
}

// Handle Ctrl+C
void signal_handler(int) {
    std::cout << "\n" << RED << "[!] Termination signal received. Shutting down..." << RESET << std::endl;
    running = false;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << RED << "Usage: " << argv[0] << " <directory_to_watch>" << RESET << std::endl;
        return 1;
    }

    signal(SIGINT, signal_handler);

    std::string target_dir = argv[1];
    if (!fs::exists(target_dir) || !fs::is_directory(target_dir)) {
        log_event("ERROR", "Invalid directory", target_dir);
        return 1;
    }

    std::cout << CYAN << "===[ WATCHER DETECTIVE STARTED ]===\n" << RESET;
    log_event("INFO", "Monitoring started at", target_dir);

    watch_directory(target_dir);

    // Wait for all watcher threads to finish
    for (auto& t : watcher_threads) {
        if (t.joinable()) t.join();
    }

    log_event("INFO", "Monitoring stopped", target_dir);
    log_file.close();

    return 0;
}

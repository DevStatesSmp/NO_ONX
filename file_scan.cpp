#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>
#include <openssl/md5.h>
#include <filesystem>
#include <vector>
#include <unordered_set>
#include <thread>
#include <mutex>
#include <future>

namespace fs = std::filesystem;

std::unordered_set<std::string> KNOWN_MALWARE_HASHES = {
    "d41d8cd98f00b204e9800998ecf8427e", 
    "e99a18c428cb38d5f260853678922e03"   
};

std::vector<std::string> safe_files;
std::vector<std::string> infected_files;
std::mutex safe_files_mutex;
std::mutex infected_files_mutex;

std::string get_file_hash(const std::string& file_path, const std::string& hash_type = "sha256") {
    unsigned char buffer[8192];
    unsigned char hash[SHA256_DIGEST_LENGTH];

    std::ifstream file(file_path, std::ifstream::binary);
    if (!file) {
        std::cerr << "Cannot open file path: " << file_path << std::endl;
        return "";
    }

    // Hash calculation
    if (hash_type == "sha256") {
        SHA256_CTX sha256_ctx;
        SHA256_Init(&sha256_ctx);
        while (file.read(reinterpret_cast<char*>(buffer), sizeof(buffer))) {
            SHA256_Update(&sha256_ctx, buffer, file.gcount());
        }
        SHA256_Final(hash, &sha256_ctx);
    } else if (hash_type == "md5") {
        MD5_CTX md5_ctx;
        MD5_Init(&md5_ctx);
        while (file.read(reinterpret_cast<char*>(buffer), sizeof(buffer))) {
            MD5_Update(&md5_ctx, buffer, file.gcount());
        }
        MD5_Final(hash, &md5_ctx);
    } else {
        std::cerr << "Unsupported hash type: " << hash_type << std::endl;
        return "";
    }

    // Convert hash to hex string
    std::ostringstream hex_stream;
    for (int i = 0; i < (hash_type == "sha256" ? SHA256_DIGEST_LENGTH : MD5_DIGEST_LENGTH); i++) {
        hex_stream << std::setw(2) << std::setfill('0') << std::hex << (int)hash[i];
    }

    return hex_stream.str();
}

void scan_file(const std::string& path) {
    if (fs::is_regular_file(path)) {
        std::string file_hash = get_file_hash(path);

        if (file_hash.empty()) return;

        bool infected = KNOWN_MALWARE_HASHES.find(file_hash) != KNOWN_MALWARE_HASHES.end();
        
        // Lock mutexes for thread-safe access
        if (infected) {
            std::lock_guard<std::mutex> lock(infected_files_mutex);
            infected_files.push_back(path);
            std::cout << "❌ WARNING: " << path << " contains malware (hash matched)\n";
        } else {
            std::lock_guard<std::mutex> lock(safe_files_mutex);
            safe_files.push_back(path);
            std::cout << "✅ Safe: " << path << "\n";
        }

    } else if (fs::is_directory(path)) {
        for (const auto& entry : fs::directory_iterator(path)) {
            scan_file(entry.path().string());
        }
    } else {
        std::cerr << "Invalid path: " << path << std::endl;
    }
}

void scan_directory(const std::string& path) {
    std::vector<std::future<void>> futures;

    // Use multithreading to scan files concurrently
    for (const auto& entry : fs::directory_iterator(path)) {
        futures.push_back(std::async(std::launch::async, scan_file, entry.path().string()));
    }

    // Wait for all threads to finish
    for (auto& future : futures) {
        future.get();
    }
}

int main() {
    std::string directory_to_scan;
    std::getline(std::cin, directory_to_scan);
    
    std::cout << "\n--- Starting scan ---\n\n";
    scan_directory(directory_to_scan);

    std::cout << "\n--- Scan Results ---\n";

    // Print infected files
    std::cout << "\n❌ Infected files:\n";
    if (infected_files.empty()) {
        std::cout << "  -> No malware found.\n";
    } else {
        for (const auto& file : infected_files) {
            std::cout << "  -> " << file << "\n";
        }
    }

    // Print safe files
    std::cout << "\n✅ Safe files:\n";
    if (safe_files.empty()) {
        std::cout << "  -> No safe files found.\n";
    } else {
        for (const auto& file : safe_files) {
            std::cout << "  -> " << file << "\n";
        }
    }

    std::cout << "\n--- Scan complete ---\n";
    return 0;
}

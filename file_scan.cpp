#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>
#include <openssl/md5.h>
#include <filesystem>
#include <vector>

namespace fs = std::filesystem;

std::vector<std::string> KNOWN_MALWARE_HASHES = {
    "d41d8cd98f00b204e9800998ecf8427e", 
    "e99a18c428cb38d5f260853678922e03"   
};

std::vector<std::string> safe_files;
std::vector<std::string> infected_files;

std::string get_file_hash(const std::string& file_path, const std::string& hash_type = "sha256") {
    unsigned char buffer[8192];
    unsigned char hash[SHA256_DIGEST_LENGTH];

    std::ifstream file(file_path, std::ifstream::binary);
    if (!file) {
        std::cerr << "Cannot open file path: " << file_path << std::endl;
        return "";
    }

    // Tính toán hash
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
        std::cerr << "Not support this hash" << std::endl;
        return "";
    }

    // Chuyển đổi hash thành chuỗi hex
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

        bool infected = false;
        for (const auto& malware_hash : KNOWN_MALWARE_HASHES) {
            if (file_hash == malware_hash) {
                std::cout << "❌ WARNING: " << path << " contains malware (hash matched)\n";
                infected_files.push_back(path);
                infected = true;
                break;
            }
        }

        if (!infected) {
            std::cout << "✅ Safe: " << path << "\n";
            safe_files.push_back(path);
        }

    } else if (fs::is_directory(path)) {
        for (const auto& entry : fs::directory_iterator(path)) {
            scan_file(entry.path().string());
        }
    } else {
        std::cerr << "Invalid path: " << path << std::endl;
    }
}

int main() {
    std::string directory_to_scan;
    std::getline(std::cin, directory_to_scan);
    
    std::cout << "\n--- Starting scan ---\n\n";
    scan_file(directory_to_scan);

    std::cout << "\n--- Scan Results ---\n";

    std::cout << "\n❌ Infected files:\n";
    if (infected_files.empty()) {
        std::cout << "  -> No malware found.\n";
    } else {
        for (const auto& file : infected_files) {
            std::cout << "  -> " << file << "\n";
        }
    }

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

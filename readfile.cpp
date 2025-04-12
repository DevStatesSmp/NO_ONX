#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;


// Check error
bool validate_file_path(const string& file_path) {
    // Trim spaces from both ends of the file path
    size_t start = file_path.find_first_not_of(" \t");
    size_t end = file_path.find_last_not_of(" \t");

    if (start == string::npos || end == string::npos) {
        cerr << "Error: The file path is empty." << endl;
        return false;
    }

    string trimmed_path = file_path.substr(start, end - start + 1);
    
    // Check if file exists and if it's a regular file
    if (!fs::exists(trimmed_path)) {
        cerr << "Error: The file at " << trimmed_path << " does not exist." << endl;
        return false;
    } else if (!fs::is_regular_file(trimmed_path)) {
        cerr << "Error: The path at " << trimmed_path << " is not a valid file." << endl;
        return false;
    }

    return true;
}


// Read file
void read_file(const string& file_path) {
    ifstream file(file_path);
    // Trim spaces from both ends of the file path
    if (!file.is_open()) {
        cerr << "Error: Could not open the file " << file_path << endl;
        return;
    }

    string line;
    size_t line_number = 1;
    while (getline(file, line)) {
        // Output line with line number
        cout << "Line " << line_number++ << ": " << line << endl;
    }

    file.close();
}

// Main code
int main() {
	string file_path; // Make file_path
	// Input file path
	getline(cin, file_path);
	
    if (!validate_file_path(file_path)) {
        return 1;
    }

    // If valid, proceed to read the file
    read_file(file_path);

    return 0;
}

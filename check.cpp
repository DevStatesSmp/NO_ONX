#include <iostream>
#include <sys/inotify.h>
#include <unistd.h>
#include <fcntl.h>
#include <cstring>
#include <dirent.h>
#include <sys/stat.h>
#include <string>

#define MAX_EVENTS 1024
#define LEN_NAME 16
#define EVENT_SIZE (sizeof(struct inotify_event))
#define BUF_LEN (MAX_EVENTS * (EVENT_SIZE + LEN_NAME))

// log
void log_event(const std::string& event_type, const std::string& file_name) {
    std::cout << "[LOG] Event: " << event_type << " on file: " << file_name << std::endl;
}

// watch
void watch_directory(int fd, const std::string& path) {
    DIR *dir = opendir(path.c_str());
    if (!dir) {
        std::cerr << "Failed to open directory: " << path << std::endl;
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != nullptr) {
        std::string file_path = path + "/" + entry->d_name;
        if (entry->d_name[0] == '.') continue;  // Bỏ qua thư mục "." và ".."

        struct stat file_stat;
        if (stat(file_path.c_str(), &file_stat) == 0) {
            // If a folder
            if (S_ISDIR(file_stat.st_mode)) {
                std::cout << "Adding watch on directory: " << file_path << std::endl;
                int wd = inotify_add_watch(fd, file_path.c_str(), IN_MODIFY | IN_CREATE | IN_DELETE | IN_MOVE);
                if (wd == -1) {
                    perror("Error adding watch on directory");
                }
                watch_directory(fd, file_path); 
            }
        }
    }
    closedir(dir);
}

// Event management
void handle_events(int fd) {
    char buffer[BUF_LEN];
    ssize_t length;

    while (true) {
        length = read(fd, buffer, BUF_LEN);
        if (length < 0) {
            std::cerr << "Error reading inotify events" << std::endl;
            return;
        }

        for (int i = 0; i < length; i += EVENT_SIZE + ((struct inotify_event *)&buffer[i])->len) {
            struct inotify_event *event = (struct inotify_event *) &buffer[i];

            if (event->mask & IN_MODIFY) {
                log_event("File modified", event->name);
            }
            if (event->mask & IN_CREATE) {
                log_event("File created", event->name);
            }
            if (event->mask & IN_DELETE) {
                log_event("File deleted", event->name);
            }
            if (event->mask & IN_MOVE_SELF) {
                log_event("File moved", event->name);
            }
        }
    }
}

int main() {
    int fd = inotify_init(); // inotify
    if (fd < 0) {
        std::cerr << "Error initializing inotify" << std::endl;
        return -1;
    }

    // Watch
    std::string path;
    //std::cout << "(Example: /home/-USER_NAME-/)";
     //std::cout << "Enter directory path to watch: "; <-- No need to use
    std::getline(std::cin, path);
    
    
    watch_directory(fd, path);

    // Handle event
    handle_events(fd);

    // CLose program
    close(fd);
    return 0;
}

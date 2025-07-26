import yaml
import os


def load(name):
    base_path = os.environ.get("NNX_PROJECT_ROOT")
    if not base_path:
        current_dir = os.path.abspath(os.path.dirname(__file__))
        while True:
            profiles_dir = os.path.join(current_dir, "profiles")
            if os.path.isdir(profiles_dir):
                base_path = current_dir
                break
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                raise FileNotFoundError("[!] Could not find 'profiles' directory in any parent folder.")
            current_dir = parent_dir

    profile_path = os.path.join(base_path, "profiles", f"{name}.yml")

    if not os.path.isfile(profile_path):
        raise FileNotFoundError(f"[!] Profile file not found: {profile_path}")

    with open(profile_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ValueError(f"[!] Profile file {profile_path} is empty or invalid YAML.")
            return data
        except yaml.YAMLError as e:
            raise ValueError(f"[!] Error parsing YAML file {profile_path}: {e}")


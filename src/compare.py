import os
import sys
import argparse
from tabulate import tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.workload.compare_module import (deep_compare_dirs, deep_compare_files, 
                            simple_compare_files, simple_compare_dirs)
from src.utils.config import FEATURE

def main():
    parser = argparse.ArgumentParser(description="Compare file or directory (simple or deep)")
    parser.add_argument("path1", help="first path")
    parser.add_argument("path2", help="second path")
    parser.add_argument("--mode", choices=["simple", "deep"], default="simple", 
                        help="Compare mode (default: simple)")
    args = parser.parse_args()

    if not os.path.exists(args.path1):
        print(f"❌ The path does not exist: {args.path1}")
        sys.exit(1)
    if not os.path.exists(args.path2):
        print(f"❌ The path does not exist: {args.path2}")
        sys.exit(1)

    is_dir1 = os.path.isdir(args.path1)
    is_dir2 = os.path.isdir(args.path2)

    if is_dir1 != is_dir2:
        print("⚠️ Cannot compare between file and directory!")
        sys.exit(1)

    if args.mode == "simple":
        if is_dir1:
            results = simple_compare_dirs(args.path1, args.path2)
            for result in results:
                print(result)
        else:
            result = simple_compare_files(args.path1, args.path2)
            print(f"Comparison result: {result}")
    else:  # deep
        if is_dir1:
            identical_files, different_files, only_in_dir1, only_in_dir2, diff_files, table_data = deep_compare_dirs(args.path1, args.path2)

            print(f"\nSummary:")
            print(f"Total files: {len(table_data)}")
            print(f"Identical files: {identical_files}")
            print(f"Different files: {different_files}")
            print(f"Only in {args.path1}: {len(only_in_dir1)}")
            print(f"Only in {args.path2}: {len(only_in_dir2)}")

            print("\nComparison Table:")
            print(tabulate(table_data, headers=["File", "Status", "Details"], tablefmt="fancy_grid"))

            if diff_files:
                print("\nDifferent files (content or permissions):")
                for f in diff_files:
                    print(f"  - {f}")
            else:
                print("")

            if only_in_dir1:
                print(f"\nFiles only in {args.path1}:")
                for f in only_in_dir1:
                    print(f"  - {f}")

            if only_in_dir2:
                print(f"\nFiles only in {args.path2}:")
                for f in only_in_dir2:
                    print(f"  - {f}")

        else:
            result = deep_compare_files(args.path1, args.path2)
            print(f"Comparison result: {result}")


if __name__ == "__main__" and FEATURE["ENABLE_DIRECT_RUN"]:
    main()
else:
    if __name__ == "__main__":
        print("[ERROR] This script cannot be run directly. Run NO_ONX.exe instead.")

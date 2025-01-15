import psutil
import time
import requests
import sys
import io
import traceback
import getpass

ban_list = ["127.0.0.1"]
FILTERS = []
VALUE = ""

with open(".filter", "r") as fp:
    for line in fp.readlines():
        if line.startswith("VAR"):
            VALUE = line.split("VAR:")[1].split("\n")[0]
        elif line.startswith("FILTER"):
            FILTERS.append(line.split("FILTER:")[1].split("\n")[0])
fp.close()

def main():
    print("[+] Start Scanning...")
    scanning_results = []
    scanning_errors = []
    for proc in psutil.process_iter():
        try:
            scanning_results.append(proc.as_dict())
            print(f" [+] Procecss: {len(scanning_results)}, Error: {len(scanning_errors)}", end="\r")
        except Exception as error:
            scanning_errors.append(error)
            print(f" [+] Procecss: {len(scanning_results)}, Error: {len(scanning_errors)}", end="\r")
    print()
    detected_results = []
    detection_errors = []
    passed = 0
    for data in scanning_results:
        try:
            if str(data[VALUE]) in FILTERS:
                detected_results.append(data)
                print(f" [+] Detected: {len(detected_results)}, Error: {len(detection_errors)}, Passed: {passed}", end="\r")
            else:
                passed += 1
                print(f" [+] Detected: {len(detected_results)}, Error: {len(detection_errors)}, Passed: {passed}", end="\r")
        except Exception as error:
            detection_errors.append(error)
            print(f" [+] Detected: {len(detected_results)}, Error: {len(detection_errors)}, Passed: {passed}", end="\r")
        time.sleep(0.005)
    print()
    print()
    for detected in detected_results:
        print(f"Process {detected['name']} (PID: {detected['pid']}) has been detected.")
    getpass.getpass("Press Enter to Exit")
    

if __name__ == '__main__':
    main()
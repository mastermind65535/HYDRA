import psutil
import time
import requests
import sys
import io
import traceback
import getpass

FILTERS = []

with open(".filter", "r") as fp:
    for line in fp.readlines():
        line = line.split("\n")[0]
        VALUE = line.split(" ")[0]
        FILTER = line.split(" ")[1]
        FILTERS.append({
            "VALUE" : VALUE,
            "FILTER" : FILTER
        })
fp.close()

def main():
    print("[+] 스캐닝 시작...")
    scanning_results = []
    scanning_errors = []
    for proc in psutil.process_iter():
        try:
            scanning_results.append(proc.as_dict())
        except KeyboardInterrupt:
            print(f"[+] 프로세스: {len(scanning_results)}, 에러: {len(scanning_errors)} [중지됨]", end="\r")
            break
        except Exception as error:
            scanning_errors.append(error)
        print(f"[+] 프로세스: {len(scanning_results)}, 에러: {len(scanning_errors)}", end="\r")
    print()
    detected_results = []
    detection_errors = []
    passed = 0
    for data in scanning_results:
        try:
            for Filter in FILTERS:
                if data[Filter["VALUE"]] == Filter["FILTER"]:
                    detected_results.append(data)
                else:
                    passed += 1
        except KeyboardInterrupt:
            print(f"[+] 감지: {len(detected_results)}, 에러: {len(detection_errors)}, 통과: {passed} [중지됨]", end="\r")
            break
        except Exception as error:
            detection_errors.append(error)
        print(f"[+] 감지: {len(detected_results)}, 에러: {len(detection_errors)}, 통과: {passed}", end="\r")
        time.sleep(0.005)
    print()
    print()
    for detected in detected_results:
        print(f"프로세스 {detected['name']} (PID: {detected['pid']})이/가 감지됨.")
    getpass.getpass("Enter를 눌러 종료")
    

if __name__ == '__main__':
    main()
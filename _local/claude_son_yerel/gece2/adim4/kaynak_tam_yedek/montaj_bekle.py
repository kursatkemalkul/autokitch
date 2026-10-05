import subprocess, time
while True:
    o = subprocess.run(["wmic", "process", "where", "name='python.exe'", "get", "CommandLine"], capture_output=True, text=True).stdout
    if "hat3_montaj_v4" not in o: break
    time.sleep(15)

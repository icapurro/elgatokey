import http.client
import json
import subprocess
import time

camera_ips = ['192.168.86.45', '192.168.86.117']

# Variable to store the last state. Possible values: 'activated', 'shutdown', or '' (empty for the start)
last_state = ""

def set_light(ip, state):
    conn = http.client.HTTPConnection(ip, 9123)
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"lights": [{"on": state}], "numberOfLights": 1})
    conn.request("PUT", "/elgato/lights", data, headers)
    response = conn.getresponse()
    conn.close()
    return response.status

while True:
    log_process = subprocess.Popen(
        ["log", "stream", "--predicate", 'subsystem == "com.apple.controlcenter"'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for line in log_process.stdout:
        if 'Sorted active attributions from SystemStatus update:' not in line:
            continue
        if "[cam]" in line:
            if last_state != "activated":
                last_state = "activated"
                print("Camera has been activated, turn on the light.")
                [ set_light(ip, 1) for ip in camera_ips ]
                print(last_state)
        else:
            if last_state != "shutdown":
                last_state = "shutdown"
                print("Camera shut down, turn off the light.")
                [ set_light(ip, 0) for ip in camera_ips ]
                print(last_state)

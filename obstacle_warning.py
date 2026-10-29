import subprocess
import re

SENSOR = "/margdrishti/ultrasonic"
CMD = "/cmd_vel"
THRESHOLD = 1.0

def stop_robot():
    subprocess.run(
        [
            "gz", "topic", "-t", CMD,
            "-m", "gz.msgs.Twist",
            "-p", "linear: {x: 0.0} angular: {z: 0.0}"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=2
    )

print("MARGDRISHTI OBSTACLE PROTECTION STARTED")
print(f"Stop threshold: {THRESHOLD:.1f} metre")

process = subprocess.Popen(
    ["gz", "topic", "-e", "-t", SENSOR],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

try:
    for line in process.stdout:
        match = re.search(
            r"ranges:\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)",
            line
        )
        if not match:
            continue

        distance = float(match.group(1))

        if 0.05 <= distance <= 4.0:
            if distance < THRESHOLD:
                stop_robot()
                print(
                    f"OBSTACLE at {distance:.2f} m — STOP COMMAND SENT",
                    flush=True
                )
            else:
                print(
                    f"Path clear: {distance:.2f} m",
                    flush=True
                )

except KeyboardInterrupt:
    print("\nDetection stopped.")
finally:
    stop_robot()
    process.terminate()
    process.wait()

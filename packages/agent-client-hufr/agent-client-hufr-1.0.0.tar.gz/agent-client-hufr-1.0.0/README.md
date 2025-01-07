# Agent Client

A Python client library for communicating with a Flask server. It provides an abstraction layer for interacting with multiple services, such as motor telemetry, sensor data, system logs, and more.

## Installation

```bash
pip install agent-client
```
# USAGE

```python
from agent.client import ServerClient
from agent.services.motor_telemetry import MotorTelemetryClient

# Initialize the core client
client = ServerClient(base_url="http://localhost:5000/api")

# Initialize the motor telemetry service
motor_client = MotorTelemetryClient(client)

# Example: Send motor telemetry data
motor_telemetry_data = {
"motor_identifier": "left_arm",
"control_signals": {"pwm": 120, "voltage": 5.0},
"mechanical_feedback": {"speed": 50, "torque": 10},
"timestamp": "2025-01-06T16:00:00"
}
response = motor_client.send_telemetry(motor_telemetry_data)
print(response)
```

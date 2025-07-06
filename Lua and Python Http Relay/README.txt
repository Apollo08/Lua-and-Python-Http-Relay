# Stormworks Data Send/Receive System

This system allows you to **send and receive numeric data between Stormworks (Lua microcontroller)**
and one or more PCs using Python HTTP servers. It supports **LAN/relay forwarding** for multi-PC setups and robust error/debug reporting.

---

## Components

### 1. Stormworks Lua Script (`Stormworks-Data-send_receive.lua`)
- Sends numbers to a Python HTTP server when triggered.
- Always retrieves the latest stored value from the server.
- Reports status and error/debug codes on output channels.

### 2. Python HTTP Server (`local-data-storage-lua-V2.py`)
- Stores and serves numeric data via HTTP.
- Can operate in two modes:
  - **LAN**: Receives data from Stormworks, forwards it to a storage server.
  - **SER**: Receives data from the LAN server and always saves locally.

---

## How It Works

### Data Flow

1. **Stormworks Lua** sends a number to the LAN Python server (when triggered).
2. **LAN Python server** forwards the number to the SER (Storage Server).
3. **SER Python server** saves the number.
4. **Stormworks Lua** can always request the latest value from the LAN server.

---

## Setup Instructions

### 1. Stormworks Lua Script

- Place `Stormworks-Data-send_receive.lua` in your Stormworks microcontroller.
- **Inputs:**
  - `input.getNumber(1)`: The number to send.
  - `input.getBool(1)`: When `true`, triggers sending the number.
- **Outputs:**
  - `output.setNumber(1, ...)`: Last received value.
  - `output.setNumber(2, ...)`: Error/debug code.

#### Error/Debug Codes

| Code   | Meaning                                 |
|--------|-----------------------------------------|
| 0      | OK (data received and valid)            |
| 1001   | Timeout or no response                  |
| 2      | Invalid number in response              |
| 3      | Empty response                          |
| 4001   | Send triggered                          |
| 4002   | Send success (number sent and received) |
| 4003   | Send failed (invalid number in response)|

---

### 2. Python HTTP Server (`local-data-storage-lua-V2.py`)

#### Configuration

- **MODE**: Set to `"LAN"` or `"SER"` at the top of the script.
  - `"LAN"`: For the PC directly interfacing with Stormworks.
  - `"SER"`: For the Storage/Server PC.
- **SER_HOST** and **SER_PORT**: Set these to the IP and port of your Storage/Server (only needed in LAN mode).
- **DATA_FILE**: File where the number is stored locally.

#### Example: LAN Server (on PC running Stormworks)

```python
MODE = "LAN"
SER_HOST = "192.168.0.7"  # IP of the SERVER PC
SER_PORT = 5001           # Port of the SERVER PC

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 5000), SimpleHandler)
    print(f"Server running on http://127.0.0.1:5000 in {MODE} mode")
    server.serve_forever()
```

#### Example: SER Server (on SERVER PC)

```python
MODE = "SER"

if __name__ == "__main__":
    server = HTTPServer(("192.168.0.7", 5001), SimpleHandler)  # Use SERVER PC's LAN IP
    print(f"Server running on http://192.168.0.7:5001 in {MODE} mode")
    server.serve_forever()
```

---

## Editing for Your Network

- **LAN PC**:
  - Set `MODE = "LAN"`
  - Set `SER_HOST` to the SERVER PC's LAN IP.
  - Set `SER_PORT` to the server's port (default: 5001).
  - Bind the server to `127.0.0.1` or the LAN PC's IP on port 5000.

- **SER (Storage/Server) PC**:
  - Set `MODE = "SER"`
  - Bind the server to the Storage/Server PC's LAN IP on port 5001.

**Make sure firewalls allow traffic on the chosen ports.**

---

## Troubleshooting

- **No data received:**  
  - Check that both Python servers are running and reachable.
  - Verify IP addresses and ports.
  - Check Stormworks output channel 2 for error/debug codes.

- **Error codes:**  
  - `1001`: Server not reachable or not running.
  - `2`: Server replied with non-numeric data.
  - `3`: Server replied with empty data.
  - `4003`: Send failed (invalid number in response).

- **Relay not saving:**  
  - Ensure the server is running in `"SER"` mode and reachable from the LAN PC.

---

## Advanced

- You can change the data file location by editing `DATA_FILE`.

---

## Example Network Diagram

```
[Stormworks Lua] --(HTTP, port 5000)--> [LAN Python Server] --(HTTP, port 5001)--> [SER Python Server]
```

---

## Editing Tips

- **Change ports/IPs** as needed for your network.
- **Edit error/debug codes** in the Lua script for more granularity.
- **Expand Python logic** for more advanced relay or backup strategies.

---

## Security

- This system is for LAN use only. Do **not** expose these servers to the public internet without additional security.

---

## Credits

- Stormworks Lua and Python HTTP relay by [Apollo08/BudgetGamers].
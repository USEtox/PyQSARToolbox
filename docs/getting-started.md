# Getting Started

This guide walks you through setting up and using the client effectively.

## Prerequisites

1. Install the official QSAR Toolbox application locally and start its Web API service.
2. Find the listening port of the local server (see below if unknown).

### Finding the Port Automatically

```python
import psutil, requests
from requests.exceptions import RequestException

def find_open_port(endpoint="/about/toolbox/version", host="127.0.0.1"):
    for conn in psutil.net_connections():
        if conn.status == "LISTEN" and getattr(conn.laddr, 'ip', host) == host:
            port = conn.laddr.port
            try:
                r = requests.get(f"http://{host}:{port}/api/v6{endpoint}", timeout=1)
                if r.status_code == 200:
                    return port
            except RequestException:
                continue
    return None

print("Detected port:", find_open_port())
```

## Instantiating the Client

```python
from pyqsartoolbox import QSARToolbox
qs = QSARToolbox(port=62008)  # use the port you found
print(qs.toolbox_version())
```

## Common Operations

```python
# Search by CAS (with or without dashes)
qs.search_CAS("50-00-0")

# Search by name
qs.search_name("formaldehyde")

# Endpoint tree
tree = qs.get_endpoints_tree()

# List calculators
calculators = qs.get_available_calculators()
```

## Error Handling

Most methods raise ValueError with the HTTP status code if the API responds with an error. Wrap calls in try/except for resilience.

## Next Steps

Dive into the full [API Reference](api.md) for advanced features.

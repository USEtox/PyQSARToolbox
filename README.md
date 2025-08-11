[![Documentation](https://img.shields.io/badge/docs-PyQSARToolbox-blue.svg)](https://usetox.github.io/PyQSARToolbox/)

# PyQSARToolbox
A Python interface to the [OECD](https://www.oecd.org/en.html) [QSAR Toolbox](https://qsartoolbox.org/download/). It only works on Windows since it is the only operating system for which QSAR Toolbox is released.

# Installation
Install it with `pip`:
```
pip install git+https://github.com/USEtox/PyQSARToolbox.git
```
For developers, you can clone the repository, and run
```
pip install -e .
```

The main dependency is the `requests` package. Other dependencies (now and in the future) are the usual scientific Python packages, e.g. `numpy`, `pandas`, etc.  
The `QSAR Toolbox` can be [downloaded for free](https://qsartoolbox.org/download/). I recommend installing `VEGA` and `OPERA` add-ons, which can be downloaded via the toolbox. They will need a working `Java` installation. I have Java on my system and everything worked out of the box. If you encounter any problems, contact me. 

# Calling QSAR Toolbox from Python
The class `QSARToolbox` provides an interface to the web API of the `QSAR Toolbox`. It can be used locally by running the `QSAR Toolbox WebSuite` program that is installed with the `QSAR Toolbox`. After running it, the user can connect to a local host at `http://127.0.0.1:[port]` where the port can be a different value given by the program in the following message:
  > WebAPI running on port [port]  

where [port] is a 4 or 5 digit integer (may be different on your system).

![websuite screenshot](./docs/Screenshot_QSAR_Toolbox_WebSuite.png)

Using the API is quite straightforward with some practical issues that I have discovered and try to clarify in this notebook.

# Getting started
Start the `QSAR Toolbox WebSuite` and wait for the port number to appear. Then load the class `QSARTooolbox` and create a `QSARToolbox` object:
```python
from pyqsartoolbox import QSARTooolbox
qs = QSARToolbox(port=51946)
api_version = qs.webapi_version()
toolbox_version = qs.toolbox_version()
print(f"API version: {api_version}")
print(f"Toolbox version: {toolbox_version}")
```

# Documents
API documents are [here](https://usetox.github.io/PyQSARToolbox/). You can also look at the [notebooks folder](./notebooks) to find notebooks with extensive examples of the usage of this package for real world problems.

# Citations
Please cite it as  
```
Eftekhari, Ali A., PyQSARToolbox: a Python interface to the OECD QSAR Toolbox, https://usetox.github.io/PyQSARToolbox/, 2025
```

# Endpoints
You can obtain experimental data and estimations for many physicochemical properties, environmental health, fate, and transport, and ecotoxicological information, as depicted in the following graph:

![endpoints graph](./docs/endpoints_tree.png)
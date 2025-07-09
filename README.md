# GirderEEGViewer

![GirderEEGViewer](https://github.com/user-attachments/assets/37796cb5-840f-4feb-885c-87b1ff2963ea)

Works only on Linux/Mac, not on Windows.

## Create environment and install dependencies
```
python -m venv env
source env/bin/activate
pip install .
```

### Contributing
Install development dependencies
```
pip install -e ".[dev]"
```

### Optional dependencies
-----------------------------------------------------------

Faster Jpeg encoding using TurboJPEG.

**macOS system install**
```
# macOS
brew install jpeg-turbo
```

**Windows install**
Download and install from Github: https://github.com/libjpeg-turbo/libjpeg-turbo/releases

**Linux install**
```
# RHEL/CentOS/Fedora
# YUM doc: https://libjpeg-turbo.org/Downloads/YUM
# Ubuntu
apt-get install libturbojpeg
```

Once your system is ready, you can install the dependencies:
```
pip install ".[turbo]"
```

## Run trame application
```
girdereegviewer file.neonatal
```
To test the application, you can try to use the [_example.neonatal_](https://github.com/KitwareMedical/GirderEEGViewer/releases/download/untagged-149f037e2bbb82651e1a/example.neonatal) file provided in the assets.
You can add ```--server``` to your command line to prevent your browser from opening and ```--port``` to specifiy the port the server should listen to, default is 8080.

## Acknowledgement

This work was supported by the Agence Nationale de la Recherche (Grant ANR-22-CE45-0034).

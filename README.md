# GirderEEGViewer

![GirderEEGViewer](https://github.com/user-attachments/assets/37796cb5-840f-4feb-885c-87b1ff2963ea)

Works only on Linux/Mac, not on Windows.

## Create environment and install dependencies
```
python -m venv env
source env/bin/activate
pip install .
```

### Build eegviz lib
To build the eegviz library, you can unzip the [_eegvizlib-0.0.0.tar.gz_](https://github.com/KitwareMedical/GirderEEGViewer/releases/download/untagged-ad480b7a640cc0981ff5/eegvizlib-0.0.0.tar.gz) archive provided in the assets and follow the instructions below. The ```PACKAGES_PATH``` should be replaced with the absolute path to the site-packages directory of your virtual environment.
```
tar xf eegvizlib-0.0.0.tar.gz
cd eegvizlib-0.0.0
mkdir {PACKAGES_PATH}/eegviz
./configure --prefix={PACKAGES_PATH}/eegviz
make
make install
```

You may have to install SDL before calling "configure":
```
sudo apt install libsdl2-dev libsdl2-ttf-dev
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
To test the application, you can try to use the [_example.neonatal_](https://github.com/KitwareMedical/GirderEEGViewer/releases/download/untagged-ad480b7a640cc0981ff5/example.neonatal) file provided in the assets.
You can add ```--server``` to your command line to prevent your browser from opening and ```--port``` to specifiy the port the server should listen to, default is 8080.

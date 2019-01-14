# BScThesis

### Starting app
Clone the repository
```
git clone https://github.com/tpyrek/BScThesis.git
```
And run app
```
cd BScThesis/OpenCV
python3 main.py
```
### Prerequisites
What you need to run app:
* Pyserial
* Numpy
* Qt 
* OpenCV 3.4
* PyQt5

## Build Qt 5.12 for Raspberry Pi 3
Update Rpi
```
sudo apt update
sudo apt upgrade
```

Install required packages
```
sudo apt install build-essential libfontconfig1-dev libdbus-1-dev libfreetype6-dev libicu-dev libinput-dev libxkbcommon-dev libsqlite3-dev libssl-dev libpng-dev libjpeg-dev libglib2.0-dev libraspberrypi-dev
```

Install optional packages
```
sudo apt install bluez libbluetooth-dev
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad libgstreamer-plugins-bad1.0-dev gstreamer1.0-pulseaudio gstreamer1.0-tools gstreamer1.0-alsa
sudo apt install libasound2-dev
sudo apt install pulseaudio libpulse-dev
sudo apt install libpq-dev libmariadbclient-dev
sudo apt install libcups2-dev
sudo apt install libwayland-dev
sudo apt install libx11-dev libxcb1-dev libxkbcommon-x11-dev libx11-xcb-dev libxext-dev
sudo apt install libatspi-dev
```

Go to [Qt Downloads](http://download.qt.io/official_releases/qt/), choose suitable Qt version (in this project used 5.12), go to single/ folder and download tar.xz file or copy link and use wget; for Qt 5.12:
```
wget http://download.qt.io/official_releases/qt/5.12/5.12.0/single/qt-everywhere-src-5.12.0.tar.xz
```
Un-tar downloaded archive
```
tar xf qt-everywhere-src-5.12.0.tar.xz
```
Create build folder
```
mkdir build
cd build/
```
Configure Qt with this command
```
PKG_CONFIG_LIBDIR=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig \
PKG_CONFIG_SYSROOT_DIR=/ \
../qt-everywhere-src-5.12.0/configure -v -opengl es2 -eglfs -no-gtk \
-device linux-rasp-pi3-g++ -device-option CROSS_COMPILE=/usr/bin/ \
-opensource -confirm-license -release -reduce-exports \
-force-pkg-config -no-kms -nomake examples -no-compile-examples -no-pch \
-skip qtwayland -skip qtwebengine -no-feature-geoservices_mapboxgl \
-qt-pcre -ssl -evdev -system-freetype -fontconfig -glib -prefix /opt/Qt5.12
```

Where:
* **qt-everywhere-src-5.12.0** change to a proper folder name where you un-tared downloaded Qt archive

If configuration succeeded, you will see something like this:
```
Qt is now configured for building. Just run 'make'.
Once everything is built, you must run 'make install'.
Qt will be installed into '/opt/Qt5.12'.
```
Compile
```
make
```
Install
```
sudo make install
```

### OpenGL Error
If you get an OpenGL error, something like this:
```
ERROR: Feature 'opengles2' was enabled, but the pre-condition 'config.win32 || (!config.watchos && !features.opengl-desktop && libs.opengl_es2)' failed.

ERROR: The OpenGL functionality tests failed!
You might need to modify the include and library search paths by editing QMAKE_INCDIR_OPENGL[_ES2],
QMAKE_LIBDIR_OPENGL[_ES2] and QMAKE_LIBS_OPENGL[_ES2] in the mkspec for your platform.
```
do the following:
* Find mkspecs/devices/linux-rasp-pi3-g++/qmake.conf file:
```
sudo apt install locate
sudo updatedb
sudo locate mkspecs/devices/linux-rasp-pi3-g++/qmake.conf
```
* Use text editor for example gedit to edit this file and change
```
what to change
```
to
```
VC_LIBRARY_PATH         = $$[QT_SYSROOT]/opt/vc/lib
VC_INCLUDE_PATH         = $$[QT_SYSROOT]/opt/vc/include

QMAKE_LIBDIR_OPENGL_ES2 = $${VC_LIBRARY_PATH}
QMAKE_LIBDIR_EGL        = $$QMAKE_LIBDIR_OPENGL_ES2
QMAKE_LIBDIR_OPENVG     = $$QMAKE_LIBDIR_OPENGL_ES2

QMAKE_INCDIR_EGL        = \
                        $${VC_INCLUDE_PATH} \
                        $${VC_INCLUDE_PATH}/interface/vcos/pthreads \
                        $${VC_INCLUDE_PATH}/interface/vmcs_host/linux
QMAKE_INCDIR_OPENGL_ES2 = $${QMAKE_INCDIR_EGL}
QMAKE_INCDIR_OPENVG     = $${QMAKE_INCDIR_EGL}

QMAKE_LIBS_OPENGL_ES2   = -lGLESv2
QMAKE_LIBS_EGL          = -lEGL -lGLESv2
QMAKE_LIBS_OPENVG       = -lEGL -lOpenVG -lGLESv2
```

* Make symbolic links
```
sudo ln -fs /opt/vc/lib/libGLESv2.so /opt/vc/lib/libGLESv2.so.2
sudo ln -fs /opt/vc/lib/libEGL.so /opt/vc/lib/libEGL.so.1
sudo ldconfig
```
* Remove everything from created build/ directory
```
cd build/
sudo rm -r *
```
* Use configure command again, compile and install.

### Pages
* http://www.tal.org/tutorials/building-qt-510-raspberry-pi-debian-stretch
* https://forum.qt.io/topic/95105/cross-compile-qt-raspberry-pi3-stretch-opengl-error/12

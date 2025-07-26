[app]

title = Skanirator
package.name = skanirator
package.domain = org.skanirator
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0
icon.filename = logo.png
orientation = portrait

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, CAMERA

# (str) Presplash background color (for new android toolchain)
presplash.color = #000000

# (str) Application theme
android.theme = '@android:style/Theme.Black.NoTitleBar'

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Supported orientation
orientation = portrait

# (str) Entry point
entrypoint = main.py

# (list) Application requirements
requirements = python3,kivy,pyzbar,opencv-python,requests

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK API to use
android.api = 31

# (str) Android minimum API your APK will support
android.minapi = 21

# (bool) Indicate if the application should be a service
android.service = False

# (str) Android entry point, default is ok
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) Copy library instead of making a libpymodules.so
copy_libs = 1

# (str) Custom source folders for requirements
# (Separate multiple paths with commas)
#requirements.source =

# (bool) Create a single APK or a bundle
android.packaging = apk

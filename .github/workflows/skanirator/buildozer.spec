[app]
title = Skanirator
package.name = skanirator
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt
version = 1.0
requirements = python3,kivy,requests,pyzbar,opencv-python,android,certifi,chardet,idna,urllib3
orientation = portrait
fullscreen = 1
icon.filename = logo.png

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
android.api = 33
android.ndk = 25b
android.sdk = 33
android.minapi = 21
android.permissions = CAMERA,INTERNET
android.arch = armeabi-v7a
android.ndk_path = 
android.sdk_path = 
# If you're using OpenCV with cv2.VideoCapture, uncomment the following:
# android.requirements = opencv-python

[app.android.ndk]
# For compatibility
android.ndk_api = 21

[app.android.dependencies]
# Extra dependencies
# (None here since opencv-python is handled via pip above)

[app.android.gradle_dependencies]
# Example: com.google.android.material:material:1.2.1

[app.android.meta_data]
# Example: com.google.android.geo.API_KEY = your_key_here

[app.android.private_storage]
# True means internal storage access
use_private_storage = False

[app.android.entrypoint]
# Default
entrypoint = org.kivy.android.PythonActivity

[app.android.logcat_filters]
# Example: *:S python:D

[app.android.p4a_whitelist]
# Optional

[app.android.add_src]
# Optional

[app.android.add_jars]
# Optional

[app.android.add_assets]
# Optional

[app.android.gradle_extra_args]
# Optional

[app.android.extra_packages]
# Optional

[app.android.permissions_ex]
# Optional

[app.android.minify]
# Optional

[app.android.enable_androidx]
# Optional

[app.android.enable_artifact_build]
# Optional

[app.android.aars]
# Optional

[app.android.include_libs]
# Optional

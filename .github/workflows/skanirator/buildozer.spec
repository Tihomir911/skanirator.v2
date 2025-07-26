[app]
title = Skanirator
package.name = skanirator
package.domain = org.skanirator.app
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,xml
version = 1.0
requirements = python3,kivy,pyzbar,opencv-python,requests
orientation = portrait
fullscreen = 1
icon.filename = logo.png

# Entry point of the application
entrypoint = main.py

# Android Permissions
android.permissions = CAMERA, INTERNET

# Include .kv and resource files
android.resource_files = style.kv, logo.png

# Exclude unnecessary files
exclude_patterns = *.md, *.zip, *.tar.gz

# Presplash and background (optional)
# presplash.filename = splash.png
# android.presplash_color = #000000

# Supported Android architectures
android.archs = arm64-v8a, armeabi-v7a

# Target Android API version
android.api = 33
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0

# Enable logcat for debugging
log_level = 2

# Hide title bar
android.hide_title = 1

# Include additional .so or .a files
# android.add_libs_armeabi = libs/armeabi/*.so
# android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

[buildozer]
log_level = 2
warn_on_root = 1
android.debug = 1


[app]
# -----------------------------------------------------
# Basic App Config
# -----------------------------------------------------
title = FaceApp Backend
package.name = faceapp_backend
package.domain = com.example
source.dir = .
source.include_exts = py,kv,jpg,png,json,xml,mp3
version = 1.0
orientation = portrait
fullscreen = 0
# Requirements
requirements = python3,kivy,flask,flask-cors,opencv,numpy,requests,plyer
# Android permissions
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
# Architectures & API levels
android.arch = arm64-v8a,armeabi-v7a
android.minapi = 23
android.api = 33
# Bootstrap for WebView hosting
p4a.bootstrap = webview
# Entry point stays default (main.py)
# Logging
log_level = 2
warn_on_root = 1

[buildozer]
# Global buildozer options
log_level = 2
warn_on_root = 1

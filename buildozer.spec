[app]
title = A&A-Bauservice
package.name = aabauservice
package.domain = com.aabauservice
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,ini,json
version = 1.0.0
orientation = portrait
fullscreen = 0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,certifi
android.api = 35
android.minapi = 24
android.arch = arm64-v8a, armeabi-v7a
android.permissions = INTERNET, ACCESS_FINE_LOCATION
# Uncomment and provide your icon paths if desired
# icon.filename = assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 0

[android]
# If Gradle memory issues occur, you can raise this
# gradle_args = -Xmx4096m
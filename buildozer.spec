[app]
title = AABauservice
package.name = aabauservice
package.domain = org.aabauservice
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer,certifi
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
# Minimalne API dla zgodności
android.api = 31
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a,armeabi-v7a

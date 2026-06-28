[app]

title = PlantDoctor AI
package.name = plantdoctor
package.domain = org.plantdoctor

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

version = 1.0

requirements = python3,kivy,requests,python-dotenv

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,CAMERA

android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b

presplash.filename =
icon.filename =

[buildozer]

log_level = 2

warn_on_root = 1
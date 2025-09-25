# A&A‑Bauservice (KivyMD, APK-ready, bez Expo)

Lekka, natywna aplikacja na Androida napisana w **Python + KivyMD**. Zawiera ekrany:
- Główna (status pracy, licznik czasu, szybkie statystyki)
- Czas pracy (projekt, pojazd, notatki, materiały)
- Pracownicy (lista przykładowa)
- Raporty (podsumowanie miesiąca, przycisk "Generuj PDF" – placeholder)
- Ustawienia (powiadomienia, GPS, automatyczne przerwy)

Stan zapisywany lokalnie w `JsonStore` (Android Internal Storage).

## Szybkie uruchomienie desktop (Windows/Mac/Linux)
1. Zainstaluj Pythona 3.10–3.12.
2. `pip install kivy==2.3.0 kivymd==1.2.0 plyer`
3. `python main.py`

## Budowanie APK (Android) – Buildozer (Linux/WSL2 zalecane)
**Opcja A (WSL2 na Windows):**
1. Zainstaluj WSL2 + Ubuntu.
2. W Ubuntu: 
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-setuptools python3-venv git zip openjdk-17-jdk
   pip install --upgrade buildozer cython
   ```
3. W katalogu projektu uruchom:
   ```bash
   buildozer android debug
   ```
   Gotowy plik znajdziesz w `bin/*.apk` (debug-apk do szybkiej instalacji).

**Opcja B (Linux natywnie):**
1. Zainstaluj wymagania systemowe zgodnie z dokumentacją Buildozera.
2. `pip install --upgrade buildozer cython`
3. `buildozer android debug`

> Pierwsza kompilacja pobierze SDK/NDK i może potrwać. Kolejne są dużo szybsze.

## Uprawnienia
- `INTERNET` – na przyszłość (np. Supabase/HTTP).
- `ACCESS_FINE_LOCATION` – pod GPS (docelowo geofencing). W demie lokalizacja nie jest wymagana.

## Gdzie dopisać funkcje?
- Logika aplikacji: `main.py` (klasa `AABauserviceApp`).
- UI: sekcja `KV` w pliku `main.py` (łatwo rozbudować ekrany).
- Materiały/raporty/pojazdy – proste do rozszerzenia (zapis w `JsonStore`).

## Integracja z Supabase (opcjonalnie)
Kivy nie ma gotowego SDK Supabase – użyj `requests` (REST) lub `supabase-py` via HTTP.
Dodaj `requests` do `requirements` w `buildozer.spec`, a potem wołaj endpointy Supabase.

## Podpisanie i publikacja
- Debug APK: `bin/*-debug.apk` (instalacja bez sklepu).
- Release: `buildozer android release`, podpisz `jarsigner`/`apksigner` i zipalign, następnie wrzuć do Google Play.

Powodzenia! :)
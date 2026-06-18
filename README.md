# Candy Icons for Android

[![Build](https://github.com/neon798/candy-icons-android/actions/workflows/build.yml/badge.svg)](https://github.com/neon798/candy-icons-android/actions/workflows/build.yml)

Android icon pack based on [Candy Icons](https://github.com/EliverLara/candy-icons) by EliverLara — sweet gradient icons for your launcher.

## Features

- 234 hand-crafted gradient icons mapped to 2105 Android app components
- Pixel-perfect 192×192 PNG renders (no scaling artifacts)
- Supports Lawnchair, Nova, Apex, Action, Niagara, Smart, Hyperion, Microsoft, and more
- Zero network permissions — completely offline
- GPL-3.0 licensed

## Usage

1. Install the APK on your device
2. Open your launcher's settings
3. Navigate to the icon pack / theme section
4. Select **Candy Icons**

### Lawnchair

`Home Settings → General → Icon Style → Icon pack → Candy Icons`

### Nova Launcher

`Nova Settings → Look & feel → Icon Theme → Candy Icons`

## Building Locally

### Prerequisites

- Python 3 with `cairosvg` (`pip install cairosvg`)
- JDK 17
- Android SDK (set `ANDROID_HOME` environment variable)

### Build

```bash
git clone --recursive https://github.com/neon798/candy-icons-android.git
cd candy-icons-android

# Generate icon PNGs and appfilter.xml
./scripts/prebuild.sh

# Build the APK
./gradlew assembleRelease
```

APK will be at `app/build/outputs/apk/release/candy-icons-android-release.apk`.

## Adding / Updating Icons

1. Add new SVGs to the `candy-icons/apps/scalable/` directory (update the submodule)
2. Re-run `./scripts/prebuild.sh` to regenerate the mapping and PNGs
3. Rebuild the APK

## License

- Code: GPL-3.0
- Icons: [Candy Icons](https://github.com/EliverLara/candy-icons) — GPL-3.0 by EliverLara

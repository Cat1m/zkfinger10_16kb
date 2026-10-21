# zkfinger10_16kb

[![pub package](https://img.shields.io/pub/v/zkfinger10_16kb.svg)](https://pub.dev/packages/zkfinger10_16kb)
[![Flutter](https://img.shields.io/badge/Flutter-3.35.3%2B-blue.svg)](https://flutter.dev)
[![Android](https://img.shields.io/badge/Android-API%2021%2B-green.svg)](https://developer.android.com)

Flutter plugin for ZKTeco USB fingerprint scanners (enroll, identify, verify), **patched to work on Android devices with a 16 KB memory page size**.

This is a fork of [zkfinger10 1.0.0+2](https://pub.dev/packages/zkfinger10) by Mamasodikov ([zk_finger_10](https://github.com/Mamasodikov/zk_finger_10)). The API is the same; only the package name, Android namespace and channel names differ.

> **Unofficial.** Not affiliated with ZKTeco. The bundled `.so`/`.jar` files are ZKTeco's SDK binaries, redistributed as in the original package.

## Why this fork?

On 16 KB page size devices (required for new apps targeting Android 15+ on Google Play), the original package crashes with `SIGSEGV` as soon as the ZKTeco native libraries are loaded.

The four arm64 libraries (`libslkidcap`, `libzkalg12`, `libzkfinger10`, `libzksensorcore`) were built with GCC 4.9 (NDK <= r17). Their `LOAD` segments are already 64 KB aligned, but `PT_GNU_RELRO` ends on a 4 KB boundary. On a 16 KB kernel the dynamic linker rounds the RELRO `mprotect` up to 16 KB and makes part of `.data` read-only, so the first write crashes.

### The patch

`tool/patch_relro.py` changes the `PT_GNU_RELRO` program header type to `PT_NULL` (4 bytes per file; no offsets or sizes change).

**Trade-off:** these four libraries no longer get RELRO hardening. Nothing else is changed.

Verify the bundled libraries:

```bash
python tool/patch_relro.py --check   # exit 0 = safe on 16 KB devices
```

SHA-256 of the patched arm64 libraries:

| File | SHA-256 |
|---|---|
| libslkidcap.so | `7135e3557ff0baec68803081a4e151c70db489ec3200577cb6cb4c9f25c3ab64` |
| libzkalg12.so | `b55e9c7cdbdca352e83d8605607395f516ec8459a9b6aec5ff104f9d46a203ce` |
| libzkfinger10.so | `c9e962f48b9c82c8a948d8acc340d951f923ce5cb031ac8b3d1c094c88718363` |
| libzksensorcore.so | `0d1d2de24da8a0dbc95f771c360c2dc3c80737fa962f3a4e8862e7004429a684` |

The Android Gradle Plugin strips the libraries when building your APK, so their hashes inside the APK will differ; the patch is preserved. To verify a built app, extract `lib/arm64-v8a/` from the APK and run `python tool/patch_relro.py <dir> --check`.

When ZKTeco ships an SDK built with NDK r28+, the libraries will be replaced and the patch dropped.

### Extra APIs

```dart
// Page size of the running device (does not load ZKTeco libraries).
int? pageSize = await ZkFinger.getPageSize(); // 4096 or 16384

// Loads the ZKTeco native libraries and initializes the algorithm without a scanner.
// Useful to confirm the app does not crash on a 16 KB device.
List<String> log = await ZkFinger.selfTest();
```

## Migrating from zkfinger10

1. Replace the dependency:
   ```yaml
   dependencies:
     zkfinger10_16kb: ^1.0.0
   ```
2. Replace imports: `package:zkfinger10/...` → `package:zkfinger10_16kb/...`.

Everything else (method names, events, the `zkfinger10.db` template database) stays the same, so enrolled fingerprints are kept.

---

## 📱 **Sample Screenshot**

<p align="center">
  <img src="https://github.com/user-attachments/assets/1f61fad1-78be-4ba5-bca7-d3a3912f269a"
       alt="screenshot"
       style="max-width: 100%; height: auto; border-radius: 10px;" />
</p>

A modern, fully updated Flutter plugin for ZKTeco fingerprint scanners with **Flutter v3.35.3 compatibility** and **Android Plugin V2 embedding**. This package provides comprehensive support for ZKTeco fingerprint devices including enrollment, verification, and advanced template management.

## ✨ **Major v1.0.0 Update - Fully Modernized!**

This plugin has been completely modernized for 2024+ Flutter development:
- 🎯 **Flutter v3.35.3 Compatible**
- 🔧 **Android Plugin V2 Embedding**
- 📱 **Android API 34+ Support**
- 🏗️ **Modern Gradle Build System**
- 💾 **Enhanced Database Management**
- 🔒 **Improved Security & Performance**

## 📱 **Supported Devices**

Compatible with ZKTeco fingerprint scanners including:
- **SLK20R** series
- **ZK9500** series
- **ZK6500** series
- **ZK8500R** series
- Other ZKTeco USB fingerprint devices

> **Note**: This is an unofficial community-maintained package

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/2fac6ad2-b718-4289-86a3-6b47b4563d27"
    alt="cbdd3449eef878911f5c7b6ec75365d2-300x300 (1)"
    style="max-width: 100%; height: auto; border-radius: 10px; object-fit: contain;"
  />
</p>


## 🚀 **Getting Started**

### **Requirements**


- **Flutter**: 3.35.0 or higher
- **Dart SDK**: 3.1.0 or higher
- **Android**: API 21+ (Android 5.0+)
- **Target Android**: API 34 (Android 14)

### **Installation**

Add this to your package's `pubspec.yaml` file:

```yaml
dependencies:
  zkfinger10_16kb: ^1.0.0
```

Then run:
```bash
flutter pub get
```

## ⚙️ **Android Configuration**

### **1. Add Permissions**

Add these permissions to your `android/app/src/main/AndroidManifest.xml`:

- In the Manifest permission section add:

```xml
   <uses-permission
        android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32" />
    <uses-permission
        android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="32"
        tools:ignore="ScopedStorage" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.hardware.usb.host" />
```
    
    
### **2. Configure Activity Intent Filters**

Add these intent filters inside the `<activity>` tag in your AndroidManifest.xml:

```xml
<intent-filter>
    <action android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED" />
    <action android:name="android.intent.action.BOOT_COMPLETED" />
  </intent-filter>
  <meta-data
           android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED"
           android:resource="@xml/device_filter" />
```
           
           
### **3. Add USB Device Filter**

Create `android/app/src/main/res/xml/device_filter.xml` with the following content:

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <usb-device vendor-id="6997" product-id="289" />
</resources>
```

## 📚 **API Reference**

### **Core Methods**

```dart
import 'package:zkfinger10_16kb/zk_finger.dart';

// Initialize connection
await ZkFinger.openConnection();

// Register a fingerprint
await ZkFinger.registerFinger(userId: "user123");

// Identify a fingerprint
await ZkFinger.identify();

// Clear all fingerprints
await ZkFinger.clearFingerDatabase();

// Close connection
await ZkFinger.closeConnection();
```

### **🆕 New Bidirectional Data Management**

```dart
// Get fingerprint feature data for a specific user
String? feature = await ZkFinger.getUserFeature(userId: "user123");

// Get all users and their fingerprint data
Map<String, String>? users = await ZkFinger.getAllUsers();

// Get total count of users
int? count = await ZkFinger.getUserCount();

// Update user's fingerprint feature data
bool? success = await ZkFinger.updateUserFeature(
  userId: "user123",
  feature: "base64_encoded_fingerprint_data"
);

// Check if user exists
bool? exists = await ZkFinger.checkUserExists(userId: "user123");
```

### **Event Streams**

```dart
// Listen to fingerprint status changes
ZkFinger.statusChangeStream.receiveBroadcastStream().listen((status) {
  print('Status: $status');
});

// Listen to fingerprint image data
ZkFinger.imageStream.receiveBroadcastStream().listen((imageBytes) {
  // Process fingerprint image
});
```

## ⚠️ **Build Configuration**

### **Release Build Settings**

Add these lines to your `android/app/build.gradle` if you have problems on release:

```gradle
    buildTypes {
        release {
           ....
            
            //Add these lines when releasing your app
            minifyEnabled false
            shrinkResources false
            // useProguard false 
            
        }
    }
```

## 🔧 **Troubleshooting**

### **Common Issues**

1. **Plugin not found**: Ensure you've run `flutter pub get` and restarted your IDE
2. **USB permission denied**: Check that your device filter XML is correctly configured
3. **Build errors**: Verify your Flutter and Android versions meet the requirements
4. **Runtime crashes**: Ensure you're targeting Android API 34+ with proper permissions

### **Migration from v0.x.x**

If upgrading from an older version:

1. **Update Flutter**: Ensure you're using Flutter 3.35.0+
2. **Update Android**: Target API 34+ in your `build.gradle`
3. **Check Permissions**: Verify all required permissions are added
4. **Test Thoroughly**: The plugin now uses V2 embedding which may affect lifecycle behavior

## 🤝 **Contributing**

Found a bug or want to contribute?

- **Issues**: [GitHub Issues](https://github.com/Cat1m/zkfinger10_16kb/issues)
- **Pull Requests**: [GitHub PRs](https://github.com/Cat1m/zkfinger10_16kb/pulls)
- **Original package**: [Mamasodikov/zk_finger_10](https://github.com/Mamasodikov/zk_finger_10)
- **SDK Reference**: [ZKFinger10Demo](https://github.com/Mamasodikov/ZKFinger10Demo)

## 📄 **License**

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- [Mamasodikov](https://github.com/Mamasodikov) for the original `zkfinger10` plugin
- ZKTeco for the original SDK
- Flutter community for continuous support
- All contributors who helped modernize this plugin

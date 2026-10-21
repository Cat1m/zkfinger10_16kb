# flutter_zkfinger10 (fork nội bộ)

Fork của [zkfinger10 1.0.0+2](https://pub.dev/packages/zkfinger10) (Mamasodikov/zk_finger_10), dùng cho HisMobile.

## Thay đổi so với bản gốc
- **Vá 16 KB page size** cho 4 thư viện ZKTeco arm64 (`libslkidcap`, `libzkalg12`, `libzkfinger10`, `libzksensorcore`).
  Các file này được build bằng GCC 4.9 (NDK <= r17): segment LOAD đã căn 64 KB, nhưng `PT_GNU_RELRO` kết thúc ở mốc 4 KB,
  nên trên máy 16 KB linker `mprotect` lan sang `.data` gây SIGSEGV. Script `tool/patch_relro.py` đổi header RELRO thành `PT_NULL`
  (chỉ đổi 4 byte, không đổi offset/size). Đánh đổi: các thư viện này không còn RELRO hardening.
  Kiểm tra: `python tool/patch_relro.py --check` (exit 0 = an toàn).
- Thêm `ZkFinger.getPageSize()` (không tải thư viện native của ZKTeco).

SHA-256 trước -> sau khi vá:
| File | Gốc | Đã vá |
|---|---|---|
| libslkidcap.so | 6dac3900…f4bbcc | 7135e355…c3ab64 |
| libzkalg12.so | da72ee1d…1ab276 | b55e9c7c…a203ce |
| libzkfinger10.so | cb61502f…fef3f3 | c9e962f4…718363 |
| libzksensorcore.so | 8e87eaac…caf794 | 0d1d2de2…29a684 |

Khi ZKTeco phát hành SDK build bằng NDK r28+, thay `.so`/`.jar` trong `android/libs` và bỏ bản vá.

---

<div align="center"><a href="https://github.com/Safouene1/support-palestine-banner/blob/master/Markdown-pages/Support.md"><img src="https://raw.githubusercontent.com/Safouene1/support-palestine-banner/master/banner-project.svg" alt="Support Palestine" style="width: 100%;"></a></div>

# zkfinger10 - Modern Fingerprint Plugin for Flutter 🚀

[![pub package](https://img.shields.io/pub/v/zkfinger10.svg)](https://pub.dev/packages/zkfinger10)
[![Flutter](https://img.shields.io/badge/Flutter-3.35.3%2B-blue.svg)](https://flutter.dev)
[![Android](https://img.shields.io/badge/Android-API%2021%2B-green.svg)](https://developer.android.com)
[![Stand with Palestine](https://img.shields.io/badge/🇵🇸%20%20Stand%20With%20Palestine-007A3D?style=plastic&logo=liberapay&logoColor=white&labelColor=007A3D)](https://www.islamic-relief.org.uk/giving/appeals/palestine/)

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
  zkfinger10: ^1.0.0
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
import 'package:zkfinger10/zkfinger10.dart';

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
ZkFinger.fingerStatusChangeStream.listen((status) {
  print('Status: ${status['message']}');
});

// Listen to fingerprint image data
ZkFinger.fingerImageStream.listen((imageBytes) {
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

- **Issues**: [GitHub Issues](https://github.com/Mamasodikov/zk_finger_10/issues)
- **Pull Requests**: [GitHub PRs](https://github.com/Mamasodikov/zk_finger_10/pulls)
- **SDK Reference**: [ZKFinger10Demo](https://github.com/Mamasodikov/ZKFinger10Demo)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- ZKTeco for the original SDK
- Flutter community for continuous support
- All contributors who helped modernize this plugin

import 'package:flutter/foundation.dart';

import 'finger_status_type.dart';

class FingerStatus {
  FingerStatus(this.message, this.statusType, this.id, this.data);

  final String message;
  final FingerStatusType statusType;
  final String id;
  final String data;

  void log() {
    debugPrint('======Finger Status======');
    debugPrint('Message: $message');
    debugPrint('Id: $id');
    debugPrint('Status: $statusType');
    debugPrint('Data: $data');
  }
}

package io.github.cat1m.zkfinger10_16kb.util;

import android.graphics.Bitmap;

public interface FingerListener {

    void onStatusChange(String message, FingerStatusType fingerStatusType, String id, String data);

    void onCaptureFinger(Bitmap fingerBitmap);

}

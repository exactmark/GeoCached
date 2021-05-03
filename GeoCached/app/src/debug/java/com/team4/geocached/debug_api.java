package com.team4.geocached;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

public class debug_api extends AppCompatActivity {

    LocationObj locationObj;
    ServerConnection serverConnection = new ServerConnection();
    String text;
    String sessionId;
    TextView tv;

    private final LocationListener l = new LocationListener() {

        @Override
        public void onLocationChanged(@NonNull Location location) {
            Log.d("Lat", String.valueOf(location.getLatitude()));
            Log.d("Long", String.valueOf(location.getLongitude()));
        }
    };
    LocationManager mLocationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_debug_api);

        tv = findViewById(R.id.getSingleLocation);

        text = "DEFAULT_TEXT";

        mLocationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        mLocationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 1, l);

//        new Thread(() -> {
//            // Run in background
//            try {
////                location = serverConnection.get_single_location(3);
////                text = location.getName();
////                text = serverConnection.get_location_list();
////                text = serverConnection.add_user("test123", "testpwd1723");
//                text = serverConnection.login("test123", "testpwd1723");
//
//
////                for(String id: text.split(",")){
//////                    Log.d("id", String.valueOf(Integer.parseInt(id)));
////                    location = serverConnection.get_single_location((Integer.parseInt(id)));
//////                    Log.d("Loc", id);
////                    text= location.getName();
////                }
//
//            }
//            catch (Exception e){
//                Log.d("ERR",e.getMessage());
//            }
//            // Update UI post execution
//            runOnUiThread(() -> tv.setText(text));
//        }).start();



    }
}
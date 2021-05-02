package com.team4.geocached;



import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;


import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;

import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.InputStream;

class MyLocationListener implements LocationListener{

    LocationObj current;
    LocationObj to;
    TextView directionText;
    ImageView directionMarker;
    Button checkin;
    MyLocationListener(LocationObj curr, LocationObj to, TextView dirText, ImageView dirMarker, Button check){
        current = curr;
        directionText = dirText;
        directionMarker = dirMarker;
        this.to = to;
        checkin = check;

    }
    @Override
    public void onLocationChanged(@NonNull Location location) {
        current = new LocationObj();
        current.setX_coord(location.getLatitude());
        current.setY_coord(location.getLongitude());
        double dir_theta = bearing(current, to);

        if(dir_theta >= 35 && dir_theta <=55){
            directionText.setText("NE");
        }
        else if(dir_theta >= 125 && dir_theta <=145){
            directionText.setText("NW");
        }
        else if(dir_theta >= 215 && dir_theta <=235){
            directionText.setText("SW");
        }
        else if(dir_theta >= 305 && dir_theta <=325){
            directionText.setText("SE");
        }
        else if(dir_theta < 35 && dir_theta > 325){
            directionText.setText("E");
        }
        else if(dir_theta > 55 && dir_theta < 125){
            directionText.setText("N");
        }
        else if(dir_theta > 145 && dir_theta < 215){
            directionText.setText("W");
        }
        else if(dir_theta >  235 && dir_theta < 305){
            directionText.setText("S");
        }

        double x = Math.round(computeDist(current, to) * 100.0) / 100.0;
        directionText.setText(directionText.getText() + ", "+ x+"m away.");
        directionMarker.setRotation((float)dir_theta);

        if(x<50){
            checkin.setEnabled(true);
        }
        else{
            checkin.setEnabled(false);
        }

        Log.d("BEARING", String.valueOf(bearing(current, to)));
        Log.d("DIST", String.valueOf(computeDist(current, to)));
    }



    private double computeDist(LocationObj from, LocationObj to){
        double R = 6378100; // metres
        double phi1 = from.getX_coord() * Math.PI/180; // φ, λ in radians
        double phi2 = to.getX_coord() * Math.PI/180;
        double dphi = (to.getX_coord()-from.getX_coord()) * Math.PI/180;
        double dlambda = (to.getY_coord()-from.getY_coord()) * Math.PI/180;

        double a = Math.sin(dphi/2) * Math.sin(dphi/2) +
                Math.cos(phi1) * Math.cos(phi2) *
                        Math.sin(dlambda/2) * Math.sin(dlambda/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        double d = R * c; // in metres

        return d;
    }

    private double bearing(LocationObj from, LocationObj to){
        double p1 = from.getX_coord() * Math.PI/180;
        double p2 = to.getX_coord() * Math.PI/180;
        double l1 = from.getY_coord() * Math.PI/180;
        double l2 = to.getY_coord() * Math.PI/180;

        double y = Math.sin(l2-l1) * Math.cos(p2);
        double x = Math.cos(p1)*Math.sin(p2) -
                Math.sin(p1)*Math.cos(p2)*Math.cos(l2-l1);
        double θ = Math.atan2(y, x);
        double brng = (θ*180/Math.PI + 360) % 360; // in degrees
        return brng;
    }
}

public class SingleLocation extends AppCompatActivity{

    TextView description;
    TextView name;
    TextView directionText;
    ImageView blurryImage;
    LocationObj locationObj;
    LocationObj current;
    LocationObj to;
    ImageView directionMarker;
    Button checkin;
    ServerConnection serverConnection = new ServerConnection();



    LocationManager locationManager;

    private double computeDist(LocationObj from, LocationObj to){
        double R = 6378100; // metres
        double phi1 = from.getX_coord() * Math.PI/180; // φ, λ in radians
        double phi2 = to.getX_coord() * Math.PI/180;
        double dphi = (to.getX_coord()-from.getX_coord()) * Math.PI/180;
        double dlambda = (to.getY_coord()-from.getY_coord()) * Math.PI/180;

        double a = Math.sin(dphi/2) * Math.sin(dphi/2) +
                        Math.cos(phi1) * Math.cos(phi2) *
                                Math.sin(dlambda/2) * Math.sin(dlambda/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        double d = R * c; // in metres

        return d;
    }

    private double bearing(LocationObj from, LocationObj to){
        double p1 = from.getX_coord() * Math.PI/180;
        double p2 = to.getX_coord() * Math.PI/180;
        double l1 = from.getY_coord() * Math.PI/180;
        double l2 = to.getY_coord() * Math.PI/180;

        double y = Math.sin(l2-l1) * Math.cos(p2);
        double x = Math.cos(p1)*Math.sin(p2) -
                        Math.sin(p1)*Math.cos(p2)*Math.cos(l2-l1);
        double θ = Math.atan2(y, x);
        double brng = (θ*180/Math.PI + 360) % 360; // in degrees
        return brng;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_single_location);

        description = findViewById(R.id.description);
        name = findViewById(R.id.location_name);
        directionMarker = findViewById(R.id.directionMarker);
        directionText = findViewById(R.id.directionText);
        blurryImage = findViewById(R.id.blurryImage);
        checkin = findViewById(R.id.checkinbutton);
        checkin.setClickable(false);
        checkin.setOnClickListener((v)->{
            Intent checkinIntent = new Intent(getApplicationContext(), CheckIn.class);
            checkinIntent.putExtra("id",getIntent().getIntExtra("id",-1));
            startActivity(checkinIntent);
        });


        current = new LocationObj();
        to = new LocationObj();


        Intent intent = getIntent();
        Log.d("GOT FROM INTENT", String.valueOf(intent.getIntExtra("id",-1)));
        int loc_id = intent.getIntExtra("id",-1);


        new Thread(()->{
            Bitmap bmp = getImageBitmap("https://exactmark.pythonanywhere.com/images/"+loc_id+".jpg");
            try{
                locationObj = serverConnection.get_single_location(loc_id);
                to.setX_coord(locationObj.getX_coord());
                to.setY_coord(locationObj.getY_coord());
            }
            catch (Exception e){
                e.printStackTrace();
            }

            runOnUiThread(()->{
                name.setText(""+ locationObj.getName());
                description.setText(""+ locationObj.getDescription());
//                int res_id = getResources().getIdentifier("i"+loc_id+"_sub_32", "drawable", getPackageName());

                
                blurryImage.setImageBitmap(bmp);
            });
        }).start();

        LocationListener locationListener = new MyLocationListener(current, to, directionText, directionMarker, checkin);

        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);

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
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 1, locationListener);


    }
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case 1: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                } else {
                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.
                }
                return;
            }
            // other 'case' lines to check for other
            // permissions this app might request
        }
    }
    private Bitmap getImageBitmap(String url){
        Bitmap bitmap = null;
        try {
            // Download Image from URL
            InputStream input = new java.net.URL(url).openStream();
            // Decode Bitmap
            bitmap = BitmapFactory.decodeStream(input);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return bitmap;
    }


}

package com.team4.geocached;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.ImageDecoder;
import android.graphics.Paint;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Set;

public class AddGeoCache extends AppCompatActivity {

    Button captureImage;
    ImageView imageView;
    Button submit;
    EditText locationName;
    EditText locationDesc;
    double[] XY;
    LocationListener locationListener;

    LocationManager locationManager;

    int addResult;

    int REQUEST_IMAGE_CAPTURE = 1;
    File photoFile;
    ServerConnection sc = new ServerConnection();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_geo_cache);

        captureImage = findViewById(R.id.captureImage);
        imageView = findViewById(R.id.imgForUpload);
        submit = findViewById(R.id.putLocationWithImage);
        submit.setEnabled(false);
        locationName = findViewById(R.id.addLocName);
        locationDesc = findViewById(R.id.addLocDesc);


        locationName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                validateFields();
            }
        });

        locationDesc.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                validateFields();
            }
        });


        captureImage.setOnClickListener(v->{
            takePicture();
        });

        submit.setOnClickListener(v->{
            upload();
        });

        XY = new double[2];

        locationListener = new ExtraLocationListener(XY);

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

    public void validateFields(){
        if(locationName.getText().length() != 0 && locationDesc.getText().length() != 0 && imageView.getDrawable() != null){
            submit.setEnabled(true);
        }
        else{
            submit.setEnabled(false);
        }
    }

    String currentPhotoPath;

    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    private void takePicture(){
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if(cameraIntent.resolveActivity(getPackageManager()) != null) {


            photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException e) {
                Log.d("AddGeoCache", e.getMessage());
            }

            if (photoFile != null) {
                Uri photoUri = FileProvider.getUriForFile(this, "com.team4.geocached", photoFile);
                cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
                startActivityForResult(cameraIntent, REQUEST_IMAGE_CAPTURE);
            }


        }

    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(resultCode == RESULT_OK){
            Bitmap image = BitmapFactory.decodeFile(photoFile.getAbsolutePath());
            imageView.setImageBitmap(image);
        }

    }


    void upload(){

        new Thread(()->{
            int result = sc.add_location_details(locationName.getText().toString(), locationDesc.getText().toString(), XY);
            addResult = result;
            if(addResult>0){
                sc.add_location_photo(result, photoFile);
                Log.d("Adding image","success");
            }
            else{
                Log.d("ADD RESULT", ""+result);
            }

            runOnUiThread(()->{
                switch (addResult){
                    case -2:
                        Toast.makeText(getApplicationContext(),"Location too close to another location", Toast.LENGTH_SHORT);
                        break;
                    default:
                        Toast.makeText(getApplicationContext(),"Successfully added", Toast.LENGTH_SHORT);
                        finish();
                        break;
                }
            });
        }).start();

    }
}

class ExtraLocationListener implements LocationListener {

    double[] XY;

    ExtraLocationListener(double[] XY){
        this.XY = XY;
    }

    @Override
    public void onLocationChanged(@NonNull Location location) {
        XY[0] = location.getLatitude();
        XY[1] = location.getLongitude();
    }

}



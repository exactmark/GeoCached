package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

public class debug_api extends AppCompatActivity {

    Location location = new Location();
    ServerConnection serverConnection = new ServerConnection();
    String text;
    TextView tv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_debug_api);

        tv = findViewById(R.id.getSingleLocation);

        text= "DEFAULT_TEXT";

        new Thread(() -> {
            // Run in background
            try {
                text = serverConnection.get_single_location(2);
            }
            catch (Exception e){
                Log.d("ERR",e.getMessage());
            }
            // Update UI post execution
            runOnUiThread(() -> tv.setText(text));
        }).start();

    }
}
package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
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
        String URL = getResources().getString(R.string.server_url) + "/?id=2";
        new Thread(() -> {
            // Run in background
            try {
                text = serverConnection.ping(URL);
            }
            catch (Exception e){
                e.printStackTrace();
            }
            // Update UI post execution
            runOnUiThread(() -> tv.setText(text));
        }).start();

    }
}
package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;


public class MainActivity extends AppCompatActivity {

    TextView textView;
    ServerConnection serverConnection;
    String text = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.tv);

        serverConnection = new ServerConnection();


        new Thread(() -> {
            // Run in background
            try {
                text = serverConnection.ping(getResources().getString(R.string.server_url));
            }
            catch (Exception e){
                e.printStackTrace();
            }
            // Update UI post execution
            runOnUiThread(() -> textView.setText(text));
        }).start();




    }


}
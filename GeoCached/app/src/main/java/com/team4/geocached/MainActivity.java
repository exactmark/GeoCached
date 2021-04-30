package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;

import java.util.ArrayList;


public class MainActivity extends AppCompatActivity {

    Button debug;
    ServerConnection sc = new ServerConnection();
    ArrayList<LogEntry> logEntries = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        debug = findViewById(R.id.debug_api);
        Intent intent = new Intent(getApplicationContext(), AddGeoCache.class);
        startActivity(intent);
        finish();

//        debug.setOnClickListener(v -> {
//            intent = new Intent(getApplicationContext(), debug_api.class);
//            startActivity(intent);
//        });

//        new Thread(() -> {
//            // Run in background
//            try {
//                logEntries = sc.get_log_entries(1);
//
//
//            }
//            catch (Exception e){
//                Log.d("ERR",e.getMessage());
//            }
//
//        }).start();

    }


}
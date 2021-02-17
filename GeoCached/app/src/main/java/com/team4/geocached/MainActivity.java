package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;


public class MainActivity extends AppCompatActivity {

    Button debug;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        debug = findViewById(R.id.debug_api);
        Intent intent = new Intent(getApplicationContext(), debug_api.class);
        startActivity(intent);

//        debug.setOnClickListener(v -> {
//            intent = new Intent(getApplicationContext(), debug_api.class);
//            startActivity(intent);
//        });
    }


}
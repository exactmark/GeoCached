package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

public class CheckIn extends AppCompatActivity {

    ImageView clearImage;
    TextView locationName;
    ServerConnection sc = new ServerConnection();
    LogEntry logEntry;
    LocationObj location;
    ListView logEntryList;
    ArrayList<LogEntry> logEntries = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_in);

        clearImage = findViewById(R.id.clearImage);
        int loc_id = getIntent().getIntExtra("id", -1);
        int res_id = getResources().getIdentifier("i"+loc_id, "drawable", getPackageName());

        clearImage.setImageDrawable(getDrawable(res_id));

        logEntryList = findViewById(R.id.logEntriesList);
        locationName = findViewById(R.id.locationName);


        new Thread(() -> {
            // Run in background
            try {
                location = sc.get_single_location(loc_id);
                logEntries = sc.get_log_entries(loc_id);
                Log.d("Name", location.getName());

            }
            catch (Exception e){
                Log.d("ERR",e.getMessage());
            }

            // Update UI post execution
            runOnUiThread(() ->{
                LogEntryAdapter logEntryAdapter = new LogEntryAdapter(this,R.layout.list_log_entry,logEntries);
                locationName.setText(location.getName());
                Log.d("Name", location.getName());
                logEntryList.setAdapter(logEntryAdapter);
            });
        }).start();



    }
}
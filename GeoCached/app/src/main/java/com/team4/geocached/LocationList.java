package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import java.util.ArrayList;

public class LocationList extends AppCompatActivity {
    ListView listView;
    LocationObj locationObj;
    ServerConnection serverConnection= new ServerConnection();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_location_list);

        listView =findViewById(R.id.listView);

        //Create data
        ArrayList<LocationObj> arrayList = new ArrayList<>();
        // TODO add locations

        new Thread(() -> {
            // Run in background
            try {
                String loc_ids = serverConnection.get_location_list();

                for(String id: loc_ids.split(",")){
                    locationObj = serverConnection.get_single_location((Integer.parseInt(id.trim())));
                    arrayList.add(locationObj);
                }

            }
            catch (Exception e){
                Log.d("ERR",e.getMessage());
            }

            // Update UI post execution
            runOnUiThread(() ->{
                    LocationAdapter locationAdapter = new LocationAdapter(this,R.layout.list_row,arrayList);

                    listView.setAdapter(locationAdapter);
                    listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                        @Override
                        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                            Intent i = new Intent(LocationList.this, SingleLocation.class);
                            LocationObj list_locationObj = (LocationObj)parent.getItemAtPosition(position);

                            i.putExtra("id", list_locationObj.getId());



                            startActivity(i);
                        }
                    });

                });
        }).start();

    }
}
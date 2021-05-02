package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;

import java.util.ArrayList;

public class LocationList extends AppCompatActivity {
    ListView listView;
    LocationObj locationObj;
    ServerConnection serverConnection= new ServerConnection();
    Button addGeoCache;

    public static Drawable getDrawableByName(String name, Context context) {
        int drawableResource = context.getResources().getIdentifier(name, "drawable", context.getPackageName());
        if (drawableResource == 0) {
            throw new RuntimeException("Can't find drawable with name: " + name);
        }
        return context.getResources().getDrawable(drawableResource);
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_location_list);

        listView =findViewById(R.id.listView);
        addGeoCache = findViewById(R.id.addLocation);

        addGeoCache.setOnClickListener((v)->{
            Intent i = new Intent(LocationList.this, AddGeoCache.class);

            startActivity(i);
        });

        //Create data
        ArrayList<LocationObj> arrayList = new ArrayList<>();


        new Thread(() -> {
            // Run in background
            try {
                String loc_ids = serverConnection.get_location_list();
                Resources resources = getResources();
                int res_id =-1;
                for(String id: loc_ids.split(",")){
                    locationObj = serverConnection.get_single_location((Integer.parseInt(id.trim())));

//                    Log.d("Discovery img:", String.valueOf(getDrawableByName("i"+id.trim(), this)));

                    res_id = getResources().getIdentifier("i"+id.trim()+"_sub_16", "drawable", getPackageName());
                    Log.d("Discovery img:", String.valueOf(res_id));
                    locationObj.setImage(res_id);
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
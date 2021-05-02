package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.material.textfield.TextInputEditText;

public class AddLogEntry extends AppCompatActivity {

    SharedPreferences sp;
    SharedPreferences.Editor editor;
    String user;

    Button addLogEntrySubmit;
    TextInputEditText comments;

    ServerConnection sc = new ServerConnection();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_log_entry);

        sp = getApplicationContext().getSharedPreferences("geocached", Context.MODE_PRIVATE);
        user = sp.getString("user_id", "no_user");
        int loc_id = getIntent().getIntExtra("loc_id", -1);

        Log.d("User", user);

        addLogEntrySubmit = findViewById(R.id.addLogEntrySubmit);
        comments = findViewById(R.id.addLogText);

        comments.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                Log.d("comments", comments.getText().toString());
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        addLogEntrySubmit.setOnClickListener((v)->{
            new Thread(()->{
                int result = sc.add_log_entry(loc_id, user, comments.getText().toString());
                if(result == -2){
                    Log.d("Failed to add","Location id error");
                }
                else if(result == -1){
                    Log.d("Failed to add","Server err");
                }
                else if (result>0){
                    Log.d("Success","Added log entry");
                }
                finish();
            }).start();
        });
    }
}
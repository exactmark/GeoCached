package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ImageView;

public class CheckIn extends AppCompatActivity {

    ImageView clearImage;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_in);

        clearImage = findViewById(R.id.clearImage);
        int loc_id = getIntent().getIntExtra("id", -1);
        int res_id = getResources().getIdentifier("i"+loc_id, "drawable", getPackageName());

        clearImage.setImageDrawable(getDrawable(res_id));
    }
}
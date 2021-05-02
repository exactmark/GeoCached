package com.team4.geocached;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.io.InputStream;
import java.util.ArrayList;

public class LocationAdapter extends ArrayAdapter<LocationObj> {
    private Context mContext;
    private int mResource;

    public LocationAdapter(@NonNull Context context, int resource, @NonNull ArrayList<LocationObj> objects) {
        super(context, resource, objects);
        this.mContext = context;
        this.mResource= resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);

        convertView = layoutInflater.inflate(mResource,parent,false);

        ImageView imageView =convertView.findViewById(R.id.image);

        TextView txtName =convertView.findViewById(R.id.txtName);

        TextView txtDes =convertView.findViewById(R.id.txtDes);

        TextView dist =convertView.findViewById(R.id.distanceLoc);

        new Thread(()->{
            Bitmap bmp = getImageBitmap("https://exactmark.pythonanywhere.com/images/"+getItem(position).getId()+"_sub_16.jpg");

            ((Activity)mContext).runOnUiThread(()->{
                imageView.setImageBitmap(bmp);
            });
        }).start();


        txtName.setText(getItem(position).getName());

        txtDes.setText(getItem(position).getDescription());

        dist.setText(""+getItem(position).getId());

        return  convertView;
    }

    private Bitmap getImageBitmap(String url){
        Bitmap bitmap = null;
        try {
            // Download Image from URL
            InputStream input = new java.net.URL(url).openStream();
            // Decode Bitmap
            bitmap = BitmapFactory.decodeStream(input);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return bitmap;
    }
}

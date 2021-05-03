package com.team4.geocached;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;

public class LogEntryAdapter extends ArrayAdapter<LogEntry> {
    private Context mContext;
    private int mResource;

    public LogEntryAdapter(@NonNull Context context, int resource, @NonNull ArrayList<LogEntry> objects) {
        super(context, resource, objects);
        this.mContext = context;
        this.mResource= resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);

        convertView = layoutInflater.inflate(mResource,parent,false);

        TextView logEntryText =convertView.findViewById(R.id.logEntryText);

        TextView userName =convertView.findViewById(R.id.userName);

        TextView timeStamp =convertView.findViewById(R.id.timeStamp);

        logEntryText.setText(""+getItem(position).getText());

        userName.setText(""+getItem(position).getUserID());

        timeStamp.setText(""+getItem(position).getTimestamp());

        return convertView;
    }
}

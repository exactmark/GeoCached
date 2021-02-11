package com.team4.geocached;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


public class ServerConnection {
    /**
     * Sample ServerConnection class to get content of a web page
     * */

    private URL url;

    public String ping(String url) throws IOException {
        this.url = new URL(url);

        HttpURLConnection httpURLConnection = (HttpURLConnection) this.url.openConnection();
        httpURLConnection.setRequestMethod("GET");

        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));

        StringBuilder stringBuilder = new StringBuilder();
        String line;

        while((line = bufferedReader.readLine())!=null){
            stringBuilder.append(line).append("\n");
        }
        bufferedReader.close();

        Log.d("SERVER BODY", stringBuilder.toString());
        Log.d("HTTP STATUS",""+httpURLConnection.getResponseCode());

        return stringBuilder.toString();

    }
}

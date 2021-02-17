package com.team4.geocached;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;


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

    private String constructURL(String URL, HashMap<String, String> queryParams){

        StringBuilder url = new StringBuilder(URL);

        try {
            for (Map.Entry<String, String> m : queryParams.entrySet()) {
                url.append("?"
                        + URLEncoder.encode(m.getKey(), "UTF-8")
                        + "="
                        + URLEncoder.encode(m.getValue(), "UTF-8"));
            }
        }
        catch (UnsupportedEncodingException unsupportedEncodingException){
            Log.d("URL", unsupportedEncodingException.getMessage());
        }


        return url.toString();

    }

    private HttpURLConnection URLConnectionObject(URL url, String requestMethod){

        HttpURLConnection connectionObject=null;
        try {
            connectionObject = (HttpURLConnection) url.openConnection();
            connectionObject.addRequestProperty("User-Agent", "com.team4.geocached");
            connectionObject.addRequestProperty("Accept-Language", "en-US");
            connectionObject.addRequestProperty("Accept", "text/json");
            connectionObject.setRequestMethod(requestMethod);

            if(connectionObject.getResponseCode() == 302){
                Log.d("302","Redirecting");
                url = new URL(connectionObject.getHeaderField("Location"));
                connectionObject = URLConnectionObject(url, requestMethod);
                return connectionObject;
            }

        } catch (IOException ioException) {
            ioException.printStackTrace();
        }

        return connectionObject;
    }

    private String ReadHttpResponse(HttpURLConnection connectionObject) {
        StringBuilder jsonData = new StringBuilder();
        BufferedReader streamData;
        try {
           streamData = new BufferedReader(new InputStreamReader(connectionObject.getInputStream()));

           String line;
           while ((line = streamData.readLine())!=null) {
               jsonData.append(line).append("\n");
           }
           streamData.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }

        return jsonData.toString();
    }

    public String get_single_location(int location_id){
        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("id", String.valueOf(location_id));

        String data=null;
        try {
            this.url = new URL(constructURL("http://exactmark.pythonanywhere.com/get_single_location", queryParams));
            httpURLConnection = URLConnectionObject(this.url, "GET");

            data = ReadHttpResponse(httpURLConnection);

        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        }

        Log.d("String", data);
        return data;


    }
}

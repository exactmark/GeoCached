package com.team4.geocached;


import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class ServerConnection {
    /**
     * Sample ServerConnection class to get content of a web page
     * */

    private URL url;
    private Object obj;

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
        boolean first = true;
        try {
            for (Map.Entry<String, String> m : queryParams.entrySet()) {
                if(first){
                    url.append("?");
                    first=false;
                }
                else
                    url.append("&");
                url.append(
                         URLEncoder.encode(m.getKey(), "UTF-8")
                        + "="
                        + URLEncoder.encode(m.getValue(), "UTF-8"));
            }
        }
        catch (UnsupportedEncodingException unsupportedEncodingException){
            Log.d("URL", unsupportedEncodingException.getMessage());
        }


        return url.toString();

    }
    private String constructPostData(HashMap<String, String> queryParams){

        StringBuilder url = new StringBuilder();
        boolean first = true;

        try {
            for (Map.Entry<String, String> m : queryParams.entrySet()) {
                if(first)
                    first=false;
                else
                    url.append("&");

                url.append(
                         URLEncoder.encode(m.getKey(), "UTF-8")
                        + "="
                        + URLEncoder.encode(m.getValue(), "UTF-8"));
            }
        }
        catch (UnsupportedEncodingException unsupportedEncodingException){
            Log.d("URL", unsupportedEncodingException.getMessage());
        }


        return url.toString();

    }

    private String constructURL(String URL){

        StringBuilder url = new StringBuilder(URL);

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

    public String get_location_list(){
        HttpURLConnection httpURLConnection = null;


        String data=null;
        try {
            this.url = new URL(constructURL("http://exactmark.pythonanywhere.com/get_location_list/"));
            httpURLConnection = URLConnectionObject(this.url, "GET");

            data = ReadHttpResponse(httpURLConnection);

        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        }

        Log.d("String", data);
        return data;
    }

    public String login(String userId, String passwd){
        /*HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("id", userId);
        queryParams.put("pw",passwd);

        String data=null;
        try {
            this.url = new URL("http://exactmark.pythonanywhere.com/login/");
            httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("GET");
            httpURLConnection.setChunkedStreamingMode(0);
            httpURLConnection.addRequestProperty("Allow","");

            OutputStream os = httpURLConnection.getOutputStream();

            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(constructPostData(queryParams));

            writer.flush();
            writer.close();
            os.close();
            int responseCode=httpURLConnection.getResponseCode();

            Map<String, List<String>> hf = httpURLConnection.getHeaderFields();
            for(Map.Entry<String, List<String>> entry: hf.entrySet()){
                for(String vals : entry.getValue()){
                    Log.d(entry.getKey(), vals);
                }
            }

            if (responseCode == HttpURLConnection.HTTP_OK) {
                StringBuilder jsonData = new StringBuilder();
                BufferedReader streamData;
                try {
                    streamData = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));

                    String line;
                    while ((line = streamData.readLine())!=null) {
                        jsonData.append(line).append("\n");
                    }
                    streamData.close();
                }
                catch (IOException e){
                    e.printStackTrace();
                }

                data=jsonData.toString();

            }

            else {
                data="";

            }


        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }

        Log.d("String", data);

        */
        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("id", String.valueOf(userId));
        queryParams.put("pw", String.valueOf(passwd));

        String data=null;
        try {
            Log.d("HIT",constructURL("http://exactmark.pythonanywhere.com/login/", queryParams));
            this.url = new URL(constructURL("http://exactmark.pythonanywhere.com/login/", queryParams));
            httpURLConnection = URLConnectionObject(this.url, "GET");

            data = ReadHttpResponse(httpURLConnection);

        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        }

        Log.d("String", data);
        String session_key="-1";
        String message="";
        String err="";
        try{
            JSONObject jsonObject = new JSONObject(data);
            try{
                session_key = jsonObject.getString("session_key");
            }
            catch (Exception e){
                try{
                    session_key = "-1";
                }
                catch (Exception ex){
                    session_key = "-1";
                }
            }

        }
        catch (JSONException e) {
            e.printStackTrace();
        }

        return session_key;
    }

    public int add_user(String userId, String passwd){
        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("id", userId);
        queryParams.put("pw",passwd);

        String data=null;
        try {
            this.url = new URL("http://exactmark.pythonanywhere.com/add_single_user/");
            httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setChunkedStreamingMode(0);

            OutputStream os = httpURLConnection.getOutputStream();

            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(constructPostData(queryParams));

            writer.flush();
            writer.close();
            os.close();
            int responseCode=httpURLConnection.getResponseCode();

            Map<String, List<String>> hf = httpURLConnection.getHeaderFields();
            for(Map.Entry<String, List<String>> entry: hf.entrySet()){
                for(String vals : entry.getValue()){
                    Log.d(entry.getKey(), vals);
                }
            }

            if (responseCode == HttpURLConnection.HTTP_OK) {
                StringBuilder jsonData = new StringBuilder();
                BufferedReader streamData;
                try {
                    streamData = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));

                    String line;
                    while ((line = streamData.readLine())!=null) {
                        jsonData.append(line).append("\n");
                    }
                    streamData.close();
                }
                catch (IOException e){
                    e.printStackTrace();
                }

                data=jsonData.toString();

            }

            else {
                data="";

            }


        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }

        Log.d("String", data);

        String response="";
        String err="";

        try{
            JSONObject jsonObject = new JSONObject(data);
            try{
                response = jsonObject.getString("debug_message");
            }
            catch (Exception e) {
                err = jsonObject.getString("debug_error");
            }
        }
        catch (JSONException e){
            e.printStackTrace();
        }

        int result=-1;

        if (response.equalsIgnoreCase("user added")){
            result = 0;
        }

        if(err.equalsIgnoreCase("user exists.")){
            result = 1;
        }
        else if(err.equalsIgnoreCase("other faliure.")){
            result = 2;
        }
        else if(err.equalsIgnoreCase("use post")){
            result = 3;
        }


        return result;
    }

    public LocationObj get_single_location(int location_id){
        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("id", String.valueOf(location_id));

        String data=null;
        try {
            this.url = new URL(constructURL("http://exactmark.pythonanywhere.com/get_single_location/", queryParams));
            httpURLConnection = URLConnectionObject(this.url, "GET");

            data = ReadHttpResponse(httpURLConnection);

        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        }

        Log.d("String", data);


        String description="";
        String name="";
        double x_coord=-1;
        double y_coord=-1;
        int id = -1;
        try{
            JSONObject jsonObject = new JSONObject(data);
            description = jsonObject.getString("description");
            name = jsonObject.getString("name");
            x_coord = Double.parseDouble(jsonObject.getString("x_coord"));
            y_coord = Double.parseDouble(jsonObject.getString("y_coord"));
            id = Integer.parseInt(jsonObject.getString("id"));
            Log.d("XXX",jsonObject.getString("id"));
        }
        catch (JSONException e){
            e.printStackTrace();
        }
        LocationObj single_locationObj = new LocationObj(id, name, x_coord, y_coord, description);

        return single_locationObj;


    }
}

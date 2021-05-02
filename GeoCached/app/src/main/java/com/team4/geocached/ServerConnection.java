package com.team4.geocached;


import android.os.Build;
import android.util.Log;
import android.util.TimeFormatException;

import androidx.annotation.RequiresApi;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Date;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TimeZone;
import java.util.UUID;


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
        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("id", userId);
        queryParams.put("pw",passwd);

        String data=null;
        try {
            this.url = new URL("https://exactmark.pythonanywhere.com/login/");
            httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("POST");
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
        String session_key = "-1";
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

       /*
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
        */

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

    public ArrayList<LogEntry> get_log_entries(int location_id){

        ArrayList<LogEntry> logEntries = new ArrayList<>();

        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("loc_id", String.valueOf(location_id));

        String data=null;
        try {
            this.url = new URL(constructURL("http://exactmark.pythonanywhere.com/get_log_entries/", queryParams));
            httpURLConnection = URLConnectionObject(this.url, "GET");

            data = ReadHttpResponse(httpURLConnection);

        }
        catch (MalformedURLException malformedURLException){
            Log.d("URL",malformedURLException.getMessage());
        }

        Log.d("String", data);


        int id;
        int locationID;
        String userID;
        Date timestamp;
        String text;
        DateFormat simpleDateFormat = new SimpleDateFormat("EE, dd MMM yyyy HH:mm:ss z");
        simpleDateFormat.setTimeZone(TimeZone.getDefault());
        try{
            JSONObject jsonObject = new JSONObject(data);
            Iterator<String> logs = jsonObject.keys();

            while (logs.hasNext()){
                String entry = logs.next();
                Log.d("Entry", entry);
                Log.d("Data",jsonObject.getString(entry));
                if(entry.equalsIgnoreCase("debug_message")){
                    break;
                }
                JSONObject entryObj = new JSONObject(jsonObject.getString(entry));
                Log.d("id",""+entryObj.getString("id"));
                id = entryObj.getInt("id");
                locationID = entryObj.getInt("location_id");
                text = entryObj.getString("text");
                timestamp = simpleDateFormat.parse(entryObj.getString("timestamp"));
                userID = entryObj.getString("user_id");
                logEntries.add(new LogEntry(id, locationID, userID, timestamp, text));
            }

        }
        catch (JSONException | ParseException e){
            e.printStackTrace();
        }


        return logEntries;
    }


    public int add_location_details(String name, String description, double[] XY){
        HttpURLConnection httpURLConnection = null;

        HashMap<String, String> queryParams = new HashMap<>();

        queryParams.put("name", name);
        queryParams.put("description",description);
        queryParams.put("x_coord", String.valueOf(XY[0]));
        queryParams.put("y_coord", String.valueOf(XY[1]));


        String data=null;
        try {
            this.url = new URL("http://exactmark.pythonanywhere.com/add_location/");
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
        JSONObject jsonObject=null;
        int result=-1;
        try{
            jsonObject = new JSONObject(data);
            try{
                response = jsonObject.getString("debug_message");
            }
            catch (Exception e) {
                err = jsonObject.getString("debug_error");
                result = -2;
            }
            if (response.equalsIgnoreCase("success")){
                Log.d("NEW LOC", jsonObject.getString("id"));
                result = Integer.parseInt(jsonObject.getString("id"));
            }
        }
        catch (JSONException e){
            e.printStackTrace();
        }

        return result;
    }

    public void add_location_photo(int location_id, File file) {
//        HttpURLConnection httpURLConnection = null;
//
//        HashMap<String, String> queryParams = new HashMap<>();
//
//        queryParams.put("loc_id", String.valueOf(location_id));
//        queryParams.put("session_key", "5c227297-a455-41b1-a737-1753e491d104");

        String requestURL = "https://exactmark.pythonanywhere.com/put_location_image";

        try {
            MultipartUtility multipart = new MultipartUtility(requestURL, "UTF-8");

            multipart.addFormField("loc_id", String.valueOf(location_id));
            multipart.addFormField("session_key", "078172d9-cae6-4777-832c-cd46d116cc46");
            multipart.addHeaderField("loc_id", String.valueOf(location_id));

            multipart.addHeaderField("session_key", "078172d9-cae6-4777-832c-cd46d116cc46");

            multipart.addHeaderField("User-Agent", "com.team4.geocached");

            multipart.addFormField("description", "Cool Pictures");
            multipart.addFormField("keywords", "Java,upload,Spring");

            multipart.addFilePart("file", file);

            List<String> response = multipart.finish();

            for (String line : response) {
                Log.d("Resp", line);

            }
        } catch (IOException ex) {
            System.err.println(ex);
        }

    }
}

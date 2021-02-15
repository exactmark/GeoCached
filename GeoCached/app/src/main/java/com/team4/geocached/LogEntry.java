package com.team4.geocached;

import java.sql.Date;

public class LogEntry {

    private int id;
    private int locationID;
    private String userID;
    private Date timestamp;
    private String text;

    public int getId() {
        return id;
    }

    public int getLocationID() {
        return locationID;
    }

    public String getUserID() {
        return userID;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

}

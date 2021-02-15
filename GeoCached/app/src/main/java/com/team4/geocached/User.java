package com.team4.geocached;

import java.sql.Date;

public class User {

    private String id;
    private String password;
    private String sessionID;
    private String sessionKey;
    private Date validThrough;

    public int Login() {
        return 0;
    }

    public int Register(){
        return 0;
    }

    public String getSessionID() {
        return sessionID;
    }

    public String getSessionKey() {
        return sessionKey;
    }

}

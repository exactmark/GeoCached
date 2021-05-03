package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.function.LongFunction;

public class Login extends AppCompatActivity {

    EditText Username;
    EditText Password;
    Button Login;
    TextView Register;
    ServerConnection serverConnection = new ServerConnection();
    String response="";
    SharedPreferences sp;
    SharedPreferences.Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Username = (EditText)findViewById(R.id.edittext_username);
        Password = (EditText)findViewById(R.id.edittext_password);
        Login = (Button)findViewById(R.id.button_login);
        Register = (TextView)findViewById(R.id.textview_register);

        sp =  getApplicationContext().getSharedPreferences("geocached", Context.MODE_PRIVATE);

        Register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent registerIntent = new Intent(Login.this,Register.class);
                startActivity(registerIntent);
            }
        });
        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String user = Username.getText().toString().trim();
                String pwd = Password.getText().toString().trim();
                new Thread(()->{
                    response = serverConnection.login(user,pwd);
                    if(!response.equals("-1")){

                        editor = sp.edit();
                        editor.putString("user_id", user);
                        editor.putString("sesssion_key", response);
                        // TODO editor.putString("score",getScore());
                        editor.apply();


                        Intent LocationList = new Intent(Login.this,LocationList.class);
                        startActivity(LocationList);
                        finish();
                    }
                }).start();


                if(response.equals("-1"))
                {
                    Toast.makeText(Login.this,"User name or password incorrect", Toast.LENGTH_SHORT).show();
                }

            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();

        if(!sp.getString("user_id", "no_user").equalsIgnoreCase("no_user")){
            Intent LocationList = new Intent(Login.this,LocationList.class);
            startActivity(LocationList);
            finish();
        }
    }
}
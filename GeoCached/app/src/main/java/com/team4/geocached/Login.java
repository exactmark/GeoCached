package com.team4.geocached;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Username = (EditText)findViewById(R.id.edittext_username);
        Password = (EditText)findViewById(R.id.edittext_password);
        Login = (Button)findViewById(R.id.button_login);
        Register = (TextView)findViewById(R.id.textview_register);
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

}
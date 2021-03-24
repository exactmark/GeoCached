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

public class Register extends AppCompatActivity {
    EditText Username;
    EditText Password;
    EditText CnfPassword;
    Button Register;
    TextView Login;
    ServerConnection serverConnection = new ServerConnection();
    int response_code;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        Username = (EditText)findViewById(R.id.edittext_username);
        Password = (EditText)findViewById(R.id.edittext_password);
        CnfPassword = (EditText)findViewById(R.id.edittext_cnf_password);
        Register = (Button)findViewById(R.id.button_register);
        Login = (TextView)findViewById(R.id.textview_login);
        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent LoginIntent = new Intent(Register.this, Login.class);
                startActivity(LoginIntent);
            }
        });

        Register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


                String user = Username.getText().toString().trim();
                String pwd = Password.getText().toString().trim();
                String cnf_pwd = CnfPassword.getText().toString().trim();

                if(pwd.equals(cnf_pwd)){
                    new Thread(() -> {
                        // Run in background
                        try {
                            response_code = serverConnection.add_user(user, pwd);

                        }
                        catch (Exception e){
                            Log.d("ERR",e.getMessage());
                        }
                    }).start();

                    if(response_code == 0){
                        Toast.makeText(Register.this,"You have successfully registered",Toast.LENGTH_SHORT).show();
                        Intent moveToLogin = new Intent(Register.this,Login.class);
                        startActivity(moveToLogin);
                    }
                    else if(response_code == 1){
                        Toast.makeText(Register.this,"User already exists",Toast.LENGTH_SHORT).show();
                    }
                    else if(response_code == 2 || response_code == 3){
                        Toast.makeText(Register.this,"Check logs for server errors",Toast.LENGTH_SHORT).show();
                    }

                }
                else{
                    Toast.makeText(Register.this,"Passwords do not match",Toast.LENGTH_SHORT).show();
                }




            }
        });
    }
}
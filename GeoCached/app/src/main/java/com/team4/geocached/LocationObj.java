package com.team4.geocached;

public class LocationObj {

    private int id;
    private String name;
    LocationObj(){

    }

    public double getX_coord() {
        return x_coord;
    }

    public void setX_coord(double x_coord) {
        this.x_coord = x_coord;
    }

    public double getY_coord() {
        return y_coord;
    }

    public void setY_coord(double y_coord) {
        this.y_coord = y_coord;
    }

    private double x_coord;
    private double y_coord;
    private String description;

    public LocationObj(int id, String name, double x_coord, double y_coord, String description) {
        this.id = id;
        this.name = name;
        this.x_coord = x_coord;
        this.y_coord = y_coord;
        this.description = description;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}

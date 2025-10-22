package com.solo.rpg.sheetservice.model;

public class SheetFieldValue {
    private Object value;

    public SheetFieldValue(Object value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }

    public void setValue(Object value) {
        this.value = value;
    }
}

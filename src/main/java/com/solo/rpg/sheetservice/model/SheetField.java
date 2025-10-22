package com.solo.rpg.sheetservice.model;

import java.util.List;

public class SheetField {
    private SheetFieldValue value;
    private boolean required;
    private List<String> options;

    public SheetField(SheetFieldValue value) {
        this.value = value;
        this.required = true;
        this.options = null;
    }

    public SheetField(SheetFieldValue value, boolean required) {
        this.value = value;
        this.required = required;
        this.options = null;
    }

    public SheetField(SheetFieldValue value, List<String> options) {
        this.value = value;
        this.required = true;
        this.options = options;
    }

    public SheetField(SheetFieldValue value, boolean required, List<String> options) {
        this.value = value;
        this.required = required;
        this.options = options;
    }

    public SheetFieldValue getValue() {
        return value;
    }
    public void setValue(SheetFieldValue value) {
        this.value = value;
    }
    public boolean isRequired() {
        return required;
    }
    public void setRequired(boolean required) {
        this.required = required;
    }
    public List<String> getOptions() {
        return options;
    }
    public void setOptions(List<String> options) {
        this.options = options;
    }
}

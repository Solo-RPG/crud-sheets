package com.solo.rpg.sheetservice.model;

import net.minidev.json.JSONObject;

import java.util.Map;

public class SheetCreateRequest {
    private String templateId;
    private String systemName;
    private String ownerId;
    private Map<String, Object> data;

    public SheetCreateRequest(String ownerId, Map<String, Object> data) {
        this.ownerId = ownerId;
        this.data = data;
    }

    public SheetCreateRequest(String value, String ownerId, Map<String, Object> data, boolean isSystemName) {
        if (isSystemName) {
            this.systemName = value;
        } else {
            this.templateId = value;
        }
        this.ownerId = ownerId;
        this.data = data;
    }

    public SheetCreateRequest(String templateId, String systemName, String ownerId, Map<String, Object> data) {
        this.templateId = templateId;
        this.systemName = systemName;
        this.ownerId = ownerId;
        this.data = data;
    }

    public String getTemplateId() {
        return templateId;
    }
    public void setTemplateId(String templateId) {
        this.templateId = templateId;
    }
    public String getSystemName() {
        return systemName;
    }
    public void setSystemName(String systemName) {
        this.systemName = systemName;
    }
    public String getOwnerId() {
        return ownerId;
    }
    public void setOwnerId(String ownerId) {
        this.ownerId = ownerId;
    }
    public Map<String, Object> getData() {
        return data;
    }
    public void setData(Map<String, Object> data) {
        this.data = data;
    }

}

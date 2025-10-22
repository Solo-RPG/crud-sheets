package com.solo.rpg.sheetservice.model;

public class SheetCreateRequest {
    private String templateId;
    private String systemName;
    private String ownerId;
    private SheetRequestData data;

    public SheetCreateRequest(String ownerId, SheetRequestData data) {
        this.ownerId = ownerId;
        this.data = data;
    }

    public SheetCreateRequest(String value, String ownerId, SheetRequestData data, boolean isSystemName) {
        if (isSystemName) {
            this.systemName = value;
        } else {
            this.templateId = value;
        }
        this.ownerId = ownerId;
        this.data = data;
    }

    public SheetCreateRequest(String templateId, String systemName, String ownerId, SheetRequestData data) {
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
    public SheetRequestData getData() {
        return data;
    }
    public void setData(SheetRequestData data) {
        this.data = data;
    }

}

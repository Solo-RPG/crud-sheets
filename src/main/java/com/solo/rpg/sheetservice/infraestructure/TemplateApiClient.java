package com.solo.rpg.sheetservice.infraestructure;

import net.minidev.json.JSONObject;
import net.minidev.json.parser.JSONParser;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

public class TemplateApiClient {

    private final RestTemplate restTemplate;
    private final String url = "http://localhost:8000/api/templates/";

    public TemplateApiClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public JSONObject getTemplates() {
        Map<String, Object> response = restTemplate.getForObject(url, Map.class);

        if(response == null) {
            throw new IllegalArgumentException("Template não encontrado");
        }

        return new JSONObject(response);

    }

    public JSONObject getTemplateById(String templateId) {
        String endpoint = url + "by-id/" + templateId;
        Map<String, Object> response = restTemplate.getForObject(endpoint, Map.class);

        if(response == null) {
            throw new IllegalArgumentException("Template não encontrado");
        }

        return new JSONObject(response);
    }

    public JSONObject getTemplateByName(String templateName) {
        String endpoint = url + "by-name/" + templateName;
        Map<String, Object> response = restTemplate.getForObject(endpoint, Map.class);

        if(response == null) {
            throw new IllegalArgumentException("Template não encontrado");
        }

        return new JSONObject(response);
    }

    public JSONObject fetchTemplate(String id, String name) {
        if (id != null && !id.isEmpty()) {
            return getTemplateById(id);
        } else if (name != null && !name.isEmpty()) {
            return getTemplateByName(name);
        } else {
            throw new IllegalArgumentException("Nenhum identificador fornecido");
        }
    }
}

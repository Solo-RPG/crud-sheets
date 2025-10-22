package com.solo.rpg.sheetservice.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.solo.rpg.sheetservice.infraestructure.TemplateApiClient;
import com.solo.rpg.sheetservice.model.SheetCreateRequest;
import com.solo.rpg.sheetservice.model.SheetForm;
import com.solo.rpg.sheetservice.repository.SheetRepository;
import com.solo.rpg.sheetservice.service.SheetService;
import net.minidev.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
public class SheetController {

    @Autowired
    private SheetService service;

    @Autowired
    private SheetRepository repository;

    @GetMapping("/")
    private Object getSheets() {
        List<SheetForm> sheets = repository.findAll();

        if(sheets.isEmpty()) {
            return ResponseEntity.noContent().build();
        }

        return sheets;
    }

    @PostMapping("/")
    public ResponseEntity<SheetCreateRequest> createSheet(ResponseBody sheet) {
        ObjectMapper mapper = new ObjectMapper();
        TemplateApiClient client = new TemplateApiClient(new RestTemplate());


        try {
            SheetCreateRequest sheetRequest = mapper.convertValue(sheet, SheetCreateRequest.class);

            JSONObject template = client.fetchTemplate(sheetRequest.getTemplateId(), sheetRequest.getSystemName());

        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok().body(null);
    }

    @GetMapping("/{id}")
    private Object getSheet(@PathVariable String id) {
        SheetForm sheet = repository.findById(id).orElse(null);

        if(sheet == null) {
            return ResponseEntity.noContent().build();
        }

        return sheet;
    }

    @GetMapping("/by-user_id/{id}")
    private Object getSheetByUserId(@PathVariable String id) {
        SheetForm sheet = repository.findByOwnerId(id).orElse(null);

        if(sheet == null) {
            return ResponseEntity.noContent().build();
        }

        return sheet;
    }

    @GetMapping("/by-name/{id}")
    private Object getTemplateByName(@PathVariable String name) {
        TemplateApiClient client = new TemplateApiClient(new RestTemplate());

        JSONObject object = client.getTemplateByName(name);

        if(object == null) {
            return ResponseEntity.noContent().build();
        }

        return object;
    }


    @DeleteMapping("/{id}")
    private Object deleteSheet(@PathVariable String id) {
        repository.deleteById(id);

        if(!repository.existsById(id)) {
            return ResponseEntity.ok().build();
        }

        return ResponseEntity.status(500).build();
    }

    @PutMapping("/{id}")
    private Object updateSheet(@PathVariable String id, @RequestBody SheetForm sheetForm) {
        SheetForm oldSheet = repository.findById(id).orElse(null);

        if(oldSheet == null) {
            return ResponseEntity.noContent().build();
        }

        repository.deleteById(id);

        repository.save(sheetForm);
        return sheetForm;
    }

    @GetMapping("/templates")
    private Object getTemplates() {
        TemplateApiClient client = new TemplateApiClient(new RestTemplate());

        Object objects = client.getTemplates();

        if(objects == null) {
            return ResponseEntity.noContent().build();
        }

        return objects;
    }
}

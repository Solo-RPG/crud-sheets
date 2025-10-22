package com.solo.rpg.sheetservice.service;

import com.solo.rpg.sheetservice.model.SheetForm;
import com.solo.rpg.sheetservice.repository.SheetRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SheetService {

    @Autowired
    private SheetRepository repository;

    public SheetForm createSheet(SheetForm sheetForm) {
       repository.save(sheetForm);
       return sheetForm;
    }
}

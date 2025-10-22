package com.solo.rpg.sheetservice.repository;

import com.solo.rpg.sheetservice.model.SheetForm;
import org.springframework.data.domain.Example;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.function.Function;

@Repository
public interface SheetRepository extends MongoRepository<SheetForm, String> {
    Optional<SheetForm> findByOwnerId(String userId);


}

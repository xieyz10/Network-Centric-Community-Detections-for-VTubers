package com.cis600.vtuber.com.cis600.vtuber.entity;
import org.springframework.data.mongodb.repository.MongoRepository;


public interface VtuberRepository extends MongoRepository<vtuber, String> {
    public vtuber findByName(String name);
}

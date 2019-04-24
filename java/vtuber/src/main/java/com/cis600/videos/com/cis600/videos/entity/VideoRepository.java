package com.cis600.videos.com.cis600.videos.entity;
import org.springframework.data.mongodb.repository.MongoRepository;


public interface VideoRepository extends MongoRepository<Video, String> {
    public Video findByName(String name);

}

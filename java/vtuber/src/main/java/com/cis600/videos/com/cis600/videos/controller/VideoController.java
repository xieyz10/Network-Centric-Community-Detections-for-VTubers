package com.cis600.videos.com.cis600.videos.controller;

import com.cis600.videos.com.cis600.videos.entity.Video;
import com.cis600.videos.com.cis600.videos.entity.VideoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
public class VideoController {
    @Autowired
    private VideoRepository repository;

    @RequestMapping(value="/testvideo", method = RequestMethod.GET)
    public @ResponseBody String showInfo(@RequestParam(value="name") String name) {
        Map<String, Video> map = new HashMap<>();
        Video v =  repository.findByName(name);
        map.put(name,v);
        return "testvideo";
    }
}
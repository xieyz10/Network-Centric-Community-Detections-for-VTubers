package com.cis600.vtuber.com.cis600.vtuber.controller;
import org.springframework.stereotype.Controller;
import com.cis600.vtuber.com.cis600.vtuber.entity.vtuber;
import com.cis600.vtuber.com.cis600.vtuber.entity.VtuberRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@Controller
public class VtuberController {
    @Autowired
    private VtuberRepository repository;

    @GetMapping("/testvtuber")
    public String showInfo(@RequestParam(value="name") String name, Model model) {
        //Map<String, vtuber> map = new HashMap<>();
        System.out.println(name);
        vtuber v =  repository.findByName(name);
        System.out.println(v.name);
        model.addAttribute("v", v);
        // map.put(name,v);
        return "testvtuber";
    }
}

package com.cis600.vtuber.com.cis600.vtuber.entity;


import org.springframework.data.annotation.Id;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
public class vtuber {

    @Id
    String id;
    @Getter @Setter
    public String group;

    @Getter @Setter
    public String name;
    @Getter @Setter
    public String channel;
    @Getter @Setter
    public String detail_url;
    @Getter @Setter
    public String channel_url;
    @Getter @Setter
    public int regsit;
    @Getter @Setter
    public String group_detail_url;
    @Getter @Setter
    public int upload;
    @Getter @Setter
    public String twi_name;
    @Getter @Setter
    public int play;

    public vtuber(){};
    public vtuber(String group, String name, String channel, String detail_url, String channel_url, int regsit,
                  String group_detail_url, int upload, String twi_name, int play){
        this.group = group;
        this.name = name;
        this.channel = channel;
        this.detail_url = detail_url;
        this.channel_url = channel_url;
        this.regsit = regsit;
        this.group_detail_url = group_detail_url;
        this.upload = upload;
        this.twi_name = twi_name;
        this.play = play;
    }
}

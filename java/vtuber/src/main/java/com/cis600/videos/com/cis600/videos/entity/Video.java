package com.cis600.videos.com.cis600.videos.entity;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;

public class Video {
    @Getter @Setter
    public double chatSpeed;
    @Getter @Setter
    public int channelOrderIndex;
    @Getter @Setter
    public int memberAuthorCount;
    @Getter @Setter
    public String subscriberCount;
    @Getter @Setter
    public String channelId;
    @Getter @Setter
    public String regDttm;
    @Getter @Setter
    public double authorCountDurationLiveIndex;
    @Getter @Setter
    public String authorTop20Ratio;
    @Getter @Setter
    public String updDttm;
    @Getter @Setter
    public double authorCountRatio;
    @Getter @Setter
    public int chatMaxCount;
    @Id @Getter @Setter
    public  String videoId;
    @Getter @Setter
    public String channelTitle;
    @Getter @Setter
    public String durationLive;
    @Getter @Setter
    public int channelCat;
    @Getter @Setter
    public String chatMaxTime;
    @Getter @Setter
    public String publishedAt;
    @Getter @Setter
    public int viewCount;
    @Getter @Setter
    public int chatCnt;
    @Getter @Setter
    public int memberCommentCount;
    @Getter @Setter
    public String duration;
    @Getter @Setter
    public int authorCount;
    @Getter @Setter
    public String videoTitle;
    @Getter @Setter
    public String description;


}

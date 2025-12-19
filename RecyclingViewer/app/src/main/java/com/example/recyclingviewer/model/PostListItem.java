package com.example.recyclingviewer.model;

import com.google.gson.annotations.SerializedName;

public class PostListItem {
    private int id;
    private String title;
    private String category;

    @SerializedName("image_url")
    private String imageUrl;

    @SerializedName("published_date")
    private String publishedDate;

    // Getters
    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getCategory() { return category; }
    public String getImageUrl() { return imageUrl; }
    public String getPublishedDate() { return publishedDate; }

    // Setters
    public void setId(int id) { this.id = id; }
    public void setTitle(String title) { this.title = title; }
    public void setCategory(String category) { this.category = category; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    public void setPublishedDate(String publishedDate) { this.publishedDate = publishedDate; }
}
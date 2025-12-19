package com.example.recyclingviewer.model;

import com.google.gson.annotations.SerializedName;

public class Post {
    private int id;
    private String title;
    private String text;
    private String category;
    private String image;

    @SerializedName("image_url")
    private String imageUrl;

    @SerializedName("created_date")
    private String createdDate;

    @SerializedName("published_date")
    private String publishedDate;

    // Getters
    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getText() { return text; }
    public String getCategory() { return category; }
    public String getImage() { return image; }
    public String getImageUrl() { return imageUrl; }
    public String getCreatedDate() { return createdDate; }
    public String getPublishedDate() { return publishedDate; }

    // Setters
    public void setId(int id) { this.id = id; }
    public void setTitle(String title) { this.title = title; }
    public void setText(String text) { this.text = text; }
    public void setCategory(String category) { this.category = category; }
    public void setImage(String image) { this.image = image; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    public void setCreatedDate(String createdDate) { this.createdDate = createdDate; }
    public void setPublishedDate(String publishedDate) { this.publishedDate = publishedDate; }

    public String getCategoryDisplay() {
        switch (category) {
            case "plastic": return "플라스틱";
            case "glass": return "유리";
            case "paper": return "종이류";
            case "metal": return "고철";
            case "food": return "음식물쓰레기";
            case "general": return "일반쓰레기";
            case "large": return "대형폐기물";
            case "electronic": return "폐가전";
            case "clothes": return "의류";
            default: return "기타";
        }
    }
}
package com.example.recyclingviewer.api;

import com.example.recyclingviewer.model.AuthResponse;
import com.example.recyclingviewer.model.Post;
import com.example.recyclingviewer.model.PostListItem;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface ApiService {

    // 로그인 (JWT 토큰 획득)
    @FormUrlEncoded
    @POST("api-token-auth/")
    Call<AuthResponse> login(
            @Field("username") String username,
            @Field("password") String password
    );

    // 게시물 목록 조회 (2-4, 3-2 요구사항)
    @GET("api/posts/")
    Call<List<PostListItem>> getPostList();

    // 카테고리별 게시물 조회
    @GET("api/posts/")
    Call<List<PostListItem>> getPostsByCategory(@Query("category") String category);

    // 게시물 상세 조회
    @GET("api/posts/{id}/")
    Call<Post> getPostDetail(@Path("id") int postId);

    // REST API 게시물 목록
    @GET("api_root/Post/")
    Call<List<Post>> getAllPosts();
}
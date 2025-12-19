package com.example.recyclingviewer;

import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.bumptech.glide.Glide;
import com.example.recyclingviewer.api.ApiClient;
import com.example.recyclingviewer.api.ApiService;
import com.example.recyclingviewer.databinding.ActivityPostDetailBinding;
import com.example.recyclingviewer.model.Post;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class PostDetailActivity extends AppCompatActivity {
    private static final String TAG = "PostDetailActivity";

    private ActivityPostDetailBinding binding;
    private ApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityPostDetailBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        setupToolbar();

        apiService = ApiClient.getClient().create(ApiService.class);

        int postId = getIntent().getIntExtra("post_id", -1);
        if (postId != -1) {
            loadPostDetail(postId);
        } else {
            Toast.makeText(this, "잘못된 접근입니다", Toast.LENGTH_SHORT).show();
            finish();
        }
    }

    private void setupToolbar() {
        setSupportActionBar(binding.toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("분리수거 가이드");
        }
    }

    private void loadPostDetail(int postId) {
        binding.progressBar.setVisibility(View.VISIBLE);
        binding.contentLayout.setVisibility(View.GONE);

        apiService.getPostDetail(postId).enqueue(new Callback<Post>() {
            @Override
            public void onResponse(Call<Post> call, Response<Post> response) {
                binding.progressBar.setVisibility(View.GONE);

                if (response.isSuccessful() && response.body() != null) {
                    binding.contentLayout.setVisibility(View.VISIBLE);
                    displayPost(response.body());
                } else {
                    showError("데이터를 불러올 수 없습니다");
                    finish();
                }
            }

            @Override
            public void onFailure(Call<Post> call, Throwable t) {
                binding.progressBar.setVisibility(View.GONE);
                Log.e(TAG, "API call failed", t);
                showError("서버 연결에 실패했습니다");
                finish();
            }
        });
    }

    private void displayPost(Post post) {
        binding.titleText.setText(post.getTitle());
        binding.categoryText.setText(post.getCategoryDisplay());
        binding.guideText.setText(post.getText());
        binding.dateText.setText("📅 " + formatDate(post.getPublishedDate()));

        String imageUrl = post.getImageUrl();
        if (imageUrl != null && !imageUrl.isEmpty()) {
            Glide.with(this)
                    .load(imageUrl)
                    .placeholder(R.drawable.placeholder_image)
                    .error(R.drawable.placeholder_image)
                    .into(binding.postImage);
        }
    }

    private String formatDate(String dateStr) {
        if (dateStr == null) return "";
        try {
            SimpleDateFormat inputFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault());
            Date date = inputFormat.parse(dateStr);
            SimpleDateFormat outputFormat = new SimpleDateFormat("yyyy년 MM월 dd일 HH:mm", Locale.KOREA);
            return outputFormat.format(date);
        } catch (ParseException e) {
            return dateStr;
        }
    }

    private void showError(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
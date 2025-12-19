package com.example.recyclingviewer;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import com.example.recyclingviewer.adapter.PostAdapter;
import com.example.recyclingviewer.api.ApiClient;
import com.example.recyclingviewer.api.ApiService;
import com.example.recyclingviewer.databinding.ActivityMainBinding;
import com.example.recyclingviewer.model.PostListItem;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;
    private PostAdapter adapter;
    private ApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        setupToolbar();
        setupRecyclerView();
        setupSwipeRefresh();

        apiService = ApiClient.getClient().create(ApiService.class);
        loadPosts();
    }

    private void setupToolbar() {
        setSupportActionBar(binding.toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setTitle("♻️ AI 분리수거 가이드");
        }
    }

    private void setupRecyclerView() {
        adapter = new PostAdapter();
        binding.recyclerView.setLayoutManager(new LinearLayoutManager(this));
        binding.recyclerView.setAdapter(adapter);

        adapter.setOnItemClickListener(post -> {
            Intent intent = new Intent(MainActivity.this, PostDetailActivity.class);
            intent.putExtra("post_id", post.getId());
            startActivity(intent);
        });
    }

    private void setupSwipeRefresh() {
        binding.swipeRefresh.setColorSchemeResources(
                R.color.purple_500,
                R.color.purple_700
        );
        binding.swipeRefresh.setOnRefreshListener(this::loadPosts);
    }

    private void loadPosts() {
        binding.progressBar.setVisibility(View.VISIBLE);
        binding.emptyView.setVisibility(View.GONE);

        apiService.getPostList().enqueue(new Callback<List<PostListItem>>() {
            @Override
            public void onResponse(Call<List<PostListItem>> call, Response<List<PostListItem>> response) {
                binding.progressBar.setVisibility(View.GONE);
                binding.swipeRefresh.setRefreshing(false);

                if (response.isSuccessful() && response.body() != null) {
                    List<PostListItem> posts = response.body();
                    if (posts.isEmpty()) {
                        binding.emptyView.setVisibility(View.VISIBLE);
                        binding.recyclerView.setVisibility(View.GONE);
                    } else {
                        binding.emptyView.setVisibility(View.GONE);
                        binding.recyclerView.setVisibility(View.VISIBLE);
                        adapter.setPosts(posts);
                    }
                    Log.d(TAG, "Loaded " + posts.size() + " posts");
                } else {
                    showError("데이터를 불러올 수 없습니다");
                }
            }

            @Override
            public void onFailure(Call<List<PostListItem>> call, Throwable t) {
                binding.progressBar.setVisibility(View.GONE);
                binding.swipeRefresh.setRefreshing(false);
                binding.emptyView.setVisibility(View.VISIBLE);
                Log.e(TAG, "API call failed", t);
                showError("서버 연결에 실패했습니다: " + t.getMessage());
            }
        });
    }

    private void showError(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadPosts();
    }
}
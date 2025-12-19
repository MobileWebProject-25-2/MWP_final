package com.example.recyclingviewer.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.resource.bitmap.RoundedCorners;
import com.example.recyclingviewer.R;
import com.example.recyclingviewer.model.PostListItem;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class PostAdapter extends RecyclerView.Adapter<PostAdapter.PostViewHolder> {

    private List<PostListItem> posts = new ArrayList<>();
    private OnItemClickListener listener;

    public interface OnItemClickListener {
        void onItemClick(PostListItem post);
    }

    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }

    public void setPosts(List<PostListItem> posts) {
        this.posts = posts;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public PostViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_post, parent, false);
        return new PostViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull PostViewHolder holder, int position) {
        PostListItem post = posts.get(position);
        holder.bind(post);
    }

    @Override
    public int getItemCount() {
        return posts.size();
    }

    class PostViewHolder extends RecyclerView.ViewHolder {
        private ImageView imageView;
        private TextView titleText;
        private TextView categoryText;
        private TextView dateText;

        public PostViewHolder(@NonNull View itemView) {
            super(itemView);
            imageView = itemView.findViewById(R.id.post_image);
            titleText = itemView.findViewById(R.id.post_title);
            categoryText = itemView.findViewById(R.id.post_category);
            dateText = itemView.findViewById(R.id.post_date);

            itemView.setOnClickListener(v -> {
                int position = getAdapterPosition();
                if (position != RecyclerView.NO_POSITION && listener != null) {
                    listener.onItemClick(posts.get(position));
                }
            });
        }

        public void bind(PostListItem post) {
            titleText.setText(post.getTitle());
            categoryText.setText(getCategoryDisplay(post.getCategory()));
            dateText.setText(formatDate(post.getPublishedDate()));

            if (post.getImageUrl() != null && !post.getImageUrl().isEmpty()) {
                Glide.with(itemView.getContext())
                        .load(post.getImageUrl())
                        .transform(new RoundedCorners(16))
                        .placeholder(R.drawable.placeholder_image)
                        .error(R.drawable.placeholder_image)
                        .into(imageView);
            } else {
                imageView.setImageResource(R.drawable.placeholder_image);
            }
        }

        private String getCategoryDisplay(String category) {
            if (category == null) return "기타";
            switch (category) {
                case "plastic": return "♻️ 플라스틱";
                case "glass": return "🫙 유리";
                case "paper": return "📄 종이류";
                case "metal": return "🔩 고철";
                case "food": return "🍎 음식물";
                case "general": return "🗑️ 일반";
                case "large": return "🛋️ 대형";
                case "electronic": return "📱 폐가전";
                case "clothes": return "👕 의류";
                default: return "📦 기타";
            }
        }

        private String formatDate(String dateStr) {
            if (dateStr == null) return "";
            try {
                SimpleDateFormat inputFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault());
                Date date = inputFormat.parse(dateStr);
                SimpleDateFormat outputFormat = new SimpleDateFormat("yyyy.MM.dd HH:mm", Locale.KOREA);
                return outputFormat.format(date);
            } catch (ParseException e) {
                return dateStr;
            }
        }
    }
}
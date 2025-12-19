package com.example.recyclingviewer.api;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {
    // PythonAnywhere 배포 시 변경
    // private static final String BASE_URL = "https://yourusername.pythonanywhere.com/";
    private static final String BASE_URL = "http://10.0.2.2:8000/"; // 에뮬레이터용

    private static Retrofit retrofit = null;
    private static String authToken = null;

    public static Retrofit getClient() {
        if (retrofit == null) {
            HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
            logging.setLevel(HttpLoggingInterceptor.Level.BODY);

            OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
            httpClient.addInterceptor(logging);

            // 인증 토큰 추가
            httpClient.addInterceptor(chain -> {
                okhttp3.Request original = chain.request();
                okhttp3.Request.Builder requestBuilder = original.newBuilder();

                if (authToken != null) {
                    requestBuilder.header("Authorization", "JWT " + authToken);
                }

                return chain.proceed(requestBuilder.build());
            });

            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .client(httpClient.build())
                    .build();
        }
        return retrofit;
    }

    public static void setAuthToken(String token) {
        authToken = token;
    }

    public static String getBaseUrl() {
        return BASE_URL;
    }
}
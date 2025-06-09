const API_BASE_URL = "http://localhost:8000/api/v1";
const BACKEND_BASE_URL = "http://localhost:8000";

export interface DreamRequest {
  prompt: string;
}

export interface DreamResponse {
  id: number;
  prompt: string;
  image_url: string;
  user_id?: number;
  created_at: string;
}

export interface VideoRequest {
  prompt: string;
}

export interface VideoResponse {
  id: number;
  prompt: string;
  video_url: string;
  user_id?: number;
  created_at: string;
}

export interface ApiError {
  detail: string;
}

class ApiService {
  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {},
    token?: string | null
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const defaultHeaders: Record<string, string> = {
      "Content-Type": "application/json",
    };

    if (token) {
      defaultHeaders.Authorization = `Bearer ${token}`;
    }

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData: ApiError = await response.json().catch(() => ({
          detail: `HTTP error! status: ${response.status}`,
        }));
        throw new Error(errorData.detail);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error("An unexpected error occurred");
    }
  }

  async generateDream(
    request: DreamRequest,
    token?: string | null
  ): Promise<DreamResponse> {
    const response = await this.makeRequest<DreamResponse>(
      "/dreams/",
      {
        method: "POST",
        body: JSON.stringify(request),
      },
      token
    );

    console.log("🔍 Raw API response image_url:", response.image_url);

    if (response.image_url && response.image_url.startsWith("/static/")) {
      response.image_url = `${BACKEND_BASE_URL}${response.image_url}`;
      console.log("✅ Converted to absolute URL:", response.image_url);
    } else {
      console.log("⚠️ URL did not start with /static/", response.image_url);
    }

    return response;
  }

  async getUserDreams(token: string): Promise<DreamResponse[]> {
    const response = await this.makeRequest<DreamResponse[]>(
      "/dreams/me",
      {
        method: "GET",
      },
      token
    );

    console.log("🔍 Raw getUserDreams response:", response);

    return response.map((dream) => ({
      ...dream,
      image_url: dream.image_url.startsWith("/static/")
        ? `${BACKEND_BASE_URL}${dream.image_url}`
        : dream.image_url,
    }));
  }

  async generateVideo(
    request: VideoRequest,
    token?: string | null
  ): Promise<VideoResponse> {
    const response = await this.makeRequest<VideoResponse>(
      "/videos/",
      {
        method: "POST",
        body: JSON.stringify(request),
      },
      token
    );

    console.log("🎬 Raw API response video_url:", response.video_url);

    if (response.video_url && response.video_url.startsWith("/static/")) {
      response.video_url = `${BACKEND_BASE_URL}${response.video_url}`;
      console.log("✅ Converted to absolute URL:", response.video_url);
    } else {
      console.log("⚠️ URL did not start with /static/", response.video_url);
    }

    return response;
  }

  async getUserVideos(token: string): Promise<VideoResponse[]> {
    const response = await this.makeRequest<VideoResponse[]>(
      "/videos/me",
      {
        method: "GET",
      },
      token
    );

    console.log("🎬 Raw getUserVideos response:", response);

    return response.map((video) => ({
      ...video,
      video_url: video.video_url.startsWith("/static/")
        ? `${BACKEND_BASE_URL}${video.video_url}`
        : video.video_url,
    }));
  }
}

export const apiService = new ApiService();

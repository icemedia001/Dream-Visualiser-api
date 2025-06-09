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

export interface ApiError {
  detail: string;
}

class ApiService {
  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const defaultHeaders = {
      "Content-Type": "application/json",
    };

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

  async generateDream(request: DreamRequest): Promise<DreamResponse> {
    const response = await this.makeRequest<DreamResponse>("/dreams/", {
      method: "POST",
      body: JSON.stringify(request),
    });

    // Convert relative image URL to absolute URL
    if (response.image_url && response.image_url.startsWith("/static/")) {
      response.image_url = `${BACKEND_BASE_URL}${response.image_url}`;
    }

    return response;
  }

  async getUserDreams(): Promise<DreamResponse[]> {
    const token = localStorage.getItem("authToken");
    return this.makeRequest<DreamResponse[]>("/dreams/me", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }
}

export const apiService = new ApiService();

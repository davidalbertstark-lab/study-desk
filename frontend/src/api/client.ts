import axios from "axios";
import {
  getAccessToken,
  getRefreshToken,
  saveTokens,
  clearTokens,
} from "../utils/token";
import { API_BASE_URL } from "../api/config";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// REQUEST INTERCEPTOR
api.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// RESPONSE INTERCEPTOR (AUTO REFRESH)
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;

    const url = original?.url ?? "";

    const isAuthRequest =
      url.includes("/auth/login") ||
      url.includes("/auth/register") ||
      url.includes("/auth/refresh");

    if (
      err.response?.status === 401 &&
      !original._retry &&
      !isAuthRequest
    ) {
      original._retry = true;

      try {
        const refresh = getRefreshToken();
        if (!refresh) throw new Error("No refresh token");

        const response = await axios.post(
          `${API_BASE_URL}/auth/refresh`,
          {
            refresh_token: refresh,
          }
        );

        const { access_token, refresh_token } = response.data.data;

        saveTokens(access_token, refresh_token);

        original.headers.Authorization = `Bearer ${access_token}`;

        return api(original);
      } catch (e) {
        clearTokens();
        window.location.href = "/login";
      }
    }

    return Promise.reject(err);
  }
);

export default api;
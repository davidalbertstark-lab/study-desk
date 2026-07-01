import { API_BASE_URL } from "./config";

export function getGoogleLoginUrl() {
  return `${API_BASE_URL}/auth/google/login`;
}
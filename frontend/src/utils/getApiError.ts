import axios from "axios";

export function getApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data;

    if (typeof data?.detail === "string") {
      return data.detail;
    }

    if (typeof data?.message === "string") {
      return data.message;
    }

    if (typeof data?.error === "string") {
      return data.error;
    }

    if (typeof data?.data?.message === "string") {
      return data.data.message;
    }

    if (!navigator.onLine) {
      return "No internet connection.";
    }

    return "Something went wrong. Please try again.";
  }

  return "Unexpected error occurred.";
}
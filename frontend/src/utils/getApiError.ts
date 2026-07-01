import axios from "axios";

export function getApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data;

    const message =
      typeof data?.detail === "string"
        ? data.detail
        : typeof data?.message === "string"
        ? data.message
        : typeof data?.error === "string"
        ? data.error
        : typeof data?.data?.message === "string"
        ? data.data.message
        : null;

    if (message) {
      if (message.toLowerCase() === "invalid credentials") {
        return "Incorrect email or password.";
      }

      return message;
    }

    if (!navigator.onLine) {
      return "No internet connection.";
    }

    return "Something went wrong. Please try again.";
  }

  return "Unexpected error occurred.";
}
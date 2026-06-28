import api from "./client";
import { saveTokens } from "../utils/token";
import type { User } from "../types/user";

export async function register(
  email: string,
  password: string
): Promise<LoginResponse> {
  const res = await api.post("/auth/register", {
    email,
    password,
  });

  console.log(res.data);

  const payload = res.data.data;

  console.log(payload);

  saveTokens(
      payload.access_token,
      payload.refresh_token
  );

  console.log(localStorage);

  const data: LoginResponse = {
    user: payload.user,
    access_token: payload.access_token,
    refresh_token: payload.refresh_token,
    token_type: payload.token_type,
  };

  saveTokens(
    data.access_token,
    data.refresh_token
  );

  return data;
}

// =========================
// LOGIN RESPONSE (FLATTENED)
// =========================
export interface LoginResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// =========================
// DEVICE ID
// =========================
function getDeviceId(): string {
  let deviceId = localStorage.getItem("device_id");

  if (!deviceId) {
    deviceId = crypto.randomUUID();
    localStorage.setItem("device_id", deviceId);
  }

  return deviceId;
}

// =========================
// LOGIN (CLEAN VERSION)
// =========================
export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const res = await api.post("/auth/login", {
    email,
    password,
    device_id: getDeviceId(),
  });

  // backend wrapper
  const payload = res.data?.data;

  const data: LoginResponse = {
    user: payload.user,
    access_token: payload.access_token,
    refresh_token: payload.refresh_token,
    token_type: payload.token_type,
  };

  // store tokens here (single responsibility rule)
  saveTokens(data.access_token, data.refresh_token);

  return data;
}
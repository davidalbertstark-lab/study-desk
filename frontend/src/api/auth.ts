import api from "./client";
import { saveTokens } from "../utils/token";
import type { User } from "../types/user";

// =========================
// TYPES
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
// REGISTER (STEP 1)
// =========================
export async function register(email: string, password: string): Promise<void> {
  await api.post("/auth/register", {
    email,
    password,
  });
}

// =========================
// VERIFY EMAIL (STEP 2)
// =========================
export async function verifyRegistration(email: string, code: string): Promise<void> {
  await api.post("/auth/verify-registration", {
    email,
    code,
  });
}

// =========================
// COMPLETE REGISTRATION (STEP 3)
// =========================
export async function completeRegistration(email: string): Promise<LoginResponse> {
  const res = await api.post("/auth/complete-registration", {
    email,
  });

  const payload = res.data.data;

  const data: LoginResponse = {
    user: payload.user,
    access_token: payload.access_token,
    refresh_token: payload.refresh_token,
    token_type: payload.token_type,
  };

  saveTokens(data.access_token, data.refresh_token);

  return data;
}

// =========================
// LOGIN
// =========================
export async function login(
  email: string,
  password: string,
  rememberMe: boolean = false
): Promise<LoginResponse> {
  const res = await api.post("/auth/login", {
    email,
    password,
    remember_me: rememberMe,
    device_id: getDeviceId(),
  });

  const payload = res.data.data;

  const data: LoginResponse = {
    user: payload.user,
    access_token: payload.access_token,
    refresh_token: payload.refresh_token,
    token_type: payload.token_type,
  };

  saveTokens(data.access_token, data.refresh_token);

  return data;
}

// =========================
// PASSWORD RESET
// =========================
export async function forgotPassword(email: string): Promise<void> {
  await api.post("/auth/forgot-password", { email });
}

export async function verifyResetCode(email: string, code: string): Promise<void> {
  await api.post("/auth/verify-reset-code", { email, code });
}

export async function resetPassword(
  email: string,
  code: string,
  newPassword: string
): Promise<void> {
  await api.post("/auth/reset-password", {
    email,
    code,
    new_password: newPassword,
  });
}


// =========================
// RESEND REGISTRATION CODE
// =========================
export async function resendRegistrationCode(
  email: string
): Promise<void> {
  await api.post("/auth/resend-registration-code", {
    email,
  });
}
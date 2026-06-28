import type { User } from "./user";

export interface LoginResponse {
  data: {
    user: User;
    access_token: string;
    refresh_token: string;
    token_type: string;
  };
}
import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

import api from "../api/client";
import type { User } from "../types/user";
import { getAccessToken, clearTokens } from "../utils/token";

type AuthContextType = {
  user: User | null;
  setUser: (user: User | null) => void;
  loading: boolean;
};

export const AuthContext = createContext<
  AuthContextType | undefined
>(undefined);

type Props = {
  children: ReactNode;
};

export const AuthProvider = ({ children }: Props) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const loadUser = async () => {
    try {
      const token = getAccessToken();

      if (!token) {
        setUser(null);
        return;
      }

      const res = await api.get("/users/me");

      setUser(res.data.data);
    } catch (err: any) {
      if (err?.response?.status === 401) {
        clearTokens();
      }

      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import api from "../../api/client";
import { saveTokens } from "../../utils/token";
import { useAuth } from "../../hooks/useAuth";

export default function GoogleCallback() {
  const [params] = useSearchParams();

  const navigate = useNavigate();

  const { setUser } = useAuth();

  useEffect(() => {
    const ticket = params.get("ticket");

    if (!ticket) {
      navigate("/login", { replace: true });
      return;
    }

    const storageKey = `google-ticket-${ticket}`;

    // Prevent duplicate exchange caused by React StrictMode
    if (sessionStorage.getItem(storageKey)) {
      return;
    }

    sessionStorage.setItem(storageKey, "processing");

    async function completeGoogleLogin() {
      try {
        const res = await api.post("/auth/google/exchange-ticket", {
          ticket,
        });

        const payload = res.data.data;

        saveTokens(
          payload.access_token,
          payload.refresh_token
        );

        setUser(payload.user);

        // Ticket successfully consumed
        sessionStorage.removeItem(storageKey);

        const user = payload.user;

        if (!user.profile_completed) {
          navigate("/signup?completeProfile=true", {
            replace: true,
          });
          return;
        }

        if (user.status === "ACTIVE") {
          navigate("/dashboard", {
            replace: true,
          });
          return;
        }

        if (user.status === "WAITLISTED") {
          navigate("/waitlist", {
            replace: true,
          });
          return;
        }

        navigate("/waitlist", {
          replace: true,
        });
      } catch {
        // Allow retry if exchange genuinely failed
        sessionStorage.removeItem(storageKey);

        navigate("/login", {
          replace: true,
        });
      }
    }

    completeGoogleLogin();
  }, [navigate, params, setUser]);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      Signing you in...
    </div>
  );
}
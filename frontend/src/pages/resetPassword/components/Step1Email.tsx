import { useState } from "react";
import { Link } from "react-router-dom";

import logo from "../../../assets/logo.svg";
import loginImage from "../../../assets/login.png";

type Props = {
  loading: boolean;
  error: string;
  onSubmit: (email: string) => Promise<void>;
};

export default function Step1Email({
  loading,
  error,
  onSubmit,
}: Props) {
  const [email, setEmail] = useState("");

  async function handleSubmit(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();

    await onSubmit(email);
  }

  return (
    <div className="studydesk-page signup-page">
      <div
        className="login-image-panel"
        style={{
          backgroundImage: `url(${loginImage})`,
        }}
      >
        <div className="loadscreen-overlay-gradient" />

        <div className="loadscreen-text">
          <div className="loadscreen-logo">
            <img
              src={logo}
              alt="Lenar"
            />

            <span className="logo-text">
              LENAR
            </span>
          </div>

          <h1 className="loadscreen-heading">
            Reset your password
          </h1>

          <p className="loadscreen-subtext">
            We'll help you get back into
            your account.
          </p>
        </div>
      </div>

      <div className="login-form-panel">
        <div className="signup-card">
          <div className="step-icon-badge">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
            >
              <rect
                x="3"
                y="11"
                width="18"
                height="9"
                rx="2"
              />
              <path d="M7 11V7a5 5 0 0110 0v4" />
            </svg>
          </div>

          <h1 className="login-heading">
            Forgot Password?
          </h1>

          <p className="step-subheading">
            Enter your email and we'll send
            you a reset code.
          </p>

          <form
            className="login-form"
            onSubmit={handleSubmit}
          >
            <div className="input-wrapper">
              <svg
                className="input-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              >
                <rect
                  x="3"
                  y="5"
                  width="18"
                  height="14"
                  rx="2"
                />
                <path d="M3 7l9 6 9-6" />
              </svg>

              <input
                type="email"
                required
                placeholder="Email address"
                autoFocus
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
              />
            </div>

            {error && (
              <p className="form-error">
                {error}
              </p>
            )}

            <button
              className="login-btn"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Sending..."
                : "Send Code"}
            </button>
          </form>

          <div className="signup-row">
            Remembered your password?

            <Link
              className="signup-link"
              to="/login"
            >
              Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
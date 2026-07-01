import { useState } from "react";

import logo from "../../../assets/logo.svg";
import loginImage from "../../../assets/login.png";

type Props = {
  loading: boolean;
  error: string;
  onSubmit: (password: string) => Promise<void>;
};

export default function Step3Password({
  loading,
  error,
  onSubmit,
}: Props) {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [localError, setLocalError] = useState("");

  async function handleSubmit(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();

    setLocalError("");

    if (password !== confirmPassword) {
      setLocalError("Passwords do not match.");
      return;
    }

    await onSubmit(password);
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
            <img src={logo} alt="Lenar" />

            <span className="logo-text">
              LENAR
            </span>
          </div>

          <h1 className="loadscreen-heading">
            Create a new password
          </h1>

          <p className="loadscreen-subtext">
            Your new password will be used
            the next time you sign in.
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
                x="4"
                y="11"
                width="16"
                height="9"
                rx="2"
              />
              <path d="M8 11V7a4 4 0 018 0v4" />
            </svg>
          </div>

          <h1 className="login-heading">
            Set New Password
          </h1>

          <p className="step-subheading">
            Choose a strong password.
          </p>

          <form
            className="login-form"
            onSubmit={handleSubmit}
          >
            <div className="input-wrapper">
              <input
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="New password"
                value={password}
                autoFocus
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                required
              />

              <button
                type="button"
                className="toggle-password"
                disabled={loading}
                onClick={() =>
                  setShowPassword((prev) => !prev)
                }
                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }
              >
                {showPassword ? (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <path d="M3 3l18 18" />
                    <path d="M10.6 10.6a2 2 0 0 0 2.83 2.83" />
                    <path d="M9.36 5.36A9.5 9.5 0 0 1 12 5c5 0 9 4.5 9 7-.55 1.1-1.4 2.3-2.5 3.36M6.5 6.64C4.4 7.7 2.55 9.9 2 11c.55 1.1 1.4 2.3 2.5 3.36A9.5 9.5 0 0 0 12 17c.7 0 1.37-.08 2-.23" />
                  </svg>
                ) : (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <path d="M2 11s3-6 10-6 10 6 10 6-3 6-10 6-10-6-10-6z" />
                    <circle
                      cx="12"
                      cy="11"
                      r="3"
                    />
                  </svg>
                )}
              </button>
            </div>

            <div className="input-wrapper">
              <input
                type={
                  showConfirmPassword
                    ? "text"
                    : "password"
                }
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) =>
                  setConfirmPassword(
                    e.target.value
                  )
                }
                required
              />

              <button
                type="button"
                className="toggle-password"
                disabled={loading}
                onClick={() =>
                  setShowConfirmPassword(
                    (prev) => !prev
                  )
                }
                aria-label={
                  showConfirmPassword
                    ? "Hide password"
                    : "Show password"
                }
              >
                {showConfirmPassword ? (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <path d="M3 3l18 18" />
                    <path d="M10.6 10.6a2 2 0 0 0 2.83 2.83" />
                    <path d="M9.36 5.36A9.5 9.5 0 0 1 12 5c5 0 9 4.5 9 7-.55 1.1-1.4 2.3-2.5 3.36M6.5 6.64C4.4 7.7 2.55 9.9 2 11c.55 1.1 1.4 2.3 2.5 3.36A9.5 9.5 0 0 0 12 17c.7 0 1.37-.08 2-.23" />
                  </svg>
                ) : (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <path d="M2 11s3-6 10-6 10 6 10 6-3 6-10 6-10-6-10-6z" />
                    <circle
                      cx="12"
                      cy="11"
                      r="3"
                    />
                  </svg>
                )}
              </button>
            </div>

            {(localError || error) && (
              <p className="form-error">
                {localError || error}
              </p>
            )}

            <button
              className="login-btn"
              disabled={loading}
              type="submit"
            >
              {loading
                ? "Updating..."
                : "Reset Password"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
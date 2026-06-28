import React from "react";
import { Link } from "react-router-dom";

interface Step1AccountProps {
  email: string;
  setEmail: React.Dispatch<React.SetStateAction<string>>;

  password: string;
  setPassword: React.Dispatch<React.SetStateAction<string>>;

  confirmPassword: string;
  setConfirmPassword: React.Dispatch<React.SetStateAction<string>>;

  showPassword: boolean;
  setShowPassword: React.Dispatch<React.SetStateAction<boolean>>;

  showConfirmPassword: boolean;
  setShowConfirmPassword: React.Dispatch<React.SetStateAction<boolean>>;

  step1Error: string;

  loading: boolean;

  handleStep1Submit: (e: React.FormEvent<HTMLFormElement>) => void;
}

export default function Step1Account({
  email,
  setEmail,
  password,
  setPassword,
  confirmPassword,
  setConfirmPassword,
  showPassword,
  setShowPassword,
  showConfirmPassword,
  setShowConfirmPassword,
  step1Error,
  loading,
  handleStep1Submit,
}: Step1AccountProps) {
  return (
    <>
      <div className="step-icon-badge">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
          <circle cx="12" cy="8" r="4" />
          <path d="M4 21v-1a8 8 0 0 1 16 0v1" />
        </svg>
      </div>

      <h1 className="login-heading">Create Account</h1>

      <p className="step-subheading">
        Let&apos;s get your Lenar account ready.
      </p>

      <form className="login-form" onSubmit={handleStep1Submit}>
        <div className="input-wrapper">
          <svg
            className="input-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
          >
            <rect x="3" y="5" width="18" height="14" rx="2" />
            <path d="M3 7l9 6 9-6" />
          </svg>

          <input
            name="email"
            type="email"
            placeholder="Email address"
            value={email}
            autoComplete="email"
            autoFocus
            disabled={loading}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="input-wrapper">
          <svg
            className="input-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
          >
            <rect x="4" y="11" width="16" height="9" rx="2" />
            <path d="M8 11V7a4 4 0 0 1 8 0v4" />
          </svg>

          <input
            name="password"
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            autoComplete="new-password"
            disabled={loading}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="button"
            className="toggle-password"
            disabled={loading}
            onClick={() => setShowPassword((prev) => !prev)}
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M3 3l18 18" />
                <path d="M10.6 10.6a2 2 0 0 0 2.83 2.83" />
                <path d="M9.36 5.36A9.5 9.5 0 0 1 12 5c5 0 9 4.5 9 7-0.55 1.1-1.4 2.3-2.5 3.36M6.5 6.64C4.4 7.7 2.55 9.9 2 11c.55 1.1 1.4 2.3 2.5 3.36A9.5 9.5 0 0 0 12 17c.7 0 1.37-.08 2-.23" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M2 11s3-6 10-6 10 6 10 6-3 6-10 6-10-6-10-6z" />
                <circle cx="12" cy="11" r="3" />
              </svg>
            )}
          </button>
        </div>

        <div className="input-wrapper">
          <svg
            className="input-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
          >
            <rect x="4" y="11" width="16" height="9" rx="2" />
            <path d="M8 11V7a4 4 0 0 1 8 0v4" />
          </svg>

          <input
            name="confirmPasword"
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Confirm password"
            value={confirmPassword}
            autoCorrect="new-password"
            disabled={loading}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          <button
            type="button"
            className="toggle-password"
            onClick={() => setShowConfirmPassword((prev) => !prev)}
            aria-label={showConfirmPassword ? "Hide password" : "Show password"}
          >
            {showConfirmPassword ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M3 3l18 18" />
                <path d="M10.6 10.6a2 2 0 0 0 2.83 2.83" />
                <path d="M9.36 5.36A9.5 9.5 0 0 1 12 5c5 0 9 4.5 9 7-0.55 1.1-1.4 2.3-2.5 3.36M6.5 6.64C4.4 7.7 2.55 9.9 2 11c.55 1.1 1.4 2.3 2.5 3.36A9.5 9.5 0 0 0 12 17c.7 0 1.37-.08 2-.23" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M2 11s3-6 10-6 10 6 10 6-3 6-10 6-10-6-10-6z" />
                <circle cx="12" cy="11" r="3" />
              </svg>
            )}
          </button>
        </div>

        {step1Error && <p className="form-error">{step1Error}</p>}

        <button
          type="submit"
          className="login-btn"
          disabled={loading}
        >
          {loading ? "Creating account..." : "Continue"}

          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
            <path d="M13 6l6 6-6 6" />
          </svg>
        </button>
      </form>

      <div className="signup-row">
        Already have an account?

            <Link
              className="signup-link"
              to={loading ? "#" : "/login"}
              onClick={(e) => {
                if (loading) e.preventDefault();
              }}
            >
          Login
        </Link>
      </div>
    </>
  );
}
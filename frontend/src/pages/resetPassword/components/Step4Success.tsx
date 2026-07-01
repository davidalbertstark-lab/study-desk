import { Link } from "react-router-dom";

import logo from "../../../assets/logo.svg";
import loginImage from "../../../assets/login.png";

export default function Step4Success() {
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
            Password Updated
          </h1>

          <p className="loadscreen-subtext">
            You're all set.
            Sign in using your new password.
          </p>
        </div>
      </div>

      <div className="login-form-panel">
        <div className="signup-card waitlist-confirmation">
          <div className="waitlist-check-circle">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
            >
              <path d="M5 13l4 4L19 7" />
            </svg>
          </div>

          <span className="waitlist-status-badge">
            PASSWORD RESET
          </span>

          <h1 className="login-heading center">
            Success!
          </h1>

          <p className="waitlist-message">
            Your password has been reset successfully.
          </p>

          <p className="waitlist-message">
            You can now log in using your new password.
          </p>

          <Link
            to="/login"
            className="login-btn as-link"
          >
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
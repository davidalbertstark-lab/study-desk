import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../../api/client";
import AuthLayout from "../../../components/layout/AuthLayout";
import "../Signup.css";

interface WaitlistData {
  full_name: string;
  matric_number: string;
  department: string | null;
  status: string;
}

const STEPS = [
  { number: 1, label: "Account" },
  { number: 2, label: "Academic Info" },
  { number: 3, label: "Waitlist" },
];

export default function Step3Waitlist() {
  const [waitlist, setWaitlist] = useState<WaitlistData | null>(null);
  const [loading, setLoading] = useState(true);

  // This page is always Step 3.
  const step = 3;

  useEffect(() => {
    async function fetchWaitlist() {
      try {
        const response = await api.get("/users/me");
        setWaitlist(response.data.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchWaitlist();
  }, []);

  return (
    <AuthLayout
      title="You're on the waitlist 🎉"
      subtitle="We'll notify you once your account has been approved."
    >
      {loading ? (
        <div className="waitlist-confirmation">
          <h1 className="login-heading center">Loading...</h1>
        </div>
      ) : (
        <div className="waitlist-confirmation">
          {/* ---------------- Step Indicator ---------------- */}
          <div className="step-indicator">
            {STEPS.map((s, i) => (
              <div
                key={s.number}
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  flex: i < STEPS.length - 1 ? 1 : undefined,
                }}
              >
                <div className="step-item">
                  <div
                    className={`step-circle ${
                      step > s.number
                        ? "completed"
                        : step === s.number
                        ? "active"
                        : ""
                    }`}
                  >
                    {step > s.number ? (
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2.5"
                      >
                        <path d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      s.number
                    )}
                  </div>

                  <span
                    className={`step-label ${
                      step >= s.number ? "active" : ""
                    }`}
                  >
                    {s.label}
                  </span>
                </div>

                {i < STEPS.length - 1 && (
                  <div
                    className={`step-line ${
                      step > s.number ? "completed" : ""
                    }`}
                  />
                )}
              </div>
            ))}
          </div>

          {/* ---------------- Waitlist Content ---------------- */}
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
            WAITLIST STATUS
          </span>

          <h1 className="login-heading center">
            You're on the waitlist 🎉
          </h1>

          <p className="waitlist-message">
            We'll notify you once your account has been approved.
          </p>

          <div className="waitlist-profile-card">
            <div className="waitlist-avatar">
              {waitlist?.full_name?.charAt(0).toUpperCase()}
            </div>

            <div className="waitlist-profile-header">
              <h2>{waitlist?.full_name}</h2>
              <p>{waitlist?.department ?? "Department not set"}</p>
            </div>

            <div className="waitlist-divider" />

            <div className="waitlist-info-list">
              <div className="waitlist-info-item">
                <span>Matric Number</span>
                <strong>{waitlist?.matric_number}</strong>
              </div>

              <div className="waitlist-info-item">
                <span>Status</span>

                <div className="status-pill">
                  {waitlist?.status}
                </div>
              </div>
            </div>
          </div>

          <Link to="/login" className="login-btn as-link">
            Back to Login
          </Link>

          <div className="signup-row">
            Need help?
            <span className="signup-link">Contact Support</span>
          </div>
        </div>
      )}
    </AuthLayout>
  );
}
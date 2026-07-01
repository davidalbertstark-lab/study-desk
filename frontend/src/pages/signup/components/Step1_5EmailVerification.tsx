import { useEffect, useRef, useState } from "react";

import logo from "../../../assets/logo.svg";
import loginImage from "../../../assets/login.png";

const OTP_LENGTH = 6;
const RESEND_SECONDS = 60;

type Props = {
  email: string;
  loading: boolean;
  error: string;

  onVerify: (code: string) => Promise<void>;
  onResend: () => Promise<void>;
  onBack: () => void;
};

export default function Step1_5EmailVerification({
  email,
  loading,
  error,
  onVerify,
  onResend,
  onBack,
}: Props) {
  const [otp, setOtp] = useState<string[]>(
    Array(OTP_LENGTH).fill("")
  );

  const refs = useRef<HTMLInputElement[]>([]);

  const [countdown, setCountdown] =
    useState(RESEND_SECONDS);

  useEffect(() => {
    if (countdown <= 0) return;

    const timer = window.setTimeout(() => {
      setCountdown((prev) => prev - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [countdown]);

  async function verify(values: string[]) {
    const code = values.join("");

    if (code.length !== OTP_LENGTH) return;

    await onVerify(code);
  }

  function handleChange(
    index: number,
    value: string
  ) {
    const digit = value.replace(/\D/g, "").slice(-1);

    const next = [...otp];

    next[index] = digit;

    setOtp(next);

    if (
      digit &&
      index < OTP_LENGTH - 1
    ) {
      refs.current[index + 1]?.focus();
    }

    if (next.every((v) => v !== "")) {
      verify(next);
    }
  }

  function handleKeyDown(
    index: number,
    e: React.KeyboardEvent<HTMLInputElement>
  ) {
    if (
      e.key === "Backspace" &&
      !otp[index] &&
      index > 0
    ) {
      refs.current[index - 1]?.focus();
    }
  }

  function handlePaste(
    e: React.ClipboardEvent<HTMLInputElement>
  ) {
    e.preventDefault();

    const pasted = e.clipboardData
      .getData("text")
      .replace(/\D/g, "")
      .slice(0, OTP_LENGTH);

    if (!pasted) return;

    const values = Array(OTP_LENGTH).fill("");

    pasted.split("").forEach((char, i) => {
      values[i] = char;
    });

    setOtp(values);

    refs.current[
      Math.min(
        pasted.length - 1,
        OTP_LENGTH - 1
      )
    ]?.focus();

    if (
      pasted.length === OTP_LENGTH
    ) {
      verify(values);
    }
  }

  async function handleResend() {
    if (
      countdown > 0 ||
      loading
    ) {
      return;
    }

    await onResend();

    setCountdown(RESEND_SECONDS);
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
            Verify your email
          </h1>

          <p className="loadscreen-subtext">
            One last step before creating your account.
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
                y="5"
                width="18"
                height="14"
                rx="2"
              />

              <path d="M3 7l9 6 9-6" />
            </svg>
          </div>

          <h1 className="login-heading">
            Verify Email
          </h1>

          <p className="step-subheading">
            Enter the 6-digit verification code sent to
            <br />
            <strong>{email}</strong>
          </p>

          <div className="otp-row">
            {otp.map((digit, index) => (
              <input
                key={index}
                ref={(el) => {
                  if (el) {
                    refs.current[index] =
                      el;
                  }
                }}
                className="otp-box"
                type="text"
                inputMode="numeric"
                maxLength={1}
                value={digit}
                onChange={(e) =>
                  handleChange(
                    index,
                    e.target.value
                  )
                }
                onKeyDown={(e) =>
                  handleKeyDown(
                    index,
                    e
                  )
                }
                onPaste={
                  index === 0
                    ? handlePaste
                    : undefined
                }
              />
            ))}
          </div>
            <div className="resend-row">
                        <span>
                        Didn't receive the code?
                        </span>

                        <button
                        type="button"
                        className="resend-link"
                        disabled={loading || countdown > 0}
                        onClick={handleResend}
                        >
                        {countdown > 0
                            ? `Resend in ${countdown}s`
                            : "Resend"}
                        </button>
                    </div>

                    {loading && (
                        <p className="step-subheading">
                        Verifying...
                        </p>
                    )}

                    {error && (
                        <p className="form-error">
                        {error}
                        </p>
                    )}

                    <button
                        type="button"
                        className="back-link"
                        disabled={loading}
                        onClick={onBack}
                    >
                        <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        >
                        <path d="M15 18l-6-6 6-6" />
                        </svg>

                        Back
                    </button>

                    </div>
                </div>
                </div>
            );
            }
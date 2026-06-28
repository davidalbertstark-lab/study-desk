import React, {
  useState,
  useEffect,
  useContext,
  type FormEvent,
} from "react";
import { useSearchParams, useNavigate } from "react-router-dom";

import SignupLeftPanel from "./components/SignupLeftPanel";
import Step1Account from "./components/Step1Account";
import Step2Academic from "./components/Step2Academic";
import Step3Waitlist from "./components/Step3Waitlist";

import { AuthContext } from "../../auth/AuthContext";
import { updateProfile } from "../../api/user";
import { register } from "../../api/auth";
import api from "../../api/client";

import logo from "../../assets/logo.svg";
import "./Signup.css";

const STEPS = [
  { number: 1, label: "Account" },
  { number: 2, label: "Academic Info" },
  { number: 3, label: "Waitlist" },
];

export default function Signup() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const completeProfileMode =
    searchParams.get("completeProfile") === "true";

  const auth = useContext(AuthContext);

  // FIX: safe navigation logic only (no blocking render logic)
  useEffect(() => {
    if (!completeProfileMode) return;
    if (!auth?.user) return;

    if (auth.user.profile_completed) {
      if (auth.user.status === "WAITLISTED") {
        navigate("/waitlist", { replace: true });
      }

      if (auth.user.status === "ACTIVE") {
        navigate("/dashboard", { replace: true });
      }
    }
  }, [auth?.user, completeProfileMode, navigate]);

  // FIX: step should NOT be derived in a way that breaks UI flow
  const [step, setStep] = useState<number>(1);

  useEffect(() => {
    if (completeProfileMode) {
      setStep(2);
    } else {
      setStep(1);
    }
  }, [completeProfileMode]);

  // Step 1
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [step1Error, setStep1Error] = useState("");
  const [loading, setLoading] = useState(false);

  // Step 2
  const [fullName, setFullName] = useState("");
  const [matricNumber, setMatricNumber] = useState("");
  const [level, setLevel] = useState("");
  const [faculty, setFaculty] = useState("");
  const [department, setDepartment] = useState("");

  type CompleteProfileData = {
    fullName: string;
    matricNumber: string;
    level: string;
    faculty: string;
    department: string;
  };

  async function handleCompleteProfile(
    data: CompleteProfileData
  ) {
    try {
      await updateProfile({
        full_name: data.fullName,
        matric_number: data.matricNumber,
        level: data.level,
        faculty: data.faculty,
        department: data.department,
      });

      const res = await api.get("/users/me");
      auth?.setUser(res.data.data);

      navigate("/waitlist", { replace: true });
    } catch (err) {
      console.error("Profile update failed:", err);
    }
  }

  async function handleStep1Submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (loading) return;

    if (password !== confirmPassword) {
      setStep1Error("Passwords do not match.");
      return;
    }

    if (password.trim().length === 0) {
    setStep1Error("Password cannot be empty.");
    return;
    }

    if (password.length < 8) {
        setStep1Error("Password must be at least 8 characters.");
        return;
    }

    if (password.length > 64) {
        setStep1Error("Password is too long.");
        return;
    }

    setStep1Error("");
    setLoading(true);

    try {

      const cleanEmail = email.trim().toLowerCase();

      await register(
          cleanEmail,
          password
      );

      const res = await api.get("/users/me");
      auth?.setUser(res.data.data);

      navigate("/signup?completeProfile=true", {
        replace: true,
      });
    } catch (err: any) {

      if (!err.response) {
        setStep1Error("No internet connection.");
        return;
      }

      if (err.response.status >= 500) {
        setStep1Error(
          "Something went wrong. Please try again."
        );
        return;
      }

      const message =
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Failed to create account.";

      setStep1Error(message);

    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="studydesk-page signup-page">
      <SignupLeftPanel />

      <div className="login-form-panel">
        <div className="signup-card">

          <div className="signup-mobile-topbar">
            {step > 1 && step < 3 && !completeProfileMode && (
              <button
                type="button"
                className="mobile-back-btn"
                onClick={() => setStep(1)}
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M15 18l-6-6 6-6" />
                </svg>
              </button>
            )}

            <span className="signup-mobile-title">
              {step === 1 && "Create Account"}
              {step === 2 && "Academic Profile"}
              {step === 3 && "Join Waitlist"}
            </span>
          </div>

          <div className="logo form-logo">
            <img src={logo} alt="Lenar logo" />
            <span className="logo-text">LENAR</span>
          </div>

          {/* Step Indicator */}
          {step !== 3 && (
            <div className="step-indicator">
              {STEPS.map((s, i) => (
                <React.Fragment key={s.number}>
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
                      {step > s.number ? "✓" : s.number}
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
                </React.Fragment>
              ))}
            </div>
          )}

          {/* STEP 1 */}
          {step === 1 && !completeProfileMode && (
            <Step1Account
              email={email}
              setEmail={setEmail}
              password={password}
              setPassword={setPassword}
              confirmPassword={confirmPassword}
              setConfirmPassword={setConfirmPassword}
              showPassword={showPassword}
              setShowPassword={setShowPassword}
              showConfirmPassword={showConfirmPassword}
              setShowConfirmPassword={setShowConfirmPassword}
              step1Error={step1Error}
              loading={loading}
              handleStep1Submit={handleStep1Submit}
            />
          )}

          {/* STEP 2 */}
          {step === 2 && (
            <Step2Academic
              fullName={fullName}
              setFullName={setFullName}
              matricNumber={matricNumber}
              setMatricNumber={setMatricNumber}
              level={level}
              setLevel={setLevel}
              faculty={faculty}
              setFaculty={setFaculty}
              department={department}
              setDepartment={setDepartment}
              onNext={() => setStep(3)}
              onBack={() => setStep(1)}
              disableBack={completeProfileMode}
              completeProfileMode={completeProfileMode}
              onCompleteProfile={handleCompleteProfile}
            />
          )}

          {/* STEP 3 */}
          {step === 3 && <Step3Waitlist />}
        </div>
      </div>
    </div>
  );
}
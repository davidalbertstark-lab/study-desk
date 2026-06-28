import { useState } from "react";
import type { FormEvent } from "react";

const LEVELS = [
  "100 Level",
  "200 Level",
  "300 Level",
  "400 Level",
  "500 Level",
];

const FACULTIES = [
  "Computing",
  "Engineering",
  "Sciences",
  "Agriculture",
  "Technology",
  "Environmental Sciences",
];

const DEPARTMENTS = [
  "Computer Science",
  "Software Engineering",
  "Cyber Security",
  "Information Technology",
  "Mathematics",
];

interface Props {
  fullName: string;
  setFullName: (v: string) => void;

  matricNumber: string;
  setMatricNumber: (v: string) => void;

  level: string;
  setLevel: (v: string) => void;

  faculty: string;
  setFaculty: (v: string) => void;

  department: string;
  setDepartment: (v: string) => void;

  onNext: () => void;
  onBack: () => void;

  disableBack?: boolean;
  completeProfileMode?: boolean;

  onCompleteProfile?: (data: {
    fullName: string;
    matricNumber: string;
    level: string;
    faculty: string;
    department: string;
  }) => Promise<void>;
}

export default function Step2Academic({
  fullName,
  setFullName,
  matricNumber,
  setMatricNumber,
  level,
  setLevel,
  faculty,
  setFaculty,
  department,
  setDepartment,
  onNext,
  onBack,
  disableBack,
  completeProfileMode = false,
  onCompleteProfile,
}: Props) {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    e: FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();
    if (loading) return;

    const cleanName = fullName.trim();
    const cleanMatric = matricNumber.trim().toUpperCase();

    if (!cleanName) {
      setError("Full name is required.");
      return;
    }

    if (cleanName.length < 2) {
      setError("Please enter your full name.");
      return;
    }

    if (!cleanMatric) {
      setError("Matric number is required.");
      return;
    }

    if (cleanMatric.includes(" ")) {
      setError("Matric number cannot contain spaces.");
      return;
    }

    if (!level) {
      setError("Please select your level.");
      return;
    }

    if (!faculty) {
      setError("Please select your faculty.");
      return;
    }

    if (!department) {
      setError("Please select your department.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      if (
        completeProfileMode &&
        onCompleteProfile
      ) {
        await onCompleteProfile({
          fullName: cleanName,
          matricNumber: cleanMatric,
          level,
          faculty,
          department,
        });

        return;
      }

      console.log(
        "Step 2 — academic profile:",
        {
          fullName: cleanName,
          matricNumber: cleanMatric,
          level,
          faculty,
          department,
        }
      );

      onNext();
    } catch (err) {
      setError(
        "Unable to save your profile. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="step-icon-badge">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
        >
          <path d="M12 3L2 8l10 5 10-5-10-5z" />
          <path d="M6 10.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-5.5" />
        </svg>
      </div>

      <h1 className="login-heading">
        Academic Profile
      </h1>

      <p className="step-subheading">
        Help us personalize your experience.
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
            <circle cx="12" cy="8" r="4" />
            <path d="M4 21v-1a8 8 0 0 1 16 0v1" />
          </svg>

          <input
            type="text"
            placeholder="Full name"
            value={fullName}
            disabled={loading}
            onChange={(e) =>
              setFullName(e.target.value)
            }
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
            <rect
              x="3"
              y="4"
              width="18"
              height="16"
              rx="2"
            />
            <path d="M3 9h18" />
            <path d="M7 13h2M11 13h2" />
          </svg>

          <input
            type="text"
            placeholder="Matric number"
            value={matricNumber}
            disabled={loading}
            onChange={(e) =>
              setMatricNumber(
                e.target.value.toUpperCase().replace(/\s/g, "")
              )
            }
            required
          />
        </div>

        <div className="input-wrapper select-wrapper">
          <select
            value={level}
            disabled={loading}
            onChange={(e) =>
              setLevel(e.target.value)
            }
            required
          >
            <option value="" disabled>
              Level
            </option>

            {LEVELS.map((lv) => (
              <option
                key={lv}
                value={lv}
              >
                {lv}
              </option>
            ))}
          </select>
        </div>

        <div className="input-wrapper select-wrapper">
          <select
            value={faculty}
            disabled={loading}
            onChange={(e) =>
              setFaculty(e.target.value)
            }
            required
          >
            <option value="" disabled>
              Faculty
            </option>

            {FACULTIES.map((f) => (
              <option
                key={f}
                value={f}
              >
                {f}
              </option>
            ))}
          </select>
        </div>

        <div className="input-wrapper select-wrapper">
          <select
            value={department}
            disabled={loading}
            onChange={(e) =>
              setDepartment(
                e.target.value
              )
            }
            required
          >
            <option value="" disabled>
              Department
            </option>

            {DEPARTMENTS.map((d) => (
              <option
                key={d}
                value={d}
              >
                {d}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <p className="form-error">
            {error}
          </p>
        )}

        <button
          type="submit"
          className="login-btn"
          disabled={loading}
        >
          {loading
            ? "Saving..."
            : completeProfileMode
            ? "Complete Profile"
            : "Join Waitlist"}

          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M5 12h14" />
            <path d="M13 6l6 6-6 6" />
          </svg>
        </button>
      </form>
            {!disableBack && (
        <button
          disabled={disableBack || loading}
          type="button"
          className="back-link"
          onClick={() => {
            if (!loading) onBack();
          }}
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
            )}
    </>
  );
}
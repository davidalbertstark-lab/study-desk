import { useState } from "react";

import "./ResetPassword.css";

import Step1Email from "./components/Step1Email";
import Step2Otp from "./components/Step2Otp";
import Step3Password from "./components/Step3Password";
import Step4Success from "./components/Step4Success";

import {
  forgotPassword,
  verifyResetCode,
  resetPassword,
} from "../../api/auth";

import { getApiError } from "../../utils/getApiError";

type Step = 1 | 2 | 3 | 4;

export default function ResetPassword() {
  const [step, setStep] = useState<Step>(1);

  const [email, setEmail] = useState("");

  const [code, setCode] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  async function handleSendCode(emailValue: string) {
    try {
      setLoading(true);
      setError("");

      const cleanEmail = emailValue.trim().toLowerCase();

      await forgotPassword(cleanEmail);

      setEmail(cleanEmail);

      setStep(2);
    } catch (err) {
      setError(getApiError(err));
    } finally {
      setLoading(false);
    }
  }

  async function handleVerifyCode(codeValue: string) {
    try {
      setLoading(true);
      setError("");

      await verifyResetCode(email, codeValue);

      setCode(codeValue);

      setStep(3);
    } catch (err) {
      setError(getApiError(err));
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(password: string) {
    try {
      setLoading(true);
      setError("");

      await resetPassword(
        email,
        code,
        password
      );

      setStep(4);
    } catch (err) {
      setError(getApiError(err));
    } finally {
      setLoading(false);
    }
  }

  switch (step) {
    case 1:
      return (
        <Step1Email
          loading={loading}
          error={error}
          onSubmit={handleSendCode}
        />
      );

    case 2:
      return (
        <Step2Otp
          email={email}
          loading={loading}
          error={error}
          onVerify={handleVerifyCode}
          onResend={() => handleSendCode(email)}
        />
      );

    case 3:
      return (
        <Step3Password
          loading={loading}
          error={error}
          onSubmit={handleResetPassword}
        />
      );

    case 4:
      return <Step4Success />;

    default:
      return null;
  }
}
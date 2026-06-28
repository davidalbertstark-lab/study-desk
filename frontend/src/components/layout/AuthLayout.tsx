import type { ReactNode } from "react";
import logo from "../../assets/logo.svg";
import loginImage from "../../assets/login.png";
import "../../pages/signup/Signup.css";

interface Props {
  children: ReactNode;
  title: string;
  subtitle: string;
}

export default function AuthLayout({
  children,
  title,
  subtitle,
}: Props) {
  return (
    <div className="studydesk-page">
      <div
        className="login-image-panel"
        style={{ backgroundImage: `url(${loginImage})` }}
      >
        <div className="loadscreen-overlay-gradient" />

        <div className="loadscreen-text">
          <div className="loadscreen-logo">
            <img src={logo} alt="Lenar logo" />
            <span className="logo-text">LENAR</span>
          </div>

          <h1 className="loadscreen-heading">{title}</h1>

          <p className="loadscreen-subtext">
            {subtitle}
          </p>
        </div>
      </div>

      <div className="login-form-panel">
        {children}
      </div>
    </div>
  );
}
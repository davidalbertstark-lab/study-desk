import logo from "../../../assets/logo.svg";
import loginImage from "../../../assets/login.png";

export default function SignupLeftPanel() {
  return (
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

        <h1 className="loadscreen-heading">
          Create your <span className="brand-blue">Lenar</span> account
        </h1>

        <p className="loadscreen-subtext">
          Join thousands of students on a better learning journey.
        </p>
      </div>
    </div>
  );
}
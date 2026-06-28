import { useState, useEffect, type FormEvent } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useContext } from "react"
import { getApiError } from "../../utils/getApiError";
import { AuthContext } from "../../auth/AuthContext"
import "./Login.css"
import logo from "../../assets/logo.svg"
import loginImage from "../../assets/login.png"
import { login } from "../../api/auth"


function isDesktopWidth() {
  return typeof window !== 'undefined' && window.innerWidth >= 1024;
}

export default function Login() {
  const [showLoadscreen, setShowLoadscreen] = useState(!isDesktopWidth());
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();
  const auth = useContext(AuthContext);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // If the window is resized across the 1024px breakpoint (tablet
  // rotation, browser resize), skip/clear the loadscreen appropriately.
  useEffect(() => {
    function handleResize() {
      if (isDesktopWidth()) {
        setShowLoadscreen(false);
      }
    }
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  function handleContinue() {
    setShowLoadscreen(false);
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (loading) return;

      setLoading(true);
      setError("");

      try {
    const cleanEmail = email.trim().toLowerCase();

    const data = await login(cleanEmail, password);

    const user = data.user;

    auth?.setUser(user);

    const status = user.status;

    if (!user.profile_completed) {
      navigate("/signup?completeProfile=true");
      return;
    }

    if (status === "ACTIVE") {
      navigate("/dashboard");
      return;
    }

    if (status === "WAITLISTED") {
      navigate("/waitlist");
      return;
    }

    navigate("/waitlist");

    } catch (err: any) {

      if (!err.response) {
        setError("No internet connection.");
        return;
      }

      if (err.response.status >= 500) {
        setError(
          "Something went wrong. Please try again."
        );
        return;
      }

      setError(getApiError(err));

    }finally {
      setLoading(false);
    }
  }

  return (
    
    <div className="studydesk-page">
      {/* ---------------- Mobile Loadscreen (shown once) ---------------- */}
       
      <div
        className={`loadscreen ${showLoadscreen ? 'active' : ''}`}
        style={{ backgroundImage: `url(${loginImage})` }}
      >
        
        <div className="loadscreen-overlay-gradient" />
        <div className="loadscreen-text">
          <div className="loadscreen-logo">
            <img src={logo} alt="Lenar logo" />
            <span className="logo-text">LENAR</span>
          </div>
          <h1 className="loadscreen-heading">Welcome back !</h1>
          <p className="loadscreen-subtext">
            Access your account and continue your learning journey.
          </p>
        </div>
        <button type="button" className="continue-btn" onClick={handleContinue}>
          Continue
          
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 12h14" />
                  <path d="M13 6l6 6-6 6" />
                </svg>
        </button>
      </div>

      {/* ---------------- Desktop/Tablet Left Image Panel ---------------- */}
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
          <h1 className="loadscreen-heading">Welcome back</h1>
          <p className="loadscreen-subtext">
            Access your account and continue your learning journey.
          </p>
        </div>
      </div>

      {/* ---------------- Login Form Panel ---------------- */}
      {!showLoadscreen && (
        <div className="login-form-panel">
          <div className="login-card">
            <div className="logo form-logo">
              <img src={logo} alt="Lenar logo" />
              <span className="logo-text">LENAR</span>
       </div>
           
            <h1 className="login-heading">Login</h1>

            <form className="login-form" onSubmit={handleSubmit}>
              <div className="input-wrapper">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
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
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                  <rect x="4" y="11" width="16" height="9" rx="2" />
                  <path d="M8 11V7a4 4 0 0 1 8 0v4" />
                </svg>
                <input
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Password"
                  value={password}
                  autoComplete="current-password"
                  disabled={loading}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="toggle-password"
                  disabled={loading}
                  onClick={() => setShowPassword((prev) => !prev)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
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

                {error && (
                    <p className="form-error">
                        {error}
                    </p>
                )}
              <div className="forgot-password-row">
              <Link
                className={`forgot-password ${loading ? "disabled" : ""}`}
                to={loading ? "#" : "/forgot-password"}
                onClick={(e) => {
                  if (loading) e.preventDefault();
                }}
              >
                Forgot password?
              </Link>
              </div>

            <button
                type="submit"
                className="login-btn"
                disabled={loading}
                >
                {loading ? "Signing in..." : "Login"}

                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14" />
                    <path d="M13 6l6 6-6 6" />
                </svg>
            </button>
            </form>

            <div className="divider-row">
              <span className="line" />
              <span className="label">OR CONTINUE WITH</span>
              <span className="line" />
            </div>

            <div className="social-row">
              <button type="button" className="social-btn" aria-label="Continue with Google">
                <svg viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M23.49 12.27c0-.79-.07-1.54-.2-2.27H12v4.51h6.47c-.29 1.48-1.14 2.73-2.4 3.58v2.97h3.86c2.26-2.09 3.56-5.17 3.56-8.79z" />
                  <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.86-2.97c-1.08.72-2.45 1.15-4.07 1.15-3.13 0-5.78-2.11-6.73-4.96H1.27v3.07C3.26 21.3 7.31 24 12 24z" />
                  <path fill="#FBBC05" d="M5.27 14.31a7.21 7.21 0 0 1 0-4.62V6.62H1.27a11.97 11.97 0 0 0 0 10.76l4-3.07z" />
                  <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.94 1.19 15.24 0 12 0 7.31 0 3.26 2.7 1.27 6.62l4 3.07C6.22 6.86 8.87 4.75 12 4.75z" />
                </svg>
              </button>

              <button type="button" className="social-btn" aria-label="Continue with Apple">
                <svg viewBox="0 0 384 512">
                  <path
                    fill="#071426"
                    d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.2C42.5 141.6 0 184.2 0 269.5c0 47.6 18.1 98.2 40.4 130.6 21.7 31.4 45.6 53.1 73.5 52.1 27.6-1 38.1-17.9 71.5-17.9 33.3 0 42.9 17.9 71.7 17.3 28.5-.6 49.2-19.7 71-50.4-22.6-10.8-43-30.8-43.4-58.5zM222.3 79c14.2-17.2 24-41.2 21.4-65-21.3 1.5-46.2 14.7-60.8 32.4-13.2 15.5-24.7 39.2-21.6 62.3 22.5 1.7 45.5-11.6 61-29.7z"
                  />
                </svg>
              </button>
            </div>

            <div className="signup-row">
              No account yet?
                <Link
                  className="signup-link"
                  to={loading ? "#" : "/signup"}
                  onClick={(e) => {
                    if (loading) e.preventDefault();
                  }}
                >
                  Sign up
                </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
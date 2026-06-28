import { useContext } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { AuthContext } from "../auth/AuthContext";

type Props = {
  children: React.ReactNode;
};

export const ProtectedRoute = ({ children }: Props) => {
  const context = useContext(AuthContext);
  const location = useLocation();

  if (!context) {
    return <Navigate to="/login" replace />;
  }

  const { user, loading } = context;

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const isWaitlistRoute = location.pathname === "/waitlist";

  // WAITLIST / REJECTED → always go waitlist page
  if (
    (user.status === "WAITLISTED" || user.status === "REJECTED") &&
    !isWaitlistRoute
  ) {
    return <Navigate to="/waitlist" replace />;
  }

  // PROFILE NOT COMPLETE
  if (!user.profile_completed) {
    return <Navigate to="/signup?completeProfile=true" replace />;
  }

  return <>{children}</>;
};
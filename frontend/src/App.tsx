import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/login/Login";
import Signup from "./pages/signup/Signup";
import Dashboard from "./pages/dashboard/Dashboard";

import Step3Waitlist from "./pages/signup/components/Step3Waitlist";
import ResetPassword from "./pages/resetPassword/ResetPassword";

import GoogleCallback from "./pages/googleCallback/GoogleCallback";

import { ProtectedRoute } from "./guards/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      {/* default */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* public */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route
          path="/auth/google/callback"
          element={<GoogleCallback />}
      />

      {/* protected */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/waitlist"
        element={
          <ProtectedRoute>
            <Step3Waitlist />
          </ProtectedRoute>
        }
      />



    </Routes>
  );
}
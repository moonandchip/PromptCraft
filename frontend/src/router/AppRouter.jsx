import { Routes, Route } from "react-router-dom";

import HomePage from "../pages/Home/HomePage";
import LoginPage from "../pages/Login/LoginPage";
import RegisterPage from "../pages/Register/RegisterPage";
import PracticePage from "../pages/Practice/PracticePage";
import ProgressPage from "../pages/Progress/ProgressPage";
import ChallengePage from "../pages/Challenge/ChallengePage";
import HowToPlayPage from "../pages/HowToPlay/HowtoPlayPage";

import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/how-to-play" element={<HowToPlayPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/practice" element={<PracticePage />} />
          <Route path="/progress" element={<ProgressPage />} />
          <Route path="/challenge" element={<ChallengePage />} />
        </Route>
      </Route>
    </Routes>
  );
}

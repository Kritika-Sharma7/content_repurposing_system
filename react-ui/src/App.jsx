import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import DemoPage from "./pages/DemoPage";
import ArchitecturePage from "./pages/ArchitecturePage";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="main-wrap">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/demo" element={<DemoPage />} />
          <Route path="/architecture" element={<ArchitecturePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

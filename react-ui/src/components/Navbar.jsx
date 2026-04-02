import { NavLink, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  return (
    <header className="topbar">
      <div className="container topbar-inner">
        <div className="brand">
          <span className="brand-mark" />
          <span>MultiAgent Studio</span>
        </div>

        <nav className="topnav-links">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/demo">Demo</NavLink>
          <NavLink to="/architecture">Architecture</NavLink>
          <a href="https://github.com" target="_blank" rel="noreferrer">
            GitHub
          </a>
        </nav>

        <button className="btn btn-dark" onClick={() => navigate("/demo")}>Try Demo</button>
      </div>
    </header>
  );
}

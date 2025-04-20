import { Link } from 'react-router-dom';
import '../styles/NavBar.css';

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="logo">InningsIQ</span>
        </Link>
        
        <div className="navbar-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/chat" className="nav-link">Chat</Link>
          <Link to="/dashboard" className="nav-link">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
};

export default NavBar; 
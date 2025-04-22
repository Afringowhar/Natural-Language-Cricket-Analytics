import { Link } from 'react-router-dom';
import '../styles/NavBar.css';

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-brand">
          <h1>InningsIQ</h1>
        </Link>
        
        <div className="nav-links">
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/login" className="nav-link">Admin</Link>
        </div>
      </div>
    </nav>
  );
};

export default NavBar; 
import { Link } from 'react-router-dom';
import '../styles/HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <div className="hero-left">
            <div className="logo-placeholder">
              <span>IPL</span>
            </div>
          </div>
          <div className="hero-right">
            <h1 className="hero-title">Cricket ChatGPT for IPL</h1>
            <p className="hero-subtitle">Ask questions. Get stats. Like a broadcaster.</p>
            <div className="hero-buttons">
              <Link to="/dashboard" className="btn btn-primary">Explore Dashboard</Link>
              <Link to="/chat" className="btn btn-accent">Ask a Question</Link>
            </div>
          </div>
        </div>
      </div>
      <div className="footer-logos">
        <span>Prototype</span>
      </div>
    </div>
  );
};

export default HomePage; 
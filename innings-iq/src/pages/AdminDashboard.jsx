import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const handleLogout = () => {
    localStorage.removeItem('isAdmin');
    navigate('/login');
  };

  return (
    <div className="admin-dashboard">
      {/* Navigation Bar */}
      <nav className="admin-nav">
        <div className="nav-left">
          <button 
            className="toggle-sidebar"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            ☰
          </button>
          <h1>InningsIQ Admin</h1>
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </nav>

      <div className="dashboard-content">
        {/* Sidebar */}
        <aside className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
          <div className="sidebar-section">
            <h3>File Management</h3>
            <button className="sidebar-btn">
              Upload Match Data
            </button>
            <button className="sidebar-btn">
              Parse Match Data
            </button>
          </div>
          
          <div className="sidebar-section">
            <h3>System</h3>
            <button className="sidebar-btn">
              System Status
            </button>
            <button className="sidebar-btn">
              Logs
            </button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          <div className="content-header">
            <h2>Admin Dashboard</h2>
            <p>Welcome to the InningsIQ Admin Panel</p>
          </div>
          
          <div className="dashboard-grid">
            <div className="dashboard-card">
              <h3>Recent Uploads</h3>
              <p>No recent uploads</p>
            </div>
            
            <div className="dashboard-card">
              <h3>System Status</h3>
              <p>All systems operational</p>
            </div>
            
            <div className="dashboard-card">
              <h3>Analytics</h3>
              <p>Coming soon</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard; 
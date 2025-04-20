import { useState } from 'react';
import '../styles/DashboardPage.css';

const DashboardPage = () => {
  const [filters, setFilters] = useState({
    team: '',
    phase: '',
    playerType: '',
    isSpinner: false
  });

  const handleFilterChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const clearFilters = () => {
    setFilters({
      team: '',
      phase: '',
      playerType: '',
      isSpinner: false
    });
  };

  // Mock data for stat cards
  const statCards = [
    {
      title: 'Top Run Scorers',
      value: 'Virat Kohli',
      stat: '845 runs',
      trend: '↑'
    },
    {
      title: 'Best Economy Rate',
      value: 'Jasprit Bumrah',
      stat: '6.8',
      trend: '↓'
    },
    {
      title: 'Most Sixes',
      value: 'Rohit Sharma',
      stat: '32 sixes',
      trend: '↑'
    },
    {
      title: 'Highest Strike Rate',
      value: 'Andre Russell',
      stat: '185.5',
      trend: '↑'
    }
  ];

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">
        <aside className="sidebar">
          <h2>Filters</h2>
          <div className="filter-group">
            <label>Team</label>
            <select name="team" value={filters.team} onChange={handleFilterChange}>
              <option value="">All Teams</option>
              <option value="MI">Mumbai Indians</option>
              <option value="CSK">Chennai Super Kings</option>
              <option value="RCB">Royal Challengers Bangalore</option>
              {/* Add more teams */}
            </select>
          </div>

          <div className="filter-group">
            <label>Phase</label>
            <select name="phase" value={filters.phase} onChange={handleFilterChange}>
              <option value="">All Phases</option>
              <option value="powerplay">Powerplay</option>
              <option value="middle">Middle Overs</option>
              <option value="death">Death Overs</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Player Type</label>
            <select name="playerType" value={filters.playerType} onChange={handleFilterChange}>
              <option value="">All Players</option>
              <option value="batter">Batter</option>
              <option value="bowler">Bowler</option>
            </select>
          </div>

          <div className="filter-group">
            <label>
              <input
                type="checkbox"
                name="isSpinner"
                checked={filters.isSpinner}
                onChange={handleFilterChange}
              />
              Spinner
            </label>
          </div>

          <button onClick={clearFilters} className="btn btn-primary">
            Clear Filters
          </button>
        </aside>

        <main className="dashboard-main">
          <div className="stat-grid">
            {statCards.map((card, index) => (
              <div key={index} className="stat-card card">
                <h3>{card.title}</h3>
                <div className="stat-value">{card.value}</div>
                <div className="stat-details">
                  <span className="stat-number">{card.stat}</span>
                  <span className="trend">{card.trend}</span>
                </div>
                <button className="btn btn-accent">View Details</button>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardPage; 
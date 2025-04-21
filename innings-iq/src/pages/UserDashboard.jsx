import { useState } from 'react';
import '../styles/UserDashboard.css';

const UserDashboard = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [selectedTimeframe, setSelectedTimeframe] = useState('last30days');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleTeamToggle = (team) => {
    setSelectedTeams(prev => 
      prev.includes(team) 
        ? prev.filter(t => t !== team)
        : [...prev, team]
    );
  };

  const handlePlayerToggle = (player) => {
    setSelectedPlayers(prev => 
      prev.includes(player) 
        ? prev.filter(p => p !== player)
        : [...prev, player]
    );
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      setMessages(prev => [...prev, { text: inputMessage, isUser: true }]);
      setInputMessage('');
      // Here you would typically send the message to your backend
      // and receive a response
    }
  };

  return (
    <div className="user-dashboard">
      {/* Chat Panel */}
      <div className="chat-panel">
        <div className="chat-header">
          <h2>Cricket Analytics Chat</h2>
          <button 
            className="toggle-sidebar"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            {isSidebarOpen ? '◀' : '▶'}
          </button>
        </div>

        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h3>Welcome to InningsIQ Chat</h3>
              <p>Ask me anything about cricket analytics!</p>
              <p>Try questions like:</p>
              <ul>
                <li>Show me Virat Kohli's performance in the last 30 days</li>
                <li>Compare India and Australia's recent form</li>
                <li>What are the key trends in T20 cricket?</li>
              </ul>
            </div>
          ) : (
            messages.map((message, index) => (
              <div 
                key={index} 
                className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}
              >
                {message.text}
              </div>
            ))
          )}
        </div>

        <form onSubmit={handleSendMessage} className="chat-input">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask about cricket analytics..."
            className="message-input"
          />
          <button type="submit" className="send-button">
            Send
          </button>
        </form>
      </div>

      {/* Right Panel */}
      <div className="right-panel">
        {/* Highlights Section */}
        <div className="highlights-section">
          <h3>Key Highlights</h3>
          <div className="highlights-grid">
            <div className="highlight-card">
              <h4>Top Run Scorer</h4>
              <p className="highlight-value">Virat Kohli</p>
              <p className="highlight-stats">1,234 runs in 12 matches</p>
            </div>
            
            <div className="highlight-card">
              <h4>Best Bowling Average</h4>
              <p className="highlight-value">Jasprit Bumrah</p>
              <p className="highlight-stats">18.5 in 8 matches</p>
            </div>
            
            <div className="highlight-card">
              <h4>Highest Strike Rate</h4>
              <p className="highlight-value">Glenn Maxwell</p>
              <p className="highlight-stats">185.6 in 10 matches</p>
            </div>
          </div>
        </div>

        {/* Graphs Section */}
        <div className="graphs-section">
          <h3>Performance Analytics</h3>
          <div className="graphs-grid">
            <div className="graph-card">
              <h4>Team Performance</h4>
              <div className="graph-placeholder">
                Team Performance Graph
              </div>
            </div>
            
            <div className="graph-card">
              <h4>Player Form</h4>
              <div className="graph-placeholder">
                Player Form Graph
              </div>
            </div>
          </div>
        </div>

        {/* Natural Language Highlights */}
        <div className="nl-highlights">
          <h3>Natural Language Insights</h3>
          <div className="insights-grid">
            <div className="insight-card">
              <h4>Rising Stars</h4>
              <ul>
                <li>Shubman Gill: +45% performance</li>
                <li>Cameron Green: +38% performance</li>
                <li>Harry Brook: +32% performance</li>
              </ul>
            </div>
            
            <div className="insight-card">
              <h4>Key Trends</h4>
              <ul>
                <li>India's middle order showing improvement</li>
                <li>Spin bowling effectiveness increasing</li>
                <li>Powerplay scoring rates up by 15%</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Filters Panel */}
        <div className={`filters-panel ${isSidebarOpen ? 'open' : 'closed'}`}>
          <div className="filters-header">
            <h3>Analytics Filters</h3>
            <button 
              className="close-filters"
              onClick={() => setIsSidebarOpen(false)}
            >
              ×
            </button>
          </div>

          <div className="filter-section">
            <h4>Timeframe</h4>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="timeframe"
                  value="last7days"
                  checked={selectedTimeframe === 'last7days'}
                  onChange={(e) => setSelectedTimeframe(e.target.value)}
                />
                Last 7 Days
              </label>
              <label>
                <input
                  type="radio"
                  name="timeframe"
                  value="last30days"
                  checked={selectedTimeframe === 'last30days'}
                  onChange={(e) => setSelectedTimeframe(e.target.value)}
                />
                Last 30 Days
              </label>
              <label>
                <input
                  type="radio"
                  name="timeframe"
                  value="last90days"
                  checked={selectedTimeframe === 'last90days'}
                  onChange={(e) => setSelectedTimeframe(e.target.value)}
                />
                Last 90 Days
              </label>
            </div>
          </div>

          <div className="filter-section">
            <h4>Teams</h4>
            <div className="checkbox-group">
              {['India', 'Australia', 'England', 'South Africa'].map(team => (
                <label key={team}>
                  <input
                    type="checkbox"
                    checked={selectedTeams.includes(team)}
                    onChange={() => handleTeamToggle(team)}
                  />
                  {team}
                </label>
              ))}
            </div>
          </div>

          <div className="filter-section">
            <h4>Players</h4>
            <div className="checkbox-group">
              {['Virat Kohli', 'Steve Smith', 'Joe Root', 'Kagiso Rabada'].map(player => (
                <label key={player}>
                  <input
                    type="checkbox"
                    checked={selectedPlayers.includes(player)}
                    onChange={() => handlePlayerToggle(player)}
                  />
                  {player}
                </label>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard; 
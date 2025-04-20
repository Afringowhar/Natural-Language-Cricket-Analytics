import { useState } from 'react';
import '../styles/ChatPage.css';

const ChatPage = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement chat functionality
    setResponse({
      stat: "Virat Kohli",
      context: "has hit the most sixes in the powerplay this season with 12 sixes.",
      sql: "SELECT player_name, COUNT(*) as sixes FROM batting_stats WHERE phase = 'powerplay' GROUP BY player_name ORDER BY sixes DESC LIMIT 1;",
      addOns: [
        { title: "Powerplay Strike Rate", value: "180.5", chart: "↑" },
        { title: "Total Runs", value: "245", chart: "↑" }
      ]
    });
  };

  return (
    <div className="chat-page">
      <h1 className="page-title">Ask Anything About IPL</h1>
      
      <div className="chat-container">
        <form onSubmit={handleSubmit} className="query-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Who hit the most sixes in the powerplay?"
            className="query-input"
          />
          <button type="submit" className="btn btn-primary send-button">
            Send
          </button>
        </form>

        {response && (
          <div className="response-container">
            <div className="main-answer card">
              <div className="stat">{response.stat}</div>
              <div className="context">{response.context}</div>
            </div>

            <div className="sql-transcript card">
              <details>
                <summary>View SQL Query</summary>
                <pre>{response.sql}</pre>
              </details>
            </div>

            <div className="add-on-cards">
              {response.addOns.map((addOn, index) => (
                <div key={index} className="add-on-card card">
                  <h3>{addOn.title}</h3>
                  <div className="value">{addOn.value}</div>
                  <div className="chart">{addOn.chart}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage; 
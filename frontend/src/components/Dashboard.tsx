import React, { useState, useEffect } from 'react';

interface Dream {
  id: number;
  prompt: string;
  image_url: string;
  created_at: string;
}

interface DashboardProps {
  token: string;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ token, onLogout }) => {
  const [dreams, setDreams] = useState<Dream[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDreams();
  }, [token]);

  const fetchDreams = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/dreams/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dreams');
      }

      const data = await response.json();
      setDreams(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dreams');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>My Dream Gallery</h1>
          <button onClick={onLogout} className="btn-secondary">
            Sign Out
          </button>
        </div>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading your dreams...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>My Dream Gallery</h1>
          <button onClick={onLogout} className="btn-secondary">
            Sign Out
          </button>
        </div>
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={fetchDreams} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>My Dream Gallery</h1>
        <div className="dashboard-actions">
          <span className="dream-count">{dreams.length} dreams saved</span>
          <button onClick={onLogout} className="btn-secondary">
            Sign Out
          </button>
        </div>
      </div>

      {dreams.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">🌙</div>
          <h2>No dreams yet</h2>
          <p>Start creating dreams to see them here!</p>
        </div>
      ) : (
        <div className="dreams-grid">
          {dreams.map((dream) => (
            <div key={dream.id} className="dream-card">
              <div className="dream-image-container">
                <img
                  src={dream.image_url.startsWith('http') 
                    ? dream.image_url 
                    : `http://localhost:8000${dream.image_url}`}
                  alt={dream.prompt}
                  className="dream-image"
                  loading="lazy"
                />
              </div>
              <div className="dream-content">
                <p className="dream-prompt">{dream.prompt}</p>
                <p className="dream-date">{formatDate(dream.created_at)}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;

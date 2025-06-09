import React, { useState } from 'react';

interface AuthDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (token: string) => void;
}

const AuthDialog: React.FC<AuthDialogProps> = ({ isOpen, onClose, onSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const url = isLogin 
        ? 'http://localhost:8000/api/v1/auth/login'
        : 'http://localhost:8000/api/v1/auth/register';

      let response;
      
      if (isLogin) {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        response = await fetch(url, {
          method: 'POST',
          body: formData,
        });
      } else {
        response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Authentication failed');
      }

      const data = await response.json();
      
      if (isLogin) {
        localStorage.setItem('token', data.access_token);
        onSuccess(data.access_token);
      } else {
        setIsLogin(true);
        setPassword('');
        setError('Registration successful! Please log in.');
        return;
      }
      
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="auth-modal-overlay">
      <div className="auth-modal">
        <button className="auth-modal-close" onClick={onClose}>×</button>
        
        <div className="auth-modal-header">
          <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
          <p>{isLogin ? 'Sign in to save your dreams' : 'Join us to save your dream gallery'}</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="form-input"
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
              placeholder="Enter your password"
              minLength={6}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading} className="auth-submit-btn">
            {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
          </button>
        </form>

        <div className="auth-toggle">
          {isLogin ? (
            <p>
              Don't have an account?{' '}
              <button 
                type="button" 
                onClick={() => setIsLogin(false)}
                className="auth-toggle-btn"
              >
                Sign up
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <button 
                type="button" 
                onClick={() => setIsLogin(true)}
                className="auth-toggle-btn"
              >
                Sign in
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthDialog; 
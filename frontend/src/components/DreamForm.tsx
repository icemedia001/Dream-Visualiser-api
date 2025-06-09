import React, { useState } from 'react';
import { apiService } from '../services/api';

interface GeneratedImage {
  id: number;
  prompt: string;
  image_url: string;
  created_at: string;
}

interface DreamFormProps {
  onDreamGenerated: (image: GeneratedImage) => void;
  token: string | null;
}

export default function DreamForm({ onDreamGenerated, token }: DreamFormProps) {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a dream description');
      return;
    }

    if (prompt.length > 500) {
      setError('Dream description must be 500 characters or less');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      console.log('🚀 Submitting dream prompt:', prompt.trim());
      const response = await apiService.generateDream({ prompt: prompt.trim() }, token);
      console.log('🎉 Dream generation successful:', response);
      console.log('📍 Image URL received:', response.image_url);
      onDreamGenerated(response);
      setPrompt('');
    } catch (err) {
      console.error('💥 Dream generation failed:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate dream');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="dream-form">
        <div className="form-field">
          <label htmlFor="dream-prompt" className="form-label">
            Describe your dream...
          </label>
          <textarea
            id="dream-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="A mystical forest with glowing mushrooms, where butterflies made of starlight dance between ancient trees under a purple moon..."
            className="input-primary dream-textarea"
            disabled={isLoading}
            maxLength={500}
          />
          <div className={`character-count ${
            prompt.length > 450 ? 'character-count-warning' : ''
          }`}>
            {prompt.length}/500
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading || !prompt.trim() || prompt.length > 500}
          className={`btn-primary submit-button ${
            isLoading ? 'loading' : ''
          }`}
        >
          {isLoading ? (
            <div className="loading-content">
              <div className="loading-spinner"></div>
              <span>Visualizing your dream...</span>
            </div>
          ) : (
            'Transform Dream into Art'
          )}
        </button>
      </form>
    </div>
  );
} 
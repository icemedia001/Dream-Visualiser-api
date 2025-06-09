import React, { useState } from 'react';
import { apiService } from '../services/api';

interface DreamFormProps {
  onDreamGenerated: (imageUrl: string, prompt: string) => void;
}

export default function DreamForm({ onDreamGenerated }: DreamFormProps) {
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
      const response = await apiService.generateDream({ prompt: prompt.trim() });
      onDreamGenerated(response.image_url, prompt);
      setPrompt('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate dream');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative">
          <label htmlFor="dream-prompt" className="block text-lg font-medium text-white mb-3">
            Describe your dream...
          </label>
          <textarea
            id="dream-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="A mystical forest with glowing mushrooms, where butterflies made of starlight dance between ancient trees under a purple moon..."
            className="input-primary w-full h-32 resize-none"
            disabled={isLoading}
            maxLength={500}
          />
          <div className={`absolute bottom-3 right-3 text-sm ${
            prompt.length > 450 ? 'text-yellow-400' : 'text-gray-400'
          }`}>
            {prompt.length}/500
          </div>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-red-200">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading || !prompt.trim() || prompt.length > 500}
          className={`btn-primary w-full text-lg py-4 ${
            isLoading ? 'opacity-75 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-3">
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
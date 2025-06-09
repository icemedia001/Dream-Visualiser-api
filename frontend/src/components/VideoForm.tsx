import React, { useState } from 'react';
import type { VideoRequest } from '../services/api';

interface VideoFormProps {
  onSubmit: (request: VideoRequest) => void;
  isLoading: boolean;
}

const VideoForm: React.FC<VideoFormProps> = ({ onSubmit, isLoading }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onSubmit({ prompt: prompt.trim() });
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">🎬 AI Video Generator</h2>
        <p className="text-gray-600">
          Transform your ideas into animated videos using AI
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="video-prompt" className="block text-sm font-medium text-gray-700 mb-2">
            Describe your video scene:
          </label>
          <textarea
            id="video-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., A peaceful sunset over a calm ocean with gentle waves..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            rows={4}
            disabled={isLoading}
            maxLength={500}
          />
          <div className="text-right text-sm text-gray-500 mt-1">
            {prompt.length}/500 characters
          </div>
        </div>

        <button
          type="submit"
          disabled={!prompt.trim() || isLoading}
          className={`w-full py-3 px-6 rounded-lg font-medium transition-all duration-200 ${
            !prompt.trim() || isLoading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-purple-600 text-white hover:bg-purple-700 transform hover:scale-105'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Generating Video...
            </div>
          ) : (
            '🎬 Generate Video'
          )}
        </button>
      </form>

      {isLoading && (
        <div className="mt-6 text-center">
          <div className="text-sm text-gray-600 mb-2">
            Creating your AI video... This may take a few moments.
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-purple-600 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoForm; 
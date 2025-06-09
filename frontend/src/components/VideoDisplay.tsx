import React, { useState } from 'react';
import type { VideoResponse } from '../services/api';

interface VideoDisplayProps {
  video: VideoResponse;
  showPrompt?: boolean;
}

const VideoDisplay: React.FC<VideoDisplayProps> = ({ video, showPrompt = true }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const handleVideoLoad = () => {
    setIsLoading(false);
    setHasError(false);
  };

  const handleVideoError = () => {
    setIsLoading(false);
    setHasError(true);
    console.error('Video failed to load:', video.video_url);
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

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="relative">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
              <p className="text-sm text-gray-600">Loading video...</p>
            </div>
          </div>
        )}

        {hasError ? (
          <div className="w-full h-64 bg-gray-100 flex items-center justify-center">
            <div className="text-center">
              <div className="text-red-500 mb-2">⚠️</div>
              <p className="text-sm text-gray-600">Failed to load video</p>
              <p className="text-xs text-gray-500 mt-1">
                URL: {video.video_url}
              </p>
            </div>
          </div>
        ) : (
          <video
            key={video.video_url}
            className="w-full h-auto"
            controls
            loop
            muted
            onLoadedData={handleVideoLoad}
            onError={handleVideoError}
            style={{ minHeight: '256px' }}
          >
            <source src={video.video_url} type="video/mp4" />
            <p className="text-sm text-gray-600 p-4">
              Your browser does not support the video tag.
              <a 
                href={video.video_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-purple-600 hover:underline ml-1"
              >
                Download video
              </a>
            </p>
          </video>
        )}
      </div>

      {showPrompt && (
        <div className="p-4">
          <h3 className="font-semibold text-gray-800 mb-2">Video Prompt:</h3>
          <p className="text-gray-600 text-sm mb-3">{video.prompt}</p>
          
          <div className="flex justify-between items-center text-xs text-gray-500">
            <span>Generated: {formatDate(video.created_at)}</span>
            <span>ID: {video.id}</span>
          </div>

          <div className="mt-3 flex gap-2">
            <a
              href={video.video_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200 transition-colors"
            >
              📱 Open Video
            </a>
            <a
              href={video.video_url}
              download={`ai-video-${video.id}.mp4`}
              className="inline-flex items-center px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              💾 Download
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoDisplay; 
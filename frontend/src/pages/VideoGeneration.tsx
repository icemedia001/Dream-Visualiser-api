import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { apiService } from '../services/api';
import type { VideoRequest, VideoResponse } from '../services/api';
import VideoForm from '../components/VideoForm';
import VideoDisplay from '../components/VideoDisplay';

const VideoGeneration: React.FC = () => {
  const { token } = useAuth();
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<VideoResponse | null>(null);
  const [userVideos, setUserVideos] = useState<VideoResponse[]>([]);
  const [isLoadingVideos, setIsLoadingVideos] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (token) {
      loadUserVideos();
    }
  }, [token]);

  const loadUserVideos = async () => {
    if (!token) return;
    
    setIsLoadingVideos(true);
    setError(null);
    
    try {
      const videos = await apiService.getUserVideos(token);
      setUserVideos(videos);
    } catch (err) {
      console.error('Failed to load user videos:', err);
      setError('Failed to load your videos. Please try again.');
    } finally {
      setIsLoadingVideos(false);
    }
  };

  const handleVideoGeneration = async (request: VideoRequest) => {
    setIsGenerating(true);
    setError(null);
    setGeneratedVideo(null);

    try {
      console.log('🎬 Generating video with prompt:', request.prompt);
      const response = await apiService.generateVideo(request, token);
      console.log('✅ Video generated successfully:', response);
      
      setGeneratedVideo(response);
      
      if (token) {
        await loadUserVideos();
      }
    } catch (err) {
      console.error('Video generation failed:', err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to generate video. Please try again.');
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const clearCurrentVideo = () => {
    setGeneratedVideo(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            AI Video Generation
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform your ideas into stunning AI-generated videos. 
            Describe a scene and watch it come to life.
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column - Video Generation Form */}
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Create Your Video
                </h2>
                
                <VideoForm
                  onSubmit={handleVideoGeneration}
                  isLoading={isGenerating}
                />

                {error && (
                  <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center">
                      <div className="text-red-500 mr-2">⚠️</div>
                      <div>
                        <h4 className="text-red-800 font-medium">Generation Failed</h4>
                        <p className="text-red-700 text-sm mt-1">{error}</p>
                      </div>
                    </div>
                  </div>
                )}

                {isGenerating && (
                  <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
                      <div>
                        <h4 className="text-blue-800 font-medium">Generating Video...</h4>
                        <p className="text-blue-700 text-sm mt-1">
                          This may take a few minutes. Please wait.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* User Guide */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">
                  💡 Tips for Better Videos
                </h3>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-start">
                    <span className="text-purple-500 mr-2">•</span>
                    <span>Be descriptive: "A serene lake at sunset with mountains"</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-purple-500 mr-2">•</span>
                    <span>Include camera movements: "slowly zooming out"</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-purple-500 mr-2">•</span>
                    <span>Specify style: "cinematic", "dreamy", "realistic"</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-purple-500 mr-2">•</span>
                    <span>Keep prompts concise but detailed (50-200 characters)</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Right Column - Generated Video */}
            <div className="space-y-6">
              {generatedVideo && (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-semibold text-gray-800">
                      Your Generated Video
                    </h2>
                    <button
                      onClick={clearCurrentVideo}
                      className="text-gray-500 hover:text-gray-700 text-sm"
                    >
                      Clear ✕
                    </button>
                  </div>
                  <VideoDisplay video={generatedVideo} />
                </div>
              )}

              {!generatedVideo && !isGenerating && (
                <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                  <div className="text-6xl mb-4">🎬</div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    Ready to Create?
                  </h3>
                  <p className="text-gray-600">
                    Enter a prompt to generate your first AI video
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* User Videos Gallery */}
          {token && (
            <div className="mt-12">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-gray-800">
                  Your Video Gallery
                </h2>
                <button
                  onClick={loadUserVideos}
                  disabled={isLoadingVideos}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoadingVideos ? 'Loading...' : 'Refresh'}
                </button>
              </div>

              {isLoadingVideos ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading your videos...</p>
                </div>
              ) : userVideos.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {userVideos.map((video) => (
                    <VideoDisplay
                      key={video.id}
                      video={video}
                      showPrompt={true}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12 bg-white rounded-lg shadow-lg">
                  <div className="text-4xl mb-4">📹</div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    No videos yet
                  </h3>
                  <p className="text-gray-600">
                    Generate your first video to see it here!
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoGeneration; 
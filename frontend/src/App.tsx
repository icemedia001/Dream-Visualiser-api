import { useState, useEffect } from 'react'
import DreamForm from './components/DreamForm'
import ImageGallery from './components/ImageGallery'
import AuthDialog from './components/AuthDialog'
import Dashboard from './components/Dashboard'
import VideoGeneration from './pages/VideoGeneration'
import './styles/globals.css'

interface GeneratedImage {
  id: number;
  prompt: string;
  image_url: string;
  created_at: string;
}

type TabType = 'dreams' | 'videos';

function App() {
  const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([])
  const [isAuthOpen, setIsAuthOpen] = useState(false)
  const [token, setToken] = useState<string | null>(null)
  const [showDashboard, setShowDashboard] = useState(false)
  const [showSavePrompt, setShowSavePrompt] = useState(false)
  const [lastGeneratedImage, setLastGeneratedImage] = useState<GeneratedImage | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('dreams')

  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      setToken(savedToken)
    }
  }, [])

  const handleDreamGenerated = (newImage: GeneratedImage) => {
    setGeneratedImages(prev => [newImage, ...prev])
    setLastGeneratedImage(newImage)
    
    if (!token) {
      setShowSavePrompt(true)
    }
  }

  const handleAuthSuccess = (newToken: string) => {
    setToken(newToken)
    setIsAuthOpen(false)
    setShowSavePrompt(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setShowDashboard(false)
  }

  const handleSavePromptResponse = (shouldSave: boolean) => {
    setShowSavePrompt(false)
    if (shouldSave) {
      setIsAuthOpen(true)
    }
  }

  if (showDashboard && token) {
    return (
      <Dashboard 
        token={token} 
        onLogout={handleLogout}
      />
    )
  }

  const isDreamsTab = activeTab === 'dreams';
  const isVideosTab = activeTab === 'videos';

  if (isVideosTab) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="container mx-auto px-6 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <span className="text-2xl">🧠</span>
                  </div>
                  <h1 className="text-2xl font-bold text-gray-800">Mind's Eye</h1>
                </div>
                
                {/* Tab Navigation */}
                <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
                  <button
                    onClick={() => setActiveTab('dreams')}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      isDreamsTab
                        ? 'bg-white text-purple-600 shadow-sm'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    🎨 Dream Images
                  </button>
                  <button
                    onClick={() => setActiveTab('videos')}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      isVideosTab
                        ? 'bg-white text-purple-600 shadow-sm'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    🎬 Dream Videos
                  </button>
                </div>
              </div>
              
              <div className="space-x-4">
                {token ? (
                  <>
                    <button 
                      onClick={() => setShowDashboard(true)}
                      className="px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors"
                    >
                      My Dreams
                    </button>
                    <button 
                      onClick={handleLogout} 
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                    >
                      Sign Out
                    </button>
                  </>
                ) : (
                  <button 
                    onClick={() => setIsAuthOpen(true)}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                  >
                    Sign In
                  </button>
                )}
              </div>
            </div>
          </div>
        </nav>

        <VideoGeneration />
        
        {/* Auth Dialog */}
        <AuthDialog
          isOpen={isAuthOpen}
          onClose={() => setIsAuthOpen(false)}
          onSuccess={handleAuthSuccess}
        />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-3/4 right-1/4 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-10 flex justify-between items-center p-6">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <span className="text-2xl">🧠</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Mind's Eye</h1>
          </div>
          
          {/* Tab Navigation */}
          <div className="flex space-x-1 bg-white/10 backdrop-blur-sm rounded-lg p-1">
            <button
              onClick={() => setActiveTab('dreams')}
              className={`px-4 py-2 rounded-md transition-colors ${
                isDreamsTab
                  ? 'bg-white/20 text-white shadow-sm'
                  : 'text-white/70 hover:text-white'
              }`}
            >
              🎨 Dream Images
            </button>
            <button
              onClick={() => setActiveTab('videos')}
              className={`px-4 py-2 rounded-md transition-colors ${
                isVideosTab
                  ? 'bg-white/20 text-white shadow-sm'
                  : 'text-white/70 hover:text-white'
              }`}
            >
              🎬 Dream Videos
            </button>
          </div>
        </div>
        
        <div className="space-x-4">
          {token ? (
            <>
              <button 
                onClick={() => setShowDashboard(true)}
                className="btn-secondary"
              >
                My Dreams
              </button>
              <button onClick={handleLogout} className="btn-secondary">
                Sign Out
              </button>
            </>
          ) : (
            <button 
              onClick={() => setIsAuthOpen(true)}
              className="btn-secondary"
            >
              Sign In
        </button>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative z-10 container mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Transform Your Dreams<br />
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Into Visual Art
            </span>
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto mb-12">
            Describe your most vivid dreams and watch as AI brings them to life in stunning, surreal imagery
        </p>
      </div>

        {/* Dream Form */}
        <div className="mb-16">
          <DreamForm 
            onDreamGenerated={handleDreamGenerated}
            token={token}
          />
        </div>

        {/* Generated Images Gallery */}
        {generatedImages.length > 0 && (
          <div className="mb-16">
            <h3 className="text-3xl font-bold text-white mb-8 text-center">Your Dream Gallery</h3>
            <ImageGallery images={generatedImages} />
          </div>
        )}

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="text-center p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🎨</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">AI-Powered Art</h3>
            <p className="text-gray-300">Advanced AI transforms your dream descriptions into breathtaking visual masterpieces</p>
          </div>
          
          <div className="text-center p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">Instant Creation</h3>
            <p className="text-gray-300">Watch your dreams come to life in seconds with our lightning-fast generation</p>
          </div>
          
          <div className="text-center p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">💾</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">Save & Share</h3>
            <p className="text-gray-300">Keep your dream gallery and share your visual stories with the world</p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 text-center text-gray-400 py-8">
        <p>&copy; 2024 Mind's Eye Dream Visualizer. All rights reserved.</p>
      </footer>

      {/* Auth Dialog */}
      <AuthDialog
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onSuccess={handleAuthSuccess}
      />

      {/* Save Prompt Dialog */}
      {showSavePrompt && lastGeneratedImage && (
        <div className="save-prompt-overlay">
          <div className="save-prompt-modal">
            <div className="save-prompt-header">
              <h3>Love this dream?</h3>
              <p>Sign up to save it to your personal gallery!</p>
            </div>
            <div className="save-prompt-preview">
              <img 
                src={lastGeneratedImage.image_url.startsWith('http') 
                  ? lastGeneratedImage.image_url 
                  : `http://localhost:8000${lastGeneratedImage.image_url}`}
                alt={lastGeneratedImage.prompt}
                className="save-prompt-image"
              />
              <p className="save-prompt-text">"{lastGeneratedImage.prompt}"</p>
            </div>
            <div className="save-prompt-actions">
              <button 
                onClick={() => handleSavePromptResponse(true)}
                className="btn-primary"
              >
                Sign Up & Save
              </button>
              <button 
                onClick={() => handleSavePromptResponse(false)}
                className="btn-secondary"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

import { useState } from 'react'
import DreamForm from './components/DreamForm'
import ImageGallery from './components/ImageGallery'

interface GeneratedImage {
  id: string;
  imageUrl: string;
  prompt: string;
  createdAt: string;
}

function App() {
  const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([]);

  const handleDreamGenerated = (imageUrl: string, prompt: string) => {
    const newImage: GeneratedImage = {
      id: Date.now().toString(),
      imageUrl,
      prompt,
      createdAt: new Date().toISOString(),
    };
    setGeneratedImages(prev => [newImage, ...prev]);
  };

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
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
            <span className="text-2xl">🧠</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Mind's Eye</h1>
        </div>
        <div className="space-x-4">
          <button className="btn-secondary">Sign In</button>
          <button className="btn-primary">Sign Up</button>
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
          <DreamForm onDreamGenerated={handleDreamGenerated} />
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
    </div>
  )
}

export default App

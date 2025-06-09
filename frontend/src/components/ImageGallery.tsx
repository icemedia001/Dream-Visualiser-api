import { useState } from 'react';

interface GeneratedImage {
  id: number;
  prompt: string;
  image_url: string;
  created_at: string;
}

interface ImageGalleryProps {
  images: GeneratedImage[];
}

export default function ImageGallery({ images }: ImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<GeneratedImage | null>(null);

  if (images.length === 0) {
    return (
      <div className="empty-gallery">
        <div className="empty-gallery-icon">🎨</div>
        <p className="empty-gallery-title">No dreams visualized yet</p>
        <p className="empty-gallery-subtitle">Generate your first dream image above!</p>
      </div>
    );
  }

  return (
    <>
      <div className="image-gallery-grid">
        {images.map((image) => (
          <div
            key={image.id}
            className="dream-card gallery-card"
            onClick={() => setSelectedImage(image)}
          >
            <div className="gallery-image-container">
              <img
                src={`${image.image_url}?t=${Date.now()}`}
                alt={image.prompt}
                className="gallery-image"
                loading="lazy"
                onError={(e) => {
                  console.error('❌ Failed to load gallery image:', image.image_url);
                  console.error('❌ Full URL attempted:', `${image.image_url}?t=${Date.now()}`);
                  e.currentTarget.style.border = '2px solid red';
                  e.currentTarget.style.backgroundColor = '#ff0000';
                }}
                onLoad={() => {
                  console.log('✅ Successfully loaded gallery image:', image.image_url);
                  console.log('✅ Full URL loaded:', `${image.image_url}?t=${Date.now()}`);
                }}
              />
            </div>
            <div className="gallery-content">
              <p className="gallery-prompt">
                {image.prompt}
              </p>
              <p className="gallery-date">
                {new Date(image.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div
          className="image-modal-overlay"
          onClick={() => setSelectedImage(null)}
        >
          <div
            className="image-modal"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="image-modal-header">
              <button
                onClick={() => setSelectedImage(null)}
                className="image-modal-close"
              >
                ×
              </button>
            </div>
            <div className="image-modal-content">
              <img
                src={`${selectedImage.image_url}?t=${Date.now()}`}
                alt={selectedImage.prompt}
                className="modal-image"
                onError={(e) => {
                  console.error('Failed to load modal image:', selectedImage.image_url);
                  e.currentTarget.style.border = '2px solid red';
                }}
                onLoad={() => {
                  console.log('Successfully loaded modal image:', selectedImage.image_url);
                }}
              />
              <div className="modal-details">
                <h3 className="modal-title">Dream Description</h3>
                <p className="modal-prompt">{selectedImage.prompt}</p>
                <p className="modal-date">
                  Generated on {new Date(selectedImage.created_at).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
} 
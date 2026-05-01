import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiX } from 'react-icons/fi';
import { analysisService } from '../services/analysisService';
import styles from './ImageUploader.module.css';

export function ImageUploader({ onAnalyze, isLoading }) {
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      
      // Validate file
      if (!file.type.startsWith('image/')) {
        setError('Please upload a valid image file');
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
        setError(null);
      };
      reader.readAsDataURL(file);

      // Trigger analysis
      onAnalyze(file);
    }
  }, [onAnalyze]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'] },
    maxSize: 10 * 1024 * 1024,
  });

  const clearPreview = () => {
    setPreview(null);
    setError(null);
  };

  return (
    <div className={styles.container}>
      <div
        {...getRootProps()}
        className={`${styles.dropzone} ${isDragActive ? styles.active : ''} ${
          isLoading ? styles.loading : ''
        }`}
      >
        <input {...getInputProps()} />
        
        {preview && !isLoading ? (
          <div className={styles.preview}>
            <img src={preview} alt="Preview" />
            <button
              className={styles.clearBtn}
              onClick={(e) => {
                e.stopPropagation();
                clearPreview();
              }}
            >
              <FiX />
            </button>
          </div>
        ) : (
          <div className={styles.content}>
            <FiUploadCloud size={48} />
            <h3>Upload UI Screenshot</h3>
            <p>Drag and drop your screenshot here, or click to select a file</p>
            <small>Supported formats: PNG, JPG, GIF, WebP (Max 10MB)</small>
          </div>
        )}

        {isLoading && <div className={styles.spinner} />}
      </div>

      {error && <div className={styles.error}>{error}</div>}
    </div>
  );
}

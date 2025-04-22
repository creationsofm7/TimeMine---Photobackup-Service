import React, { useState } from "react";
import axios from "axios";

const Uploader = () => {
  const [images, setImages] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [token, setToken] = useState("");
  const [uploadProgress, setUploadProgress] = useState<{
    total: number;
    completed: number;
    current: string | null;
    results: Array<{
      file: string;
      status: "success" | "error";
      data?: any;
      error?: string;
    }>;
  }>({
    total: 0,
    completed: 0,
    current: null,
    results: [],
  });

  // Function to handle login and get token
  const handleLogin = async (username : string | null, password : string | null) => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/dj-rest-auth/login/",
        {
          username: username,
          password: password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const authToken = response.data.key;
      setToken(authToken);

      console.log("Login successful, token received");
      return authToken;
    } catch (err) {
      setError("Login failed: " + (err.response?.data?.detail || err.message));
      console.error("Login error:", err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Function to handle file selection
  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setImages(Array.from(e.target.files));
      setError(null);
      setSuccess(false);
      setUploadProgress({
        total: 0,
        completed: 0,
        current: null,
        results: [],
      });
    }
  };

  // Function to upload a single image
  const uploadSingleImage = async (image: File, token: string) => {
    try {
      // Create FormData object to send the image
      const formData = new FormData();
      formData.append("image", image);
      // Add additional fields that the API expects
      formData.append("name", image.name || "Uploaded image");
      formData.append("folder", "1"); // Default folder ID

      // Make the request with the auth token
      const response = await axios.post(
        "http://localhost:8000/api/v1/images/",
        formData,
        {
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Upload successful:", response.data);
      return {
        status: "success" as const,
        data: response.data
      };
    } catch (err) {
      console.error("Upload error:", err);
      
      // If the error is due to an expired token
      if (err.response?.status === 401) {
        setToken("");
        throw new Error("Session expired. Please login again.");
      }

      return {
        status: "error" as const, 
        error: "Upload failed: " + (err.response?.data?.detail || err.message)
      };
    }
  };

  // Function to upload all images
  const uploadImages = async () => {
    if (images.length === 0) {
      setError("Please select images first");
      return;
    }

    if (!token) {
      // You could either show a login form or automatically try to login with stored credentials
      const username = prompt("Enter your username:");
      const password = prompt("Enter your password:");
      const authToken = await handleLogin(username, password);
      if (!authToken) return; // Login failed
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);
      
      // Initialize progress tracker
      setUploadProgress({
        total: images.length,
        completed: 0,
        current: images[0]?.name || null,
        results: []
      });

      // Upload each image sequentially
      for (const image of images) {
        setUploadProgress(prev => ({ 
          ...prev, 
          current: image.name 
        }));

        const result = await uploadSingleImage(image, token);
        
        setUploadProgress(prev => ({
          ...prev,
          completed: prev.completed + 1,
          results: [...prev.results, {
            file: image.name,
            ...result
          }]
        }));
      }

      // All uploads complete
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-md mt-10">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
        Upload Images
      </h2>

      {!token && (
        <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <p className="mb-3 text-gray-700 dark:text-gray-300">
            You need to login first
          </p>
          <button
            onClick={() => {
              const username = prompt("Enter your username:");
              const password = prompt("Enter your password:");
              if (username && password) {
                handleLogin(username, password);
              }
            }}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </div>
      )}

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Select Images
        </label>
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={handleFileChange}
          disabled={loading || !token}
          className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed"
        />
        {images.length > 0 && (
          <p className="mt-2 text-sm text-gray-500">{images.length} image(s) selected</p>
        )}
      </div>

      <button
        onClick={uploadImages}
        disabled={images.length === 0 || loading || !token}
        className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Uploading..." : "Upload Images"}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-md">
          {error}
        </div>
      )}

      {/* Display upload progress */}
      {loading && uploadProgress.total > 0 && (
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-md">
          <h3 className="font-bold mb-2">Upload Progress</h3>
          <p>
            Uploading {uploadProgress.completed} of {uploadProgress.total} images
          </p>
          <p className="text-sm mt-1">Currently uploading: {uploadProgress.current}</p>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ 
                width: `${Math.round((uploadProgress.completed / uploadProgress.total) * 100)}%` 
              }}
            ></div>
          </div>
        </div>
      )}

      {/* Display upload results */}
      {uploadProgress.results.length > 0 && !loading && (
        <div className="mt-4 p-3 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 rounded-md">
          <h3 className="font-bold mb-2">Upload Results</h3>
          <div className="text-sm max-h-64 overflow-y-auto">
            {uploadProgress.results.map((result, idx) => (
              <div 
                key={idx} 
                className={`p-2 mb-2 rounded ${
                  result.status === 'success' 
                    ? 'bg-green-100 dark:bg-green-900/30' 
                    : 'bg-red-100 dark:bg-red-900/30'
                }`}
              >
                <p className="font-medium">{result.file}</p>
                {result.status === 'success' ? (
                  <div className="mt-1">
                    <p className="text-xs">ID: {result.data?.id}</p>
                    {result.data?.image && (
                      <img 
                        src={result.data.image} 
                        alt="Thumbnail" 
                        className="max-h-20 max-w-full mt-2 rounded" 
                      />
                    )}
                  </div>
                ) : (
                  <p className="text-xs text-red-600 dark:text-red-400">{result.error}</p>
                )}
              </div>
            ))}
          </div>
          <div className="mt-2 text-right">
            <p>
              {uploadProgress.results.filter(r => r.status === 'success').length} of {uploadProgress.total} uploads successful
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Uploader;

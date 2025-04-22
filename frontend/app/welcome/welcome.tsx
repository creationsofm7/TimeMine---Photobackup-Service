import { useState } from "react";
import { RowsPhotoAlbum } from "react-photo-album";
import "react-photo-album/rows.css";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Fullscreen from "yet-another-react-lightbox/plugins/fullscreen";
import Slideshow from "yet-another-react-lightbox/plugins/slideshow";
import Thumbnails from "yet-another-react-lightbox/plugins/thumbnails";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import "yet-another-react-lightbox/plugins/thumbnails.css";
import { Image, Video, FolderOpen, Settings } from "lucide-react";
import axios from "axios";
import Cookies from "js-cookie";

// Define the type for your API response
interface ApiPhoto {
  id: number;
  name: string;
  image: string;
  image_height: number | null;
  image_width: number | null;
  is_trashed: boolean;
  trashed_at: string | null;
  is_deleted: boolean;
  deleted_at: string | null;
  is_starred: boolean;
  starred_at: string | null;
  is_encrypted: boolean;
  encrypted_at: string | null;
  is_locked: boolean;
  locked_at: string | null;
  is_protected: boolean;
  protected_at: string | null;
  is_archived: boolean;
  is_shared: boolean;
  folder: number;
}


export function Welcome() {
  const [Log, SetLog] = useState(false);
  const [index, setIndex] = useState(-1);
  const [username, setUsername] = useState("testuser@id.com");
  const [password, setPassword] = useState("123456");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [photos, setPhotos] = useState<any[]>([]);

  // Transform API photos to the format expected by RowsPhotoAlbum
  const transformApiPhotos = (apiPhotos: ApiPhoto[]) => {
    return apiPhotos.map((photo) => ({
      src: photo.image,
      key: `photo-${photo.id}`,
      width: photo.image_width || 1500, // Use default if null
      height: photo.image_height || 1000, // Use default if null
      alt: photo.name,
      title: photo.name,
    }));
  };

  const handleLogin = async () => {
    setIsLoading(true);
    setError("");

    try {
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

      // Handle successful login
      SetLog(true);

      // Store token in cookie instead of localStorage
      // Set cookie to expire in 7 days and with secure attributes when possible
      Cookies.set("authToken", response.data.token, { 
        expires: 7, 
        secure: window.location.protocol === "https:",
        sameSite: "strict" 
      });

      // Fetch images
      fetchImages(response.data.key);
    } catch (err) {
      // Handle error
      console.error("Login failed:", err);
      setError("Invalid credentials or server error");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchImages = (token: string) => {
    axios.get("http://127.0.0.1:8000/api/v1/images/", {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    .then((response) => {
      console.log("Images fetched successfully:", response.data);
      // Transform and set the photos
      const transformedPhotos = transformApiPhotos(response.data);
      setPhotos(transformedPhotos);
    })
    .catch((error) => {
      console.error("Failed to fetch images:", error);
    });
  };

  // Helper function to get token from cookies
  const getAuthToken = () => {
    return Cookies.get("authToken");
  };

  function LoginButton() {
    return (
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white px-2 rounded"
        disabled={isLoading}
      >
        {isLoading ? "Logging in..." : "Login"}
      </button>
    );
  }

  return (
    <main className="flex bg-black h-full">
      <nav className="z-100 p-4 w-full flex justify-between h-1/12 top-0 fixed text-white bg-black backdrop-blur-sm shadow-sm">
        <h2 className="text-4xl">TIMEMINE</h2>
        {Log ? <LogoutButton /> : <LoginButton />}
      </nav>
      <div className="flex flex-row w-full pt-16">
        {/* <div className="z-50 flex flex-col justify-around w-1/6 fixed text-white bg-black backdrop-blur-sm shadow-md left-0 h-screen">
          <div>
            <div className="flex items-center px-6 py-3 text-xl bg-blue-200 text-black rounded-md transition-colors cursor-pointer">
              <Image size={24} className="mr-2" />
              <span>Pictures</span>
            </div>
            <div className="flex items-center px-6 py-3 text-xl hover:bg-gray-200 hover:text-black rounded-md transition-colors cursor-pointer">
              <Video size={24} className="mr-2" />
              <span>Videos</span>
            </div>
            <div className="flex items-center px-6 py-3 text-xl hover:bg-gray-200 hover:text-black rounded-md transition-colors cursor-pointer">
              <FolderOpen size={24} className="mr-2" />
              <span>Albums</span>
            </div>
          </div>
          <div className="flex items-center px-6 py-3 text-xl hover:bg-gray-200 hover:text-black rounded-md transition-colors cursor-pointer">
            <Settings size={24} className="mr-2" />
            <span>Settings</span>
          </div>
        </div> */}
        <div className="w-full overflow-y h-screen p-4 bg-white rounded-t-2xl">
          {/* <div className="flex flex-row gap-4 mb-4 overflow-x-auto">
            {Array.from({ length: 4 }).map((_, index) => (
              <div
                key={`rect-${index}`}
                className="h-40 w-60 bg-gradient-to-br from-purple-800 via-blue-700 to-indigo-900 text-white rounded-2xl flex items-center justify-center shadow-md hover:shadow-lg transition-shadow"
              >
                Moment {index + 1}
              </div>
            ))}
          </div> */}
          
          {photos.length > 0 ? (
            <RowsPhotoAlbum
              photos={photos}
              targetRowHeight={250}
              onClick={({ index }) => setIndex(index)}
              spacing={3}
            />
          ) : (
            <div className="flex items-center justify-center h-screen text-gray-500">
              {Log ? "Loading photos..." : "Login to view your photos"}
            </div>
          )}

          <Lightbox
            slides={photos}
            open={index >= 0}
            index={index}
            close={() => setIndex(-1)}
            plugins={[Fullscreen, Slideshow, Thumbnails, Zoom]}
          />
        </div>
      </div>
      {error && (
        <div className="fixed bottom-4 right-4 bg-red-500 text-white p-2 rounded shadow-lg">
          {error}
        </div>
      )}
    </main>
  );
}

function LogoutButton() {
  const handleLogout = () => {
    // Remove the auth token from cookies when logging out
    Cookies.remove("authToken");
    // Reload the page or redirect to login
    window.location.reload();
  };

  return <button onClick={handleLogout} className="bg-red-500 text-white px-2 rounded">Logout</button>;
}

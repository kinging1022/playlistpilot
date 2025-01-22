<template>
  <div class="w-full min-h-screen bg-black text-white overflow-x-hidden">
    <div class="relative w-full">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-purple-500 rounded-full opacity-10 blur-3xl"></div>
      <div class="absolute top-40 left-1/4 w-[600px] h-[400px] bg-blue-500 rounded-full opacity-10 blur-3xl"></div>
    </div>
    <main class="max-w-6xl mx-auto px-4 py-12 relative min-h-screen flex flex-col items-center justify-center">
      <div class="flex items-center justify-center mb-8">
        <Music class="w-12 h-12 text-green-500 mr-2" />
        <h1 class="text-5xl font-bold">PlaylistPilot</h1>
      </div>
      <div class="text-center max-w-md mx-auto">
        <div v-if="uploadStatus === 'authenticating'" class="scale-in-center">
          <div class="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-8">
            <Check class="w-12 h-12 text-white" />
          </div>
          <h2 class="text-2xl font-bold mb-4">Authentication Successful!</h2>
          <p class="text-gray-400">Preparing to create your playlist...</p>
        </div>
        <div v-else-if="uploadStatus === 'uploading'" class="scale-in-center">
          <div class="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-8">
            <Loader class="w-12 h-12 text-white animate-spin" />
          </div>
          <h2 class="text-2xl font-bold mb-4">Creating Your Playlist</h2>
          <p class="text-gray-400">Uploading to Spotify...</p>
        </div>
        <div v-else-if="uploadStatus === 'success'" class="scale-in-center">
          <div class="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-8">
            <Check class="w-12 h-12 text-white" />
          </div>
          <h2 class="text-2xl font-bold mb-4">Playlist Created!</h2>
          <p class="text-gray-400 mb-8">Your playlist has been successfully uploaded to Spotify.</p>
          <div class="flex justify-center space-x-4">
            <button class="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-full transition-colors" @click="openSpotify">
              Open Spotify
            </button>
            <button class="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-full transition-colors" @click="goHome">
              Go Back Home
            </button>
          </div>
        </div>
        <div v-else-if="uploadStatus === 'error'" class="scale-in-center">
          <div class="w-20 h-20 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-8">
            <XCircle class="w-12 h-12 text-white" />
          </div>
          <h2 class="text-2xl font-bold mb-4">Error!</h2>
          <p class="text-gray-400">Failed to create your playlist. Please try again.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Check, Loader, Music, XCircle } from 'lucide-vue-next';
import { useSongStore } from "@/stores/songs";
import axios from "axios";
import { useRouter } from 'vue-router';

export default {
  name: "App",
  components: { Check, Loader, Music, XCircle },
  setup() {
    const router = useRouter();
    const songStore = useSongStore();
    const uploadStatus = ref('authenticating');
    const playlistUrl = ref(null);

    const startAuthenticationProcess = () => {
      setTimeout(() => {
        uploadStatus.value = "uploading";
        uploadPlaylist();
      }, 3000);
    };

    const uploadPlaylist = async () => {
      try {
        const response = await axios.post("create_playlist/", {
          song_list: songStore.songs,
          name: songStore.title,
          description: songStore.description,
        }, { withCredentials: true });
        
        if (response.data && response.data.playlist_url) {
          playlistUrl.value = response.data.playlist_url;
          uploadStatus.value = "success";
        } else {
          throw new Error("Invalid response: playlist_url missing");
        }
      } catch (error) {
        console.error(error);
        uploadStatus.value = "error";
      }
    };

    const openSpotify = () => {
      if (playlistUrl.value) {
        window.open(playlistUrl.value, "_blank");
      }
    };

    const goHome = () => {
      router.push('/');
    };

    onMounted(() => {
      startAuthenticationProcess();
    });

    return {
      uploadStatus,
      playlistUrl,
      openSpotify,
      goHome,
    };
  },
};
</script>

<style scoped>
@keyframes scale-in-center {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
.scale-in-center {
  animation: scale-in-center 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}
</style>


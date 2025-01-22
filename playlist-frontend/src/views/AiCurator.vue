<template>
  <div class="w-full min-h-screen bg-black text-white overflow-x-hidden">
    <div class="relative w-full">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-blue-500 rounded-full opacity-10 blur-3xl"></div>
      <div class="absolute top-40 left-1/4 w-[600px] h-[400px] bg-purple-500 rounded-full opacity-10 blur-3xl"></div>
    </div>
    <main class="max-w-4xl mx-auto px-4 py-12 relative">
      <header class="text-center mb-16">
        <div class="flex items-center justify-center mb-4">
          <Sparkles class="w-12 h-12 text-blue-500 mr-2" />
          <h1 class="text-4xl font-bold">AI Curator</h1>
        </div>
        <p class="text-xl text-gray-400">
          Let our AI create the perfect playlist based on your preferences
        </p>
      </header>
      <form @submit.prevent="handleGenerate" class="mb-12">
        <div class="bg-zinc-900 rounded-xl p-8 space-y-6">
          <div>
            <label class="block text-gray-400 mb-2">
              Describe your perfect playlist
            </label>
            <textarea
              v-model="prompt"
              class="w-full bg-zinc-800 rounded-lg p-4 text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="E.g., 'Create a workout playlist with upbeat rock and hip-hop songs from the 2010s'"
              rows="3"
            ></textarea>
          </div>
          <div class="flex items-center gap-4">
            <label class="text-gray-400">Number of songs:</label>
            <div class="flex items-center bg-zinc-800 rounded-lg">
              <button
                type="button"
                @click="decrementSongCount"
                class="p-2 hover:text-blue-500 transition-colors"
              >
                <Minus class="w-5 h-5" />
              </button>
              <span class="w-12 text-center">{{ songCount }}</span>
              <button
                type="button"
                @click="incrementSongCount"
                class="p-2 hover:text-blue-500 transition-colors"
              >
                <Plus class="w-5 h-5" />
              </button>
            </div>
          </div>
          <button
            type="submit"
            :disabled="isGenerating || !prompt"
            class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-700 disabled:cursor-not-allowed text-white px-6 py-3 rounded-full transition-colors flex items-center justify-center gap-2"
          >
            <Loader2 v-if="isGenerating" class="w-5 h-5 animate-spin" />
            <Send v-else class="w-5 h-5" />
            {{ isGenerating ? "Generating..." : "Generate Playlist" }}
          </button>
        </div>
      </form>
      <div v-if="playlist.length > 0" class="bg-zinc-900 rounded-xl p-8">
        <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
          <Music class="w-6 h-6 text-blue-500" />
          Your Curated Playlist
        </h2>
        <div class="space-y-2 mb-6">
          <div
            v-for="(song, index) in playlist"
            :key="index"
            class="flex items-center justify-between bg-zinc-800 rounded-lg p-4 hover:bg-zinc-700 transition-colors group"
          >
            <div class="flex-1">
              <h3 class="font-medium">{{ song.title }}</h3>
              <p class="text-gray-400 text-sm">{{ song.artist }}</p>
            </div>
            <div class="flex items-center gap-4">
              <button
                @click="removeSong(index)"
                class="p-2 text-gray-400 hover:text-red-500 transition-colors rounded-full hover:bg-zinc-600"
              >
                <X class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
        <button
          @click="importToSpotify"
          :disabled="playlist.length === 0"
          class="w-full bg-green-600 hover:bg-green-700 disabled:bg-zinc-700 disabled:cursor-not-allowed text-white px-6 py-3 rounded-full transition-colors flex items-center justify-center gap-2"
        >
          <Music class="w-5 h-5" />
          Import Playlist to Spotify
        </button>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import { useSongStore } from "@/stores/songs";
import { 
  Sparkles, 
  Music, 
  Minus, 
  Plus, 
  Loader2, 
  Send,
  X 
} from 'lucide-vue-next'

export default {
  name: 'PlaylistGenerator',
  components: {
    Sparkles,
    Music,
    Minus,
    Plus,
    Loader2,
    Send,
    X
  },
  data() {
    return {
      prompt: '',
      songCount: 10,
      isGenerating: false,
      playlist: [],
      songStore: useSongStore()
    }
  },
  methods: {
    async handleGenerate() {
      this.isGenerating = true;
      try {
        const response = await axios.get("ai-generator/", {
          params: {
            prompt: this.prompt,
            song_count: this.songCount
          },
        });
        this.playlist = response.data.playlist.map((song, index) => ({
          id: index + 1,
          title: song.title || "Untitled Song",
          artist: song.artist || "Unknown Artist"
        }));
        console.log(this.playlist);
      } catch (error) {
        console.error("Error generating playlist:", error);
        this.playlist = [];
      } finally {
        this.isGenerating = false;
      }
    },
    
    removeSong(index) {
      this.playlist = this.playlist.filter((_, i) => i !== index);
    },
    decrementSongCount() {
      this.songCount = Math.max(1, this.songCount - 1);
    },
    incrementSongCount() {
      this.songCount++;
    },
    async importToSpotify() {
      if (this.playlist.length === 0) {
        alert("Please generate a playlist first.");
        return;
      }

      try {
        const title = `AI Curated: ${this.prompt.slice(0, 50)}...`;
        const description = `AI-generated playlist from playlist pilot based on: ${this.prompt}`;

        this.songStore.addPlaylist(this.playlist, title, description);

        const response = await axios.get('login/',{ withCredentials: true });
        if(response.data && response.data.auth_url){
          window.location.href = response.data.auth_url;
        } else {
          throw new Error('Invalid response: auth_url missing');
        }
      } catch (error) {
        console.error("Failed to import playlist:", error);
        alert("An error occurred while importing the playlist. Please try again.");
      }
    }
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>


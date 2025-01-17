<template>
  <div class="w-full min-h-screen bg-black text-white overflow-x-hidden">
    <div class="relative w-full">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-purple-500 rounded-full opacity-10 blur-3xl animate-pulse"></div>
      <div class="absolute top-40 left-1/4 w-[600px] h-[400px] bg-blue-500 rounded-full opacity-10 blur-3xl animate-pulse"></div>
    </div>
    <main class="max-w-6xl mx-auto px-4 py-12 relative">
      <header class="text-center mb-16">
        <div class="flex items-center justify-center mb-4">
          <Clock class="w-12 h-12 text-purple-500 mr-2 animate-spin-slow" />
          <h1 class="text-4xl font-bold">Time Machine</h1>
        </div>
        <p class="text-xl text-gray-400">
          Travel back in time and rediscover the greatest hits
        </p>
      </header>
      <div class="mb-16">
        <div class="bg-zinc-900/50 rounded-2xl p-8 backdrop-blur-sm transition-all duration-300 hover:bg-zinc-900/60">
          <h2 class="text-2xl font-bold mb-8 text-center">
            Choose Your Date
          </h2>
          <div class="mb-12">
            <div
              class="bg-zinc-800/50 rounded-xl p-6 transition-all duration-300 hover:bg-zinc-800/70 cursor-pointer flex items-center justify-center"
            >
              <Calendar class="w-6 h-6 text-purple-500 mr-2" />
              <input
                type="date"
                :max="maxDate"
                v-model="dateInput"
                class="text-xl font-bold text-purple-500 bg-transparent border-none outline-none cursor-pointer"
              />
            </div>
          </div>
          <div class="grid md:grid-cols-2 gap-8 mb-12">
            <div class="bg-zinc-800/50 rounded-xl p-6 transition-all duration-300 hover:bg-zinc-800/70">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  <Disc class="w-6 h-6 text-purple-500 mr-2" />
                  <h3 class="text-lg font-semibold">Top Charts</h3>
                </div>
                <div class="text-sm text-gray-400">
                  {{ songList.filter(song => song.selected).length }} songs selected
                </div>
              </div>
              <div class="space-y-4">
                <div
                  v-for="(song, index) in songList"
                  :key="song.id"
                  class="flex items-center gap-3 text-gray-400 group animate-fadeIn"
                  :style="{ animationDelay: `${index * 100}ms` }"
                >
                  <button
                    @click="toggleSongSelection(song.id)"
                    class="flex items-center justify-center w-8 h-8 rounded-full transition-all duration-200 hover:bg-purple-500/10"
                  >
                    <CheckCircle2 v-if="song.selected" class="w-5 h-5 text-purple-500" />
                    <Circle v-else class="w-5 h-5 text-gray-500" />
                  </button>
                  <div class="w-8 h-8 bg-zinc-700 rounded-full flex items-center justify-center">
                    {{ index + 1 }}
                  </div>
                  <div
                    :class="['flex-1 transition-opacity duration-200', song.selected ? 'opacity-100' : 'opacity-50']"
                  >
                    <div class="font-medium text-white">
                      {{ song.title }}
                    </div>
                    <div class="text-sm">{{ song.artist }}</div>
                  </div>
                  <button
                    @click="removeSong(song.id)"
                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X class="w-5 h-5 text-red-500 hover:text-red-400" />
                  </button>
                </div>
              </div>
            </div>
            <div class="bg-zinc-800/50 rounded-xl p-6 transition-all duration-300 hover:bg-zinc-800/70">
              <div class="flex items-center mb-4">
                <ListMusic class="w-6 h-6 text-purple-500 mr-2" />
                <h3 class="text-lg font-semibold">Playlist Options</h3>
              </div>
              <div class="space-y-4">
                <div class="flex items-center justify-between text-gray-400">
                  <span>Number of songs</span>
                  <select class="bg-zinc-700 rounded px-3 py-1 transition-colors hover:bg-zinc-600">
                    <option>20 songs</option>
                    <option>30 songs</option>
                    <option>50 songs</option>
                  </select>
                </div>
                <div class="flex items-center justify-between text-gray-400">
                  <span>Include remixes</span>
                  <button class="w-12 h-6 bg-zinc-700 rounded-full relative transition-colors hover:bg-zinc-600">
                    <div class="absolute w-4 h-4 bg-purple-500 rounded-full left-1 top-1"></div>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <button
            @click="handleGenerate"
            :disabled="isLoading"
            class="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-full transition-all flex items-center mx-auto disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
          >
            <Loader v-if="isLoading" class="w-6 h-6 mr-2 animate-spin" />
            <PlayCircle v-else class="w-6 h-6 mr-2" />
            {{ isLoading ? "Generating..." : "Generate Time Machine Playlist" }}
          </button>
        </div>
      </div>
      <footer class="text-center text-gray-400">
        <p>© 2024 PlaylistForge. All rights reserved.</p>
      </footer>
    </main>
  </div>
</template>

<script>
import {
  Clock,
  Disc,
  ListMusic,
  PlayCircle,
  X,
  Loader,
  CheckCircle2,
  Circle,
  Calendar,
} from "lucide-vue-next";

export default {
  components: {
    Clock,
    Disc,
    ListMusic,
    PlayCircle,
    X,
    Loader,
    CheckCircle2,
    Circle,
    Calendar,
  },
  data() {
    return {
      dateInput: "1990-01-01",
      isLoading: false,
      songList: [
        {
          id: 1,
          title: "Nothing Compares 2 U",
          artist: "Sinéad O'Connor",
          selected: true,
        },
        {
          id: 2,
          title: "Vision of Love",
          artist: "Mariah Carey",
          selected: true,
        },
        {
          id: 3,
          title: "Ice Ice Baby",
          artist: "Vanilla Ice",
          selected: true,
        },
        {
          id: 4,
          title: "Hold On",
          artist: "Wilson Phillips",
          selected: true,
        },
      ],
    };
  },
  computed: {
    maxDate() {
      return new Date().toISOString().split("T")[0];
    },
  },
  methods: {
    removeSong(id) {
      this.songList = this.songList.filter((song) => song.id !== id);
    },
    toggleSongSelection(id) {
      this.songList = this.songList.map((song) =>
        song.id === id
          ? {
              ...song,
              selected: !song.selected,
            }
          : song
      );
    },
    handleGenerate() {
      this.isLoading = true;
      setTimeout(() => {
        this.isLoading = false;
      }, 2000);
    },
  },
};
</script>

<style scoped>
.animate-spin-slow {
  animation: spin 3s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

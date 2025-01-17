
<template>
    <div class="w-full min-h-screen bg-black text-white overflow-x-hidden">
      <div class="relative w-full">
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-purple-500 rounded-full opacity-10 blur-3xl"></div>
        <div class="absolute top-40 left-1/4 w-[600px] h-[400px] bg-blue-500 rounded-full opacity-10 blur-3xl"></div>
      </div>
      <main class="max-w-6xl mx-auto px-4 py-12 relative">
        <header class="text-center mb-24">
          <div class="flex items-center justify-center mb-4">
            <Music class="w-12 h-12 text-green-500 mr-2" />
            <h1 class="text-5xl font-bold">PlaylistPilot</h1>
          </div>
          <p class="text-2xl text-gray-400 mb-8">
            Create the perfect playlist, powered by time travel and AI
          </p>
          <div class="flex items-center justify-center gap-4 text-sm text-gray-400">
            <div class="flex items-center">
              <Check class="w-4 h-4 text-green-500 mr-2" />
              <span>100K+ Users</span>
            </div>
            <div class="flex items-center">
              <Check class="w-4 h-4 text-green-500 mr-2" />
              <span>1M+ Playlists Created</span>
            </div>
            <div class="flex items-center">
              <Check class="w-4 h-4 text-green-500 mr-2" />
              <span>user friendly</span>
            </div>
          </div>
        </header>
        <div class="grid md:grid-cols-2 gap-8 mb-24">
          <div class="bg-zinc-900 rounded-xl p-8 hover:bg-zinc-800 transition-colors cursor-pointer group relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-purple-500 opacity-5 rounded-full translate-x-16 -translate-y-16"></div>
            <div class="flex items-center justify-between mb-6">
              <Clock class="w-12 h-12 text-purple-500" />
              <ChevronRight class="w-6 h-6 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            <h2 class="text-2xl font-bold mb-4">Time Machine</h2>
            <p class="text-gray-400 mb-6">
              Travel back in time and generate playlists from Billboard Hot 100
              charts of any era. Rediscover the classics!
            </p>
            <RouterLink to="/time-machine" class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-full transition-colors">
              Create Retro Playlist
            </RouterLink>
          </div>
          <div class="bg-zinc-900 rounded-xl p-8 hover:bg-zinc-800 transition-colors cursor-pointer group relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500 opacity-5 rounded-full translate-x-16 -translate-y-16"></div>
            <div class="flex items-center justify-between mb-6">
              <Sparkles class="w-12 h-12 text-blue-500" />
              <ChevronRight class="w-6 h-6 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            <h2 class="text-2xl font-bold mb-4">AI Curator</h2>
            <p class="text-gray-400 mb-6">
              Let our AI understand your music taste and create the perfect
              playlist tailored just for you.
            </p>
            <RouterLink to="/ai-curator" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-full transition-colors">
              Generate AI Playlist
            </RouterLink>
          </div>
        </div>
        <div class="mb-24">
          <h2 class="text-3xl font-bold text-center mb-12">
            Why Choose PlaylistPilot?
          </h2>
          <div class="grid md:grid-cols-3 gap-8">
            <div class="text-center p-6">
              <div class="bg-zinc-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star class="w-8 h-8 text-yellow-500" />
              </div>
              <h3 class="text-xl font-semibold mb-2">Smart Curation</h3>
              <p class="text-gray-400">
                Advanced algorithms that understand your unique music taste
              </p>
            </div>
            <div class="text-center p-6">
              <div class="bg-zinc-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users class="w-8 h-8 text-green-500" />
              </div>
              <h3 class="text-xl font-semibold mb-2">Community Powered</h3>
              <p class="text-gray-400">
                Join thousands of music lovers discovering new tracks daily
              </p>
            </div>
            <div class="text-center p-6">
              <div class="bg-zinc-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Headphones class="w-8 h-8 text-purple-500" />
              </div>
              <h3 class="text-xl font-semibold mb-2">Perfect Match</h3>
              <p class="text-gray-400">
                Get playlists that match your mood and preferences
              </p>
            </div>
          </div>
        </div>
        <div class="mb-24">
          <h2 class="text-3xl font-bold text-center mb-12">
            What Our Users Say
          </h2>
          <div class="grid md:grid-cols-2 gap-8">
            <div class="bg-zinc-900 p-6 rounded-xl">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-purple-500 rounded-full mr-4"></div>
                <div>
                  <h4 class="font-semibold">Sarah K.</h4>
                  <div class="flex text-yellow-500">
                    <Star v-for="i in 5" :key="i" class="w-4 h-4 fill-current" />
                  </div>
                </div>
              </div>
              <p class="text-gray-400">
                "The Time Machine feature helped me create the perfect 90s
                playlist for my party!"
              </p>
            </div>
            <div class="bg-zinc-900 p-6 rounded-xl">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-blue-500 rounded-full mr-4"></div>
                <div>
                  <h4 class="font-semibold">Mike R.</h4>
                  <div class="flex text-yellow-500">
                    <Star v-for="i in 5" :key="i" class="w-4 h-4 fill-current" />
                  </div>
                </div>
              </div>
              <p class="text-gray-400">
                "AI Curator understands my taste better than my friends do!
                Incredible recommendations."
              </p>
            </div>
          </div>
        </div>
        <div class="text-center bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded-2xl p-12 mb-16">
          <h2 class="text-3xl font-bold mb-4">
            Ready to Transform Your Music Experience?
          </h2>
          <p class="text-gray-400 mb-8">
            Connect with Spotify and start creating amazing playlists today
          </p>
          <button class="bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-full transition-colors flex items-center mx-auto">
            <PlayCircle class="w-6 h-6 mr-2" />
            Get Started Now
          </button>
        </div>
        <footer class="text-center text-gray-400">
          <p>© {{ currentYear }} PlaylistForge. All rights reserved.</p>
        </footer>
      </main>
    </div>
  </template>
  
  <script>
  import { RouterLink } from 'vue-router'
  import { 
    Clock,
    Sparkles,
    Music,
    ChevronRight,
    Star,
    Users,
    Headphones,
    PlayCircle,
    Check
  } from 'lucide-vue-next'
  
  export default {
    name: 'App',
    components: {
      Clock,
      Sparkles,
      Music,
      ChevronRight,
      Star,
      Users,
      Headphones,
      PlayCircle,
      Check
    },
    data() {
      return {
        currentYear: new Date().getFullYear()
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>
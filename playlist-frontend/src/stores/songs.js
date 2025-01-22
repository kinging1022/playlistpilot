import { defineStore } from 'pinia';

export const useSongStore = defineStore('song', {
    state: () => ({
        songs: JSON.parse(localStorage.getItem('songItems') || '[]'),
        title: localStorage.getItem('title') || null,
        description: localStorage.getItem('description') || null,
    }),
    actions: {
        addPlaylist(song_list, title, description) {
            if (!Array.isArray(song_list)) {
                throw new Error('song_list must be an array');
            }
            if (typeof title !== 'string' || typeof description !== 'string') {
                throw new Error('title and description must be strings');
            }

            this.songs = song_list;
            this.title = title;
            this.description = description;
            this.savePlaylist();
        },
        clearPlaylist() {
            this.songs = [];
            this.title = null;
            this.description = null;
            ['songItems', 'title', 'description'].forEach(key => localStorage.removeItem(key));
        },
        savePlaylist() {
            localStorage.setItem('songItems', JSON.stringify(this.songs));
            localStorage.setItem('title', this.title);
            localStorage.setItem('description', this.description);
        },
    },
});

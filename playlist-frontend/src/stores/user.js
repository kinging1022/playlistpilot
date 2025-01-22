import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user",{
    state: () => ({
        isAuthenticated: false,
        access: null,
        expireAt: null

    }),
    actions: {
        setToken(data){
            this.access = data.access_token;
            const expiresInMs = data.expires_in * 1000; 
            this.expireAt = Date.now() + expiresInMs;
            this.isAuthenticated = true;
            this.saveUserToLocalStorage()
            
        },
        removeToken() {
            this.isAuthenticated = false;
            this.access = null;
            this.expireIn = null;
            this.saveUserToLocalStorage()
        },
        
        checkTokenValidity(){
            if (Date.now() === this.expireAt){
                this.removeToken()
                this.initiateSpotifyLogin
            }


        },

        async initiateSpotifyLogin() {
            try{
                const response = await axios.get('spotify-login/')
                window.location.href = response.data.auth_url

            }catch(error){
                console.error('Login failed:', error);
            }

        },

        
        saveUserToLocalStorage(){
            const userData = {
               isAuthenticated: this.isAuthenticated ,
               access: this.access,
               expireIn : this.expireAt
            };
            localStorage.setItem("user", JSON.stringify(userData))
        }
    }
})
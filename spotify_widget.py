# spotify_widget.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from io import BytesIO
import threading
import time
import os
from dotenv import load_dotenv
import webbrowser

# Load environment variables
load_dotenv()

class ModernSpotifyWidget:
    def __init__(self):
        # Initialize Spotify client
        self.init_spotify()
        
        # Create main window
        self.root = tk.Tk()
        self.setup_window()
        
        # Variables
        self.current_track_info = None
        self.album_art_image = None
        self.is_playing = False
        self.update_thread_running = True
        
        # Create UI
        self.create_widgets()
        
        # Start updates
        self.update_display()
        
    def init_spotify(self):
        """Initialize Spotify API client"""
        try:
            # Spotify API credentials - You need to set these up
            client_id = os.getenv("SPOTIFY_CLIENT_ID")
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
            
            if not client_id or not client_secret:
                print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file")
                self.sp = None
                return
                
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri="http://127.0.0.1:8888/callback",
                scope="user-read-currently-playing user-read-playback-state user-modify-playback-state",
                cache_path=".spotify_cache"
            ))
            print("✓ Spotify connected successfully")
        except Exception as e:
            print(f"✗ Failed to connect to Spotify: {e}")
            self.sp = None
    
    def setup_window(self):
        """Configure the main window"""
        # self.root.overrideredirect(True) # removes title bar and borders/ makes it disappear when tabbed out
        # self.root.
        self.root.attributes("-transparentcolor", "#0f0f0f")
        self.root.configure(bg='#0f0f0f')
        
        # Window size
        self.window_width = 400
        self.window_height = 120
        self.root.geometry(f"{self.window_width}x{self.window_height}+100+100")
        
        # Make window draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<ButtonRelease-1>', self.stop_move)
        self.root.bind('<B1-Motion>', self.do_move)
        
        # Add right-click menu
        self.create_context_menu()
    
    # we'll have this just in case
    def create_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Play/Pause", command=self.toggle_playback)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Next Track", command=self.next_track)
        self.context_menu.add_command(label="Previous Track", command=self.previous_track)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Close Widget", command=self.quit)
        
        self.root.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        """Display context menu"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def stop_move(self, event):
        self.x = None
        self.y = None
    
    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create all UI elements"""
        # Main frame with rounded corners (using custom styling)
        self.main_frame = tk.Frame(self.root, bg=self.root.cget('bg'), highlightthickness=0)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Left side - Album art placeholder
        self.album_art_label = tk.Label(self.main_frame, bg=self.main_frame.cget('bg'))
        self.album_art_label.pack(side='left', padx=(10, 5), pady=10)
        
        # Right side - Song info frame
        self.info_frame = tk.Frame(self.main_frame, bg=self.main_frame.cget('bg'))
        self.info_frame.pack(side='left', fill='both', expand=True, padx=(0, 10), pady=10)
        
        # Song title
        self.song_title_label = tk.Label(
            self.info_frame,
            text="Not Playing",
            font=("Helvetica", 12, "bold"),
            bg=self.info_frame.cget('bg'),
            fg="#44e95f",
            anchor='w'
        )
        self.song_title_label.pack(anchor='w', pady=(0, 1))
        
        # Artist name
        self.artist_label = tk.Label(
            self.info_frame,
            text="No song playing",
            font=("Helvetica", 10),
            bg=self.info_frame.cget('bg'),
            fg="#e0e0e0",
            anchor='w'
        )
        self.artist_label.pack(anchor='w', pady=(0, 2.5))

        
        # Progress bar
        self.progress_frame = tk.Frame(self.info_frame, bg=self.info_frame.cget('bg'))
        self.progress_frame.pack(anchor='w', fill='x', pady=(5, 0))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=250,
            mode='determinate',
            style='Spotify.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(side='left', fill='x', expand=True)
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Spotify.Horizontal.TProgressbar",
                       background='#1db954',
                       troughcolor='#404040',
                       bordercolor='#1a1a1a',
                       lightcolor='#1db954',
                       darkcolor='#1db954')
        
        # Time labels
        self.time_frame = tk.Frame(self.info_frame, bg='#1a1a1a')
        self.time_frame.pack(anchor='w', fill='x', pady=(2, 0))
        
        self.current_time_label = tk.Label(
            self.time_frame,
            text="0:00",
            font=("Helvetica", 8),
            bg='#1a1a1a',
            fg='#b3b3b3'
        )
        self.current_time_label.pack(side='left')
        
        self.total_time_label = tk.Label(
            self.time_frame,
            text="0:00",
            font=("Helvetica", 8),
            bg='#1a1a1a',
            fg='#b3b3b3'
        )
        self.total_time_label.pack(side='right')
        
        # Playback controls
        self.controls_frame = tk.Frame(self.info_frame, bg='#1a1a1a')
        self.controls_frame.pack(anchor='w', pady=(10, 0))
        
        # Control buttons (using text for simplicity, you can use emojis or custom images)
        self.prev_button = tk.Button(
            self.controls_frame,
            text="⏮",
            command=self.previous_track,
            bg='#1a1a1a',
            fg='#ffffff',
            font=("Helvetica", 12),
            relief='flat',
            activebackground="#333333",
            activeforeground='#1db954'
        )
        self.prev_button.pack(side='left', padx=(0, 10))
        
        self.play_pause_button = tk.Button(
            self.controls_frame,
            text="▶",
            command=self.toggle_playback,
            bg='#1a1a1a',
            fg='#1db954',
            font=("Helvetica", 14, "bold"),
            relief='flat',
            activebackground="#990F0F",
            activeforeground='#1db954'
        )
        self.play_pause_button.pack(side='left', padx=(0, 10))  
        
        self.next_button = tk.Button(
            self.controls_frame,
            text="⏭",
            command=self.next_track,
            bg='#1a1a1a',
            fg='#ffffff',
            font=("Helvetica", 12),
            relief='flat',
            activebackground='#333333',
            activeforeground='#1db954'
        )
        self.next_button.pack(side='left')
    
        # Status indicator
        self.status_label = tk.Label(
            self.info_frame,
            text="● Live",
            font=("Helvetica", 7),
            bg='#1a1a1a',
            fg='#1db954',
            anchor='w'
        )
        self.status_label.pack(anchor='w', pady=(5, 0))


    
    def get_album_art(self, url):
        """Download and resize album art"""
        try:
            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content))
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            
            # Create circular mask for album art
            mask = Image.new('L', (80, 80), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 80, 80), fill=255)
            
            # Apply mask
            output = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
            output.paste(img, (0, 0))
            output.putalpha(mask)
            
            return ImageTk.PhotoImage(output)
        except Exception as e:
            print(f"Error loading album art: {e}")
            return None
    
    def get_current_playback(self):
        """Get current playback information from Spotify"""
        if not self.sp:
            return None
            
        try:
            playback = self.sp.current_playback()
            if playback and playback.get('is_playing'):
                return playback
            return None
        except Exception as e:
            print(f"Error getting playback: {e}")
            return None
    
    def toggle_playback(self):
        """Toggle play/pause"""
        if not self.sp:
            return
            
        try:
            if self.is_playing:
                self.sp.pause_playback()
                self.play_pause_button.config(text="▶")
                self.is_playing = False
            else:
                self.sp.start_playback()
                self.play_pause_button.config(text="⏸")
                self.is_playing = True
        except Exception as e:
            print(f"Error toggling playback: {e}")
    
    def next_track(self):
        """Skip to next track"""
        if self.sp:
            try:
                self.sp.next_track()
                time.sleep(0.5)  # Wait for Spotify to update
                self.update_display()
            except Exception as e:
                print(f"Error skipping track: {e}")
    
    def previous_track(self):
        """Go to previous track"""
        if self.sp:
            try:
                self.sp.previous_track()
                time.sleep(0.5)
                self.update_display()
            except Exception as e:
                print(f"Error going to previous track: {e}")
    
    def update_display(self):
        """Update the widget display with current song info"""
        if not self.sp:
            self.song_title_label.config(text="Spotify Not Connected")
            self.artist_label.config(text="Check your credentials in .env file")
            self.root.after(5000, self.update_display)
            return
        
        playback = self.get_current_playback()
        
        if playback:
            track = playback['item']
            self.is_playing = playback['is_playing']
            
            # Update song info
            song_title = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            
            self.song_title_label.config(text=self.truncate_text(song_title, 35))
            self.artist_label.config(text=self.truncate_text(artists, 35))
            
            # Update play/pause button
            if self.is_playing:
                self.play_pause_button.config(text="⏸")
                self.status_label.config(text="● Playing", fg='#1db954')
            else:
                self.play_pause_button.config(text="▶")
                self.status_label.config(text="○ Paused", fg='#ffb74d')
            
            # Update progress bar
            progress_ms = playback['progress_ms']
            duration_ms = track['duration_ms']
            progress_percent = (progress_ms / duration_ms) * 100 if duration_ms > 0 else 0
            
            self.progress_bar['value'] = progress_percent
            
            # Update time labels
            self.current_time_label.config(text=self.format_time(progress_ms))
            self.total_time_label.config(text=self.format_time(duration_ms))
            
            # Update album art
            if track['album']['images']:
                album_art_url = track['album']['images'][0]['url']
                new_art = self.get_album_art(album_art_url)
                if new_art:
                    self.album_art_image = new_art
                    self.album_art_label.config(image=self.album_art_image)
        else:
            # No song playing
            self.song_title_label.config(text="Not Playing")
            self.artist_label.config(text="Start playing on Spotify")
            self.play_pause_button.config(text="▶")
            self.status_label.config(text="○ Idle", fg='#888888')
            self.progress_bar['value'] = 0
            self.current_time_label.config(text="0:00")
            self.total_time_label.config(text="0:00")
            
            # Set default album art
            default_art = self.create_default_art()
            if default_art:
                self.album_art_image = default_art
                self.album_art_label.config(image=self.album_art_image)
        
        # Schedule next update
        self.root.after(1000, self.update_display)
    
    def create_default_art(self):
        """Create default album art placeholder"""
        img = Image.new('RGB', (80, 80), color='#333333')
        draw = ImageDraw.Draw(img)
        draw.ellipse((20, 20, 60, 60), fill='#1db954')
        return ImageTk.PhotoImage(img)
    
    def format_time(self, milliseconds):
        """Convert milliseconds to MM:SS format"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def truncate_text(self, text, max_length):
        """Truncate text if too long"""
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text
    
    def quit(self):
        """Quit the application"""
        self.update_thread_running = False
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the widget"""
        self.root.mainloop()

# Create .env template file
def create_env_template():
    """Create a .env template file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""# Spotify API Credentials
                # Get these from: https://developer.spotify.com/dashboard
                SPOTIFY_CLIENT_ID=your_client_id_here
                SPOTIFY_CLIENT_SECRET=your_client_secret_here
                """)
        print("Created .env template file. Please add your Spotify credentials.")
        return False
    return True

if __name__ == "__main__":
    print("🎵 Spotify Widget Starting...")
    
    # Create .env template if needed
    create_env_template()
    
    # Check if credentials are set
    if not os.getenv("SPOTIFY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID") == "your_client_id_here":
        print("\n⚠️  Spotify credentials not configured!")
        print("1. Go to https://developer.spotify.com/dashboard")
        print("2. Create a new app")
        print("3. Add http://localhost:8888/callback to Redirect URIs")
        print("4. Copy your Client ID and Client Secret to the .env file")
        print("\nPress Enter to continue once configured...")
        input()
    
    # Run the widget
    widget = ModernSpotifyWidget()
    widget.run()
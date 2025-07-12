import pygame
import time
import random
import threading

pygame.mixer.init()

# define max number of playing sounds
MAX_SIMULTANEOUS_SOUNDS = 3
play_semaphore = threading.Semaphore(MAX_SIMULTANEOUS_SOUNDS)

sounds = [
  {"file": "fauna/crickets.wav", "min_delay": 0, "max_delay": 100},
  {"file": "fauna/crickets2.wav", "min_delay": 5, "max_delay": 45},
  {"file": "fauna/crickets3.wav", "min_delay": 10, "max_delay": 45},
  {"file": "fauna/crickets4.wav", "min_delay": 15, "max_delay": 130},
  {"file": "fauna/birds.wav", "min_delay": 10, "max_delay": 30},
  {"file": "fauna/cricket.wav", "min_delay": 10, "max_delay": 25},
  {"file": "fauna/cricket2.wav", "min_delay": 5, "max_delay": 60},
  {"file": "fauna/wood-thrush.mp3", "min_delay": 30, "max_delay": 200},
  {"file": "fauna/brown-thrasher.wav", "min_delay": 20, "max_delay": 340},
  {"file": "fauna/rufous-capped-nunlet.mp3", "min_delay": 45, "max_delay": 150},
  {"file": "scape/field.wav", "min_delay": 0, "max_delay": 300},
  {"file": "scape/prairie.wav", "min_delay": 0, "max_delay": 120},
  {"file": "scape/prairie2.wav", "min_delay": 50, "max_delay": 200},
  {"file": "scape/night.wav", "min_delay": 20, "max_delay": 60},
  {"file": "scape/night2.wav", "min_delay": 30, "max_delay": 100},
  {"file": "weather/distant-storm.wav", "min_delay": 100, "max_delay": 300}
]

# play looped sounds
for sound in sounds:
  if sound.get("loop"):
    print(f"playing loop: {sound['file']}")
    s = pygame.mixer.Sound(sound["file"])
    s.play(loops=.1)

# randomly play other sounds, at varying volumes
def play_randomly(sound_file, min_delay, max_delay):
  s = pygame.mixer.Sound(sound_file)
  while True:
    delay = random.uniform(min_delay, max_delay)
    volume = random.uniform(0.25, 0.8)
    time.sleep(delay)

    if not s.get_num_channels():  # prevent overlapping the same sound
      if play_semaphore.acquire(blocking=False):  # limit total concurrent sounds
          print(f"+ playing {sound_file} at volume {volume:.2f}")
          s.set_volume(volume)
          s.play()
                
          # automatically release semaphore when sound finishes
          threading.Timer(s.get_length(), play_semaphore.release).start()
      else:
        print(f"- skipped {sound_file} — too many sounds playing.")
    else:
      print(f"= skipping {sound_file} — already playing.")

# start threads for each non-looping sound
for sound in sounds:
    threading.Thread(
        target=play_randomly,
        args=(sound["file"], sound["min_delay"], sound["max_delay"]),
        daemon=True
    ).start()

# keep running
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  print("exiting.")
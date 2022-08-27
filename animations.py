# from pygmtls v4.0


import pygame

class Animation_group:
  def __init__(self):
    self.animations = []
    
  def get_animations(self, display = True):
    if display == True:
      print(self.animations)
    return self.animations
    
  def set_animations(self, animations):
    self.animations = animations
    
  def add_animation(self, animation_object):
    self.animations.append(animation_object)

  def play_all(self, window, auto_increment_frame):
    for animation in self.animations:
      animation.play(window, auto_increment_frame)
  
  def play(self, animation_object, window,auto_increment_frame):
    animation_object.play(window, auto_increment_frame)
    
  def create_animation(self, x, y, frame_type = "image"):
    self.animations.append(Animation(x, y, frame_type))
    
  def remove_animation(self, animation_object_or_index):
    if isinstance(int, animation_object_or_index):
      self.animations.pop(animation_object_or_index)
    else:
      self.animations.remove(animation_object_or_index)

class Animation:
  def __init__(self, x, y, frame_type = "image"):
    self.initial_x = x
    self.initial_y = y
    self.current_x = x
    self.current_y = y
    self.frames = []
    self.offsets = []
    self.type = frame_type
    self.current = 0
    self.state = "stop"
    
  def start(self):
    self.state = "playing"
    
  def stop(self):
    self.state = "stop"
    
  def set_coords(self, initial_x, initial_y, current_x, current_y):
    self.initial_x = initial_x
    self.initial_y = initial_y
    self.current_x = current_x
    self.current_y = current_y
    
  def get_coords(self, display = True):
    if display == True:
      print("%s, %s" %(self.initial_x, self.initial_y))
    return self.initial_x, self.initial_y
    
  def get_frames(self, display = True):
    if display == True:
      print(self.frames)
    return self.frames
  
  def set_frames(self, frames = []):
    self.frames = frames
    
  def get_offsets(self, display = True):
    if display == True:
      print(self.offsets)
    return self.offsets
  
  def set_offsets(self, offsets = []):
    self.offsets = offsets
    
  def duplicate_frame(self, frame_index, duplication_factor = 2):
    
    # gets the frame and offset
    frame = self.frames[frame_index]
    offset = self.offsets[frame_index]
    
    # gets the current range of frames
    frames = self.frames
    offsets = self.offsets
    
    for _ in range(0, duplication_factor):
      frames.insert(frame_index, frame)
      offsets.insert(frame_index, offset)
      
    self.set_frames(frames)
    self.set_offsets(offsets)
    
  def duplicate_range(self, index_list, duplication_factor = 2):
    
    # reverses the index list to prevent duplicating the incorrect 
    index_list.sort(reverse = True)
    for index in index_list:
      self.duplicate_frame(index, duplication_factor)
    
  def duplicate_all_frames(self, duplication_factor = 2):
    
    self.duplicate_range([x for x in range(0, len(self.frames))], duplication_factor)
    
    # frames = []
    # offsets = []
    # [frames.extend([frame for _ in range(duplication_factor)]) for frame in self.frames]
    # [offsets.extend([offset for _ in range(duplication_factor)]) for offset in self.offsets]
    # self.set_frames(frames)
    # self.set_offsets(offsets)

  def get_current_frame(self, display = True):
    if display == True:
      print(self.current)
    return self.current
  
  def set_current_frame(self, frame):
    self.current = frame
    
  def increment_frame(self):
    self.current += 1
    if self.current >= len(self.frames):
      self.current = 0
  
  def decrement_frame(self):
    self.current -= 1
    if self.current < 0:
      self.current = len(self.frames) - 1
    
  def add_frame(self, image, offset = [0, 0]):
    self.frames.append(image)
    self.offsets.append(offset)
    
  def remove_frame(self, index):
    self.frames.pop(index)
    self.offsets.pop(index)
    
  def play_next_frame(self, window, auto_increment_frame = True, auto_stop = False):
    if self.state == "playing":
      if self.type == "image":
        
        # adjusts image position
        self.current_x += self.offsets[self.current][0]
        self.current_y += self.offsets[self.current][1]
        
        # draws image on screen
        window.blit(self.frames[self.current], (self.current_x, self.current_y))
        
        if auto_stop == True:
          if self.current == len(self.frames) - 1:
            self.stop()
        
        #moves frame forwards by 1
        if auto_increment_frame == True:
          self.increment_frame()
      #if self.type == ""

  def play(self, window, auto_increment_frame, auto_stop = False):
    self.play_next_frame(window, auto_increment_frame, auto_stop)

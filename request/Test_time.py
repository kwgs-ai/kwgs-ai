import pygame
import pygame.mixer
import time
import pygame.mixer
pygame.mixer.init(frequency=44100)
pygame.mixer.music.load("teru-teru.mp3")
pygame.mixer.music.play(1)
time.sleep(3)
pygame.mixer.music.stop()



# def sound():
#     pygame.mixer.init() #初期化
#     pygame.mixer.music.load("teru-teru.mp3") #読み込み
#     pygame.mixer.music.play(1) #再生
#     time.sleep(3)
#     pygame.mixer.music.stop() #終了
#
# if __name__ == '__main__':
#     sound()
# thư viện
import pygame
from os import listdir
import cv2
import numpy as np
from keras.models import  load_model
pygame.init()
clock=pygame.time.Clock()

#tiêu đề và icon
pygame.display.set_caption('Dino Game')
icon = pygame.image.load(r'assets\dinosaur.png')
#cửa sổ game
screen = pygame.display.set_mode((600,300))

#tải hình
bg=pygame.image.load(r'assets\background.jpg')
tree=pygame.image.load(r'assets\tree.png')
dino = pygame.image.load(r'assets\dinosaur.png')
logo=pygame.image.load(r'assets\logo.jpg')
khoa=pygame.image.load(r'assets\khoa.png')
truong=pygame.image.load(r'assets\truong.jpg')

#load âm thanh
sound1=pygame.mixer.Sound(r'sound\tick.wav')
sound2=pygame.mixer.Sound(r'sound\te.wav')

#các biến khởi tạo
score=0 #khởi tạo điểm
hscore=0
bg_x = 0 
bg_y = 0
logo_x = 10 
logo_y = 10
truong_x = 0 
truong_y = 0
khoa_x = 500 
khoa_y = 10
tree_x=550
tree_y = 230
dino_x=0
dino_y = 230
x_def=17 #tốc độ chạy
y_def=20 #tốc độ rơi
jump=False
gameplay=True
stop=False
wait=True

cap = cv2.VideoCapture(0)

# Dinh nghia class
class_name = ['pause','go','nhay','continue']

my_model=load_model(r'cu_chi_project.h5')

#hàm kiểm tra va chạm
def checkvc():
    if dino_hcn.colliderect(tree_hcn):
        pygame.mixer.Sound.play(sound2)
        return False
    else:
        return True
    
#đưa score vào game:
game_font=pygame.font.Font('04B_19.TTF',20)

def score_view():
    if gameplay:
        score_txt=game_font.render(f'score: {int(score)}',True,(255,0,0))
        screen.blit(score_txt,(250,50))
        hscore_txt=game_font.render(f'High score: {int(hscore)}',True,(255,0,0))
        screen.blit(hscore_txt,(350,50))

    else:
        hscore_txt=game_font.render(f'High score: {int(hscore)}',True,(255,0,0))
        screen.blit(hscore_txt,(250,50))
        over_txt=game_font.render(f'Game Over',True,(255,0,0))
        screen.blit(over_txt,(250,200))
        
a=1

#vòng lặp xử lý game
running=True
while running:
    # Capture frame-by-frame

    ret, image_org = cap.read()
    if not ret:
        continue
    image_org = cv2.resize(image_org, dsize=None,fx=0.2,fy=0.4)
    # Resize
    image = image_org.copy()
    image = cv2.resize(image, dsize=(128, 192))
    image = image.astype('float')*1./255
    # Convert to tensor
    image = np.expand_dims(image, axis=0)

    # Predict
    predict = my_model.predict(image)


    # Show image
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 50)
    fontScale = 1.5
    color = (0, 255, 0)
    thickness = 2
    cv2.putText(image_org, class_name[np.argmax(predict)], org, font,
                fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow("Picture", image_org)
    if class_name[np.argmax(predict)] == 'continue': a=1
    if class_name[np.argmax(predict)] == 'go': a=2
    if class_name[np.argmax(predict)] == 'nhay': a=2
    if class_name[np.argmax(predict)] == 'pause': a=4
    print(class_name[np.argmax(predict)])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    if a==2 and gameplay:
        print('nhảy')
        if dino_y==230 and stop==False:
            pygame.mixer.Sound.play(sound1)
            jump=True
    if a==4 and gameplay:
        stop=True
        if wait==False:
            stop_txt=game_font.render(f'PAUSE',True,(255,0,0))
            screen.blit(stop_txt,(250,200))
    if a==1 and gameplay:
        stop=False
    if a==2 and gameplay==False:
        gameplay=True
    print(a)

    if wait:
        truong_hcn=screen.blit(truong,(truong_x,truong_y)) 
        logo_hcn=screen.blit(logo,(logo_x,logo_y))
        khoa_hcn=screen.blit(khoa,(khoa_x,khoa_y))
        begin=game_font.render(f'BEGIN',True,(200,255,150))
        screen.blit(begin,(270,150))
        if a==2:
            wait=False




    elif gameplay and stop==False:
        #hình nền
        bg_hcn=screen.blit(bg,(bg_x,bg_y)) 
        bg2_hcn=screen.blit(bg,(bg_x+600,bg_y))  
        bg_x-=x_def
        if bg_x<=-600: bg_x=0
        #cây
        tree_hcn=screen.blit(tree,(tree_x,tree_y)) 
        tree_x-=x_def
        if tree_x<=-20: tree_x=600
        #khủng long
        dino_hcn=screen.blit(dino,(dino_x,dino_y))  
        if dino_y>80 and jump:
            dino_y-=y_def
        else:
            jump=False
        if dino_y<230 and jump==False:
            dino_y+=y_def
        score+=0.01
        if hscore<score: hscore=score
        gameplay=checkvc()
        score_view()


    elif gameplay==False:
        #reset game
        score=0
        bg_x = 0 
        bg_y = 0
        tree_x=550
        tree_y = 230
        dino_x=0
        dino_y = 230
        bg_hcn=screen.blit(bg,(bg_x,bg_y)) 
        tree_hcn=screen.blit(tree,(tree_x,tree_y))
        dino_hcn=screen.blit(dino,(dino_x,dino_y)) 
        score_view()

    pygame.display.update()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



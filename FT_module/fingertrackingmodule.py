from unittest import result
import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=0, detectionCon=0.75, trackingCon=0.75):
        mpHands = mp.solutions.hands  # говорим, что хотим распознавать руки
        self.hands = mpHands.Hands(mode, maxHands, complexity, detectionCon, trackingCon)  # характеристики для распознавания
        self.mpDraw = mp.solutions.drawing_utils # инициализация утилиты для рисования
        self.fingertips = [4, 8, 12, 16, 20] # кончики
        self.pointPosition(0)

        def findHands(self, img, draw=False):
            RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.result = self.hands.process(RGB_image)
            img.flags.writeable = True
            if draw:
                    multiLandMarks = result.multi_hand_landmarks  # извлекаем коллекцию (список) найденных рук
                    if multiLandMarks:
                        for idx, handLms in enumerate(multiLandMarks):
                            self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        def findFingersPosition(self, img=None, draw=False):
            mhl = self.resuit.multi_hand_landmarks
            if mhl:
                for idx, handLms in enumerate(mhl):
                    self.pointPostiton[idx] = []
                for lm in handLms.landmark:
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h) 
                    self.position[idx].append((x, y))

            

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while cap.isOpened():  # пока камера "работает"
        success, image = cap.read()  # получение кадра с камеры
        image.flags.writeable = False
        prevTime = time.time()
        if not success:  # если не удалось получить кадр
            print('Не удалось получить кадр с web-камеры')
            continue  # возвращаемся к ближайшему циклу
        image = cv2.flip(image, 1)  # зеркально отражаем изображение
        prevTime = time.time()
        detector.findHands(image)
        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        cv2.putText(image, f"FPS: {fps}", (200, 100), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
        cv2.imshow('web-cam', image)

        if cv2.waitKey(1) & 0xFF == 27:  # Ожидаем нажатие ESC 
                break
main()
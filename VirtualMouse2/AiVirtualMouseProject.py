import cv2
import numpy as np
# import autopy
import HandTrackingModule as htm
import time
import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0) # Ubah dari 1 ke 0 untuk mengatasi error "Camera index out of range"
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1, detectionCon=1, trackCon=1)
# wScr, hScr = autopy.screen.size()
wScr, hScr = pyautogui.size()
# print(wScr, hScr)

while True:
    # 1. Temukan Landmark tangan
    success, img = cap.read()
    if not success:
        continue  # Jika tidak berhasil membaca frame, lanjutkan ke iterasi berikutnya
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Dapatkan ujung jari telunjuk dan jari tengah
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
    
    # 3. Periksa jari mana yang terangkat
    fingers = detector.fingersUp()
    # print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
    (255, 0, 255), 2)
    # 4. Hanya Jari Telunjuk : Mode Gerakan
    if len(fingers) >= 3:
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Konversi Koordinat
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Haluskan Nilai
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
        
            # 7. Gerakkan Mouse
            # autopy.mouse.move(wScr - clocX, clocY)
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        
    # 8. Kedua Jari Telunjuk dan Jari Tengah Terangkat : Mode Klik
    if len(fingers) >= 3:
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Temukan jarak antara jari
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. Klik mouse jika jarak pendek
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                15, (0, 255, 0), cv2.FILLED)
                # autopy.mouse.click()
                pyautogui.click()
        
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Tampilkan
    cv2.imshow("Image", img)
    cv2.waitKey(1)

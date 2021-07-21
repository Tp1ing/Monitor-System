import cv2
import imutils
import numpy as np
from cv2 import getStructuringElement, CAP_OPENCV_MJPEG
from imutils.object_detection import non_max_suppression
from imutils.video import FileVideoStream

def markMovingObject(videoPath):
    cap = cv2.VideoCapture(videoPath)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel = getStructuringElement(cv2.MORPH_RECT, (3, 3))
    vw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    vh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fileName = "D:/test.mp4"
    out = cv2.VideoWriter(fileName, cv2.CAP_ANY,int(cap.get(cv2.CAP_PROP_FOURCC)), fps, (int(vw),int(vh)), True)
    while True:
        ret, frame = cap.read()
        if ret is True:
            fgmask = fgbg.apply(frame)
            dilate = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            cnts, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)  # 计算轮廓线的外框
                if cv2.contourArea(c) < 2000:  # 计算轮廓面积
                    continue
                #标记移动物体，画矩形方框
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.imshow("frame", frame)
            out.write(frame)
            c = cv2.waitKey(1)
            # 27对应Esc，当点击该键时退出
            if c == 27:
                break
    cap.release()
    cv2.destroyAllWindows()
    return fileName



def drawRectangle(frame,x,y,w,h):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

def imageProcessing(videoPath):

    cap = cv2.VideoCapture(videoPath)  #视频文件
    #使用opencv预置的人体检测与人脸识别的模型
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    #body_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    while True:

        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        (rects, weights) = hog.detectMultiScale(
            gray, winStride=(4, 4), padding=(8, 8), scale=1.05
        )
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #     # apply non-maxima suppression to the bounding boxes using a
        #     # fairly large overlap threshold to try to maintain overlapping
        #     # boxes that are still people
             rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        # show the output images
        #将原图画转换为灰阶图像

        face = face_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(24, 24))
        #body = body_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(30, 30))

        # 在图像中画上矩形框
        '''
        #身体
        for (x, y, w, h) in body:
            #cv2.putText(frame, "body", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            drawRectangle(frame,x, y, w, h)
            print("body ",w,h)
        '''
        #脸
        for (fx, fy, fw, fh) in face:
            cv2.putText(frame, "face", (fx,fy-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 255),1)
            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (0, 0, 255), 1)
            print("face ", fw, fh)

        cv2.imshow("frame", frame)
        #out.write(frame)
        c = cv2.waitKey(1)
        # 27对应Esc，当点击该键时退出
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    video_path = 0#"E:/test2.mp4"
    #fileName = markMovingObject(video_path)
    imageProcessing(video_path)

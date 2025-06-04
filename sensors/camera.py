# sensors/camera.py

import cv2
import torch
from ultralytics import YOLO


class Camera:
    def __init__(self, source=0, model_path="yolo11n.pt"):
        """
        source: источник видео (0 — встроенная камера)
        model_path: путь к модели YOLO
        """
        self.source = source
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Используется устройство: {self.device.upper()}")

        # Загружаем модель и отправляем её на нужное устройство
        self.model = YOLO(model_path).to(self.device)

        # Подключаем камеру
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Не удалось открыть камеру по источнику {self.source}")

        # Устанавливаем разрешение
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def detect_people(self):
        """
        Обнаруживает людей на текущем кадре.
        Возвращает количество людей и кадр.
        """
        ret, frame = self.cap.read()
        if not ret:
            print("Ошибка захвата кадра")
            return 0, frame

        results = self.model(frame, verbose=False)  # verbose=False скрывает логи
        people_count = 0

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls)
                if cls == 0:  # 0 — это класс "person"
                    people_count += 1

        return people_count, frame

    def show_video_with_boxes(self):
        """
        Отображает видеопоток с рамками вокруг людей.
        Выполняет полную детекцию и отрисовку.
        Возвращает количество людей и кадр.
        """
        # Получаем только количество людей и кадр
        people_count, frame = self.detect_people()

        # Теперь делаем детекцию заново, но уже сохраняем боксы
        results = self.model(frame, verbose=False)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls)
                if cls == 0:
                    xyxy = box.xyxy[0].cpu().numpy().astype(int)
                    cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                    cv2.putText(frame, 'Person', (xyxy[0], xyxy[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Показываем количество людей на экране
        cv2.putText(frame, f"People: {people_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Уменьшаем кадр для вывода
        display_frame = cv2.resize(frame, (640, 480))
        cv2.imshow("Camera Feed", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            raise StopIteration("Пользователь прервал показ видео")

        return people_count, frame

    def release(self):
        """Освобождает ресурсы камеры"""
        self.cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.release()
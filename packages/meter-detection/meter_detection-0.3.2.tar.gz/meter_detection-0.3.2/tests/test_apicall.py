import cv2

from meter_detection.apicall import Detector


def test_apicall():
  detector = Detector("./resources/detection.keras")
  detector.detect("./resources/pics/test.jpg")


def test_apicall_np():
  detector = Detector("./resources/detection.keras")
  img = cv2.imread("./resources/pics/test.jpg")
  detector.detect_np(img)

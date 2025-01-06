from meter_detection.apicall import Detector


def test_apicall():
  detector = Detector("./resources/detection.keras")
  detector.detect("./resources/pics/test.jpg")

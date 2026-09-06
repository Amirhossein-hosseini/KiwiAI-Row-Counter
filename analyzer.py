"""Local kiwi row counter: YOLO detection + ByteTrack + two-container verification."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TrackState:
    seen_first: bool = False
    seen_second: bool = False
    counted: bool = False


@dataclass
class TCV:
    """Counts a track only after it has passed both virtual containers."""
    first_y: float = 0.42
    second_y: float = 0.64
    tracks: dict[int, TrackState] = field(default_factory=dict)

    def update(self, track_id: int, center_y: float, frame_height: int) -> bool:
        position = center_y / frame_height
        state = self.tracks.setdefault(track_id, TrackState())
        if position >= self.first_y:
            state.seen_first = True
        if state.seen_first and position >= self.second_y:
            state.seen_second = True
        if state.seen_second and not state.counted:
            state.counted = True
            return True
        return False


def analyze_video(video_path: str, weights_path: str, output_path: str, progress=None) -> int:
    """Run local YOLO weights. The model must have class 0=kiwifruit, 1=support-post."""
    try:
        import cv2
    except ImportError as error:
        raise RuntimeError("اول requirements.txt را نصب کن.") from error
    if not Path(weights_path).is_file():
        raise FileNotFoundError("فایل وزن YOLOv5m پیدا نشد. بعد از آموزش، مسیر best.pt را انتخاب کن.")
    try:
        from ultralytics import YOLO
    except ImportError as error:
        raise RuntimeError("اول requirements.txt را نصب کن.") from error
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise RuntimeError("ویدئو باز نشد.")
    width, height = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    model, tcv, count, index = YOLO(weights_path), TCV(), 0, 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            result = model.track(frame, persist=True, tracker="bytetrack.yaml", classes=[0, 1], conf=0.25, iou=0.5, verbose=False)[0]
            annotated = result.plot()
            if result.boxes is not None and result.boxes.id is not None:
                ids = result.boxes.id.int().cpu().tolist()
                classes = result.boxes.cls.int().cpu().tolist()
                boxes = result.boxes.xyxy.int().cpu().tolist()
                for track_id, class_id, box in zip(ids, classes, boxes):
                    if class_id == 0 and tcv.update(track_id, (box[1] + box[3]) / 2, height):
                        count += 1
            cv2.putText(annotated, f"Verified count: {count}", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            writer.write(annotated)
            index += 1
            if progress:
                progress(index / total, count)
    finally:
        capture.release(); writer.release()
    return count

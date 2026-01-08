import cv2
import numpy as np

# Store clicked points
points = []
lane_polygons = []

def get_points(event, x, y, flags, param):
    global points, lane_polygons
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point selected: {x}, {y}")

        # Once 4 points are selected, save them as a polygon
        if len(points) == 4:
            lane_polygons.append(np.array(points, dtype=np.int32))
            print(f"Polygon saved: {points}")
            points = []  # Reset for next polygon

# Load video and grab the first frame
cap = cv2.VideoCapture("traffic 1.mp4")
ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read video.")
    exit()

cv2.namedWindow("Select Lanes (Click 4 points per lane, press Q when done)")
cv2.setMouseCallback("Select Lanes (Click 4 points per lane, press Q when done)", get_points)

while True:
    display_frame = frame.copy()

    # Draw current clicked points
    for p in points:
        cv2.circle(display_frame, p, 5, (0, 0, 255), -1)

    # Draw saved polygons
    for poly in lane_polygons:
        cv2.polylines(display_frame, [poly], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imshow("Select Lanes (Click 4 points per lane, press Q when done)", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

print("\nFinal lane polygons:")
for i, poly in enumerate(lane_polygons):
    print(f"vertices{i+1} = np.array({poly.tolist()}, dtype=np.int32)")
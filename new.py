import cv2
import numpy as np
import random

width, height = 1280, 720
out_video = cv2.VideoWriter('synthetic_lanes.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))

left_lane_poly = np.array([(465, 350), (609, 350), (510, 630), (2, 630)], np.int32)
right_lane_poly = np.array([(678, 350), (815, 350), (1203, 630), (743, 630)], np.int32)

# Define lane region bounding boxes for vehicle position generation
left_xmin, left_xmax, left_ymin, left_ymax = 50, 520, 370, 620
right_xmin, right_xmax, right_ymin, right_ymax = 800, 1200, 370, 620

frame_count = 320

# Create a vehicle list: each vehicle is (lane, x, y, color, speed, size)
vehicles = []

# Populate vehicles in each lane
for i in range(7):
    # left lane vehicles
    vehicles.append(['left',
                    random.randint(left_xmin, left_xmax), 
                    random.randint(left_ymin, left_ymax), 
                    (0, 255, 255),  # yellow
                    random.randint(2,4),
                    (60, 30)])
for i in range(6):
    # right lane vehicles
    vehicles.append(['right',
                    random.randint(right_xmin, right_xmax), 
                    random.randint(right_ymin, right_ymax), 
                    (0, 128, 255),  # orange
                    random.randint(3,5),
                    (58, 32)])

for frame_id in range(frame_count):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    # Draw lanes
    cv2.polylines(frame, [left_lane_poly], True, (0, 255, 0), 3)
    cv2.polylines(frame, [right_lane_poly], True, (255, 0, 0), 3)
    cv2.putText(frame, "LEFT LANE", (200, 345), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "RIGHT LANE", (900, 345), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    # Move and draw vehicles
    for i, v in enumerate(vehicles):
        lane, x, y, color, speed, size = v
        if lane == 'left':
            y += speed
            # Loop the vehicle to the top when it gets out of lane region
            if y > left_ymax:
                y = left_ymin
                x = random.randint(left_xmin, left_xmax)
            vehicles[i][2] = y
            vehicles[i][1] = x
        elif lane == 'right':
            y += speed
            if y > right_ymax:
                y = right_ymin
                x = random.randint(right_xmin, right_xmax)
            vehicles[i][2] = y
            vehicles[i][1] = x
        # Draw the vehicle
        cv2.rectangle(frame, (x, y), (x + size[0], y + size[1]), color, -1)
    out_video.write(frame)

out_video.release()

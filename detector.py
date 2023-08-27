import os
import cv2
import numpy as np
import tensorflow as tf

def detectCoins(image_path):
    interpreter = tf.lite.Interpreter(model_path="./model/detect.tflite")
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load the label map into memory
    with open("./model/labelmap.txt", 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Load and preprocess an image
    input_image = cv2.imread(image_path)
    imH, imW, _ = input_image.shape
    rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(rgb_image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    input_data = np.expand_dims(resized_image, axis=0).astype(np.float32)



    input_mean = 127.5
    input_std = 127.5
    float_input = (input_details[0]['dtype'] == np.float32)
    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform object detection
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get detection results
    #boxes = interpreter.get_tensor(output_details[0]['index'])
    #classes = interpreter.get_tensor(output_details[1]['index'])[0]
    #scores = interpreter.get_tensor(output_details[2]['index'])

    boxes = interpreter.get_tensor(output_details[1]['index'])[0]  # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0]  # Confidence of detected objects
    num_detections = int(output_details[3]['index'])

    detections = []
    total_value=0

    print("num_detections: "+str(num_detections))


    # Print detected objects
    for i in range(len(scores)):
        if ((scores[i] > 0.50) and (scores[i] <= 100.0)):
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            cv2.rectangle(input_image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            # Draw label
            object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
            cv2.rectangle(input_image, (xmin, label_ymin - labelSize[1] - 10), (xmin + labelSize[0], label_ymin + baseLine - 10),
                          (255, 255, 255), cv2.FILLED)  # Draw white box to put label text in
            cv2.putText(input_image, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                        2)  # Draw label text

            detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])

            if object_name[1] == "-":
                coin_value = object_name[0]
            else:
                coin_value = object_name[:2]

            total_value = total_value + int(coin_value)

    print(detections)
    print("Total value of coins detected: " + str(total_value))

    # Display the image with bounding boxes
    cv2.imshow('Object Detection', input_image)
    cv2.imwrite("./result.jpg", input_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#path = input("Path to query image: ")
#detectCoins(path)


import os
import cv2
import numpy as np
import tensorflow as tf

def detectCoins(image_path):
    #loading needed files and settings
    interpreter = tf.lite.Interpreter(model_path="./model/detect.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    with open("./model/labelmap.txt", 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    input_image = cv2.imread(image_path)
    imH, imW, _ = input_image.shape
    rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(rgb_image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    input_data = np.expand_dims(resized_image, axis=0).astype(np.float32)

    # floating point correction
    input_mean = 127.5
    input_std = 127.5
    float_input = (input_details[0]['dtype'] == np.float32)
    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # detection
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # get results
    boxes = interpreter.get_tensor(output_details[1]['index'])[0]
    classes = interpreter.get_tensor(output_details[3]['index'])[0]
    scores = interpreter.get_tensor(output_details[0]['index'])[0]
    num_detections = int(output_details[3]['index'])

    detections = []
    total_value=0

    coin_counts = {}

    # Print results
    for i in range(len(scores)):
        if ((scores[i] > 0.50) and (scores[i] <= 100.0)):

            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            cv2.rectangle(input_image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            # Draw
            object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
            cv2.rectangle(input_image, (xmin, label_ymin - labelSize[1] - 10), (xmin + labelSize[0], label_ymin + baseLine - 10),
                          (255, 255, 255), cv2.FILLED)  # Draw white box to put label text in
            cv2.putText(input_image, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                        2)  # Draw label text

            detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])

            # get coin value
            if object_name[1] == "-":
                coin_value = object_name[0]
            else:
                coin_value = object_name[:2]

            total_value = total_value + int(coin_value)

            # update num of coins
            if coin_value in coin_counts:
                coin_counts[coin_value] += 1
            else:
                coin_counts[coin_value] = 1

        # Write .txt file
        with open("./assets/results.txt", "w") as file:
            file.write("Total Value: {}\n".format(total_value))
            file.write("\nCoin Counts:\n")
            for coin_value, count in coin_counts.items():
                file.write("{} denar: {}\n".format(coin_value, count))



    print(detections)
    print("Total value of coins detected: " + str(total_value))

    # save the image with bounding boxes
    cv2.imwrite("./assets/result.png", input_image)



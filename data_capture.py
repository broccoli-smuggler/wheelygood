import cv2

if __name__ == '__main__':
    data_folder = '../darknet/data/chair/'

    cap = cv2.VideoCapture(1)
    start = False
    index = 0
    max_data = 200

    while True:
        r, frame = cap.read()
        cv2.imshow('chair', frame)

        if start:
            cv2.imwrite(data_folder + str(index) + 'chair.jpg', frame)
            index += 1
            if index >= max_data:
                break

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break

        if key & 0xFF == ord('s'):
            start = not start
            print('saving %d' % start)

    # release the capture
    cap.release()
    cv2.destroyAllWindows()

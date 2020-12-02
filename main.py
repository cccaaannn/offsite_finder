import cv2
import numpy as np



def draw_angled_lines(image, points , pts_src = [[283, 239],[410, 241],[309, 644],[606, 619]]):

    pts_src = np.array(pts_src)
    pts_dst = np.array([[0, 0],[image.shape[1], 0],[0, image.shape[0]],[image.shape[1], image.shape[0]]])
    
    # find homography and reverse homography
    h, _ = cv2.findHomography(pts_src, pts_dst)
    h_reversed, _ = cv2.findHomography(pts_dst, pts_src)

    # homography of the selectedpoint
    point = np.array([points[0]], dtype='float32')
    point = np.array([point])    
    pointsOut = cv2.perspectiveTransform(point, h)

    # 2 points needed to draw a line using selected points homographed coordinate construct those two lines
    start_point = (pointsOut[0][0][0], 0)
    end_point = (pointsOut[0][0][0], image.shape[0]) 
    
    # finding those two line points on the original image (not homographed)
    # to do that we find reverse homographs of the points
    start = np.array([start_point], dtype='float32')
    start = np.array([start])    
    start = cv2.perspectiveTransform(start, h_reversed)
    
    end = np.array([end_point], dtype='float32')
    end = np.array([end])    
    end = cv2.perspectiveTransform(end, h_reversed)


    # convert to tuple line takes tuple
    start_tuple = (int(start[0][0][0]),int(start[0][0][1]))
    end_tuple = (int(end[0][0][0]),int(end[0][0][1]))
    cv2.line(image, start_tuple, end_tuple, (0, 255, 0), 3) 

    return image

def show_homographed_image(image_path, pts_src):

    im_src = cv2.imread(image_path)

    pts_src = np.array(pts_src)
 
    pts_dst = np.array([[0, 0],[im_src.shape[1], 0],[0, im_src.shape[0]],[im_src.shape[1], im_src.shape[0]]])

    h, status = cv2.findHomography(pts_src, pts_dst)

    im_out = cv2.warpPerspective(im_src, h, (im_src.shape[1],im_src.shape[0]))
        
    cv2.imshow("Warped Source Image", im_out)

def find_distance(image, points, field_size, pts_src = [[283, 239],[410, 241],[309, 644],[606, 619]]):

    pts_src = np.array(pts_src)
    pts_dst = np.array([[0, 0],[image.shape[1], 0],[0, image.shape[0]],[image.shape[1], image.shape[0]]])
    


    # find homography and reverse homography
    h, _ = cv2.findHomography(pts_src, pts_dst)
    h_reverse, _ = cv2.findHomography(pts_dst, pts_src)



    # homography of the selectedpoint
    point = np.array([points[0]], dtype='float32')
    point = np.array([point])    
    homographed_first_points = cv2.perspectiveTransform(point, h)

    # 2 points needed to draw a line using selected points homographed coordinate construct those two lines
    start_point = (homographed_first_points[0][0][0], 0)
    end_point = (homographed_first_points[0][0][0], image.shape[0]) 
    
    # finding those two line points on the original image (not homographed)
    # to do that we find reverse homographs of the points
    new_points = np.array([start_point, end_point], dtype='float32')
    new_points = np.array([new_points])    
    new_points = cv2.perspectiveTransform(new_points, h_reverse)

    # convert to tuple line takes tuple
    start_tuple = (int(new_points[0][0][0]),int(new_points[0][0][1]))
    end_tuple = (int(new_points[0][1][0]),int(new_points[0][1][1]))
    image = cv2.line(image, start_tuple, end_tuple, (0, 255, 0), 3) 


    # -----second point------


    # homography of the selectedpoint
    point = np.array([points[1]], dtype='float32')
    point = np.array([point])    
    homographed_second_points = cv2.perspectiveTransform(point, h)

    # 2 points needed to draw a line using selected points homographed coordinate construct those two lines
    start_point2 = (homographed_second_points[0][0][0], 0)
    end_point2 = (homographed_second_points[0][0][0], image.shape[0]) 
    
    # finding those two line points on the original image (not homographed)
    # to do that we find reverse homographs of the points
    new_points = np.array([start_point2, end_point2], dtype='float32')
    new_points = np.array([new_points])    
    new_points = cv2.perspectiveTransform(new_points, h_reverse)


    # convert to tuple line takes tuple
    start_tuple2 = (int(new_points[0][0][0]),int(new_points[0][0][1]))
    end_tuple2 = (int(new_points[0][1][0]),int(new_points[0][1][1]))
    image = cv2.line(image, start_tuple2, end_tuple2, (0, 255, 0), 3) 



    # -----middle connection-----


    # middle connection needs 2 points y coordinate of those 2 points are same and they are middle point of other 2 lines
    middle_connection_y =  int(abs(start_point[1] - end_point[1])/2)
    
    # pixel distance diffrence
    middle_connection_distance_pixel = int(abs(homographed_first_points[0][0][0]-homographed_second_points[0][0][0]))

    # middle connections points are already homographed so only reverse them
    middle_connection_points = np.array([[homographed_first_points[0][0][0], middle_connection_y],[homographed_second_points[0][0][0], middle_connection_y]], dtype='float32')
    middle_connection_points = np.array([middle_connection_points])    
    middle_connection_points = cv2.perspectiveTransform(middle_connection_points, h_reverse)

    start_tuple = (int(middle_connection_points[0][0][0]),int(middle_connection_points[0][0][1]))
    end_tuple = (int(middle_connection_points[0][1][0]),int(middle_connection_points[0][1][1]))
    cv2.line(image, start_tuple, end_tuple, (0, 0, 255), 3) 

    meter_distance = 100/field_size*middle_connection_distance_pixel
    print("pixel distance: {0:.3f}\nmeter distance: {1:.3f}".format(middle_connection_distance_pixel, meter_distance))
    
    # finding the smallest x location for determining starting position of the text
    if(start_tuple[0] < end_tuple[0]):
        text_tuple = start_tuple
    else:
        text_tuple = end_tuple

    cv2.putText(image, "{0:.2f}m".format(meter_distance), text_tuple, cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=2)

    return image


def draw_circle(event,x,y,flags,param):
    if(event == cv2.EVENT_LBUTTONDOWN):
        cv2.circle(image,(x,y),3,(255,0,0),-1)

        points_temp = []
        points_temp.append(x)
        points_temp.append(y)
        points.append(points_temp)
        print("points in memory: {0}".format(points))





image_path = "samples/c.jpg"

image = cv2.imread(image_path)

points = []
cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_circle)
 
while(True):
    cv2.imshow("image", image)
    key = cv2.waitKey(1)

    if(key == ord("1")):
        if(len(points) == 1):
            image = draw_angled_lines(image, points, pts_src=[[344, 113], [738, 102], [174, 655], [1155, 634]])
            points = []
        else:
            print("selected point count is wrong\nclear selected points with c")

    if(key == ord("2")):
        if(len(points) == 4):
            show_homographed_image(image_path, points)
            points = []
        else:
            print("selected point count is wrong\nclear selected points with c")

    if(key == ord("3")):
        if(len(points) == 2):
            image = find_distance(image, points, field_size=5536, pts_src=[[344, 113], [738, 102], [174, 655], [1155, 634]])
            points = []
        else:
            print("selected point count is wrong\nclear selected points with c")

    if(key == ord("4")):
        if(len(points) == 6):
            image = find_distance(image, points[4:], field_size=5536, pts_src=points[:-2])
            points = []
        else:
            print("selected point count is wrong\nclear selected points with c")


    # options
    if(key == ord("r")):
        print("image reloaded")
        image = cv2.imread(image_path)
        points = []
    
    if(key == ord("c")):
        print("points memory is deleted")
        points = []

    if(key == 27):
        break

cv2.destroyAllWindows()

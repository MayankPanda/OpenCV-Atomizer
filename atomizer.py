import cv2
import numpy as np
import math

def calibrate_percentile(line_angles_1,line_angles_2,image_num,data):
    minper=0
    mindiff=1000000
    percentile_vals=np.linspace(0,100,10000)
    for i in percentile_vals:
        val=0
        for j in range(image_num):
            angle_value=data[j]
            line_angles_1_arr=line_angles_1[j]
            line_angles_2_arr=line_angles_2[j]
            val=val+abs(((np.percentile(line_angles_1_arr,i)+np.percentile(line_angles_2_arr,i))/2)-angle_value)
        if(val<mindiff):
            mindiff=val
            minper=i
    return minper

def calibrate_percentile_breakup_length(y_vals,image_num,data):
    percentile_vals=np.linspace(0,100,10000)
    minper=0
    mindiff=10000000
    for i  in percentile_vals:
        val=0
        for j in range(image_num):
            length_value=data[j]
            y_vals_arr=y_vals[j]
            val=val+abs(np.percentile(y_vals_arr,i)-length_value)
        if(val<mindiff):
            mindiff=val
            minper=i
    return minper

def use_config_length(crop_parameter,image_names,length_scaling_factor,breakup_length_parameter):
    y_vals_all=[]
    for i in range(len(image_names)):
        image=cv2.imread(image_names[i])
        crop_coordinate=(int)((crop_parameter/100)*image.shape[0])
        crop = image[crop_coordinate:,:]  
        image=crop
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(grayscale_image, 10, 40)
        lines=cv2.HoughLinesP(canny_edges,1,np.pi/180,20,maxLineGap=40)
        y_vals_individual=[]
        for line in lines:
            x1,y1,x2,y2=line[0]
            y_vals_individual.append((y1+y2)/2)
        y_vals_all.append(y_vals_individual)
    perc=breakup_length_parameter
    for i in range(len(image_names)):
        y_vals_arr=y_vals_all[i]
        print("Image Name: ",image_names[i]," Estimated Breakup Length: (Pixels) ",np.percentile(y_vals_arr,perc)," Estimated Breakup Length : (cm) ",np.percentile(y_vals_arr,perc)/length_scaling_factor)

def test_calibrate_length(crop_parameter,image_names,breakup_length_data_cm,image_names_test,breakup_length_data_cm_test,length_scaling_factor):
    max_prediction_error=0
    breakup_length_data_pixels=[]
    breakup_length_data_pixels_test=[]
    for i in breakup_length_data_cm:
        breakup_length_data_pixels.append(i*length_scaling_factor)
    for i in breakup_length_data_cm_test:
        breakup_length_data_pixels_test.append(i*length_scaling_factor)
    y_vals_all=[]
    for i in range(len(image_names)):
        image=cv2.imread(image_names[i])
        crop_coordinate=(int)((crop_parameter/100)*image.shape[0])
        crop = image[crop_coordinate:,:]  
        image=crop
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(grayscale_image, 10, 40)
        lines=cv2.HoughLinesP(canny_edges,1,np.pi/180,20,maxLineGap=40)
        y_vals_individual=[]
        for line in lines:
            x1,y1,x2,y2=line[0]
            #cv2.line(image,(x1,y1),(x2,y2),(0,255,0),4)
            y_vals_individual.append((y1+y2)/2)
        y_vals_all.append(y_vals_individual)
    perc=calibrate_percentile_breakup_length(y_vals_all,len(image_names),breakup_length_data_pixels)
    for i in range(len(image_names)):
        y_vals_arr=y_vals_all[i]
        estimation_error=abs(np.percentile(y_vals_arr,perc)-breakup_length_data_pixels[i])
        if(estimation_error>max_prediction_error):
            max_prediction_error=estimation_error
        print("Image Name: ",image_names[i]," Estimated Breakup Length: (Pixels) ",np.percentile(y_vals_arr,perc)," Actual Breakup Length: (Pixels)",breakup_length_data_pixels[i])
    for i in range(len(image_names_test)):
        image=cv2.imread(image_names_test[i])
        crop_coordinate=(int)((crop_parameter/100)*image.shape[0])
        crop = image[crop_coordinate:,:]  
        image=crop
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(grayscale_image, 10, 40)
        lines=cv2.HoughLinesP(canny_edges,1,np.pi/180,20,maxLineGap=40)
        y_vals_individual_test=[]
        for line in lines:
            x1,y1,x2,y2=line[0]
            #cv2.line(image,(x1,y1),(x2,y2),(0,255,0),4)
            y_vals_individual_test.append((y1+y2)/2)
        estimation_error=abs(np.percentile(y_vals_individual_test,perc)-breakup_length_data_pixels_test[i])
        if(estimation_error>max_prediction_error):
            max_prediction_error=estimation_error
        print("Image Name: ",image_names_test[i]," Estimated Breakup Length: (Pixels) ",np.percentile(y_vals_individual_test,perc)," Actual Breakup Length: (Pixels) ",breakup_length_data_pixels_test[i])
    print("Max Prediction Error in Pixels:",max_prediction_error)
    print("Max Prediction Error in cm",max_prediction_error/length_scaling_factor)
    return perc

def angle_with_vertical(slope):
    angle = math.atan(slope)
    angle = math.degrees(angle)

    if angle < 0:
        angle += 360

    return angle

def use_config_half_angle(centerline_parameter,crop_parameter,image_names,half_angle_parameter):
    line_type_1_angles_all=[]
    line_type_2_angles_all=[]
    for i in range(len(image_names)):
        image=cv2.imread(image_names[i])
        crop_coordinate=(int)((crop_parameter/100)*image.shape[0])
        crop = image[crop_coordinate:,:]  
        image=crop
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(grayscale_image, 10, 40)
        lines=cv2.HoughLinesP(canny_edges,1,np.pi/180,20,maxLineGap=40)
        line_type_1_angles_individual=[]
        line_type_2_angles_individual=[]
        centerline=(int)((centerline_parameter/100)*image.shape[1])
        for line in lines:
            x1,y1,x2,y2=line[0]
            if(((x2-x1)*(y2-y1))>0)and(min(x1,x2)>centerline):
                slope=(x2-x1)/(y2-y1)
                line_type_1_angles_individual.append((math.degrees(math.atan(slope))))
            if(((x2-x1)*(y2-y1))<0)and(max(x1,x2)<centerline):
                slope=(x1-x2)/(y2-y1)
                line_type_2_angles_individual.append(math.degrees(math.atan(slope)))
        line_type_1_angles_all.append(line_type_1_angles_individual)
        line_type_2_angles_all.append(line_type_2_angles_individual)
    perc=half_angle_parameter
    for i in range(len(image_names)):
        line_type_1_angles_arr=line_type_1_angles_all[i]
        line_type_2_angles_arr=line_type_2_angles_all[i]
        print("Image Name: ",image_names[i]," ","Estimated Half Angle: (Degrees) ",(np.percentile(line_type_1_angles_arr,perc)+np.percentile(line_type_2_angles_arr,perc))/2)

def test_calibration_half_angle(centerline_parameter,crop_parameter,image_names,half_angle_data,image_names_test,half_angle_data_test):
    max_prediction_error=0
    line_type_1_angles_all=[]
    line_type_2_angles_all=[]
    for i in range(len(image_names)):
        image=cv2.imread(image_names[i])
        crop_coordinate=(int)((crop_parameter/100)*image.shape[0])
        crop = image[crop_coordinate:,:]  
        image=crop
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(grayscale_image, 10, 40)
        lines=cv2.HoughLinesP(canny_edges,1,np.pi/180,20,maxLineGap=40)
        line_type_1_angles_individual=[]
        line_type_2_angles_individual=[]
        centerline=(int)((centerline_parameter/100)*image.shape[1])
        for line in lines:
            x1,y1,x2,y2=line[0]
            if(((x2-x1)*(y2-y1))>0)and(min(x1,x2)>centerline):
                slope=(x2-x1)/(y2-y1)
                line_type_1_angles_individual.append((math.degrees(math.atan(slope))))
            if(((x2-x1)*(y2-y1))<0)and(max(x1,x2)<centerline):
                slope=(x1-x2)/(y2-y1)
                line_type_2_angles_individual.append(math.degrees(math.atan(slope)))
        line_type_1_angles_all.append(line_type_1_angles_individual)
        line_type_2_angles_all.append(line_type_2_angles_individual)
    perc=calibrate_percentile(line_type_1_angles_all,line_type_2_angles_all,len(image_names),half_angle_data)
    for i in range(len(image_names)):
        line_type_1_angles_arr=line_type_1_angles_all[i]
        line_type_2_angles_arr=line_type_2_angles_all[i]
        estimation_error=abs((np.percentile(line_type_1_angles_arr,perc)+np.percentile(line_type_2_angles_arr,perc))/2-half_angle_data[i])
        if(estimation_error>max_prediction_error):
            max_prediction_error=estimation_error
        print("Image Name: ",image_names[i]," ","Estimated Half Angle: (Degrees) ",(np.percentile(line_type_1_angles_arr,perc)+np.percentile(line_type_2_angles_arr,perc))/2,"Data: (Degrees) ",half_angle_data[i])
    for i in range(len(image_names_test)):
        image=cv2.imread(image_names[i])
        crop_coordinate=(int)((crop_parameter/100)*image.shape[0])
        crop = image[crop_coordinate:,:]  
        image=crop
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(grayscale_image, 10, 40)
        lines=cv2.HoughLinesP(canny_edges,1,np.pi/180,20,maxLineGap=40)
        line_type_1_angles_individual=[]
        line_type_2_angles_individual=[]
        for line in lines:
            x1,y1,x2,y2=line[0]
            if(((x2-x1)*(y2-y1))>0)and(min(x1,x2)>centerline):
                slope=(x2-x1)/(y2-y1)
                line_type_1_angles_individual.append((math.degrees(math.atan(slope))))
            if(((x2-x1)*(y2-y1))<0)and(max(x1,x2)<centerline):
                slope=(x1-x2)/(y2-y1)
                line_type_2_angles_individual.append(math.degrees(math.atan(slope)))
        estimation_error=abs((np.percentile(line_type_1_angles_individual,perc)+np.percentile(line_type_2_angles_individual,perc))/2-half_angle_data_test[i])
        if(estimation_error>max_prediction_error):
            max_prediction_error=estimation_error
        print("Image Name: ",image_names_test[i]," ","Estimated Half Angle: (Degrees) ",(np.percentile(line_type_1_angles_individual,perc)+np.percentile(line_type_2_angles_individual,perc))/2,"Data: (Degrees) ",half_angle_data_test[i])
    print("Maximum Prediction Error in Degrees: ",max_prediction_error)
    return perc




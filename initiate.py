import set_centreline
import crop_image
import atomizer
import csv
import tempfile
import shutil

crop_parameter=None
centerline_parameter=None
def clear_console():
      print('\r', end='')

def determine_centerline(image_name):
    centerline_parameter=set_centreline.initiate_centerline_calibration(image_name)
    return centerline_parameter

def determine_cropping_parameter(image_name):
    crop_parameter=crop_image.initiate_crop_calibration(image_name)
    return crop_parameter

def calibrate_image(image_name):
    centerline=determine_centerline(image_name)
    crop=determine_cropping_parameter(image_name)
    return centerline,crop

def train_and_test_half_angle(training_image_names,training_image_half_angle_data,test_image_names,test_image_half_angle_data):
    global crop_parameter
    global centerline_parameter
    atomizer.test_calibration_half_angle(centerline_parameter,crop_parameter,training_image_names,training_image_half_angle_data,test_image_names,test_image_half_angle_data)

def train_and_test_breakup_length(training_image_names,training_image_breakup_length_data,test_image_names,test_image_breakup_length_data,length_scaling_factor):
    global crop_parameter
    atomizer.test_calibrate_length(crop_parameter,training_image_names,training_image_breakup_length_data,test_image_names,test_image_breakup_length_data,length_scaling_factor)

def add_row_to_csv(csv_file, config_name, half_angle, breakup_length):
    # Open the CSV file in append mode
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the new row to the CSV file
        writer.writerow([config_name, half_angle, breakup_length])

    print("New row added to the CSV file.")

def create_new_configuration(training_image_names,training_image_half_angle_data,test_image_names,test_image_half_angle_data,training_image_breakup_length_data,test_image_breakup_length_data,length_scaling_factor):
    global crop_parameter
    global centerline_parameter
    breakup_length_parameter=atomizer.test_calibrate_length(crop_parameter,training_image_names,training_image_breakup_length_data,test_image_names,test_image_breakup_length_data,length_scaling_factor)
    half_angle_parameter=atomizer.test_calibration_half_angle(centerline_parameter,crop_parameter,training_image_names,training_image_half_angle_data,test_image_names,test_image_half_angle_data)
    config_name=input("Enter configuration Name:")
    add_row_to_csv("configurations.csv",config_name,half_angle_parameter,breakup_length_parameter)

def list_all_configs():
    config_names = []
    csv_file="configurations.csv"
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            config_name = row[0]  
            config_names.append(config_name)
    for i in config_names:
        print(i)

def get_config_parameters(config_name):
    with open("configurations.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == config_name:
                half_angle = float(row[1])  
                breakup_length = float(row[2])  
                return half_angle, breakup_length
    return None

def delete_config(config_name):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    with open("configurations.csv", mode='r') as file, temp_file:
        reader = csv.reader(file)
        writer = csv.writer(temp_file)

        for row in reader:
            if row[0] != config_name:
                writer.writerow(row)

    shutil.move(temp_file.name, "configurations.csv")
    print(f"Config '{config_name}' deleted from the CSV file.")

def use_config(config_name,training_image_names,length_scaling_factor):
    half_angle_parameter,breakup_length_parameter=get_config_parameters(config_name)
    global crop_parameter
    global centerline_parameter
    atomizer.use_config_length(crop_parameter,training_image_names,length_scaling_factor,breakup_length_parameter)
    atomizer.use_config_half_angle(centerline_parameter,crop_parameter,training_image_names,half_angle_parameter)


    



image_name="DSC_1009.jpg"
centerline_parameter,crop_parameter=calibrate_image(image_name)
training_image_names=["DSC_1009.jpg","DSC_1010.jpg","DSC_1011.jpg","DSC_1012.jpg","DSC_1013.jpg"]
training_image_half_angle_data=[27.01,26.89,26.9,25.6,25.68]
test_image_names=["DSC_1014.jpg","DSC_1015.jpg","DSC_1016.jpg","DSC_1017.jpg"]
test_image_half_angle_data=[25.07,25.94,25.31,26.22]
training_image_breakup_length_data=[11.67,10.07,10.1,9.93,10.14]
test_image_breakup_length_data=[10.89,10.18,9.89,9.46]
length_scaling_factor=156.00
predict_image_names=["DSC_1009.jpg","DSC_1010.jpg","DSC_1011.jpg","DSC_1012.jpg","DSC_1013.jpg","DSC_1014.jpg","DSC_1015.jpg","DSC_1016.jpg","DSC_1017.jpg"]
#create_new_configuration(training_image_names,training_image_half_angle_data,test_image_names,test_image_half_angle_data,training_image_breakup_length_data,test_image_breakup_length_data,length_scaling_factor)
#list_all_configs()
#use_config("gcsc_1",predict_image_names,length_scaling_factor)
train_and_test_breakup_length(training_image_names,training_image_breakup_length_data,test_image_names,test_image_breakup_length_data,length_scaling_factor)
train_and_test_half_angle(training_image_names,training_image_half_angle_data,test_image_names,test_image_half_angle_data)


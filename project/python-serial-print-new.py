import matplotlib.pyplot as plt
import serial # for serial port
import numpy as np # for arrays, numerical processing
import time
import csv

port = '/dev/tty.usbmodem12203'  #For mac
audiodata = []
times = []
folder_path = "/Users/harrisonlee/Code/C programming/UBC PHYS 319/project/"
csv_savename = folder_path + "audiodata.csv"
create_plot = True  # set true to create updating plot


# try:  
#     import IPython
#     shell = IPython.get_ipython()
#     shell.enable_matplotlib(gui='qt')
# except:
#     print("Need to enter '%matplotlib qt' manually in console.")
#     pass

# # initialize figureç
# if create_plot:
#     plt.figure()
#     plt.xlabel("Time (s)")
#     plt.ylabel("ADC output")
#     plt.title("Audio Signal ADC")
#     # plt.ylim(0, 100)

try:
    with serial.Serial(port,9600,timeout = 0.1) as ser:
        print(ser.name)
        print("Flushing serial...")
        ser.flushInput()
        ser.flushOutput()
        print("Flushed")
        start_time = time.time()
        while(1): #loop forever
            data = ser.read(1)
            if len(data) > 0: #was there a byte to read?
                print(ord(data))
                # get current time and save in list
                current_time = time.time()-start_time
                times.append(current_time)
                audiodata.append(ord(data))
            
                # if create_plot:
                #     plt.pause(0.0001)# wait for plot to update (INCREASE IF PLOT ISN'T UPDATING PROPERLY)
                #     plt.clf()  # clear figure
                #     plt.plot(times, audiodata)



#on ctrl-c (in console), save to CSV in specified location
except KeyboardInterrupt:
    create_plot = False
    print("Collection stopped - saving to CSV...")
    startcsv = time.time()
    with open(csv_savename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        rows = zip(times, audiodata)
        for row in rows:
            writer.writerow(row)
    endcsv = time.time()
    print("Data saved to " + csv_savename)
    print("Took " + str(endcsv - startcsv) + " s")
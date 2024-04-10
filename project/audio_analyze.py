import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

folder_path = "/Users/harrisonlee/Code/C programming/UBC PHYS 319/project/"

# import data
def count_peaks(filename):
    print("processing file: {}".format(filename))
    data = np.loadtxt(folder_path+filename, delimiter=',')
    time = data[:, 0]
    power = data[:, 1]

    # print(np.mean(power), np.max(power))
    fs = 1/(time[1]-time[0]) # sampling frequency

    # find peaks
    # peaks, props = find_peaks(power, distance=40, height=50)
    # peaks, props = find_peaks(power, distance=20*fs, height=np.max(power[-100:]))
    peaks, props = find_peaks(power, distance=40, height=np.mean(power)+np.std(power))
    print("time_arr, power_arr length", time.shape, power.shape)
    print("peak array shape", peaks.shape)
    print("fs=" ,fs)
    print("peaks idx", peaks)

    # plot 1: audio data with peaks
    plt.figure(figsize=(12, 6))
    plt.plot(time, power)
    plt.scatter(time[peaks], power[peaks], marker='x', c='red', label="peaks")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("ADC output")
    plt.title("total peaks: {}".format(len(peaks)))
    plt.show()

    # plot 2: performance with total count frequncy
    total_time = time[peaks[-1]] - time[peaks[0]]
    plt.figure(figsize=(12, 6))
    for i, idx in enumerate(peaks):
        counts = i + 1
        plt.scatter(time[idx]-time[peaks[0]], counts, c='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Count')
    if total_time // 60 == 0:
        plt.title("Moshikame Performance, counts: {}, total time: {:.2f} s, frequency = {:.3f} bpm"
                  .format(counts, total_time % 60, counts / total_time * 60))
    else:
        plt.title("Moshikame Performance, counts: {}, total time: {} min {:.2f} s, frequency = {:.3f} bpm"
                  .format(counts, total_time // 60, total_time % 60, counts / total_time * 60))
    plt.show()
    
    return len(peaks)

file1 = "audiodata_approx30_peaks.csv"
file2 = "audiodata_approx100_peaks.csv"
count_peaks(file1)
count_peaks(file2)

file3 = "audiodata43.csv"
file4 = "audiodata8.csv"
count_peaks(file3)
count_peaks(file4)

# count_peaks("audiodata.csv")
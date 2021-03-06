import os, sys, time, subprocess, shutil, re
from distutils.dir_util import copy_tree
import numpy as np


def auto_run():
    path = os.getcwd()
    synth_file = path + os.sep + "scripts" + os.sep + "synth.tcl"

	#TODO: mkdir if not exist
    auto_result_folder = path + os.sep + "auto_result"

    start = 1.0
    end = 100.0
    step = 1
    unit = "MHz"
    run_range = np.arange(start, end, step)

    for i in run_range:
        period = float(1.00 / float(i) * 1000.00)
        print("Running: " + str(i) + unit + " (" + str('%.10f' % period) + "us)")

        o_file = open(synth_file, "r+")
        text = o_file.read()
        o_file.close()

        str_a = "-period"
        str_b = "{clk}"
        new_str = str_a + " " + str('%.10f' % period) + " -waveform {0 " + str('%.10f' % (period / 2.0)) + "} " + str_b

        text_search = text[text.find(str_a):text.rfind(str_b) + len(str_b)]
        new_text = text.replace(text_search, new_str, 1)
        
        # TODO: if mult-thread create file+tailname run run.sh delete file
        # results folder need to be redone

        file = open(synth_file, "wt")
        file.truncate(0)
        file.write(new_text)
        file.flush()
        file.close()

        os.system("tcsh ./run.sh")

        time.sleep(2)
        os.rename("results", "results" + "_" + str(i) + unit)
        os.mkdir("results")
        time.sleep(2)

        # fromDirectory = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
        # toDirectory = os.getcwd() + os.sep + "results"
        # copy_tree(fromDirectory, toDirectory)

        src = os.getcwd() + os.sep + "scripts" + os.sep + "synth.tcl"
        dst = os.getcwd() + os.sep + "results" + "_" + str(i) + unit + os.sep + "synth.tcl"
        shutil.copyfile(src, dst)

        src = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
        dst = auto_result_folder
        shutil.move(src, dst)


def gen_results(folder_path):
    auto_result_folder = folder_path
    dir_list = os.listdir(auto_result_folder)
    dir_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    report_list = []

    for folder in dir_list:
        if ("MHz" in folder or "kHz" in folder) and "_" in folder:
            files = os.listdir(auto_result_folder + os.sep + folder)
            for name in files:
                if ".rpt" in name:
                    file = auto_result_folder + os.sep + folder + os.sep + name
                    report_list.append(file)
                    break

    data = []
    header = "Period(ns), Freq(MHz), Area(um^2), Area(KGate), Leakage(uW), Dynamic(uW), Dynamic(uW/MHz), slack(ns)"
    print(header)

    for report in report_list:
        name = report
        name_list = name.split(os.sep)
        freq = 0.00
        for item in name_list:
            if "MHz" in item and "_" in item and "auto" not in item:
                freq = float((item.split("_")[-1]).replace("MHz", ""))
            elif "kHz" in item and "_" in item and "auto" not in item:
                freq = float((item.split("_")[-1]).replace("kHz", "")) / 1000.0

        period = float(1.00 / float(freq) * 1000.00)

        o_report = open(report, "r+")
        text = o_report.readlines()
        o_report.close()

        total_area = ""
        dynamic = ""
        leakage = ""
        slack = ""
        dynamic_value = ""
        dynamic_unit = ""
        leakage_value = ""
        leakage_unit = ""

        for line in text:
            if "Total" in line and "references" in line:
                total_area = line.split(" ")[-1].replace("\n", "")
            elif "Total Dynamic Power" in line:
                dynamic = line.split("=")[-1].split("(")[0].replace("\n", "")
            elif "Cell Leakage Power" in line:
                leakage = line.split("=")[-1].replace("\n", "")
            elif "slack (MET)" in line or "slack (VIOLATED)" in line:
                slack = line.replace("\n", "").split(" ")[-1]

        total_area = total_area.replace(" ", "")
        dynamic_list = dynamic.split(" ")

        for item in dynamic_list:
            if "." in item:
                dynamic_value = item
            elif "W" in item:
                dynamic_unit = item

        leakage_list = leakage.split(" ")
        for item in leakage_list:
            if "." in item:
                leakage_value = item
            elif "W" in item:
                leakage_unit = item

        if dynamic_unit == "mW":
            dynamic_value = str(float(dynamic_value) * 1000.0)

        if leakage_unit == "mW":
            leakage_value = str(float(leakage_value) * 1000.0)

        # print("total_area: " + str(total_area))
        # print("KGate: " + str(float(total_area)/0.8/1000.0))
        # print("dynamic: " + str(dynamic_value) + " " + dynamic_unit)
        # print("leakage: " + str(leakage_value) + " " + leakage_unit)

        data_line = str('%.10f' % period) + "," + str(freq) + "," + str(total_area) + "," + str(float(total_area) / 0.8 / 1000.0) + "," + str(leakage_value) + "," + str(dynamic_value) + ",," + str(slack)
        data.append(data_line)
        print(data_line)

    # w_file = open(folder_name+".txt" , "a+")
    # w_file.truncate(0)
    # w_file.write(header + "\n")
    # for line in data:
    #      w_file.write(line + "\n")
    # w_file.close()
    return data


def combine_data():
    data = []
    folder = os.getcwd() + os.sep + "auto_result_not_worst"
    dir_list = os.listdir(folder)
    for item in dir_list:
        if os.path.isdir(folder + os.sep + item) and ".idea" != item:
            print("\n" + folder + os.sep + item)
            data.append(gen_results(folder + os.sep + item))

    arr = []
    for item in data:
        for line in item:
            arr.append(line.split(","))

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]

    n = len(arr)
    swapped = True
    x = -1
    while swapped:
        swapped = False
        x = x + 1
        for i in range(1, n - x):
            if float(arr[i - 1][1]) > float(arr[i][1]):
                swap(i - 1, i)
                swapped = True

    w_file = open(folder.split(os.sep)[-1] + ".txt", "a+")
    w_file.truncate(0)
    for line in arr:
        joined = ",".join(line)
        w_file.write(joined + "\n")
        print(joined)
    w_file.close()


def parse_hspice(file):
    hspice_file = file
    o_file = open(hspice_file, "r+")
    text = o_file.read().split("\n")
    o_file.close()

    data = []
    gates = {}

    for line in text:
        if "parameter ttran" in line and "warning" not in line:
            data.append("\n" + line)
        elif ("nor " in line or "nand " in line or "inv " in line or "buff" in line or "testbench" in line) and "warning" not in line:
            data.append(line)
        elif ("tpdr" in line or "tpdf" in line or "ttrf" in line or "ttrr" in line) and "warning" not in line and "meas_variable" not in line:
            data.append(line)
        elif ("tpd_fall" in line or "tpd_rise" in line or "ttr_fall" in line or "ttr_rise" in line) and "warning" not in line and "meas_variable" not in line:
            data.append(line)
        # elif ("leak_pow" in line or " dyn_pow" in line) and "meas_variable" not in line:
        #     data.append(line)

    for line in data:
        print(line)

    for i in range(0, len(data)):
        if "parameter ttran" in data[i] and "testbench" not in data[i + 1]:
            t_time = data[i].split(" ")[-2]
            gate = data[i + 1]
            index_1 = ""
            index_2 = ""
            if t_time == "1.000E-09":
                index_1 = "1ns"
            elif t_time == "2.000E-09":
                index_1 = "2ns"
            if "2" in gate:
                index_2 = "2fF"
            elif "10" in gate:
                index_2 = "10fF"

            if "x4" in gate:
                if "2a" in gate or "10a" in gate:
                    tail = "_a_x4"
                    if gate.split(" ")[1] + tail not in gates:
                        gates[gate.split(" ")[1] + tail] = {}
                elif "2b" in gate or "10b" in gate:
                    tail = "_b_x4"
                    if gate.split(" ")[1] + tail not in gates:
                        gates[gate.split(" ")[1] + tail] = {}
                else:
                    tail = "_x4"
                    if gate.split(" ")[1] + tail not in gates:
                        gates[gate.split(" ")[1] + tail] = {}
            else:
                if "2a" in gate or "10a" in gate:
                    tail = "_a_x1"
                    if gate.split(" ")[1] + tail not in gates:
                        gates[gate.split(" ")[1] + tail] = {}
                elif "2b" in gate or "10b" in gate:
                    tail = "_b_x1"
                    if gate.split(" ")[1] + tail not in gates:
                        gates[gate.split(" ")[1] + tail] = {}
                else:
                    tail = "_x1"
                    if gate.split(" ")[1] + tail not in gates:
                        gates[gate.split(" ")[1] + tail] = {}

            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2] = {}
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["tpd_fall"] = ""
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["tpd_rise"] = ""
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["ttr_fall"] = ""
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["ttr_rise"] = ""

    for i in range(0, len(data)):
        if "parameter ttran" in data[i] and "testbench" not in data[i + 1]:
            t_time = data[i].split(" ")[-2]
            gate = data[i + 1]
            index_1 = ""
            index_2 = ""
            if t_time == "1.000E-09":
                index_1 = "1ns"
            elif t_time == "2.000E-09":
                index_1 = "2ns"
            if "2" in gate:
                index_2 = "2fF"
            elif "10" in gate:
                index_2 = "10fF"

            tpd_fall = data[i + 2].split(" ")[5]
            tpd_rise = data[i + 3].split(" ")[5]
            ttr_fall = data[i + 4].split(" ")[5]
            ttr_rise = data[i + 5].split(" ")[5]

            if "x4" in gate:
                if "2a" in gate or "10a" in gate:
                    tail = "_a_x4"
                elif "2b" in gate or "10b" in gate:
                    tail = "_b_x4"
                else:
                    tail = "_x4"
            else:
                if "2a" in gate or "10a" in gate:
                    tail = "_a_x1"
                elif "2b" in gate or "10b" in gate:
                    tail = "_b_x1"
                else:
                    tail = "_x1"

            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["tpd_fall"] = tpd_fall
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["tpd_rise"] = tpd_rise
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["ttr_fall"] = ttr_fall
            gates[gate.split(" ")[1] + tail][index_1 + "," + index_2]["ttr_rise"] = ttr_rise

    act_list = ["tpd_fall", "tpd_rise", "ttr_fall", "ttr_rise"]
    x_1_2 = ""
    x_1_10 = ""
    x_2_2 = ""
    x_2_10 = ""

    for key in sorted(gates.keys()):
        if "x1" in key:
            for act in act_list:
                for item in gates[key]:
                    if "1ns,2fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_1_2 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_1_2 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                    elif "1ns,10fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_1_10 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_1_10 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                    elif "2ns,2fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_2_2 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_2_2 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                    elif "2ns,10fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_2_10 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_2_10 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")

                print(key + " " + act)
                print('"' + x_1_2 + "," + x_1_10 + "\",\"" + x_2_2 + "," + x_2_10 + '"\n')
            print("-----------------------------------\n")

    for key in sorted(gates.keys()):
        if "x4" in key:
            for act in act_list:
                for item in gates[key]:
                    if "1ns,2fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_1_2 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_1_2 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                    elif "1ns,10fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_1_10 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_1_10 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                    elif "2ns,2fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_2_2 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_2_2 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                    elif "2ns,10fF" in item:
                        if "E-10" in gates[key][item][act]:
                            x_2_10 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                        elif "E-11" in gates[key][item][act]:
                            x_2_10 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")

                print(key + " " + act)
                print('"' + x_1_2 + "," + x_1_10 + "\",\"" + x_2_2 + "," + x_2_10 + '"\n')
            print("-----------------------------------\n")

if __name__ == "__main__":
	
	# TODO: multi thread it
    # auto_run()

    gen_results(os.getcwd() + os.sep + "auto_result_not_worst")
    # combine_data()

    #parse_hspice("../comb_stdcell_liberty2/hspice_2.out")
    #parse_hspice("../comb_stdcell_liberty2/hspice_buf_2.out")

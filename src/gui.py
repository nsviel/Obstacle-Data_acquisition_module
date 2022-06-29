#! /usr/bin/python
#---------------------------------------------

from src import parameter
from src import device
from src import callback
from src import io
from src import lidar
from src import saver

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

def init():
    saver.determine_path()

def loop():
    a = 1;

    #print(parameter.with_two_lidar)

def build_parameter():
    with dpg.group():
        dpg.add_text("Parameter", color=(125, 125, 125))
        dpg.add_checkbox(tag="wgeo", label="With geolocalization", default_value=parameter.with_geolocalization, callback=callback.callback_parameter);
        dpg.add_checkbox(tag="cwf", label="With LiDAR forwarding", default_value=parameter.with_forwarding, callback=callback.callback_parameter);
        dpg.add_checkbox(tag="cwtl", label="With two lidar", default_value=parameter.with_two_lidar, callback=callback.callback_parameter);
        dpg.add_checkbox(tag="cwws", label="With writing on SSD", default_value=parameter.with_writing, callback=callback.callback_parameter);

        dpg.add_text("")
        dpg.add_input_int(tag="ls", label="Lidar speed", default_value=parameter.lidar_speed, step=60, min_value=0, max_value=1200, width=100, min_clamped=True, max_clamped=True, callback=callback.callback_parameter);

        dpg.add_text("")
        dpg.add_input_text(tag="veloip", label="Velodium IP", default_value=parameter.velo_ip, width=100, callback=callback.callback_parameter);
        dpg.add_input_int(tag="velopo", label="Velodium port", default_value=parameter.velo_port, min_value=0, min_clamped=True, width=100, callback=callback.callback_parameter);

def build_device():
    with dpg.group():
        dpg.add_text("Device", color=(125, 125, 125))
        with dpg.group(horizontal=True):

            devices = device.get_all_device()
            with dpg.group():
                dpg.add_text("LiDAR 1")
                dpg.add_listbox(devices, tag="l1d", callback=callback.callback_parameter, default_value=parameter.lidar_1_dev, width=150, num_items=len(devices))

            with dpg.group():
                dpg.add_text("LiDAR 2")
                dpg.add_listbox(devices, tag="l2d", callback=callback.callback_parameter, default_value=parameter.lidar_2_dev, width=150, num_items=len(devices))

def build_saving():
    with dpg.group(horizontal=True):
        dpg.add_text("Capture ID: [")
        dpg.add_text(parameter.capture_ID, color=(31, 140, 250))
        dpg.add_text("]")
    dpg.add_input_text(tag="ssdp", label="Path SSD", default_value=parameter.path_ssd, width=200, callback=callback.callback_path);
    dpg.add_text(parameter.path_file_l1, tag="l1p", color=(31, 140, 250));
    dpg.add_text(parameter.path_file_l2, tag="l2p", color=(31, 140, 250));

def build_runtime():
    dpg.add_separator()
    dpg.add_text("Runtime", color=(125, 125, 125))
    with dpg.group(horizontal=True):
        with dpg.group():
            with dpg.group(horizontal=True):
                dpg.add_text("Country: [")
                dpg.add_text(parameter.geo_country, color=(31, 140, 250))
                dpg.add_text("]")

            with dpg.group(horizontal=True):
                dpg.add_text("LiDAR 1 packet: [")
                dpg.add_text(parameter.lidar_1_nb_packet, color=(31, 140, 250))
                dpg.add_text("]")
                dpg.add_button(label="Start", tag="l1dstart", indent=200, callback=lidar.start_l1_motor)
                dpg.add_button(label="Stop", tag="l1dstop", callback=lidar.stop_l1_motor)

            with dpg.group(horizontal=True):
                dpg.add_text("LiDAR 2 packet: [")
                dpg.add_text(parameter.lidar_2_nb_packet, color=(31, 140, 250))
                dpg.add_text("]")
                dpg.add_button(label="Start", tag="l2dstart", indent=200, callback=lidar.start_l2_motor)
                dpg.add_button(label="Stop", tag="l2dstop", callback=lidar.stop_l2_motor)

        dpg.add_button(label="False alarm", indent=200)

def build_stat():
    dpg.add_separator()
    dpg.add_text("Statistics", color=(125, 125, 125))
    with dpg.group(horizontal=True):
        dpg.add_text("Capture time: [")
        dpg.add_text(parameter.time_capture, color=(31, 140, 250))
        dpg.add_text("]")

    with dpg.group(horizontal=True):
        dpg.add_text("LiDAR 1 - Size of capture file: [")
        dpg.add_text(io.get_size_Gb(parameter.path_file_l1), color=(31, 140, 250))
        dpg.add_text("]")

    with dpg.group(horizontal=True):
        dpg.add_text("LiDAR 2 - Size of capture file: [")
        dpg.add_text(io.get_size_Gb(parameter.path_file_l2), color=(31, 140, 250))
        dpg.add_text("]")

def build_end():
    dpg.add_separator()
    dpg.add_button(label="close", tag="bclo", callback=callback.callback_event)

def start():
    dpg.create_context()

    with dpg.window(tag="window", label="Pywardium"):
        with dpg.group(horizontal=True):
            build_parameter()
            build_device()
        build_saving()
        build_runtime()
        build_stat()
        build_end()
        #demo.show_demo()

    dpg.create_viewport(title='Pywardium', width=parameter.gui_width, height=parameter.gui_height)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("window", True)

    # Start main loop program
    init()
    while parameter.run and dpg.is_dearpygui_running():
        loop()
        dpg.render_dearpygui_frame()

    # Finish program
    dpg.destroy_context()
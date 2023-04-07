import obspython as S
import glob, win32gui, win32process, re, psutil, os, os.path, shutil
from pathlib import Path
from ctypes import windll

class Data:
    OutputDir = None
    Extension = None
    ExtensionMask = None



def on_event(event):

    if event == S.OBS_FRONTEND_EVENT_RECORDING_STOPPED:

        print("Triggered when the recording stopped")
        path = find_latest_file(Data.OutputDir, '\*')
        dir = os.path.dirname(path)
        rawfile = os.path.basename(path)
        title = get_window_title()
        newFolder = dir + '\\' + title 
        
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
        
        newfile = title + ' ' + rawfile[:-4] + '.'+Data.Extension        
        file = rawfile[:-3]+Data.Extension
        oldPath = dir +'\\'+ file
        newPath = newFolder + '\\' + newfile
        textFile = (oldPath[:-3]+"txt")
        
        f = open(oldPath[:-3]+"txt", "w")
        f.write(newfile)
        f.close()

        shutil.move(oldPath, newPath)
        os.remove(textFile)
        
        print(file)
        print(oldPath)
        print(newfile)



    
    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:

        print("Triggered when the replay buffer saved")
        path = find_latest_file(Data.OutputDir, '\*')
        dir = os.path.dirname(path)
        rawfile = os.path.basename(path)
        title = get_window_title()
        newFolder = dir + '\\' + title 
        
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
        
        newfile = title + ' ' + rawfile[:-4] + '.'+Data.Extension
        file = rawfile[:-3]+Data.Extension
        oldPath = dir +'\\'+ file
        newPath = newFolder + '\\' + newfile
        textFile = (oldPath[:-3]+"txt")
        
        f = open(oldPath[:-3]+"txt", "w")      
        f.write(newfile)
        f.close()
        
        shutil.move(oldPath, newPath)
        os.remove(textFile)
        
        print(file)
        print(oldPath)
        print(newfile)




def get_window_title():

    user32 = windll.user32

    swd, sht = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Add in fullscreen detection here! 
    w = win32gui
    win_title = w.GetWindowText(w.GetForegroundWindow())
    
    l, t, r, b = w.GetWindowRect(w.GetForegroundWindow())
    wd, ht = r - l, b - t

    tid, pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
    p = psutil.Process(pid)
    exe = p.name()

    desktopOveride = 0
    fullscreenOveride = 0

    with open(script_path()+'/DesktopOverride.cfg') as dofile:
     if exe in dofile.read():
            desktopOveride = 1
    
    with open(script_path()+'/FullscreenOverride.cfg') as fsfile:
        if exe in fsfile.read():
            fullscreenOveride = 1

    if win_title[:3] == 'OBS':
        title = "Manual Recording"
    elif desktopOveride == 1:
        title = win_title
    else:
        if  wd == swd and ht == sht and fullscreenOveride == 0:
            title = win_title
        else:
            title = "Desktop"

    title = re.sub(r'[^0-9A-Za-z .-]', '', title)
    title = title[:50]

    return title



def find_latest_file(folder_path, file_type):
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    return max_file



def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)



def script_update(settings):
    Data.OutputDir = S.obs_data_get_string(settings,"outputdir")
    Data.OutputDir = Data.OutputDir.replace('/','\\')
    Data.Extension = S.obs_data_get_string(settings,"extension")
    Data.ExtensionMask = '\*' + Data.Extension



def script_description():
    desc = "Renames and organizes recordings into subfolders like NVidia ShadowPlay.\n\nAuthor: francedv23"
    return desc


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_path(
        props, "outputdir", "Recordings folder", S.OBS_PATH_DIRECTORY,
        None, str(Path.home()))
    S.obs_properties_add_text(
        props,"extension","File extension",S.OBS_TEXT_DEFAULT)

    return props
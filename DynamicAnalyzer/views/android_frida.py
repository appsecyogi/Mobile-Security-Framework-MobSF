import frida
from MobSF.utils import PrintException

def get_vm(dev_id, dev_type):
    """find android vm"""
    try:
        devices = frida.enumerate_devices()
        for device in devices:
            if (dev_id == device.id and
                dev_type == device.type
               ):
                return device.id
        print "[WARNING] Frida Cannot Find Android Device/VM"
    except:
        PrintException("[ERROR] Frida Cannot Enumerate Device/VM")
    return None

def frida_connect(device_identifier):
    """Connect to VM/Device"""
    try:
        device = frida.get_device(device_identifier)
        return device
    except:
        PrintException("[ERROR] Cannot Connect to Device/VM")
    return None


def create_app_session(device, package):
    """create a session for script execution"""
    try:
        '''
        #import ipdb; ipdb.set_trace()
        processes = device.enumerate_processes()
        pid = None
        for proc in processes:
            if proc.name == package:
                pid = proc.pid
                break
        if pid == None:
            pid = device.spawn([package])
        '''
        return device.spawn([package])
         
    except:
        PrintException("[ERROR] Frida Cannot Attach to - " + package)
    return None

def execute_script(device, package, pid, script_content):
    """Execute a script in app context"""
    session = device.attach(pid)
    script = session.create_script(script_content)
    script.on('message',js_response)
    #http://stackoverflow.com/questions/36680128/frida-spawn-process-failed-on-android
    #session.on('detached', on_detached)
    script.load()
    device.resume(pid)
    session.detach()

def js_response(message, data):
    """Response from Device"""
    print data
    print message

def get_process(device):
    """enumerate processes"""
    return device.enumerate_processes()

def get_apps(device):
    """enumerate applications"""
    return device.enumerate_applications()

def hook_process_on_front(device):
    """select running app"""
    device.get_frontmost_application()

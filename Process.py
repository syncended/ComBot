import psutil

system = [
    'svchost.exe', 'smss.exe', 'System', 'Registry', 'System Idle Process', 'wininit.exe', 'wargamingerrormonitor.exe',
    'csrss.exe', 'services.exe', 'lsass.exe', 'fontdrvhost.exe', 'RuntimeBroker.exe', 'winlogon.exe', 'WUDFHost.exe',
    'dwm.exe', 'browser_broker.exe', 'ctfmon.exe', 'SearchFilterHost.exe', 'jucheck.exe', 'audiodg.exe', 'spoolsv.exe',
    'OneDrive.exe', 'AGMService.exe', 'AESMSr64.exe', 'sihost.exe', 'HPStatusAlerts.exe', 'MemCompression',
    'atkexComSvc.exe', 'Video.UI.exe', 'SecurityHealthSystray.exe', 'MsMpEng.exe', 'StartMenuExperienceHost.exe',
    'jusched.exe', 'WinStore.App.exe', 'taskhostw.exe', 'HPLaserJetService.exe', 'ApplicationFrameHost.exe',
    'explorer.exe', 'dllhost.exe', 'conhost.exe', 'dasHost.exe', 'AGSService.exe', 'wgc.exe', 'NVIDIA Share.exe',
    'hpwuschd2.exe', 'python.exe', 'YourPhone.exe', 'SecurityHealthService.exe', 'NisSrv.exe', 'fsnotifier64.exe',
    'unsecapp.exe', 'rundll32.exe', 'SgrmBroker.exe', 'SearchUI.exe', 'SoundDeck.exe', 'wgc_renderer.exe',
    'webwallpaper32.exe', 'SearchProtocolHost.exe', 'MicrosoftEdgeCP.exe', 'SearchIndexer.exe', 'nvcontainer.exe',
    'winpty-agent.exe', 'HPBDSService.exe', 'wallpaper32.exe', 'nvsphelper64.exe', 'LockApp.exe', 'SystemSettings.exe',
    'ShellExperienceHost.exe', 'MicrosoftEdgeSH.exe', 'SettingSyncHost.exe', 'NVIDIA Web Helper.exe', 'mstsc.exe',
    'TeamViewer_Service.exe', 'smartscreen.exe'
]


def get_processes():
    out = set()
    for proc in psutil.process_iter():
        try:
            if proc.name() not in system:
                out.add(proc.name())
        except:
            # nothing
            print(end='')
    return out


def kill(name):
    for proc in psutil.process_iter():
        try:
            if proc.name() == name:
                proc.kill()
        except:
            # nothing
            print(end='')

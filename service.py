import xbmc
import xbmcaddon
import xbmcgui

from resources.lib import hyperion

__addon__ = xbmcaddon.Addon()
__title__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__language__ = __addon__.getLocalizedString
__hyperion__ = None


def log(txt):
    message = '%s: %s' % (__title__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGNOTICE)


class Main:
    def __init__(self):
        hyperion_host = __addon__.getSetting('hyperion_host')
        hyperion_port = __addon__.getSetting('hyperion_port')
        priority = __addon__.getSetting('priority')
        global __hyperion__

        if not hyperion_host or not hyperion_port:
            log('Service: ' + __language__(20000))
            xbmcgui.Dialog().notification(__title__, __language__(20000), __icon__, 5000)
            return

        __hyperion__ = hyperion.Remote(hyperion_host=hyperion_host, hyperion_port=hyperion_port, priority=priority)

        self.Player = MyPlayer()
        self.Monitor = MyMonitor()
        self._daemon()

    def _daemon(self):
        while not self.Monitor.abortRequested():
            if self.Monitor.waitForAbort(10):
                self.Monitor.onShutdown()
                break


class MyMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.onStart()

    def onStart(self):
        if __addon__.getSetting('clear_on_start') == 'true':
            log('Monitor: onStart(clearAll)')
            __hyperion__.clearAll()

        if __addon__.getSetting('effect_on_kodi_startup'):
            log('Monitor: onStart(effect)')
            __hyperion__.effect(__addon__.getSetting('effect_on_kodi_startup'))

    def onShutdown(self):
        if __addon__.getSetting('off_on_shutdown') == 'true':
            log('Monitor: onShutdown')
            __hyperion__.color('black')

    def onScreensaverActivated(self):
        if __addon__.getSetting('off_on_screensaver_activated') == 'true':
            log('Monitor: onScreensaverActivated')
            __hyperion__.color('black')

    def onScreensaverDeactivated(self):
        if __addon__.getSetting('effect_on_screensaver_deactived'):
            log('Monitor: onScreensaverDeactivated')
            __hyperion__.effect(__addon__.getSetting('effect_on_screensaver_deactived'))


class MyPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)

    def onPlayBackStarted(self):
        if __addon__.getSetting('clear_on_video_playback') and xbmc.Player().isPlayingVideo():
            log('Player: onPlayBackStarted(clearAll)')
            __hyperion__.clearAll()

        if __addon__.getSetting('effect_on_playback_audio') and xbmc.Player().isPlayingAudio():
            log('Player: onPlayBackStarted(effect)')
            __hyperion__.effect(__addon__.getSetting('effect_on_playback_audio'))

    def onPlayBackResumed(self):
        if __addon__.getSetting('clear_on_video_playback') == 'true' and xbmc.Player().isPlayingVideo():
            log('Player: onPlayBackResumed')
            __hyperion__.clearAll()

    def onPlayBackPaused(self):
        if __addon__.getSetting('effect_on_playback_paused') and xbmc.Player().isPlayingVideo():
            log('Player: onPlayBackPaused')
            __hyperion__.effect(__addon__.getSetting('effect_on_playback_paused'))

    def onPlayBackStopped(self):
        if __addon__.getSetting('effect_on_playback_stopped'):
            log('Player: onPlayBackStopped')
            __hyperion__.effect(__addon__.getSetting('effect_on_playback_stopped'))

    def onPlayBackEnded(self):
        self.onPlayBackStopped()


if __name__ == '__main__':
    if __addon__.getSetting('autostart') == 'true':
        log('Service: autostart execute')
        Main()

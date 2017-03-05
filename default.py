import sys
import subprocess
import xbmc
import xbmcaddon
import xbmcgui

from urlparse import parse_qsl
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
            print 'Hyperion.Script: ' + __language__(20000)
            xbmcgui.Dialog().notification(__title__, __language__(20000), __icon__, 5000)
            return

        __hyperion__ = hyperion.Remote(hyperion_host=hyperion_host, hyperion_port=hyperion_port, priority=priority)

        self.params = dict(parse_qsl('&'.join(sys.argv)))

        if not self.params:
            xbmc.executebuiltin('Addon.OpenSettings(script.hyperion)')

        command = self.params.get('command', None)

        log('Script: command: %s' % command)

        if command is None:
            log('Script: no command given?!')

        elif command == 'effect':
            self._effect()

        elif command == 'color':
            self._color()

        elif command == 'clear':
            self._clear()

        elif command == 'clearall':
            self._clearAll()

        elif command == 'switch':
            self._switch()

    def _effect(self):
        effect = self.params.get('effect', None)
        priority = self.params.get('priority', None)

        if not effect:
            return

        xbmcgui.Dialog().notification(__title__, effect, __icon__, 3000)
        __hyperion__.effect(effect, priority)

    def _color(self):
        color = self.params.get('color', None)
        priority = self.params.get('priority', None)

        if not color:
            return

        try:
            __hyperion__.color(color, priority)
        except ValueError as e:
            color = e.message

        xbmcgui.Dialog().notification(__title__, color, __icon__, 3000)

    def _clear(self):
        priority = self.params.get('priority', None)

        xbmcgui.Dialog().notification(__title__, __language__(20001), __icon__, 3000)
        __hyperion__.clear(priority)

    def _clearAll(self):
        xbmcgui.Dialog().notification(__title__, __language__(20001), __icon__, 3000)
        __hyperion__.clearAll()

    def _switch(self):

        if not __addon__.getSetting('switch_type'):
            return

        priority = self.params.get('priority', None)

        if __hyperion__.getState() == 'on':
            __hyperion__.color('black', priority)
        else:
            if __addon__.getSetting('switch_type') == '1':
                __hyperion__.effect(__addon__.getSetting('switch_effect'), priority)
            else:
                __hyperion__.clearAll()

        if __addon__.getSetting('switch_additional'):
            cmd = '%s %s' % (__addon__.getSetting('switch_additional'), __hyperion__.getState())
            log('Script: switch additional %s' % cmd)
            subprocess.Popen(cmd, shell=True)


if __name__ == '__main__':
    log('Script: execute')
    Main()

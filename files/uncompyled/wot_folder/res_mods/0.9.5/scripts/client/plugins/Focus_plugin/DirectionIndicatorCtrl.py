from account_helpers.AccountSettings import AccountSettings

class DirectionIndicatorCtrl():
    def __init__(self, indicator, config, position):
        self.__shapes = config["colors"]
        shape = self.__shapes[0]
        if AccountSettings.getSettings('isColorBlind'):
            shape = self.__shapes[1]
        self.__indicator = indicator
        self.__indicator.setShape(shape)
        self.__indicator.track(position)
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        g_settingsCore.onSettingsChanged += self.__as_onSettingsChanged

    def update(self, distance, position = None):
        self.__indicator.setDistance(distance)
        if position is not None:
            self.__indicator.setPosition(position)

    def clear(self):
        if self.__indicator is not None:
            self.__indicator.remove()
        self.__indicator = None
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        g_settingsCore.onSettingsChanged -= self.__as_onSettingsChanged

    def __as_onSettingsChanged(self, diff):
        if 'isColorBlind' in diff:
            shape = self.__shapes[0]
            if diff['isColorBlind']:
                shape = self.__shapes[1]
            if self.__indicator is not None:
                self.__indicator.setShape(shape)
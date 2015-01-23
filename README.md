wotmods
=======

World of Tanks Modifications 100% python


#### The new plugin system 

The mods are now part of a plugin system.    
Expecially, it's better structured than before recycling common code and managing some behaviors to increase stability,performance and decreasing maintenance time.    
Every plugin can be de/activate from it configuration file, or you can also add or remove plugins.   

This is not xvm and will never be like xvm.

Some plugins are used from others, i will write a note in case. Anyway "Engine" folder is the core library, don't touch it.


#### Plugins

[SixthSenseDuration_plugin](http://forum.worldoftanks.eu/index.php?/topic/358159-095sixth-sense-duration-iconaudiocountdown/#topmost)   
Increase duration of sixth sense lamp,eventually with a sound and a countdown.

[Statisticv_plugin](http://forum.worldoftanks.eu/index.php?/topic/455834-095statisticv2-mod-no-xvm/)  
Provide performance rating,win chance,client language,battle amount of every player in the battle. 

[SpotMessanger_plugin](http://forum.worldoftanks.eu/index.php?/topic/353419-095spotmessanger/)   
Send message to team or platoon ,eventually with a "help" or "ping" command,if you are spotted and under some conditions.   
Note: it use ingame_messanger plugin

[Focus_plugin](http://forum.worldoftanks.eu/index.php?/topic/463328-095-focus-mod/)    
Put a red arrow indicating the targetted enemies from your team. 
Usefull to increase focus fire's efficiency 

#### Installation
Download all code from [here](https://github.com/jstar88/wotmods/archive/master.zip)      
Then extract the content of *files/recompyled/wot_folder* in your game root.   

To enale a plugin,open *game_root/res_mods/0.9.5/scripts/client/plugins/{plugin_name}/config.xml* and set pluginEnable to true.


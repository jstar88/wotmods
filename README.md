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

* [SixthSenseDuration_plugin](http://forum.worldoftanks.eu/index.php?/topic/358159-095sixth-sense-duration-iconaudiocountdown/#topmost)   
Increase duration of sixth sense lamp,eventually with a sound and a countdown.

* [Statistics_plugin](http://forum.worldoftanks.eu/index.php?/topic/455834-095statisticv2-mod-no-xvm/)  
Provide performance rating,win chance,client language,battle amount of every player in the battle. 

* [SpotMessanger_plugin](http://forum.worldoftanks.eu/index.php?/topic/353419-095spotmessanger/)   
Send message to team or platoon ,eventually with a "help" or "ping" command,if you are spotted and under some  conditions.   
Note: it use ingame_messanger plugin

* [Focus_plugin](http://forum.worldoftanks.eu/index.php?/topic/463328-095-focus-mod/)    
Put a red arrow indicating the targetted enemies from your team. 
Usefull to increase focus fire's efficiency 

* [Builder_plugin](http://forum.worldoftanks.eu/index.php?/topic/493804-097ingame-map-editor/)  
Pressing a combinations of buttons you are able to put objects around wot maps, the map that you created is automatically saved and loaded.  
Both render engine and editor are only enabled in training battle and in replay mode.  
Edited maps can be seen by other players using this mod and, of course, every map can be shared in safe way.  
It's possible to use all models inside shared_content.pkg , but in future will be easy to add external models too.  

* [SpotExtended_plugin](http://forum.worldoftanks.eu/index.php?/topic/510979-0981-spottedextended-no-xvm/)  
This mod write to the ingame right panel(where kills are announced)  name of  tanks spotted by you.  
It can also show an "eye" marker above the spotted tank for a chosen time.  

#### Installation
Download all code from [here](https://github.com/jstar88/wotmods/archive/master.zip)      
Then extract the content of *files/recompyled/wot_folder* in your game root.   

To enable/disable plugins,open *{game_root}/res_mods/0.9.x/scripts/client/plugins/{plugin_name}/config.xml* and set pluginEnable to true/false.

where  

* {game_root} is your World of Tank installation directory
* x is the wot version   
* {plugin_name} is the plugin's name


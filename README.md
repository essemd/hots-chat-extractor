Want to see what the enemy team was saying about you during the match? This tool allows you to do so; since you can't read the enemies chat either while in-game or even when watching the replay back.

Deps:  
	- Python 3.x  
	- mpyq>0.2.5 and six>1.14.0  
	- The appropriate protocolXXXXX.py file for the current HotS version must be included in the projects root directory.  
	  It can be found at https://github.com/Blizzard/heroprotocol/tree/master/heroprotocol/versions. You must also  
	  change the import on line 10 of extract-chat.py to point to the version you include.  
  
Usage:  
	- python3 extract-chat.py </path/to/replay>  


# supertux-engine
Clone of a SuperTux level renderer written in PyGame. Level files are specified with JSON files (located in `levels` folder).<br>`main.py` is just a single level render main code for everything (collisions, player drawings and other things).

## Requirements
`pygame` library is needed (`pip install pygame`, or `apt install python3-pygame` depending of environment you have).

## Running
You can simply test the example provided level (`levels/welcome.json`) by running `main.py` with Python (after installing PyGame):
```bash
python3 main.py
```
Usable controls are set in `config.py` and they are currently left and right arrow key for moving left and right, and space for jumping.

## License
Since the main licenses for sprites and music are located in SuperTux, you can refer to them by seeing it's [license](https://github.com/SuperTux/supertux/blob/master/LICENSE.txt) and general [repository](https://github.com/SuperTux/supertux).

Code is licensed with GPLv3 (same as SuperTux).

## Preview
<img width="1920" height="1080" src="https://github.com/user-attachments/assets/99ef2b24-7d88-490c-847e-04d0d6b8ad5f" />

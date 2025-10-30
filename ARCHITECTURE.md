├── 📁 assets/
│   ├── 📁 images/
│   │   ├── earth.jpg
│   └── 📁 audio/
|       
├── 📁 src/
│   ├── 🐍 __init__.py   # These files mark folders as packages (Like Java, and allows src.core.engine import Engine)
│   │
│   ├── 📁 core/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 engine.py         # Main simulation loop, PyGame/OpenGL setup will be here!
│   │   ├── 🐍 time_manager.py   # Manages simulation time, delta time, speed, pausing...anything time
│   │   └── 🐍 input_handler.py  # Processes PyGame events (mouse/keyboard).
│   │
│   ├── 📁 simulation/
│   │   ├── 🐍 __init__.py
│   │   ├── 📁 models/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 celestial_body.py # Base class (position, mass, velocity).
│   │   │   ├── 🐍 planet.py         # Extends Celestial_Body.
│   │   │   └── 🐍 star.py           # Extends Celestial_Body.
│   │   │
│   │   ├── 📁 services/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 physics_service.py # Gravitational calculations, updates positions.
│   │   │   └── 🐍 orbit_service.py   # Logic for calculating and drawing orbital paths. (I'd like to use NASA's Horizon's API for real time orbits)
│   │   │
│   │   └── 📁 data/                    #Basically our repo
│   │       ├── 🐍 __init__.py
│   │       └── 🐍 simulation_data.py # Python dictionary/list with planet data.
│   │
│   ├── 📁 graphics/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 camera.py           # Manages the OpenGL view and projection matrices.
│   │   ├── 🐍 renderer.py         # Contains functions for drawing objects with OpenGL.
│   │   ├── 🐍 texture_loader.py   # Utility to load images into OpenGL textures.
│   │   └── 🐍 primitives.py       # Functions to create primitive shapes (e.g., a sphere).
│   │
│   ├── 📁 ui/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 main_menu.py
│   │   └── 🐍 hud.py
│   │
│   └── 🐍 main.py                 # Entry point of the game.
│
└── 🐍 requirements.txt            # Lists dependencies (pygame, pyopengl, numpy) for documention.


Icons for Additions
🐍  - Python Script
📁  - Folder
|    - Continue Folder
├    - Extend Folder
└──  - End Folder
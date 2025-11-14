├── 📁 assets/
│ ├── 📁 images/
│ │ ├── 🌑 mercury.jpg
│ │ ├── 🌕 venus.jpg
│ │ ├── 🌍 earth.jpg
│ │ ├── 🔴 mars.jpg
│ │ ├── 🪐 jupiter.jpg
│ │ ├── 🌀 saturn.jpg
│ │ ├── 🌀 uranus.jpg
│ │ ├── 🌀 neptune.jpg
│ │ └── ❄️ pluto.jpg
| | └── sun.jpg  
│
├── 📁 src/
│ ├── 🐍 **init**.py
│ │
│ ├── 📁 core/
│ │ ├── 🐍 **init**.py
│ │ ├── 🐍 engine.py ✅ fully implemented
│ │ │ - initializes pygame (window only)
│ │ │ - configures OpenGL perspective
│ │ │ - manages app states (menu ↔ simulation)
│ │ │ - integrates physics + renderer systems
│ │ │ - main update/render loop
│ │ │
│ │ ├── 🐍 time_manager.py 🕓 placeholder (frame timing / delta time)
│ │ └── 🐍 input_handler.py ✅ implemented
│ │ - processes pygame keyboard/mouse/quit
│ │
│ ├── 📁 simulation/
│ │ ├── 🐍 **init**.py
│ │ ├── 📁 models/
│ │ │ ├── 🐍 **init**.py
│ │ │ ├── 🐍 celestial_body.py ✅ implemented (base body: pos, vel, mass)
│ │ │ ├── 🐍 planet.py ✅ implemented (planet subclass)
│ │ │ └── 🐍 star.py ✅ implemented (star subclass)
│ │ │
│ │ ├── 📁 services/
│ │ │ ├── 🐍 **init**.py
│ │ │ ├── 🐍 physics_service.py ✅ fully implemented
│ │ │ │ - gravitational calculations
│ │ │ │ - integration over time
│ │ │ │ - start/pause/toggle/reset control
│ │ │ │ - time scaling support
│ │ │ └── 🐍 orbit_service.py 🕓 placeholder (for orbital path logic)
│ │ │
│ │ └── 📁 data/
│ │ ├── 🐍 **init**.py
│ │ └── 🐍 simulation_data.py ✅ implemented
│ │ - provides texture file paths for planets
│ │
│ ├── 📁 graphics/
│ │ ├── 🐍 **init**.py
│ │ ├── 🐍 camera.py ✅ implemented (view/zoom/pan control)
│ │ ├── 🐍 renderer.py ✅ fully implemented
│ │ │ - OpenGL-only rendering
│ │ │ - draws planets as textured spheres
│ │ │ - handles basic lighting setup
│ │ │
│ │ ├── 🐍 texture_loader.py ✅ implemented
│ │ │ - loads .jpg images into OpenGL textures
│ │ │
│ │ └── 🐍 primitives.py 🕓 planned (custom geometry helpers)
│ │
│ ├── 📁 ui/
│ │ ├── 🐍 **init**.py
│ │ ├── 🐍 main_menu.py ✅ fully functional
│ │ │ - OpenGL-based text & buttons
│ │ │ - draw_text() + draw_button() utilities
│ │ │ - transitions to simulation
│ │ │
│ │ └── 🐍 hud.py ✅ fully functional
│ │ - OpenGL-based overlay for simulation
│ │ - draw_text() + draw_button() utilities
│ │ - return-to-menu button
│ │
│ └── 🐍 main.py ✅ entry point
│ - initializes Engine
│ - starts main loop
│
└── 🐍 requirements.txt ✅ lists pygame, pyopengl, numpy


Icons for Additions
🐍 - Python Script
📁 - Folder
| - Continue Folder
├ - Extend Folder
└── - End Folder

├── 📁 assets/
│   ├── 📁 images/
│   │   ├── 🌑 mercury.jpg
│   │   ├── 🌕 venus.jpg
│   │   ├── 🌍 earth.jpg
│   │   ├── 🔴 mars.jpg
│   │   ├── 🪐 jupiter.jpg
│   │   ├── 🌀 saturn.jpg
│   │   ├── 🌀 uranus.jpg
│   │   ├── 🌀 neptune.jpg
│   │   └── ❄️ pluto.jpg
│
├── 📁 src/
│   ├── 🐍 __init__.py
│   │
│   ├── 📁 core/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 engine.py          ✅ implemented
│   │   │                           - sets up PyGame (window only)
│   │   │                           - configures OpenGL viewport
│   │   │                           - manages app states: menu ↔ simulation
│   │   │                           - main update/render loop
│   │   │
│   │   ├── 🐍 time_manager.py    🕓 placeholder (frame timing, delta-time control)
│   │   └── 🐍 input_handler.py   ✅ implemented
│   │                               - processes PyGame mouse/keyboard/quit events
│   │
│   ├── 📁 simulation/
│   │   ├── 🐍 __init__.py
│   │   ├── 📁 models/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 celestial_body.py  🕓 not implemented yet
│   │   │   ├── 🐍 planet.py          🕓 placeholder for planet subclass
│   │   │   └── 🐍 star.py            🕓 placeholder for star subclass
│   │   │
│   │   ├── 📁 services/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 physics_service.py 🕓 planned: gravitational & motion updates
│   │   │   └── 🐍 orbit_service.py   🕓 planned: orbital path logic (NASA Horizons later)
│   │   │
│   │   └── 📁 data/
│   │       ├── 🐍 __init__.py
│   │       └── 🐍 simulation_data.py 🕓 placeholder for static solar system data
│   │
│   ├── 📁 graphics/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 camera.py          🕓 planned: manage OpenGL projection/view matrices
│   │   ├── 🐍 renderer.py        🕓 planned: encapsulate all OpenGL draw calls
│   │   ├── 🐍 texture_loader.py  🕓 planned: load JPG textures into OpenGL
│   │   └── 🐍 primitives.py      🕓 planned: sphere, orbit rings, etc.
│   │
│   ├── 📁 ui/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 main_menu.py       ✅ fully functional
│   │   │                           - OpenGL-only rendering
│   │   │                           - draw_text() + draw_button() utilities
│   │   │                           - text alignment support
│   │   │                           - transitions to simulation screen
│   │   │
│   │   └── 🐍 hud.py             ✅ fully functional
│   │                               - OpenGL-only rendering
│   │                               - same utilities as menu
│   │                               - “Return to Menu” button working
│   │
│   └── 🐍 main.py                ✅ entry point
│                                   - initializes Engine
│                                   - starts main loop
│
└── 🐍 requirements.txt           ✅ lists pygame, pyopengl, numpy


Icons for Additions
🐍  - Python Script
📁  - Folder
|    - Continue Folder
├    - Extend Folder
└──  - End Folder
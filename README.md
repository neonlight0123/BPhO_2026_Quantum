# BPhO Computational Physics Challenge 2026 — Quantum Mechanics

An interactive web application solving all ten quantum mechanics tasks from the
**BPhO Computational Physics Challenge 2026**, built with Streamlit and deployed live.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.61.1-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Award](https://img.shields.io/badge/BPhO%202026-Gold%20Award-FFD700)](#acknowledgements)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-00C7B7?logo=streamlit&logoColor=white)](#-live-demo)

---

## 🔬 Overview

This repository is my submission for the **BPhO Computational Physics Challenge 2026
(Quantum Mechanics)**, awarded a **Gold Award**. It contains ten self-contained
physics simulations covering random walks, statistical mechanics, quantum theory, and
relativistic scattering — each with live interactive controls and the underlying
derivation.

Rather than submitting static graphs, every task is an **interactive exploration tool**:
sliders recompute the physics in real time, plots are fully zoomable, and the theory
behind each result is available in-app.

### Highlights

- **10/10 tasks** implemented as interactive simulations (1,934 lines of Python)
- **Real-time numerics** — `numba`-JIT particle collision engine, not a precomputed animation
- **Analytic + numerical agreement** — every result cross-checked against theory
- **Modern Streamlit** — `st.Page`/`st.navigation` multi-page API and `components.v2`

---

## 🚀 Live Demo

**▶ [Launch the interactive app](https://bpho2026quantum.streamlit.app)**

> The app sleeps after periods of inactivity on the free hosting tier. If you see a
> wake-up prompt, click **"Yes, get this app back up!"** and it will start in ~30 seconds.

Running locally instead:

```bash
git clone https://github.com/neonlight0123/BPhO_2026_Quantum.git
cd BPhO_2026_Quantum
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 📋 The Tasks

| # | Task | Physics | Numerical technique |
|---|------|---------|---------------------|
| 1 | **Random Walk** | Diffusive transport, ⟨R²⟩ = Ns² | Monte Carlo, vectorised cumsum |
| 2 | **Brownian Motion** | Kinetic theory, Knudsen number, elastic collisions | ZMF rigid-sphere collisions (`numba` JIT) |
| 3 | **Black Body Radiation** | Planck's law, Einstein heat capacity, Dulong–Petit | Two-tab radiance + C_V explorer |
| 4 | **Photoelectric Effect** | Einstein equation, V_s = (h/e)f − W/e | Live canvas sim (`components.v2`) |
| 5 | **Hydrogen Spectra** | Rydberg formula, Lyman/Balmer/Paschen series | Series resampling, log axis |
| 6 | **Electron Diffraction** | de Broglie wavelength, Bragg's law, 1/√V linearisation | Ring geometry on phosphor screen |
| 7 | **Particle in a Box** | Schrödinger solutions, Heisenberg uncertainty | Analytic Δx·Δp, ψ and \|ψ\|² |
| 8 | **Quantum Cryptography** | Bell/CHSH, classical local realism vs QM | Probability sweep, Aspect violation |
| 9 | **Compton Scattering** | Δλ = (h/m_e c)(1−cos θ), relativistic recoil | Energy/momentum conservation |
| 10 | **Hydrogenic Orbitals** | R_nl(r) Y_l^m, real spherical harmonics | 2D slices + 3D isosurfaces (`go.Volume`) |

### Selected verification results

Every task is checked against its closed-form prediction:

| Quantity | Computed | Reference |
|---|---|---|
| H-α wavelength (Balmer, n=3→2) | 656.14 nm | 656.28 nm |
| Compton max shift Δλ (θ = 180°) | 4.8526 pm | 4.8523 pm |
| C_V aluminium @ 1000 K | 24.70 J mol⁻¹ K⁻¹ | 3R = 24.94 |
| Planck radiance B(500 nm, 6000 K) | 3.179 × 10¹³ | — |
| Δx·Δp / ℏ, ground state (n=1) | 0.5679 | > 0.5 (HUP) |

---

## 🏗️ Project Structure

```
BPhO_2026_Quantum/
├── app.py                    # Entry point — navigation & page registry
├── requirements.txt          # Pinned dependencies
├── tasks/                    # One module per challenge task
│   ├── homepage.py           # Animated landing page
│   ├── task1.py  …  task10.py
└── .streamlit/
    └── config.toml           # Dracula dark theme
```

Each `tasks/taskN.py` exposes a single `render()` function that draws the whole page,
keeping the physics, controls, and plots for a task together in one file.

---

## 🧮 Technical Notes

**Task 2 — Brownian motion.** The collision engine is a `@njit`-compiled rigid-sphere
simulator working in the zero-momentum frame. Post-collision normal velocities use the
coefficient of restitution `C`:

```
v₁ₙ = [(M − Cm)u₁ₙ + (1+C)m·u₂ₙ] / (M + m)
v₂ₙ = [(m − CM)u₂ₙ + (1+C)M·u₁ₙ] / (M + m)
```

with gas-particle directions re-randomised every Knudsen interval. Timestep resolves the
molecular collision timescale (`dt = 0.01 · Kn · r/v`).

**Task 10 — orbital rendering.** Radial parts use `scipy.special.genlaguerre` and angular
parts `scipy.special.sph_harm_y` (the modern API — the legacy `sph_harm` was removed in
SciPy 1.15+). This is why `requirements.txt` pins versions rather than floating:
unpinned installs break this task.

**Overflow guarding.** Planck's law and the Einstein heat capacity both involve
`exp(hc/λk_BT)` and `exp(T_E/T)`, which overflow in float64. Exponents are clipped at 700
before evaluation.

---

## 🛠️ Deployment

Hosted on **Streamlit Community Cloud**, which builds directly from this repository.
A push to `main` redeploys automatically.

Configuration requirements:

- `requirements.txt` at the repo root — **versions pinned** for reproducibility
- Entry point: `app.py`
- `.streamlit/config.toml` at the repo root (only root-level config is read)

---

## 🏆 Acknowledgements

**Gold Award**, BPhO Computational Physics Challenge 2026 — Quantum.

The challenge is run by the [British Physics Olympiad](https://www.bpho.org.uk/bpho/computational-challenge/)
and sponsored by G-Research. It grew out of the BPhO Computational Physics course and
Dr Andrew French's book *Science by Simulation* (World Scientific).

Submissions are judged on how well the physics is solved computationally; entries are
graded Bronze, Silver, or Gold, and are submitted as a screen-cast walkthrough.

---

## 📄 License

Released for educational reference. Physics coursework — please use it to learn, not to
re-submit.

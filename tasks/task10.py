import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.special import genlaguerre, sph_harm_y
from math import factorial

def radial_wavefunction(r, n, l, Z=1):
    a0 = 0.529 # Bohr radius in Angstroms
    a = a0 / Z
    x = 2 * r / (n * a)
    
    # Normalization constant
    norm = np.sqrt(factorial(n - l - 1) / (2 * n * factorial(n + l))) * (2 / (n * a))**1.5
    
    # Laguerre polynomial
    L = genlaguerre(n - l - 1, 2 * l + 1)
    
    R = norm * (x**l) * np.exp(-x / 2) * L(x)
    return R

def hydrogenic_wavefunction(x, y, z, n, l, m, Z=1):
    r = np.sqrt(x**2 + y**2 + z**2)
    # Handle origin avoiding division by zero
    r = np.where(r == 0, 1e-10, r)
    
    theta = np.arccos(z / r) # polar angle
    phi = np.mod(np.arctan2(y, x), 2 * np.pi) # azimuthal angle [0, 2pi]
    
    R = radial_wavefunction(r, n, l, Z)
    
    # Calculate Real Spherical Harmonics for standard orbital shapes (lobes)
    Y_complex = sph_harm_y(l, abs(m), theta, phi)
    if m < 0:
        Y = np.sqrt(2) * np.imag(Y_complex)
    elif m > 0:
        Y = np.sqrt(2) * np.real(Y_complex)
    else:
        Y = np.real(Y_complex)
    
    psi = R * Y
    psi_sq = np.abs(psi)**2
    
    # Avoid division by zero when normalizing
    max_val = np.max(psi_sq)
    if max_val > 0:
        psi_sq = psi_sq / max_val
        
    return psi_sq

def render():
    st.header("Task 10: Hydrogenic Orbitals")
    st.markdown(r"""
        **Objective:** Compute and visualize 2D cross-section slices and 3D isosurfaces of the electron probability density $|\psi_{nlm}|^2$ for hydrogenic orbitals ($s, p, d, f, g$).
        $$\psi_{nlm}(r, \theta, \phi) = R_{nl}(r) Y_l^m(\theta, \phi)$$
    """)
    
    # Preset Orbital Selector & Controls
    st.markdown("### Orbital Selection & Quantum Parameters")
    
    orbital_presets = {
        "Custom": (1, 0, 0, 5),
        "1s Ground State (n=1, l=0, m=0)": (1, 0, 0, 4),
        "2s State (n=2, l=0, m=0)": (2, 0, 0, 10),
        "2pz Dumbbell (n=2, l=1, m=0)": (2, 1, 0, 10),
        "3s State (n=3, l=0, m=0)": (3, 0, 0, 18),
        "3dz2 Clover (n=3, l=2, m=0)": (3, 2, 0, 18),
        "3d (n=3, l=2, m=2)": (3, 2, 2, 18),
        "4f Orbital (n=4, l=3, m=0)": (4, 3, 0, 25),
        "5g Orbital (n=5, l=4, m=0)": (5, 4, 0, 35)
    }
    
    selected_preset = st.selectbox("Quick Orbital Presets", list(orbital_presets.keys()), index=1)
    
    if selected_preset != "Custom":
        def_n, def_l, def_m, def_scale = orbital_presets[selected_preset]
    else:
        def_n, def_l, def_m, def_scale = 1, 0, 0, 5

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        n = st.number_input("Principal (n)", min_value=1, max_value=7, value=def_n, step=1)
    with col2:
        l = st.number_input("Angular (l)", min_value=0, max_value=max(0, n-1), value=min(def_l, n-1), step=1, key=f"l_k_{n}")
    with col3:
        m = st.number_input("Magnetic (m)", min_value=-l, max_value=l, value=int(np.clip(def_m, -l, l)), step=1, key=f"m_k_{n}_{l}")
    with col4:
        scale = st.slider("Plot Scale (Å)", min_value=1, max_value=60, value=def_scale)
    with col5:
        threshold = st.slider("PDF Cutoff Threshold", min_value=0.0, max_value=0.4, value=0.15, step=0.05, help="BPhO PDF specifies ignoring values < 0.15 max density")

    orbital_letters = {0: 's', 1: 'p', 2: 'd', 3: 'f', 4: 'g', 5: 'h', 6: 'i'}
    subshell_name = f"{n}{orbital_letters.get(l, '?')}"
    st.info(f"**Selected Quantum State:** `{subshell_name}` Orbital (n={n}, l={l}, m={m}) | Boundary Box: `[-{scale} Å, +{scale} Å]`")

    st.markdown("---")
    st.subheader("1. 2D Probability Density Slice (z-plane)")
    
    z_slice = st.slider("Z-Plane Depth (Å)", min_value=float(-scale), max_value=float(scale), value=0.0, step=0.1)
    
    res_2d = 250
    x_vals = np.linspace(-scale, scale, res_2d)
    y_vals = np.linspace(-scale, scale, res_2d)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.full_like(X, z_slice)
    
    psi_sq_2d = hydrogenic_wavefunction(X, Y, Z, n, l, m)
    psi_sq_2d_filtered = np.where(psi_sq_2d < threshold, np.nan, psi_sq_2d)
    
    fig_2d = go.Figure(data=go.Heatmap(
        z=psi_sq_2d_filtered,
        x=x_vals,
        y=y_vals,
        colorscale='Magma',
        showscale=True,
        zmin=threshold,
        zmax=1.0
    ))
    
    fig_2d.update_layout(
        title=f"2D Probability Density Cut at z = {z_slice:.1f} Å for {subshell_name} (m={m})",
        xaxis_title="x (Å)",
        yaxis_title="y (Å)",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=650,
        height=650
    )
    fig_2d.update_yaxes(scaleanchor="x", scaleratio=1)
    st.plotly_chart(fig_2d, use_container_width=True)

    st.markdown("---")
    st.subheader("2. 3D Volume Visualization & Isosurfaces")
    
    res_3d = 45
    val = np.linspace(-scale, scale, res_3d)
    X3, Y3, Z3 = np.meshgrid(val, val, val, indexing='ij')
    psi_sq_3d = hydrogenic_wavefunction(X3, Y3, Z3, n, l, m)
    
    fig_3d = go.Figure(data=go.Volume(
        x=X3.flatten(),
        y=Y3.flatten(),
        z=Z3.flatten(),
        value=psi_sq_3d.flatten(),
        isomin=threshold,
        isomax=1.0,
        opacity=0.25,
        surface_count=12,
        colorscale='Magma'
    ))
    
    fig_3d.update_layout(
        title=f"3D Probability Density Isosurfaces for {subshell_name} (m={m})",
        scene=dict(
            xaxis_title='x (Å)',
            yaxis_title='y (Å)',
            zaxis_title='z (Å)'
        ),
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=700,
        height=700
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Hydrogenic Orbitals

        #### 1. 3D Time-Independent Schrödinger Equation
        For a single-electron atom with atomic number $Z$, the spatial wavefunction $\psi_{nlm}(r, \theta, \phi)$ in spherical coordinates decomposes into separable radial and angular components:
        $$ \psi_{nlm}(r, \theta, \phi) = R_{nl}(r) Y_l^m(\theta, \phi) $$

        #### 2. Radial Wavefunction $R_{nl}(r)$ & Associated Laguerre Polynomials
        The radial solution depends on principal quantum number $n$ ($1, 2, 3, \dots$) and orbital angular momentum number $l$ ($0 \le l \le n-1$):
        $$ R_{nl}(r) = \sqrt{\left(\frac{2Z}{n a_0}\right)^3 \frac{(n-l-1)!}{2n [(n+l)!]^3}} \cdot \rho^l e^{-\rho/2} L_{n-l-1}^{2l+1}(\rho), \quad \rho = \frac{2 Z r}{n a_0} $$
        where $a_0 = 0.529 \text{ \AA}$ is the Bohr radius and $L_k^k(\rho)$ are Associated Laguerre polynomials.

        #### 3. Angular Wavefunction $Y_l^m(\theta, \phi)$ & Spherical Harmonics
        The angular shape depends on $l$ and magnetic quantum number $m$ ($-l \le m \le l$). Real spherical harmonics are formed from Associated Legendre polynomials $P_l^m(\cos\theta)$ to represent physical atomic orbital lobes ($s, p, d, f, g$):
        * **$s$-orbitals ($l=0$):** Spherically symmetric density distributions.
        * **$p$-orbitals ($l=1$):** Dumbbell-shaped directional lobes.
        * **$d$-orbitals ($l=2$) & $f$-orbitals ($l=3$):** Multi-lobed cloverleaf and complex node geometries.

        The probability density of finding the electron at point $(r, \theta, \phi)$ is given by $|\psi_{nlm}(r, \theta, \phi)|^2$.
        """)

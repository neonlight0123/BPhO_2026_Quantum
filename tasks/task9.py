import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

h = 6.62607004e-34
m_e = 9.10938356e-31
c = 2.99792458e8
e = 1.60217662e-19

def render():
    st.header("Task 9: Compton Scattering")
    st.markdown("""
        **Objective:** Plot fractional wavelength shift $\\Delta\\lambda / \\lambda$, electron recoil speed $v/c$, and electron recoil angle $\\phi$ vs photon scattering angle $\\theta$.
    """)
    
    energies_kev = [50, 100, 200, 500, 1000]
    
    theta_deg = np.linspace(0, 180, 500)
    # Avoid division by zero at exactly 0
    theta_deg[0] = 1e-5 
    theta_rad = np.radians(theta_deg)
    
    fig = make_subplots(rows=2, cols=2, subplot_titles=(
        "Fractional Wavelength Shift Δλ/λ", 
        "Electron Recoil Speed v/c", 
        "Electron Recoil Angle φ (deg)"
    ), vertical_spacing=0.15, horizontal_spacing=0.1)
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, E_kev in enumerate(energies_kev):
        color = colors[i % len(colors)]
        name = f"E={E_kev}keV"
        
        # Energy to wavelength
        E_joules = E_kev * 1000 * e
        lambda_0 = (h * c) / E_joules
        
        # Delta lambda
        delta_lambda = (h / (m_e * c)) * (1 - np.cos(theta_rad))
        lambda_prime = lambda_0 + delta_lambda
        
        frac_shift = delta_lambda / lambda_0
        
        # Recoil speed
        # v/c = sqrt(1 - (m_e c^2 / (hc/lambda_0 - hc/lambda_prime + m_e c^2))^2 )
        rest_energy = m_e * c**2
        kinetic_energy = (h * c / lambda_0) - (h * c / lambda_prime)
        gamma = (kinetic_energy + rest_energy) / rest_energy
        v_over_c = np.sqrt(1 - (1 / gamma**2))
        
        # Recoil angle phi
        # tan(phi) = sin(theta) / ( (1 + h/(m_e c lambda_0)) * (1 - cos(theta)) )
        factor = 1 + (h / (m_e * c * lambda_0))
        tan_phi = np.sin(theta_rad) / (factor * (1 - np.cos(theta_rad)))
        phi_rad = np.arctan(tan_phi)
        phi_deg = np.degrees(phi_rad)
        
        # Plot fractional shift
        fig.add_trace(go.Scatter(x=theta_deg, y=frac_shift, mode='lines', name=name, line=dict(color=color), legendgroup=name), row=1, col=1)
        
        # Plot recoil speed
        fig.add_trace(go.Scatter(x=theta_deg, y=v_over_c, mode='lines', name=name, line=dict(color=color), legendgroup=name, showlegend=False), row=1, col=2)
        
        # Plot recoil angle
        fig.add_trace(go.Scatter(x=theta_deg, y=phi_deg, mode='lines', name=name, line=dict(color=color), legendgroup=name, showlegend=False), row=2, col=1)
        
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=800,
        hovermode="x unified"
    )
    
    fig.update_xaxes(title_text="Photon scattering angle θ (deg)", row=1, col=1)
    fig.update_yaxes(title_text="Δλ/λ", row=1, col=1)
    
    fig.update_xaxes(title_text="Photon scattering angle θ (deg)", row=1, col=2)
    fig.update_yaxes(title_text="Electron recoil speed v/c", row=1, col=2)
    
    fig.update_xaxes(title_text="Photon scattering angle θ (deg)", row=2, col=1)
    fig.update_yaxes(title_text="Electron recoil angle φ (deg)", range=[0, 90], row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Compton Scattering

        #### 1. Quantum Relativistic Scattering
        Compton scattering demonstrates the particle nature of X-ray photons colliding with free stationary electrons ($m_e$). Treating the collision in 2D using conservation of relativistic energy and momentum:

        #### 2. Fractional Wavelength Shift ($\Delta\lambda / \lambda_0$)
        The shift in photon wavelength $\Delta\lambda = \lambda' - \lambda_0$ depends exclusively on the photon scattering angle $\theta$:
        $$ \Delta\lambda = \frac{h}{m_e c} (1 - \cos\theta) \implies \frac{\Delta\lambda}{\lambda_0} = \frac{h}{m_e c \lambda_0} (1 - \cos\theta) $$
        where $\lambda_C = \frac{h}{m_e c} \approx 2.426 \times 10^{-12} \text{ m}$ is the Compton wavelength of the electron.

        #### 3. Electron Recoil Speed ($v/c$) & Recoil Angle ($\phi$)
        Applying relativistic kinetic energy $K_e = E_{\gamma,0} - E_{\gamma}' = m_e c^2 (\gamma - 1)$:
        * **Recoil Speed ($v/c$):** $\frac{v}{c} = \sqrt{1 - \left( \frac{m_e c^2}{K_e + m_e c^2} \right)^2}$
        * **Recoil Angle ($\phi$):** $\tan\phi = \frac{\sin\theta}{\left(1 + \frac{h}{m_e c \lambda_0}\right) (1 - \cos\theta)}$
        As photon scattering angle $\theta$ increases toward $180^\circ$ (backscattering), the electron absorbs maximum recoil momentum and speed.
        """)

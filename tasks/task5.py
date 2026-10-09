import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render():
    st.header("Task 5: Hydrogen Spectra")
    st.markdown(r"""
        **Objective:** Create a graph of photon energy vs wavelength for photon emissions from hydrogen atoms due to transitions between electron energy levels.
        
        The photon energy for a transition from state $n$ to $m$ (where $n > m$) is:
        $$ E = 13.6 \left( \frac{1}{m^2} - \frac{1}{n^2} \right) \text{eV} $$
        And the corresponding wavelength is given by the Balmer-Rydberg formula:
        $$ \lambda_{nm} = \frac{91.13\text{nm}}{\frac{1}{m^2} - \frac{1}{n^2}} $$
    """)
    
    series_data = {
        "Lyman (m=1)": {"m": 1, "color": "#FF79C6"},   # Neon Pink
        "Balmer (m=2)": {"m": 2, "color": "#50FA7B"},  # Neon Green
        "Paschen (m=3)": {"m": 3, "color": "#8BE9FD"}, # Cyan
        "Brackett (m=4)": {"m": 4, "color": "#F1FA8C"},# Yellow
        "Pfund (m=5)": {"m": 5, "color": "#FFB86C"}    # Orange
    }
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_series = st.multiselect("Select Spectral Series", list(series_data.keys()), default=list(series_data.keys()))
    with col2:
        st.write("") # Spacing
        st.write("")
        log_scale = st.checkbox("Use Logarithmic X-Axis", value=True)
    
    if selected_series:
        fig = go.Figure()
        
        # Max n to compute to show the decay towards the series limit
        max_n = 50
        
        for s_name in selected_series:
            m = series_data[s_name]["m"]
            color = series_data[s_name]["color"]
                
            n_vals = np.arange(m + 1, max_n + 1)
            
            # Energy in eV
            E = 13.6 * (1/(m**2) - 1/(n_vals**2))
            
            # Wavelength in nm
            wl = 91.13 / (1/(m**2) - 1/(n_vals**2))
            
            fig.add_trace(go.Scatter(
                x=wl, y=E,
                mode='markers',
                marker=dict(symbol='circle', size=10, color=color, line=dict(width=1, color='#F8F8F2')),
                name=s_name,
                hovertemplate="n: %{customdata}<br>Wavelength: %{x:.2f} nm<br>Energy: %{y:.3f} eV<extra></extra>",
                customdata=n_vals
            ))
            
            # Optimize dashed lines by combining them into a single trace per series
            x_lines = []
            y_lines = []
            for n_val, x_val, y_val in zip(n_vals, wl, E):
                x_lines.extend([x_val, x_val, None])
                y_lines.extend([0, y_val, None])
                
            fig.add_trace(go.Scattergl(
                x=x_lines, y=y_lines,
                mode='lines',
                line=dict(color=color, width=2, dash="dash"),
                opacity=0.7,
                showlegend=False,
                hoverinfo='skip'
            ))

        fig.update_layout(
            title="Bohr Model of Hydrogenic Atom Photon Emissions (Z=1)",
            xaxis_title="Wavelength λ (nm)",
            yaxis_title="Photon Energy (eV)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="closest",
            xaxis=dict(type='log' if log_scale else 'linear'),
            yaxis=dict(range=[0, 14])
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Hydrogen Emission Spectra

        #### 1. Bohr Model of the Hydrogenic Atom
        Niels Bohr postulated that electrons in a hydrogen atom revolve in discrete, non-radiating circular orbits where angular momentum is quantized: $L = m_e v r = n \hbar$ (where $n = 1, 2, 3, \dots$).

        Solving Coulomb attraction with quantized angular momentum yields discrete energy levels for atomic number $Z$:
        $$ E_n = -\frac{m_e Z^2 e^4}{8 \varepsilon_0^2 h^2} \frac{1}{n^2} \approx -13.6 \frac{Z^2}{n^2} \text{ eV} $$

        #### 2. Photon Emission & Spectral Lines
        When an electron transitions from a higher energy state $n$ to a lower state $m$ ($n > m$), it emits a single photon with energy $\Delta E = E_n - E_m = h f$:
        $$ E_{\text{photon}} = 13.6 Z^2 \left( \frac{1}{m^2} - \frac{1}{n^2} \right) \text{ eV} $$

        The corresponding emission wavelength $\lambda$ follows the Rydberg formula:
        $$ \frac{1}{\lambda} = R_{\infty} Z^2 \left( \frac{1}{m^2} - \frac{1}{n^2} \right) \implies \lambda = \frac{91.13 \text{ nm}}{Z^2 \left( \frac{1}{m^2} - \frac{1}{n^2} \right)} $$

        * **Lyman Series ($m=1$):** Transitions to ground state (Ultraviolet region).
        * **Balmer Series ($m=2$):** Transitions to $n=2$ (Visible light spectrum).
        * **Paschen ($m=3$), Brackett ($m=4$), Pfund ($m=5$):** Infrared region.
        """)

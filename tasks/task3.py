import streamlit as st
import numpy as np
import plotly.graph_objects as go
import scipy.constants as const

# Physics Constants
h = 6.626e-34
c = 2.998e8
k_B = 1.381e-23
R = 8.314

def B_lambda(wavelength_nm, T):
    wl_m = wavelength_nm * 1e-9
    # Avoid division by zero or overflow
    with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
        exponent = (h * c) / (wl_m * k_B * T)
        # Prevent overflow in exp
        exponent = np.clip(exponent, None, 700) 
        spectral_radiance = (2 * h * c**2) / (wl_m**5) * (1 / (np.exp(exponent) - 1))
    return spectral_radiance

def heat_capacity(T, f_E):
    # Convert Einstein frequency to Einstein Temperature
    T_E = (h * f_E) / k_B
    with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
        x = T_E / T
        x = np.clip(x, None, 700)
        exp_x = np.exp(x)
        C = 3 * R * (x**2 * exp_x) / ((exp_x - 1)**2)
    # Handle T=0 limits
    C = np.where(T == 0, 0, C)
    return C

def render():
    st.header("Task 3: Black Body Radiation & Heat Capacity")
    
    tab1, tab2 = st.tabs(["Black Body Radiation", "Einstein Solid Heat Capacity"])
    
    with tab1:
        st.markdown("**Planck's Law:** Model the spectral irradiance of a black body across different temperatures.")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### Temperatures (K)")
            t1 = st.slider("T1", 3000, 7000, 4000, 100)
            t2 = st.slider("T2", 3000, 7000, 5000, 100)
            t3 = st.slider("T3", 3000, 7000, 6000, 100)
        
        with col2:
            wavelengths = np.linspace(50, 3000, 500) # nm
            fig1 = go.Figure()
            
            for t, color in zip([t1, t2, t3], ['#8BE9FD', '#50FA7B', '#FFB86C']):
                B = B_lambda(wavelengths, t)
                # To match standard solar irradiance graphs, we can plot spectral irradiance W/m^2/nm
                # Our B_lambda is W/m^2/sr/m. Let's just scale it or plot raw shape.
                # Actually, presentation plots W m^-2 nm^-1, which includes a solid angle factor (pi) 
                # and wavelength scaling. Let's just plot the theoretical shape.
                fig1.add_trace(go.Scatter(x=wavelengths, y=B * 1e-9 * np.pi, mode='lines', name=f"T = {t}K", line=dict(color=color)))
                
            fig1.update_layout(
                title="Planck Blackbody Spectrum",
                xaxis_title="Wavelength (nm)",
                yaxis_title="Spectral Irradiance",
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified"
            )
            st.plotly_chart(fig1, use_container_width=True)
            
    with tab2:
        st.markdown("**Einstein's Model:** Solid molar heat capacity $C$ vs temperature.")
        
        materials = {
            "Gold (Au)": 0.2855e13,
            "Copper (Cu)": 0.5769e13,
            "Titanium (Ti)": 0.7054e13,
            "Aluminium (Al)": 0.7188e13,
            "Iron (Fe)": 0.7893e13,
            "Silicon (Si)": 1.0832e13,
            "Carbon (C)": 3.7451e13
        }
        
        temperatures = np.linspace(1, 800, 400) # K
        fig2 = go.Figure()
        
        for mat, f_E in materials.items():
            C = heat_capacity(temperatures, f_E)
            fig2.add_trace(go.Scatter(x=temperatures, y=C, mode='lines', name=mat))
            
        # Dulong-Petit limit
        fig2.add_trace(go.Scatter(
            x=[0, 800], y=[3*R, 3*R],
            mode='lines',
            name="Dulong-Petit Limit (3R)",
            line=dict(dash='dash', color='#F8F8F2', width=1)
        ))
        
        fig2.update_layout(
            title="Einstein Model of Solid Molar Heat Capacity",
            xaxis_title="Temperature (K)",
            yaxis_title="Molar Heat Capacity (J/mol·K)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Black Body Radiation & Heat Capacity

        #### 1. Planck's Black Body Radiation Law
        Classical physics (Rayleigh-Jeans law) failed at short wavelengths, predicting infinite energy (the *Ultraviolet Catastrophe*). In 1900, Max Planck solved this by postulating that electromagnetic energy is quantized in discrete packets $E = h f$.

        Planck's spectral radiance formula for a black body at absolute temperature $T$ as a function of wavelength $\lambda$ is:
        $$ B(\lambda, T) = \frac{2 h c^2}{\lambda^5} \frac{1}{\exp\left(\frac{h c}{\lambda k_B T}\right) - 1} $$
        * As $T$ increases, the total radiated power increases ($\propto T^4$, Stefan-Boltzmann law).
        * The peak wavelength shifts to shorter wavelengths ($\lambda_{\text{max}} T = b$, Wien's displacement law).

        #### 2. Einstein's Model of Molar Heat Capacity of Solids
        Albert Einstein extended Planck's quantum concept to solid lattice vibrations by treating all $N_A$ atoms in a crystal as independent 3D quantum harmonic oscillators vibrating at a single characteristic *Einstein frequency* $f_E$.

        The internal energy of 1 mole of solid is $U = 3 N_A \langle E \rangle$, yielding molar heat capacity:
        $$ C_V = \frac{dU}{dT} = 3 R \left( \frac{x^2 e^x}{(e^x - 1)^2} \right), \quad \text{where } x = \frac{h f_E}{k_B T} = \frac{T_E}{T} $$
        * **High Temperatures ($T \gg T_E$):** $C_V \to 3R \approx 24.9 \text{ J/(mol}\cdot\text{K)}$, recovering the classical **Dulong-Petit limit**.
        * **Low Temperatures ($T \to 0$):** Thermal energy is insufficient to excite quantum vibrational states, causing heat capacity to freeze out exponentially to zero ($C_V \to 0$).
        """)

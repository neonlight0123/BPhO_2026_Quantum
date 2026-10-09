import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Physics Constants
h = 6.626e-34
m_e = 9.109e-31
e = 1.602e-19
r_bulb = 65.0 # mm (Screen radius R)
d1 = 0.213 # nm (d1 lattice spacing)
d2 = 0.123 # nm (d2 lattice spacing)

def render():
    st.header("Task 6: Electron Diffraction")
    st.markdown("""
        **Objective:** Model the de Broglie wavelength of accelerated electrons diffracting through polycrystalline graphite layers ($d_1 = 0.213\\text{ nm}, d_2 = 0.123\\text{ nm}$), forming concentric rings on a spherical phosphor screen ($R = 65\\text{ mm}$).
    """)
    
    tab1, tab2, tab3 = st.tabs([
        "Ring Radius x vs Voltage V", 
        "Validation: 1/√V vs sin(φ/2)",
        "2D Phosphor Screen Rings"
    ])
    
    V_kv = np.linspace(1.0, 5.0, 500)
    V = V_kv * 1000 # in Volts
    wavelength = h / np.sqrt(2 * m_e * e * V) # in meters
    
    with tab1:
        fig1 = go.Figure()
        
        for d_nm, name, color in [(d1, "d1 = 0.213 nm", '#8BE9FD'), (d2, "d2 = 0.123 nm", '#FF5555')]:
            d = d_nm * 1e-9 # meters
            sin_theta = wavelength / (2 * d)
            valid = sin_theta <= 1.0
            
            theta = np.arcsin(sin_theta[valid])
            x = r_bulb * np.tan(2 * theta) # Ring radius x = R * tan(2*theta) in mm
            
            fig1.add_trace(go.Scatter(
                x=V_kv[valid], y=x,
                mode='lines',
                name=name,
                line=dict(color=color, width=2.5)
            ))

        fig1.update_layout(
            title="Diffraction Ring Radius x vs Accelerating Voltage V",
            xaxis_title="Accelerating Voltage V (kV)",
            yaxis_title="Ring Radius x (mm)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with tab2:
        fig2 = go.Figure()
        
        for d_nm, name, color in [(d1, "d1 = 0.213 nm", '#8BE9FD'), (d2, "d2 = 0.123 nm", '#FF5555')]:
            d = d_nm * 1e-9 # meters
            sin_theta = wavelength / (2 * d)
            valid = sin_theta <= 1.0
            
            inv_sqrt_V = 1 / np.sqrt(V[valid])
            
            fig2.add_trace(go.Scatter(
                x=sin_theta[valid], y=inv_sqrt_V,
                mode='lines',
                name=name,
                line=dict(color=color, width=2.5)
            ))

        fig2.update_layout(
            title="Validation Graph (1/√V vs sin(θ))",
            xaxis_title="sin(θ) = sin(φ/2)",
            yaxis_title="1/√V (V<sup>-1/2</sup>)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.markdown("### Interactive 2D Phosphor Screen Rings")
        v_sim = st.slider("Accelerating Voltage V (kV)", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
        
        v_sim_v = v_sim * 1000
        wl_sim = h / np.sqrt(2 * m_e * e * v_sim_v)
        
        x1 = r_bulb * np.tan(2 * np.arcsin(wl_sim / (2 * d1 * 1e-9)))
        x2 = r_bulb * np.tan(2 * np.arcsin(wl_sim / (2 * d2 * 1e-9)))
        
        fig3 = go.Figure()
        
        # Screen background circle
        t_ring = np.linspace(0, 2*np.pi, 200)
        fig3.add_trace(go.Scatter(
            x=r_bulb*np.cos(t_ring), y=r_bulb*np.sin(t_ring),
            mode='lines', line=dict(color='#44475A', width=2),
            name='Phosphor Screen Edge (R=65mm)'
        ))
        
        # Ring 1 (d1 = 0.213 nm)
        fig3.add_trace(go.Scatter(
            x=x1*np.cos(t_ring), y=x1*np.sin(t_ring),
            mode='lines', line=dict(color='#8BE9FD', width=3),
            name=f'Ring 1 (d1=0.213nm): x = {x1:.2f} mm'
        ))
        
        # Ring 2 (d2 = 0.123 nm)
        fig3.add_trace(go.Scatter(
            x=x2*np.cos(t_ring), y=x2*np.sin(t_ring),
            mode='lines', line=dict(color='#FF5555', width=3),
            name=f'Ring 2 (d2=0.123nm): x = {x2:.2f} mm'
        ))
        
        # Central electron spot
        fig3.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers', marker=dict(color='#50FA7B', size=10),
            name='Central Electron Beam'
        ))
        
        fig3.update_layout(
            title=f"Phosphor Screen Diffraction Pattern at V = {v_sim:.2f} kV (λ = {wl_sim*1e12:.2f} pm)",
            xaxis=dict(range=[-70, 70], scaleanchor="y", scaleratio=1, title="x (mm)"),
            yaxis=dict(range=[-70, 70], title="y (mm)"),
            template="plotly_dark",
            plot_bgcolor='#0e1117',
            paper_bgcolor='rgba(0,0,0,0)',
            width=500, height=500
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Electron Diffraction

        #### 1. De Broglie Wavelength of Accelerated Electrons
        Louis de Broglie hypothesized that all matter possesses wave-like properties. An electron of rest mass $m_e$ accelerated through a potential difference $V$ gains kinetic energy $e V = p^2 / (2 m_e)$, yielding a de Broglie wavelength:
        $$ \lambda = \frac{h}{p} = \frac{h}{\sqrt{2 m_e e V}} $$

        #### 2. Bragg's Law & Ring Formation
        When the electron wave beam strikes polycrystalline graphite layers with atomic plane spacing $d$, constructive interference occurs according to Bragg's condition:
        $$ 2 d \sin\theta = n \lambda $$
        Since the diffraction scatter angle is $\phi = 2\theta$, this simplifies to:
        $$ \sin\left(\frac{\phi}{2}\right) = \frac{n \lambda}{2 d} = \frac{n h}{2 d \sqrt{2 m_e e V}} $$

        #### 3. Linear Validation Graph
        Rearranging terms shows that $1/\sqrt{V}$ is directly proportional to $\sin(\phi/2)$:
        $$ \frac{1}{\sqrt{V}} = \left( \frac{2 d \sqrt{2 m_e e}}{n h} \right) \sin\left(\frac{\phi}{2}\right) $$
        Plotting $1/\sqrt{V}$ vs $\sin(\phi/2)$ yields a straight line whose slope allows precise experimental determination of the graphite interplanar lattice spacing $d$ ($d_1 = 0.213$ nm, $d_2 = 0.123$ nm).
        """)

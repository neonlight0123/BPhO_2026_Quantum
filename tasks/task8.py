import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render():
    st.header("Task 8: Quantum Cryptography & Entanglement")
    st.markdown(r"""
        **Objective:** Build an interactive visual calculator for classical local realism vs quantum mechanics (Bell state entanglement) mismatch probabilities as a function of polarizer detector angles $\theta$ (Alice) and $\phi$ (Bob).
    """)
    
    st.subheader("1. Mismatch Probability Calculator (Angles θ and φ)")
    
    col1, col2 = st.columns(2)
    with col1:
        theta_deg = st.slider("Alice's Polarizer Angle θ (°)", min_value=0, max_value=180, value=30, step=1)
    with col2:
        phi_deg = st.slider("Bob's Polarizer Angle φ (°)", min_value=0, max_value=180, value=60, step=1)
        
    theta = np.radians(theta_deg)
    phi = np.radians(phi_deg)
    
    # PDF formulas
    # Classical local realism mismatch: P_c = 1 - cos^2(theta)cos^2(phi) - sin^2(theta)sin^2(phi) = sin^2(theta) + sin^2(phi) - 2 sin^2(theta) sin^2(phi)
    p_mismatch_c = np.sin(theta)**2 + np.sin(phi)**2 - 2 * np.sin(theta)**2 * np.sin(phi)**2
    # Quantum mechanics mismatch: P_q = sin^2(phi - theta)
    p_mismatch_q = np.sin(phi - theta)**2
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Classical Mismatch P_classical", f"{p_mismatch_c:.4f} ({p_mismatch_c*100:.1f}%)")
    c2.metric("Quantum Mismatch P_quantum", f"{p_mismatch_q:.4f} ({p_mismatch_q*100:.1f}%)")
    c3.metric("Quantum Match P_match", f"{(1 - p_mismatch_q):.4f}")
    c4.metric("Aspect Experiment Violation |P_q - P_c|", f"{abs(p_mismatch_q - p_mismatch_c):.4f}", delta="Violation!" if abs(p_mismatch_q - p_mismatch_c) > 0.01 else "Equal")

    # Sweep graph vs Bob's angle phi (0° to 180°)
    phi_sweep_deg = np.linspace(0, 180, 500)
    phi_sweep_rad = np.radians(phi_sweep_deg)
    
    p_c_sweep = np.sin(theta)**2 + np.sin(phi_sweep_rad)**2 - 2 * np.sin(theta)**2 * np.sin(phi_sweep_rad)**2
    p_q_sweep = np.sin(phi_sweep_rad - theta)**2
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=phi_sweep_deg, y=p_c_sweep,
        mode='lines',
        name=f"Classical Local Realism (Malus' Law, θ={theta_deg}°)",
        line=dict(color='#6272A4', dash='dash', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=phi_sweep_deg, y=p_q_sweep,
        mode='lines',
        name=f"Quantum Entanglement (Bell State, θ={theta_deg}°)",
        line=dict(color='#FF5555', width=2.5)
    ))
    
    # Current selection markers
    fig.add_trace(go.Scatter(
        x=[phi_deg], y=[p_mismatch_c],
        mode='markers', marker=dict(size=12, color='#8BE9FD', symbol='circle'),
        name=f"Classical Choice (P={p_mismatch_c:.3f})"
    ))
    
    fig.add_trace(go.Scatter(
        x=[phi_deg], y=[p_mismatch_q],
        mode='markers', marker=dict(size=12, color='#FF5555', symbol='diamond'),
        name=f"Quantum Choice (P={p_mismatch_q:.3f})"
    ))

    fig.update_layout(
        title=f"Mismatch Probability vs Bob's Polarizer Angle φ for Fixed Alice Angle θ = {theta_deg}°",
        xaxis_title="Bob's Polarizer Angle φ (degrees)",
        yaxis_title="Mismatch Probability P(mismatch)",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        xaxis=dict(range=[0, 180]),
        yaxis=dict(range=[0, 1.05])
    )
    
    st.plotly_chart(fig, use_container_width=True)



    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Quantum Cryptography & Entanglement

        #### 1. Photonic Polarization & Malus' Law
        In quantum key distribution protocols (e.g., BB84 or Ekert91), Alice and Bob measure pairs of entangled photons with polarizers set at orientation angles $\theta$ and $\phi$.

        #### 2. Classical vs. Quantum Mismatch Probabilities
        * **Classical Local Realism (Malus' Law):** If photons possessed predetermined hidden properties prior to measurement, the probability that Alice and Bob record conflicting detection outcomes (mismatch) is:
          $$ P_{\text{classical}}(\text{mismatch}) = \sin^2\theta + \sin^2\phi - 2\sin^2\theta\sin^2\phi $$
        * **Quantum Mechanics (Wavefunction Collapse):** Entangled photon pairs share a joint wave state. Alice measuring photon A at angle $\theta$ instantly collapses the wavefunction of photon B. The quantum mismatch probability depends solely on relative detector angle $(\phi - \theta)$:
          $$ P_{\text{quantum}}(\text{mismatch}) = \sin^2(\phi - \theta) $$

        #### 3. Eavesdropping Detection
        If an eavesdropper (Eve) intercepts a photon en route, her measurement collapses the state prematurely, altering Bob's measurement statistics. By comparing mismatch probabilities on a sample subset of bits, Alice and Bob can detect eavesdropping with absolute security guaranteed by the laws of quantum mechanics.
        """)

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

h = 6.626e-34
m_e = 9.109e-31
e = 1.602e-19

def render():
    st.header("Task 7: Particle in a 1D Box & Uncertainty Principle")
    st.markdown(r"""
        **Objective:** Solve the 1D Schrödinger equation for a particle of mass $m$ in an infinite potential well of width $a$ ($0 \le x \le a$).
        $$\psi_n(x) = \sqrt{\frac{2}{a}} \sin\left(\frac{n\pi x}{a}\right), \quad E_n = \frac{n^2 \pi^2 \hbar^2}{2 m a^2} = \frac{h^2 n^2}{8 m a^2}$$
    """)
    
    st.subheader("1. Quantum States, Wavefunctions & Probability Densities")
    col1, col2 = st.columns(2)
    with col1:
        a_angstroms = st.slider("Box Width a (Å)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    with col2:
        max_n = st.slider("Max Quantum Number (n)", min_value=1, max_value=6, value=4, step=1)
        
    a = a_angstroms * 1e-10 # meters
    n_vals = np.arange(1, max_n + 1)
    E_joules = (h**2 * n_vals**2) / (8 * m_e * a**2)
    E_eV = E_joules / e
    
    # 3 Subplots: Energy vs n, Wavefunction psi_n(x), Probability Density |psi_n(x)|^2
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Energy Levels E_n", "Wavefunction ψ_n(x)", "Probability Density |ψ_n(x)|²"),
        horizontal_spacing=0.08
    )
    
    # Subplot 1: Energy vs n
    n_smooth = np.linspace(0, max_n, 100)
    E_smooth = ((h**2 * n_smooth**2) / (8 * m_e * a**2)) / e
    fig.add_trace(go.Scatter(
        x=n_smooth, y=E_smooth,
        mode='lines', line=dict(dash='dash', color='#6272A4', width=1),
        showlegend=False
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=n_vals, y=E_eV,
        mode='markers', marker=dict(size=9, color='#8BE9FD'),
        name="Energy Levels"
    ), row=1, col=1)
    
    # Subplots 2 & 3: Wavefunctions & Probability Densities
    x_angstroms = np.linspace(0, a_angstroms, 500)
    x = x_angstroms * 1e-10
    colors = ['#8BE9FD', '#50FA7B', '#FFB86C', '#FF79C6', '#BD93F9', '#FF5555']
    
    for n in range(1, max_n + 1):
        col_c = colors[(n-1) % len(colors)]
        psi = np.sqrt(2 / a) * np.sin(n * np.pi * x / a)
        psi_sq = psi**2
        
        # Scale for clean plotting
        psi_scaled = psi * np.sqrt(1e-10)
        psi_sq_scaled = psi_sq * 1e-10
        
        fig.add_trace(go.Scatter(
            x=x_angstroms, y=psi_scaled,
            mode='lines', name=f"n={n}",
            line=dict(color=col_c, width=1.8),
            showlegend=False
        ), row=1, col=2)
        
        fig.add_trace(go.Scatter(
            x=x_angstroms, y=psi_sq_scaled,
            mode='lines', name=f"n={n} (E={E_eV[n-1]:.1f} eV)",
            line=dict(color=col_c, width=1.8)
        ), row=1, col=3)
        
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
    )
    fig.update_xaxes(title_text="Quantum number n", row=1, col=1)
    fig.update_yaxes(title_text="Energy (eV)", row=1, col=1)
    fig.update_xaxes(title_text="x (Å)", row=1, col=2)
    fig.update_yaxes(title_text="ψ_n(x) (scaled)", row=1, col=2)
    fig.update_xaxes(title_text="x (Å)", row=1, col=3)
    fig.update_yaxes(title_text="|ψ_n(x)|² (x 10¹⁰)", row=1, col=3)
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Extension: Heisenberg's Uncertainty Principle Verification")
    
    hbar = h / (2 * np.pi)
    
    # Interactive verification table
    n_sel = st.slider("Select Quantum State n for Verification", min_value=1, max_value=10, value=1, step=1)
    
    delta_x = a * np.sqrt(1/12 - 1/(2 * n_sel**2 * np.pi**2))
    delta_p = (n_sel * np.pi * hbar) / a
    product_hbar = np.sqrt((n_sel**2 * np.pi**2)/12 - 0.5)
    
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Position Uncertainty Δx", f"{delta_x*1e10:.3f} Å")
    c_m2.metric("Momentum Uncertainty Δp", f"{delta_p:.3e} kg·m/s")
    c_m3.metric("Product Δx Δp / ℏ", f"{product_hbar:.4f}")
    c_m4.metric("Minimum Allowed Limit", "0.5000 ℏ", delta=f"+{(product_hbar-0.5):.4f} ℏ")

    st.markdown(r"""
    #### Analytical Mathematical Proof:
    For a particle in a 1D box of width $a$:
    
    * **Position Uncertainty ($\Delta x$):**
      $$\langle x \rangle = \frac{a}{2}, \quad \langle x^2 \rangle = a^2 \left(\frac{1}{3} - \frac{1}{2n^2\pi^2}\right) \implies \Delta x = a \sqrt{\frac{1}{12} - \frac{1}{2n^2\pi^2}}$$
      
    * **Momentum Uncertainty ($\Delta p$):**
      $$\langle p \rangle = 0, \quad \langle p^2 \rangle = \frac{n^2 \pi^2 \hbar^2}{a^2} \implies \Delta p = \frac{n \pi \hbar}{a}$$
      
    * **Uncertainty Product ($\Delta x \Delta p$):**
      Combining position and momentum variances, the box width $a$ cancels out exactly:
      $$\Delta x \Delta p = \hbar \sqrt{\frac{n^2 \pi^2}{12} - \frac{1}{2}}$$
      
    For the ground state ($n=1$):
    $$\Delta x \Delta p = \hbar \sqrt{\frac{\pi^2}{12} - \frac{1}{2}} \approx 0.568 \hbar > 0.5 \hbar$$
    This proves that **every quantum state** in an infinite potential well strictly satisfies Heisenberg's Uncertainty Principle $\Delta x \Delta p \ge \frac{\hbar}{2}$.
    """)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Particle in a Box & Uncertainty Principle

        #### 1. Quantum Infinite Potential Well
        A particle of mass $m$ confined within a 1D infinite potential well of width $a$ ($V(x) = 0$ for $0 < x < a$, $V(x) = \infty$ elsewhere) satisfies the time-independent Schrödinger equation:
        $$ -\frac{\hbar^2}{2m} \frac{d^2\psi}{dx^2} = E \psi $$

        Applying boundary conditions $\psi(0) = \psi(a) = 0$ yields quantized standing wavefunctions and energy levels:
        $$ \psi_n(x) = \sqrt{\frac{2}{a}} \sin\left(\frac{n\pi x}{a}\right), \quad E_n = \frac{n^2 \pi^2 \hbar^2}{2m a^2} = \frac{h^2 n^2}{8 m a^2} $$
        The probability density of finding the particle at displacement $x$ is $|\psi_n(x)|^2 = \frac{2}{a} \sin^2\left(\frac{n\pi x}{a}\right)$.

        #### 2. Verification of Heisenberg's Uncertainty Principle (Non-Analytical / Numerical Method)
        Rather than relying purely on algebraic proofs, we can verify the Uncertainty Principle by performing continuous numerical integration over the spatial domain $[0, a]$. We approximate the expectation integrals using numerical arrays:
        * **Position Expectation:** $\langle x \rangle = \int_0^a x |\psi_n(x)|^2 dx \approx \sum x_i |\psi_n(x_i)|^2 \Delta x$
        * **Position Variance:** $\langle x^2 \rangle = \int_0^a x^2 |\psi_n(x)|^2 dx \approx \sum x_i^2 |\psi_n(x_i)|^2 \Delta x$
        * **Momentum Variance:** Using the momentum operator $\hat{p} = -i\hbar\frac{d}{dx}$, we compute $\langle p^2 \rangle = \int_0^a \psi_n^*(x) \left(-\hbar^2 \frac{d^2}{dx^2}\right) \psi_n(x) dx$, which can be evaluated numerically using finite difference methods for the second derivative.
        
        The standard deviations are then simply $\Delta x = \sqrt{\langle x^2 \rangle - \langle x \rangle^2}$ and $\Delta p = \sqrt{\langle p^2 \rangle - \langle p \rangle^2}$.

        #### 3. Verification of Heisenberg's Uncertainty Principle (Analytical Method)
        Calculating the exact analytical expectation values yields:
        * **Position Variance ($\Delta x$):** $\langle x \rangle = \frac{a}{2}$, $\langle x^2 \rangle = a^2 \left( \frac{1}{3} - \frac{1}{2n^2\pi^2} \right) \implies \Delta x = a \sqrt{\frac{1}{12} - \frac{1}{2n^2\pi^2}}$
        * **Momentum Variance ($\Delta p$):** $\langle p \rangle = 0$, $\langle p^2 \rangle = 2m E_n = \frac{\pi^2 \hbar^2 n^2}{a^2} \implies \Delta p = \frac{n \pi \hbar}{a}$

        Multiplying position and momentum uncertainties cancels the box width $a$:
        $$ \Delta x \Delta p = \hbar \sqrt{\frac{n^2 \pi^2}{12} - \frac{1}{2}} $$
        For the ground state ($n=1$), $\Delta x \Delta p \approx 0.568 \hbar > 0.5 \hbar$, rigorously proving that the particle in a box strictly obeys Heisenberg's Uncertainty Principle $\Delta x \Delta p \ge \frac{\hbar}{2}$.
        """)

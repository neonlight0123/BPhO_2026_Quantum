import streamlit as st
import numpy as np
import plotly.graph_objects as go
from numba import njit

# Constants
k_B = 1.38e-23

@njit
def simulate_brownian_motion(N, m, M, r, R, v, dt, tmax, Kn_time, box_size, C, n_frames=60):
    # Initialize large particle
    X, Y = 0.0, 0.0
    Vx, Vy = 0.0, 0.0
    
    a = box_size
    x = np.random.uniform(-a, a, N)
    y = np.random.uniform(-a, a, N)
    
    # Ensure no small particle starts inside the large particle
    for i in range(N):
        while np.sqrt(x[i]**2 + y[i]**2) < (R + r):
            x[i] = np.random.uniform(-a, a)
            y[i] = np.random.uniform(-a, a)
    
    theta = np.random.uniform(0, 2*np.pi, N)
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)
    
    t = 0.0
    timer_Kn = 0.0
    
    num_steps = int(tmax / dt)
    frame_interval = max(1, num_steps // n_frames)
    max_saved_frames = (num_steps // frame_interval) + 5
    
    large_X_hist = np.zeros(max_saved_frames)
    large_Y_hist = np.zeros(max_saved_frames)
    small_X_hist = np.zeros((max_saved_frames, N))
    small_Y_hist = np.zeros((max_saved_frames, N))
    time_hist = np.zeros(max_saved_frames)
    
    step = 0
    frame_idx = 0
    
    while t < tmax:
        if step % frame_interval == 0 and frame_idx < max_saved_frames:
            large_X_hist[frame_idx] = X
            large_Y_hist[frame_idx] = Y
            small_X_hist[frame_idx, :] = x
            small_Y_hist[frame_idx, :] = y
            time_hist[frame_idx] = t
            frame_idx += 1
            
        X += Vx * dt
        Y += Vy * dt
        x += vx * dt
        y += vy * dt
        
        for i in range(N):
            dx = x[i] - X
            dy = y[i] - Y
            dist = np.sqrt(dx**2 + dy**2)
            
            if dist <= (R + r):
                nx = dx / dist
                ny = dy / dist
                dvx = vx[i] - Vx
                dvy = vy[i] - Vy
                
                if (dvx*nx + dvy*ny) < 0:
                    u1_n = Vx * nx + Vy * ny
                    u2_n = vx[i] * nx + vy[i] * ny
                    
                    v1_n = ((M - C*m)*u1_n + (1+C)*m*u2_n) / (M + m)
                    v2_n = ((m - C*M)*u2_n + (1+C)*M*u1_n) / (M + m)
                    
                    Vx += (v1_n - u1_n) * nx
                    Vy += (v1_n - u1_n) * ny
                    vx[i] += (v2_n - u2_n) * nx
                    vy[i] += (v2_n - u2_n) * ny

        timer_Kn += dt
        if timer_Kn >= Kn_time:
            timer_Kn = 0.0
            new_theta = np.random.uniform(0, 2*np.pi, N)
            vx = v * np.cos(new_theta)
            vy = v * np.sin(new_theta)
            
        t += dt
        step += 1
        
    return large_X_hist[:frame_idx], large_Y_hist[:frame_idx], small_X_hist[:frame_idx, :], small_Y_hist[:frame_idx, :], time_hist[:frame_idx]

def render():
    st.header("Task 2: Brownian Motion")
    st.markdown("""
        **Objective:** Consider $N$ small particles of mass $m$ and radius $r$ moving randomly, 
        some of which collide with a large particle of mass $M$ and radius $R$. 
        Use a random walk to model smaller particles, conservation of momentum in ZMF for collisions, 
        and **animate the motion** of the system.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.slider("Number of small particles (N)", min_value=100, max_value=2500, value=800, step=100)
        tmax = st.slider("Max simulation time (ps)", min_value=50, max_value=1000, value=300, step=50)
        T_C = st.slider("Temperature (°C)", min_value=0, max_value=500, value=100, step=10)
    with col2:
        mass_ratio = st.slider("Mass ratio (M/m)", min_value=1.0, max_value=50.0, value=5.0, step=1.0, help="Lower ratio makes the large particle movement larger & easier to see!")
        radius_ratio = st.slider("Radius ratio (R/r)", min_value=1.0, max_value=30.0, value=10.0, step=1.0)
        C = st.slider("Coefficient of Restitution (C)", min_value=0.0, max_value=1.0, value=1.0, step=0.05, help="1.0 = Elastic collision, <1.0 = Inelastic / Sticky")
    with col3:
        Kn = st.slider("Knudsen's number (Kn)", min_value=1, max_value=50, value=15, step=1)
        zoom_view = st.select_slider("Axis View Zoom", options=["Tight Zoom on Trail", "Focused View", "Full Bounding Box"], value="Tight Zoom on Trail")
        anim_mode = st.radio("Display Mode", options=["Interactive Animation", "Static Trail Summary"], horizontal=True)

    if st.button("Run Simulation", type="primary"):
        with st.spinner("Calculating Brownian Motion & Building Animation Frames..."):
            m = 28.96e-3 / 6.02e23 # Mass of small particle (kg)
            M = mass_ratio * m
            r = 0.16 # Radius of small particle (nm)
            R = radius_ratio * r
            a = 7 * R # Boundary for small particles
            
            v = np.sqrt(3 * k_B * (T_C + 273) / m) / 1000
            dt = 0.01 * Kn * r / v
            Kn_time = Kn * r / v
            
            large_X, large_Y, small_X, small_Y, time_hist = simulate_brownian_motion(
                int(N), float(m), float(M), float(r), float(R), float(v), float(dt), float(tmax), float(Kn_time), float(a), float(C), n_frames=60
            )
            
            total_f = len(large_X)
            theta_circle = np.linspace(0, 2*np.pi, 60)
            
            # Initial Base Traces (Frame 0 or Final for Static)
            init_k = 0 if anim_mode == "Interactive Animation" else total_f - 1
            
            c_x0 = large_X[init_k] + R * np.cos(theta_circle)
            c_y0 = large_Y[init_k] + R * np.sin(theta_circle)

            fig = go.Figure()
            
            # Trace 0: Small particles
            fig.add_trace(go.Scattergl(
                x=small_X[init_k], y=small_Y[init_k],
                mode='markers',
                marker=dict(size=5, color='#8BE9FD', opacity=0.75, symbol='circle'),
                name='Small Particles'
            ))
            
            # Trace 1: Large particle trail
            fig.add_trace(go.Scattergl(
                x=large_X[:init_k+1], y=large_Y[:init_k+1],
                mode='lines',
                line=dict(width=3, color='#FF5555'),
                name="Large Particle Trail"
            ))
            
            # Trace 2: Start Position (0,0)
            fig.add_trace(go.Scattergl(
                x=[0], y=[0],
                mode='markers',
                marker=dict(size=14, color='#50FA7B', symbol='star', line=dict(color='#000000', width=1)),
                name='Start Position (0,0)'
            ))

            # Trace 3: Current / Final Position
            fig.add_trace(go.Scattergl(
                x=[large_X[init_k]], y=[large_Y[init_k]],
                mode='markers',
                marker=dict(size=16, color='#FF79C6', symbol='star', line=dict(color='#FFFFFF', width=1)),
                name='Current Position'
            ))
            
            # Trace 4: Large Particle Body Circle
            fig.add_trace(go.Scattergl(
                x=c_x0, y=c_y0,
                mode='lines',
                line=dict(color='#FF5555', width=2),
                name=f'Large Particle Body (R={R:.2f}nm)'
            ))

            # Add visual bounding box
            fig.add_shape(type="rect",
                x0=-a, y0=-a, x1=a, y1=a,
                line=dict(color="#F1FA8C", width=2, dash="dash")
            )

            # Determine Zoom Ranges
            max_trail_dist = max(np.max(np.abs(large_X)), np.max(np.abs(large_Y)), R * 2)
            if zoom_view == "Tight Zoom on Trail":
                limit = max(max_trail_dist * 1.5, R * 3)
            elif zoom_view == "Focused View":
                limit = max(max_trail_dist * 3.0, a * 0.4)
            else: # Full Bounding Box
                limit = a * 1.1

            # Build Animation Frames if enabled
            if anim_mode == "Interactive Animation":
                frames = []
                for k in range(total_f):
                    c_xk = large_X[k] + R * np.cos(theta_circle)
                    c_yk = large_Y[k] + R * np.sin(theta_circle)
                    
                    frames.append(go.Frame(
                        data=[
                            go.Scattergl(x=small_X[k], y=small_Y[k]),
                            go.Scattergl(x=large_X[:k+1], y=large_Y[:k+1]),
                            go.Scattergl(x=[0], y=[0]),
                            go.Scattergl(x=[large_X[k]], y=[large_Y[k]]),
                            go.Scattergl(x=c_xk, y=c_yk)
                        ],
                        name=f"f_{k}"
                    ))
                
                updatemenus = [dict(
                    type="buttons",
                    direction="left",
                    showactive=True,
                    x=0.05, y=-0.15,
                    xanchor="right", yanchor="top",
                    buttons=[
                        dict(
                            label="▶ Play",
                            method="animate",
                            args=[None, dict(frame=dict(duration=60, redraw=True), fromcurrent=True, mode="immediate")]
                        ),
                        dict(
                            label="⏸ Pause",
                            method="animate",
                            args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]
                        )
                    ]
                )]

                sliders = [dict(
                    steps=[dict(
                        method="animate",
                        label=f"{time_hist[k]:.0f}ps",
                        args=[[f"f_{k}"], dict(frame=dict(duration=0, redraw=True), mode="immediate")]
                    ) for k in range(total_f)],
                    transition=dict(duration=0),
                    x=0.08, y=-0.15,
                    currentvalue=dict(font=dict(size=12, color="#F8F8F2"), prefix="Time: ", visible=True, xanchor="right"),
                    len=0.88
                )]

                fig.update_layout(
                    updatemenus=updatemenus,
                    sliders=sliders
                )
                fig.frames = frames

            fig.update_layout(
                title=f"Brownian Motion Simulation: t = {tmax} ps | M/m = {mass_ratio}, C = {C}",
                xaxis_title="x / nm",
                yaxis_title="y / nm",
                height=720,
                template="plotly_dark",
                hovermode="closest",
                margin=dict(l=20, r=20, t=50, b=30),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                xaxis=dict(range=[-limit, limit]),
                yaxis=dict(range=[-limit, limit])
            )
            
            fig.update_yaxes(scaleanchor="x", scaleratio=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Brownian Motion
        Brownian motion describes the random, macroscopic jitter of a large particle (e.g., soot or pollen grain of mass $M$, radius $R$) suspended in a fluid due to relentless collisions with smaller gas molecules (mass $m$, radius $r$).

        #### 1. Zero Momentum Frame (ZMF) Collisions
        When a small particle moving at velocity $\mathbf{u}_2$ collides with the large particle moving at $\mathbf{u}_1$, we transform into the center-of-mass (Zero Momentum Frame) with velocity:
        $$ \mathbf{V}_{\text{ZMF}} = \frac{M\mathbf{u}_1 + m\mathbf{u}_2}{M + m} $$

        In 2D rigid sphere collisions, momentum is exchanged exclusively along the unit normal vector $\hat{\mathbf{n}}$ connecting their centers. The post-collision normal velocities with coefficient of restitution $C$ are:
        $$ v_{1,n} = \frac{(M - C m) u_{1,n} + (1+C)m u_{2,n}}{M + m} $$
        $$ v_{2,n} = \frac{(m - C M) u_{2,n} + (1+C)M u_{1,n}}{M + m} $$

        #### 2. Knudsen Number & Molecular Collisions
        Small gas particles execute random walk directions after a collision time interval determined by Knudsen's number $Kn = \text{mean free path} / \text{molecular radius}$. Elastic collisions ($C=1.0$) conserve kinetic energy, while inelastic collisions ($C < 1.0$) demonstrate stickiness and energy dissipation.
        """)



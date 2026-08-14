import streamlit as st
import numpy as np
import plotly.graph_objects as go

def generate_random_walks(n_walks, n_steps, step_size):
    walks = []
    for i in range(n_walks):
        theta = np.random.uniform(0, 2 * np.pi, n_steps)
        dx = step_size * np.cos(theta)
        dy = step_size * np.sin(theta)
        x = np.concatenate(([0], np.cumsum(dx)))
        y = np.concatenate(([0], np.cumsum(dy)))
        walks.append((x, y))
    return walks

def render():
    st.header("Task 1: Random Walk")
    st.markdown("""
        **Objective:** Create a model of a random walk of $N$ steps of size $s$. 
        Each step is in a random direction, with angle $\\theta$ chosen from a uniform distribution between $0$ and $2\\pi$ radians.
    """)

    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        n_steps = st.number_input("Number of steps (N)", min_value=100, max_value=100000, value=5000, step=1000)
    with col2:
        step_size = st.number_input("Step size (s)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    with col3:
        n_walks = st.slider("Number of paths to overlay", min_value=1, max_value=50, value=5)

    # Simulation Trigger
    if st.button("Simulate Random Walk", type="primary"):
        with st.spinner('Calculating walks...'):
            fig = go.Figure()
            
            # Premium color palette for multiple walks
            colors = [
                '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
            ]
            
            walks = generate_random_walks(n_walks, n_steps, step_size)
            
            for i, (x, y) in enumerate(walks):
                
                color = colors[i % len(colors)]
                
                fig.add_trace(go.Scattergl(
                    x=x, y=y,
                    mode='lines',
                    line=dict(width=1.0, color=color),
                    opacity=0.6,
                    name=f"Walk {i+1}"
                ))
            
            # Add a starting point marker
            fig.add_trace(go.Scattergl(
                x=[0], y=[0],
                mode='markers',
                marker=dict(size=12, color='#F8F8F2', symbol='star', line=dict(color='#FF5555', width=2)),
                name='Start',
                showlegend=True
            ))

            fig.update_layout(
                title=f"Overlay of {n_walks} Random Walk(s) with N={n_steps}",
                xaxis_title="X Position",
                yaxis_title="Y Position",
                height=700,
                template="plotly_dark", # Sleek dark mode
                hovermode="closest",
                showlegend=False if n_walks > 10 else True,
                margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            # Ensure equal aspect ratio so the walk visually represents true distance
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=1,
            )
            
            st.plotly_chart(fig, use_container_width=True)

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of Random Walks
        A **2D isotropic random walk** models a particle undergoing a series of $N$ discrete steps of constant length $s$, where each step's direction angle $\theta$ is independently chosen from a uniform distribution over $[0, 2\pi)$.

        #### 1. Mathematical Formulation
        Starting at the origin $(x_0, y_0) = (0, 0)$, the step displacements at step $i$ are:
        $$ \Delta x_i = s \cos(\theta_i), \quad \Delta y_i = s \sin(\theta_i) $$
        The total position after $N$ steps is the cumulative sum:
        $$ x_N = \sum_{i=1}^N \Delta x_i, \quad y_N = \sum_{i=1}^N \Delta y_i $$

        #### 2. Mean Squared Displacement & Diffusion
        Because $\langle \cos\theta \rangle = 0$ and $\langle \sin\theta \rangle = 0$, the expected net displacement is zero: $\langle \mathbf{R}_N \rangle = 0$. However, the **mean squared distance** grows linearly with the number of steps:
        $$ \langle R_N^2 \rangle = \langle x_N^2 + y_N^2 \rangle = N s^2 $$
        Thus, the root-mean-square (RMS) distance from the origin scales as $R_{\text{rms}} = s \sqrt{N}$. This $\sqrt{N}$ dependence is the fundamental signature of diffusive transport in statistical mechanics and Brownian motion.
        """)

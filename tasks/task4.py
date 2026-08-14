import streamlit as st
import numpy as np
import plotly.graph_objects as go
import scipy.constants as const

h = 6.626e-34
e = 1.602e-19

work_functions = {
    "Silver (Ag)": 4.3,
    "Aluminium (Al)": 4.3,
    "Gold (Au)": 5.1,
    "Copper (Cu)": 4.7,
    "Tin (Sn)": 4.4,
    "Lead (Pb)": 4.3,
    "Tungsten (W)": 4.5,
    "Nickel (Ni)": 4.6,
    "Sodium (Na)": 2.4
}

def render():
    st.header("Task 4: Photoelectric Effect")
    st.markdown("""
        **Objective:** Plot photoelectron stopping voltage vs frequency of incident photons for various metals.
        
        The stopping voltage $V$ is given by Millikan's equation:
        $$ V = \\frac{h}{e}f - \\frac{W}{e} $$
        where $W$ is the work function of the metal.
    """)
    
    st.subheader("1. Stopping Voltage vs Frequency")
    selected_metals = st.multiselect(
        "Select Metals to Compare", 
        list(work_functions.keys()), 
        default=["Sodium (Na)", "Copper (Cu)", "Gold (Au)"]
    )
    
    if selected_metals:
        # Frequencies from 0 to 2.5e15 Hz
        f = np.linspace(0, 2.5e15, 200)
        
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        for idx, metal in enumerate(selected_metals):
            W_eV = work_functions[metal]
            color = colors[idx % len(colors)]
            
            # V = (h/e) * f - W_eV
            V = (h / e) * f - W_eV
            
            # Split into positive and negative (extrapolated) parts for styling
            f_cutoff = W_eV * e / h
            
            mask_real = f >= f_cutoff
            mask_extrap = f <= f_cutoff
            
            # Plot extrapolated line
            fig.add_trace(go.Scatter(
                x=f[mask_extrap], y=V[mask_extrap],
                mode='lines',
                line=dict(color=color, dash='dash'),
                showlegend=False
            ))
            
            # Plot real line
            fig.add_trace(go.Scatter(
                x=f[mask_real], y=V[mask_real],
                mode='lines',
                line=dict(color=color),
                name=f"{metal} (W={W_eV} eV)"
            ))
            
            # Add cutoff frequency marker
            fig.add_trace(go.Scatter(
                x=[f_cutoff], y=[0],
                mode='markers',
                marker=dict(color=color, size=8),
                showlegend=False,
                hovertemplate=f"Cutoff {metal}: {f_cutoff:.2e} Hz<extra></extra>"
            ))
            
        fig.update_layout(
            title="Stopping Voltage vs Frequency",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Stopping Voltage (V)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            xaxis=dict(range=[0, 2.5e15]),
            yaxis=dict(range=[-6, 6])
        )
        
        # Add thin strands for visible light spectrum frequencies behind the metal lines
        visible_wls = [
            (700e-9, "#FF5555"),
            (590e-9, "#F1FA8C"),
            (530e-9, "#50FA7B"),
            (450e-9, "#8BE9FD"),
            (400e-9, "#BD93F9")
        ]
        
        for wl, col in visible_wls:
            f_v = 3e8 / wl
            fig.add_vline(
                x=f_v,
                line_width=1.2,
                line_color=col,
                opacity=0.5
            )
            
        # Add a horizontal line at V=0
        fig.add_hline(y=0, line_width=1, line_color="#F8F8F2")
        
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Interactive Photoelectric Effect Simulation (PhET-style)")
    
    # Controls
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        metal_choice = st.selectbox("Cathode Material", list(work_functions.keys()), index=0)
        work_func = work_functions[metal_choice]
    with col_c2:
        wavelength = st.slider("Wavelength (nm)", min_value=200, max_value=850, value=400, step=10)
    with col_c3:
        intensity = st.slider("Intensity (%)", min_value=0, max_value=100, value=50, step=1)
    with col_c4:
        voltage = st.slider("Battery Voltage (V)", min_value=-8.0, max_value=8.0, value=0.0, step=0.1, help="Positive voltage retards electrons (stopping potential)")
        
    HTML = """
    <div style="position: relative; width: 100%; height: 400px; background: #0e1117; border-radius: 8px; overflow: hidden; border: 1px solid #333; margin-top: 10px;">
      <canvas id="simCanvas" width="800" height="400" style="width: 100%; height: 100%;"></canvas>
      <div id="currentMeter" style="position: absolute; top: 10px; right: 10px; color: #00ffcc; font-family: monospace; font-size: 18px; background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 4px; border: 1px solid #00ffcc;">Current: 0.000 A</div>
    </div>
    """
    
    JS = """
    export default function (component) {
      const { data, parentElement } = component;
      if (!data) return;
      
      if (!parentElement.customData) {
         parentElement.customData = {
             photons: [],
             electrons: [],
             currentFrames: [],
             lastTime: performance.now(),
             accumulator: 0,
             canvas: parentElement.querySelector("#simCanvas"),
             meter: parentElement.querySelector("#currentMeter"),
             ctx: null,
             reqId: null
         };
         
         const state = parentElement.customData;
         state.ctx = state.canvas.getContext('2d');
         
         function wavelengthToRGB(Wavelength) {
             let R, G, B, alpha;
             if(Wavelength >= 380 && Wavelength < 440) { R = -(Wavelength - 440) / (440 - 380); G = 0.0; B = 1.0; }
             else if(Wavelength >= 440 && Wavelength < 490) { R = 0.0; G = (Wavelength - 440) / (490 - 440); B = 1.0; }
             else if(Wavelength >= 490 && Wavelength < 510) { R = 0.0; G = 1.0; B = -(Wavelength - 510) / (510 - 490); }
             else if(Wavelength >= 510 && Wavelength < 580) { R = (Wavelength - 510) / (580 - 510); G = 1.0; B = 0.0; }
             else if(Wavelength >= 580 && Wavelength < 645) { R = 1.0; G = -(Wavelength - 645) / (645 - 580); B = 0.0; }
             else if(Wavelength >= 645 && Wavelength <= 750) { R = 1.0; G = 0.0; B = 0.0; }
             else if(Wavelength < 380) { R = 0.5; G = 0; B = 1.0; } // UV
             else { R = 1.0; G = 0; B = 0.0; } // IR
             if(Wavelength > 750 || Wavelength < 380) alpha = 0.4;
             else alpha = 1.0;
             return `rgba(${Math.round(R * 255)}, ${Math.round(G * 255)}, ${Math.round(B * 255)}, ${alpha})`;
         }
         
         function updateAndDraw(state, currentData, dt) {
             const ctx = state.ctx;
             const cw = state.canvas.width;
             const ch = state.canvas.height;
             
             ctx.clearRect(0, 0, cw, ch);
             
             const cathodeX = 150;
             const anodeX = cw - 150;
             const plateWidth = 20;
             const plateHeight = 250;
             const plateY = ch/2 - plateHeight/2;
             
             const wl_m = currentData.wavelength * 1e-9;
             const f = 3e8 / wl_m;
             const E_photon_eV = (6.626e-34 * f) / 1.602e-19;
             const W_eV = currentData.work_function;
             const V = currentData.voltage;
             const intensity = currentData.intensity / 100.0;
             const color = wavelengthToRGB(currentData.wavelength);
             
             ctx.fillStyle = "rgba(255,255,255,0.03)";
             ctx.beginPath();
             ctx.moveTo(50, 0);
             ctx.lineTo(cathodeX + 20, plateY);
             ctx.lineTo(cathodeX + 20, plateY + plateHeight);
             ctx.fill();
             
             const spawnRate = 25 * intensity;
             if (spawnRate > 0) {
                 state.accumulator += dt * spawnRate;
                 while (state.accumulator >= 1) {
                     state.accumulator -= 1;
                     state.photons.push({
                         x: 50, y: 0,
                         targetX: cathodeX,
                         targetY: plateY + Math.random() * plateHeight,
                         speed: 300,
                         phase: Math.random() * Math.PI * 2
                     });
                 }
             }
             
             ctx.strokeStyle = color;
             ctx.lineWidth = 2;
             for (let i = state.photons.length - 1; i >= 0; i--) {
                 const p = state.photons[i];
                 const dx = p.targetX - p.x;
                 const dy = p.targetY - p.y;
                 const dist = Math.hypot(dx, dy);
                 
                 if (dist < 5) {
                     state.photons.splice(i, 1);
                     if (E_photon_eV >= W_eV) {
                         const K_eV = (E_photon_eV - W_eV) * (0.8 + 0.2*Math.random()); 
                         const vx_initial = 120 * Math.sqrt(K_eV);
                         state.electrons.push({
                             x: cathodeX + plateWidth,
                             y: p.targetY,
                             vx: vx_initial,
                             vy: (Math.random() - 0.5) * 15
                         });
                     }
                     continue;
                 }
                 const vx = (dx / dist) * p.speed;
                 const vy = (dy / dist) * p.speed;
                 p.x += vx * dt;
                 p.y += vy * dt;
                 p.phase += 20 * dt;
                 
                 ctx.beginPath();
                 const numSegments = 5;
                 for (let j=0; j<=numSegments; j++) {
                     const frac = j/numSegments;
                     const w_amp = 8;
                     const perpX = -vy / p.speed;
                     const perpY = vx / p.speed;
                     const offset = Math.sin(p.phase - frac * 10) * w_amp;
                     const segX = p.x - (vx/p.speed)*(1-frac)*20 + perpX*offset;
                     const segY = p.y - (vy/p.speed)*(1-frac)*20 + perpY*offset;
                     if (j===0) ctx.moveTo(segX, segY);
                     else ctx.lineTo(segX, segY);
                 }
                 ctx.stroke();
             }
             
             let hitCount = 0;
             const ax = -60 * V;
             ctx.fillStyle = "#00ffcc";
             for (let i = state.electrons.length - 1; i >= 0; i--) {
                 const el = state.electrons[i];
                 el.vx += ax * dt;
                 el.x += el.vx * dt;
                 el.y += el.vy * dt;
                 if (el.x >= anodeX) {
                     state.electrons.splice(i, 1);
                     hitCount++;
                     continue;
                 }
                 if (el.x <= cathodeX + plateWidth && el.vx < 0) {
                     state.electrons.splice(i, 1);
                     continue;
                 }
                 if (el.y < 0 || el.y > ch) {
                     state.electrons.splice(i, 1);
                     continue;
                 }
                 ctx.beginPath();
                 ctx.arc(el.x, el.y, 4, 0, Math.PI*2);
                 ctx.fill();
                 ctx.shadowBlur = 10;
                 ctx.shadowColor = "#00ffcc";
                 ctx.fill();
                 ctx.shadowBlur = 0;
             }
             
             state.currentFrames.push({ time: performance.now(), hits: hitCount });
             while (state.currentFrames.length > 0 && performance.now() - state.currentFrames[0].time > 1000) {
                 state.currentFrames.shift();
             }
             const totalHits = state.currentFrames.reduce((sum, f) => sum + f.hits, 0);
             const currentA = (totalHits * 0.05).toFixed(3);
             state.meter.textContent = `Current: ${currentA} A`;
             
             ctx.fillStyle = "#555";
             ctx.fillRect(cathodeX, plateY, plateWidth, plateHeight);
             ctx.fillRect(anodeX, plateY, plateWidth, plateHeight);
             
             ctx.fillStyle = "#fff";
             ctx.font = "16px sans-serif";
             ctx.fillText(currentData.metal, cathodeX - 60, plateY - 10);
             ctx.fillText("Anode", anodeX - 10, plateY - 10);
         }
         
         function loop(time) {
             state.reqId = requestAnimationFrame(loop);
             const dt = Math.min((time - state.lastTime) / 1000, 0.1);
             state.lastTime = time;
             const currentData = parentElement.latestData || data;
             updateAndDraw(state, currentData, dt);
         }
         state.reqId = requestAnimationFrame(loop);
         
         return () => {
             cancelAnimationFrame(parentElement.customData.reqId);
         };
      }
      parentElement.latestData = data;
    }
    """
    
    sim_component = st.components.v2.component(
        "photoelectric_sim",
        html=HTML,
        js=JS,
    )
    
    sim_component(
        data={
            "metal": metal_choice,
            "work_function": work_func,
            "wavelength": wavelength,
            "intensity": intensity,
            "voltage": voltage
        }
    )

    # Explanation Section
    with st.expander("Explanation"):
        st.markdown(r"""
        ### Underlying Physics & Theory of the Photoelectric Effect

        #### 1. Einstein's Photoelectric Equation
        In 1905, Albert Einstein explained the photoelectric effect by demonstrating that light consists of localized quanta (photons), each carrying energy $E = h f$. When a photon strikes an electron in a metal cathode:
        * Part of the energy is used to overcome the metal's binding energy (the **Work Function** $W$).
        * The remaining energy is converted into the maximum kinetic energy $K_{\text{max}}$ of the emitted photoelectron:
        $$ K_{\text{max}} = h f - W $$

        #### 2. Stopping Voltage ($V_s$) & Cutoff Frequency ($f_0$)
        To stop the fastest emitted electrons from reaching the anode, an opposing potential (stopping voltage $V_s$) is applied:
        $$ e V_s = K_{\text{max}} = h f - W \implies V_s = \frac{h}{e} f - \frac{W}{e} $$
        * **Cutoff Frequency ($f_0 = W/h$):** Below this threshold frequency, no electrons are emitted regardless of light intensity.
        * **Slope ($h/e$):** The linear slope of $V_s$ vs $f$ is a universal fundamental physical constant ratio, verified experimentally by Robert Millikan.
        * **Intensity:** Increasing light intensity increases the rate of photon arrivals (and thus photocurrent current $I$), but does *not* alter the individual electron kinetic energy or stopping voltage.
        """)

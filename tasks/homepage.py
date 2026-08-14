import streamlit as st
import streamlit.components.v1 as components

def render():
    # Hide the default padding of Streamlit so the canvas can be flush
    st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            height: 100vh !important;
        }
        </style>
    """, unsafe_allow_html=True)

    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap');
            body, html { margin: 0; padding: 0; overflow: hidden; background-color: transparent; }
            canvas { display: block; width: 100%; height: 100vh; }
            .overlay {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: white;
                font-family: 'Inter', sans-serif;
                pointer-events: none;
                width: 100%;
            }
            .overlay h1 {
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                letter-spacing: -1px;
                background: -webkit-linear-gradient(45deg, #FF79C6, #8BE9FD);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .overlay p {
                font-size: 1.2rem;
                color: #A9B2C3;
                font-weight: 300;
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <canvas id="quantumCanvas"></canvas>
        <div class="overlay">
            <h1>BPhO Computational Physics Challenge 2026</h1>
            <h2 style="font-size: 2rem; color: #BD93F9; font-weight: 300; margin-top: 0; margin-bottom: 0.5rem;">Quantum Mechanics</h2>
            <p>Yi-Fan Wu</p>
        </div>
        <script>
            const canvas = document.getElementById('quantumCanvas');
            const ctx = canvas.getContext('2d');
            
            let width, height;
            let particles = [];
            const connectionDistance = 120;
            const mouse = { x: null, y: null, radius: 150 };
            
            function resize() {
                width = window.innerWidth;
                height = window.innerHeight;
                canvas.width = width;
                canvas.height = height;
                initParticles();
            }
            
            window.addEventListener('resize', resize);
            window.addEventListener('mousemove', (e) => {
                mouse.x = e.x;
                mouse.y = e.y;
            });
            window.addEventListener('mouseleave', () => {
                mouse.x = null;
                mouse.y = null;
            });
            
            class Particle {
                constructor() {
                    this.x = Math.random() * width;
                    this.y = Math.random() * height;
                    this.vx = (Math.random() - 0.5) * 1.5;
                    this.vy = (Math.random() - 0.5) * 1.5;
                    this.baseRadius = Math.random() * 2 + 1;
                    this.radius = this.baseRadius;
                    // Mix of neon colors: pink, cyan, purple
                    const colors = ['#FF79C6', '#8BE9FD', '#BD93F9'];
                    this.color = colors[Math.floor(Math.random() * colors.length)];
                }
                
                update() {
                    this.x += this.vx;
                    this.y += this.vy;
                    
                    if (this.x < 0 || this.x > width) this.vx *= -1;
                    if (this.y < 0 || this.y > height) this.vy *= -1;
                    
                    // Mouse interaction (repulsion)
                    if (mouse.x != null) {
                        const dx = mouse.x - this.x;
                        const dy = mouse.y - this.y;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        if (distance < mouse.radius) {
                            const forceDirectionX = dx / distance;
                            const forceDirectionY = dy / distance;
                            const maxDistance = mouse.radius;
                            const force = (maxDistance - distance) / maxDistance;
                            const directionX = forceDirectionX * force * 5;
                            const directionY = forceDirectionY * force * 5;
                            this.x -= directionX;
                            this.y -= directionY;
                        }
                    }
                }
                
                draw() {
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                    ctx.fillStyle = this.color;
                    ctx.fill();
                }
            }
            
            function initParticles() {
                particles = [];
                let numberOfParticles = (width * height) / 9000;
                for (let i = 0; i < numberOfParticles; i++) {
                    particles.push(new Particle());
                }
            }
            
            function animate() {
                requestAnimationFrame(animate);
                ctx.clearRect(0, 0, width, height);
                
                for (let i = 0; i < particles.length; i++) {
                    particles[i].update();
                    particles[i].draw();
                    
                    for (let j = i; j < particles.length; j++) {
                        const dx = particles[i].x - particles[j].x;
                        const dy = particles[i].y - particles[j].y;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance < connectionDistance) {
                            ctx.beginPath();
                            ctx.strokeStyle = particles[i].color;
                            ctx.globalAlpha = 1 - (distance / connectionDistance);
                            ctx.lineWidth = 1;
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                            ctx.globalAlpha = 1.0;
                        }
                    }
                }
            }
            
            resize();
            animate();
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=600)
    

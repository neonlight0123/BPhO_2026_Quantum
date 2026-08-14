import streamlit as st
import tasks.homepage
import tasks.task1
import tasks.task2
import tasks.task3
import tasks.task4
import tasks.task5
import tasks.task6
import tasks.task7
import tasks.task8
import tasks.task9
import tasks.task10

# Ensure the page config is the very first Streamlit command
st.set_page_config(
    page_title="BPhO Computational Challenge 2026",
    page_icon=":material/science:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define pages using the modern st.Page API with callable renders
home = st.Page(tasks.homepage.render, title="Home", icon=":material/home:", url_path="home")
t1 = st.Page(tasks.task1.render, title="Task 1: Random Walk", icon=":material/route:", url_path="task1")
t2 = st.Page(tasks.task2.render, title="Task 2: Brownian Motion", icon=":material/blur_on:", url_path="task2")
t3 = st.Page(tasks.task3.render, title="Task 3: Black Body Radiation", icon=":material/thermostat:", url_path="task3")
t4 = st.Page(tasks.task4.render, title="Task 4: Photoelectric Effect", icon=":material/lightbulb:", url_path="task4")
t5 = st.Page(tasks.task5.render, title="Task 5: Hydrogen Spectra", icon=":material/graphic_eq:", url_path="task5")
t6 = st.Page(tasks.task6.render, title="Task 6: Electron Diffraction", icon=":material/radar:", url_path="task6")
t7 = st.Page(tasks.task7.render, title="Task 7: Particle in a Box", icon=":material/check_box_outline_blank:", url_path="task7")
t8 = st.Page(tasks.task8.render, title="Task 8: Quantum Cryptography", icon=":material/lock:", url_path="task8")
t9 = st.Page(tasks.task9.render, title="Task 9: Compton Scattering", icon=":material/sync_alt:", url_path="task9")
t10 = st.Page(tasks.task10.render, title="Task 10: Hydrogenic Orbitals", icon=":material/public:", url_path="task10")

# Build navigation
pg = st.navigation({
    "Overview": [home],
    "Challenge Tasks": [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
})


# Run the selected page
pg.run()

import streamlit as st
import random
import time
from PIL import Image

# Load images
blue_rectangle = Image.open("blue_rectangle.png")
red_rectangle = Image.open("red_rectangle.png")

# Initial explanation screen
st.title("Human Visual Search Experiment")
st.write("""
    This app will explore aspects of human visual search by having the user perform various visual search tasks. 
    In each task, you will be tasked with finding a specific feature among a number of items.
""")

# Start button
start = st.button("Start")

if start:
    for test_round in range(3):  # Run three tests
        st.write("Press the Blue box")
        time.sleep(3)  # Display message for 3 seconds
        
        # Generate a random grid size between 3x3 and 10x10
        grid_size = random.randint(3, 10)

        # Randomly select a position for the blue rectangle
        blue_position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

        # Flag to track if blue rectangle is clicked
        blue_clicked = False

        # Create a container to hold the grid
        with st.container():
            for i in range(grid_size):
                cols = st.columns(grid_size)
                for j in range(grid_size):
                    # Place a single blue rectangle in the grid and fill others with red rectangles
                    if (i, j) == blue_position:
                        with cols[j]:
                            if st.image(blue_rectangle, use_container_width=True):#, output_format="auto", key=f"blue_{i}_{j}"):
                                # Set flag when blue rectangle is clicked
                                blue_clicked = True
                    else:
                        with cols[j]:
                            st.image(red_rectangle, use_container_width=True)

        # Break the loop if the blue rectangle was clicked
        if blue_clicked:
            st.success("You clicked the Blue box!")
            st.write("Next task starting in 3 seconds...")
            time.sleep(3)
        else:
            st.warning("Try clicking on the Blue box!")

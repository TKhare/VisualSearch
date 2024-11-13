import streamlit as st
import random
import time

# Function to create a visual search task with red and blue blocks
def create_feature_search_task():
    # Randomly position the blue block among red blocks
    blocks = ['red'] * 20
    blue_block_index = random.randint(0, 19)
    blocks[blue_block_index] = 'blue'
    
    # Display the blocks
    for i in range(5):  # Display blocks in 5 rows for better visual layout
        cols = st.columns(5)  # Create 5 columns
        for j in range(5):
            index = i * 5 + j
            if index < len(blocks):
                block_color = blocks[index]
                if block_color == 'blue':
                    cols[j].button("Blue", key=f"block_{index}", on_click=block_clicked, args=(index,))

                else:
                    cols[j].button("Red", key=f"block_{index}")

# Global variable to track the start time
start_time = None

# Function to record the time when the blue block is clicked
def block_clicked(index):
    global start_time
    
    if start_time is None:
        start_time = time.time()  # Capture the start time when the first block is clicked
    else:
        reaction_time = time.time() - start_time
        st.session_state.reaction_time = reaction_time
        st.session_state.clicked_index = index
        st.write(f"Time taken to find the blue block: {reaction_time:.2f} seconds")
        st.stop()

# Streamlit app layout
def main():
    st.title("Feature Search Experiment")
    st.write("In this task, you need to find the blue block among red blocks.")
    
    if 'reaction_time' not in st.session_state:
        st.session_state.reaction_time = None
        st.session_state.clicked_index = None

    create_feature_search_task()
    
    if st.session_state.reaction_time is not None:
        st.write(f"Reaction Time: {st.session_state.reaction_time:.2f} seconds.")
        st.write(f"Block clicked: {st.session_state.clicked_index}")
        
if __name__ == "__main__":
    main()
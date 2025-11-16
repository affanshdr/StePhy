import streamlit as st

# Inisialisasi session state yang diperlukan
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'history' not in st.session_state:
    st.session_state.history = []

if 'redo_stack' not in st.session_state:
    st.session_state.redo_stack = []

# Fungsi untuk menambah nilai counter
def increment():
    st.session_state.history.append(st.session_state.counter)
    st.session_state.counter += 1
    st.session_state.redo_stack.clear()

# Fungsi untuk mengurangi nilai counter
def decrement():
    st.session_state.history.append(st.session_state.counter)
    st.session_state.counter -= 1
    st.session_state.redo_stack.clear()

# Fungsi undo (kembali ke nilai sebelumnya)
def undo():
    if st.session_state.history:
        st.session_state.redo_stack.append(st.session_state.counter)
        st.session_state.counter = st.session_state.history.pop()

# Fungsi redo (maju ke nilai yang dibatalkan undo)
def redo():
    if st.session_state.redo_stack:
        st.session_state.history.append(st.session_state.counter)
        st.session_state.counter = st.session_state.redo_stack.pop()

# UI Streamlit
st.title("Counter dengan Undo/Redo")

st.write("Nilai counter:", st.session_state.counter)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Tambah (+1)"):
        increment()

with col2:
    if st.button("Kurang (-1)"):
        decrement()

with col3:
    if st.button("Undo"):
        undo()

with col4:
    if st.button("Redo"):
        redo()

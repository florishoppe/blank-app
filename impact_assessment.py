import streamlit as st

# Sample data
data = {
    "Copywriter": [
        {"sub_task": "Research and Analysis", "time_allocation": 25, "ai_impact": 3},
        {"sub_task": "Planning and Strategy Development", "time_allocation": 30, "ai_impact": 4},
    ],
    "Data Analyst": [
        {"sub_task": "Data Cleaning", "time_allocation": 40, "ai_impact": 5},
        {"sub_task": "Data Visualization", "time_allocation": 20, "ai_impact": 2},
    ]
}

# Page Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Select Roles", "Edit Data", "Summary"])

# Initialize session state
if 'selected_roles' not in st.session_state:
    st.session_state.selected_roles = []
if 'role_data' not in st.session_state:
    st.session_state.role_data = {}

# Page 1: Select Roles
if page == "Select Roles":
    st.title("Select Job Roles")

    available_roles = list(data.keys())
    selected_roles = st.multiselect("Choose roles to include", available_roles, st.session_state.selected_roles)

    # Store selected roles in session state
    if selected_roles:
        st.session_state.selected_roles = selected_roles
        # Initialize role data if not already done
        for role in selected_roles:
            if role not in st.session_state.role_data:
                st.session_state.role_data[role] = data[role]

# Page 2: Edit Data
elif page == "Edit Data":
    st.title("Edit Role Data")

    for role in st.session_state.selected_roles:
        st.subheader(f"Role: {role}")
        for task in st.session_state.role_data[role]:
            task["sub_task"] = st.text_input(f"Sub-task ({role})", task["sub_task"])
            task["time_allocation"] = st.number_input(f"Time Allocation ({role})", value=task["time_allocation"], min_value=0, max_value=100)
            task["ai_impact"] = st.number_input(f"AI Impact Score ({role})", value=task["ai_impact"], min_value=0, max_value=10)

# Page 3: Summary
elif page == "Summary":
    st.title("Summary of Selected Roles")

    for role, tasks in st.session_state.role_data.items():
        st.subheader(f"Role: {role}")
        for task in tasks:
            st.write(f"Sub-task: {task['sub_task']}, Time Allocation: {task['time_allocation']}%, AI Impact: {task['ai_impact']}")

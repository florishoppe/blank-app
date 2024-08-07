import streamlit as st

# Sample data
data = {
    "Copywriter": [
        {"sub_task": "Research and Analysis", "time_allocation": 25, "ai_impact": 4},
        {"sub_task": "Content Creation", "time_allocation": 40, "ai_impact": 3},
        {"sub_task": "Editing and Proofreading", "time_allocation": 25, "ai_impact": 4},
        {"sub_task": "SEO Optimization", "time_allocation": 10, "ai_impact": 5}
    ],
    "Content Strategist": [
        {"sub_task": "Market Research", "time_allocation": 30, "ai_impact": 3},
        {"sub_task": "Audience Analysis", "time_allocation": 25, "ai_impact": 4},
        {"sub_task": "Content Planning", "time_allocation": 30, "ai_impact": 4},
        {"sub_task": "Performance Tracking", "time_allocation": 15, "ai_impact": 5}
    ],
    "SEO Specialist": [
        {"sub_task": "Keyword Research", "time_allocation": 25, "ai_impact": 5},
        {"sub_task": "On-page Optimization", "time_allocation": 30, "ai_impact": 4},
        {"sub_task": "Link Building", "time_allocation": 20, "ai_impact": 3},
        {"sub_task": "Performance Analysis", "time_allocation": 25, "ai_impact": 5}
    ],
    "Graphic Designer": [
        {"sub_task": "Concept Development", "time_allocation": 20, "ai_impact": 3},
        {"sub_task": "Design Creation", "time_allocation": 50, "ai_impact": 4},
        {"sub_task": "Revisions and Updates", "time_allocation": 20, "ai_impact": 3},
        {"sub_task": "Asset Management", "time_allocation": 10, "ai_impact": 3}
    ],
    "Social Media Manager": [
        {"sub_task": "Content Scheduling", "time_allocation": 20, "ai_impact": 5},
        {"sub_task": "Engagement and Community Management", "time_allocation": 30, "ai_impact": 3},
        {"sub_task": "Analytics and Reporting", "time_allocation": 25, "ai_impact": 5},
        {"sub_task": "Campaign Strategy", "time_allocation": 25, "ai_impact": 4}
    ],
    "Video Producer": [
        {"sub_task": "Pre-production Planning", "time_allocation": 20, "ai_impact": 3},
        {"sub_task": "Filming and Production", "time_allocation": 40, "ai_impact": 2},
        {"sub_task": "Editing and Post-production", "time_allocation": 30, "ai_impact": 4},
        {"sub_task": "Publishing and Distribution", "time_allocation": 10, "ai_impact": 5}
    ],
    "Data Analyst": [
        {"sub_task": "Data Cleaning", "time_allocation": 30, "ai_impact": 5},
        {"sub_task": "Data Visualization", "time_allocation": 25, "ai_impact": 4},
        {"sub_task": "Data Interpretation", "time_allocation": 25, "ai_impact": 3},
        {"sub_task": "Reporting Insights", "time_allocation": 20, "ai_impact": 4}
    ]
}

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_roles' not in st.session_state:
    st.session_state.selected_roles = []
if 'role_data' not in st.session_state:
    st.session_state.role_data = {}

def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# Step 1: Select Roles
if st.session_state.step == 1:
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

    st.button("Next", on_click=next_step)

# Step 2: Edit Data
elif st.session_state.step == 2:
    st.title("Edit Role Data")

    for role in st.session_state.selected_roles:
        st.subheader(f"Role: {role}")
        for idx, task in enumerate(st.session_state.role_data[role]):
            task["sub_task"] = st.text_input(f"Sub-task ({role})", task["sub_task"], key=f"{role}-{idx}-sub_task")
            task["time_allocation"] = st.number_input(f"Time Allocation ({role})", value=task["time_allocation"], min_value=0, max_value=100, key=f"{role}-{idx}-time_allocation")
            task["ai_impact"] = st.number_input(f"AI Impact Score ({role})", value=task["ai_impact"], min_value=0, max_value=10, key=f"{role}-{idx}-ai_impact")

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 3: Summary
elif st.session_state.step == 3:
    st.title("Summary of Selected Roles")

    for role, tasks in st.session_state.role_data.items():
        st.subheader(f"Role: {role}")
        for task in tasks:
            st.write(f"Sub-task: {task['sub_task']}, Time Allocation: {task['time_allocation']}%, AI Impact: {task['ai_impact']}")

    st.button("Back", on_click=prev_step)

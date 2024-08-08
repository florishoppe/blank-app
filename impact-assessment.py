import streamlit as st
import pandas as pd

# Sample data with descriptions and salaries
data = {
    "Copywriter": {
        "tasks": [
            {"sub_task": "Research and Analysis", "time_allocation": 25, "description": "Conducting research on assigned topics.", "ai_impact": 4},
            {"sub_task": "Content Creation", "time_allocation": 40, "description": "Creating compelling and engaging content.", "ai_impact": 3},
            {"sub_task": "Editing and Proofreading", "time_allocation": 25, "description": "Reviewing and refining content for accuracy.", "ai_impact": 4},
            {"sub_task": "SEO Optimization", "time_allocation": 10, "description": "Enhancing content for search engine visibility.", "ai_impact": 5}
        ],
        "salary": 50000
    },
    "Content Strategist": {
        "tasks": [
            {"sub_task": "Market Research", "time_allocation": 30, "description": "Analyzing market trends and competitor activities.", "ai_impact": 3},
            {"sub_task": "Audience Analysis", "time_allocation": 25, "description": "Identifying and understanding target audience behavior.", "ai_impact": 4},
            {"sub_task": "Content Planning", "time_allocation": 30, "description": "Developing long-term content strategies.", "ai_impact": 4},
            {"sub_task": "Performance Tracking", "time_allocation": 15, "description": "Tracking and measuring content performance.", "ai_impact": 5}
        ],
        "salary": 60000
    },
    "SEO Specialist": {
        "tasks": [
            {"sub_task": "Keyword Research", "time_allocation": 25, "description": "Identifying the best keywords for search ranking.", "ai_impact": 5},
            {"sub_task": "On-page Optimization", "time_allocation": 30, "description": "Enhancing content and HTML for better ranking.", "ai_impact": 4},
            {"sub_task": "Link Building", "time_allocation": 20, "description": "Creating backlinks for better search engine visibility.", "ai_impact": 3},
            {"sub_task": "Performance Analysis", "time_allocation": 25, "description": "Analyzing SEO campaign performance.", "ai_impact": 5}
        ],
        "salary": 55000
    },
    "Graphic Designer": {
        "tasks": [
            {"sub_task": "Concept Development", "time_allocation": 20, "description": "Brainstorming and developing initial design ideas.", "ai_impact": 3},
            {"sub_task": "Design Creation", "time_allocation": 50, "description": "Creating visual designs and graphics.", "ai_impact": 4},
            {"sub_task": "Revisions and Updates", "time_allocation": 20, "description": "Making necessary changes and updates to designs.", "ai_impact": 3},
            {"sub_task": "Asset Management", "time_allocation": 10, "description": "Organizing and managing design assets.", "ai_impact": 3}
        ],
        "salary": 45000
    },
    "Social Media Manager": {
        "tasks": [
            {"sub_task": "Content Scheduling", "time_allocation": 20, "description": "Scheduling content posts for social media engagement.", "ai_impact": 5},
            {"sub_task": "Engagement and Community Management", "time_allocation": 30, "description": "Interacting with followers and managing community.", "ai_impact": 3},
            {"sub_task": "Analytics and Reporting", "time_allocation": 25, "description": "Tracking social media performance metrics.", "ai_impact": 5},
            {"sub_task": "Campaign Strategy", "time_allocation": 25, "description": "Developing strategies for social media campaigns.", "ai_impact": 4}
        ],
        "salary": 50000
    },
    "Video Producer": {
        "tasks": [
            {"sub_task": "Pre-production Planning", "time_allocation": 20, "description": "Planning and organizing video production.", "ai_impact": 3},
            {"sub_task": "Filming and Production", "time_allocation": 40, "description": "Shooting and capturing video content.", "ai_impact": 2},
            {"sub_task": "Editing and Post-production", "time_allocation": 30, "description": "Editing video content and adding effects.", "ai_impact": 4},
            {"sub_task": "Publishing and Distribution", "time_allocation": 10, "description": "Publishing and distributing video content.", "ai_impact": 5}
        ],
        "salary": 60000
    },
    "Data Analyst": {
        "tasks": [
            {"sub_task": "Data Cleaning", "time_allocation": 30, "description": "Preparing data for analysis by cleaning and organizing.", "ai_impact": 5},
            {"sub_task": "Data Visualization", "time_allocation": 25, "description": "Creating visual representations of data.", "ai_impact": 4},
            {"sub_task": "Data Interpretation", "time_allocation": 25, "description": "Interpreting data to provide insights.", "ai_impact": 3},
            {"sub_task": "Reporting Insights", "time_allocation": 20, "description": "Reporting findings and insights from data.", "ai_impact": 4}
        ],
        "salary": 70000
    }
}

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_roles' not in st.session_state:
    st.session_state.selected_roles = []
if 'role_data' not in st.session_state:
    st.session_state.role_data = {}

def go_to_step(step):
    st.session_state.step = step

# Breadcrumb-like Navigation
st.sidebar.title("Navigation")
st.sidebar.write("")

if st.session_state.step >= 1:
    if st.sidebar.button("Step 1: Select Roles"):
        go_to_step(1)

if st.session_state.step >= 2:
    if st.sidebar.button("Step 2: Verify Role Details"):
        go_to_step(2)

if st.session_state.step == 3:
    if st.sidebar.button("Step 3: Summary"):
        go_to_step(3)

# Step text
def step_text():
    if st.session_state.step == 1:
        return "Step 1. Select Job Roles"
    elif st.session_state.step == 2:
        return "Step 2. Verify Role Details"
    elif st.session_state.step == 3:
        return "Step 3. Summary"

# Step 1: Select Roles
if st.session_state.step == 1:
    st.title(step_text())

    available_roles = list(data.keys())
    selected_roles = st.multiselect("Choose roles to include", available_roles, st.session_state.selected_roles)

    # Ensure the session state updates immediately after selection
    if set(selected_roles) != set(st.session_state.selected_roles):
        st.session_state.selected_roles = selected_roles
        # Initialize role data if not already done
        for role in selected_roles:
            if role not in st.session_state.role_data:
                st.session_state.role_data[role] = data[role]

    st.button("Next", on_click=lambda: go_to_step(2))

# Step 2: Verify Data
elif st.session_state.step == 2:
    st.title(step_text())

    valid_time_allocation = True
    for role in st.session_state.selected_roles:
        st.subheader(role)
        salary_str = st.text_input(
            "Salary (€)", value=str(st.session_state.role_data[role]['salary']), key=f"{role}-salary")

        if salary_str != str(st.session_state.role_data[role]['salary']):
            try:
                st.session_state.role_data[role]['salary'] = int(salary_str)
            except ValueError:
                st.error("Please enter a valid salary amount")

        total_time_allocation = 0
        for idx, task in enumerate(st.session_state.role_data[role]['tasks']):
            cols = st.columns([1, 0.6, 0.6])  # Adjust the layout
            with cols[0]:
                st.markdown(f"**{task['sub_task']}**")
                st.markdown(f"*{task['description']}*", unsafe_allow_html=True)
            with cols[1]:
                time_allocation_str = st.text_input(
                    "Time allocation (%)", value=str(task["time_allocation"]), key=f"{role}-{idx}-time_allocation")
                try:
                    time_allocation = int(time_allocation_str)
                    total_time_allocation += time_allocation
                    if time_allocation != task["time_allocation"]:
                        task["time_allocation"] = time_allocation
                except ValueError:
                    st.error("Please enter a valid time allocation percentage")
            with cols[2]:
                ai_impact_str = st.text_input(
                    "AI Impact Score", value=str(task["ai_impact"]), key=f"{role}-{idx}-ai_impact")
                try:
                    ai_impact = int(ai_impact_str)
                    if ai_impact != task["ai_impact"]:
                        task["ai_impact"] = ai_impact
                except ValueError:
                    st.error("Please enter a valid AI impact score")

            st.markdown("<br>", unsafe_allow_html=True)  # Add space between tasks
        
        if total_time_allocation != 100:
            valid_time_allocation = False

        st.markdown(f"**Total Time Allocation**: {total_time_allocation}%")
    
    if not valid_time_allocation:
        st.error("Total time allocation for each role must be 100%.")

    # Correctly define and use the columns for navigation buttons
    col1, col2, col3 = st.columns([7, 1, 1])
    with col2:
        st.button("Back", on_click=lambda: go_to_step(1))
    with col3:
        if valid_time_allocation:
            st.button("Next", on_click=lambda: go_to_step(3))

# Step 3: Summary
elif st.session_state.step == 3:
    st.title(step_text())

    for role in st.session_state.role_data.keys():
        st.subheader(role)
        salary = int(st.session_state.role_data[role]['salary'])
        st.markdown(f"**Salary**: €{salary:,.2f}")

        table_data = {
            "Description": [],
            "Time Allocation (%)": [],
            "AI Impact": []
        }

        for task in st.session_state.role_data[role]['tasks']:
            table_data["Description"].append(task['description'])
            table_data["Time Allocation (%)"].append(task['time_allocation'])
            table_data["AI Impact"].append(task['ai_impact'])
        
        df = pd.DataFrame(table_data)

        # Hide the index and fix Description column width
        styled_df = df.style.hide(axis='index').set_table_styles(
            {
                "Description": [
                    {'selector': 'th', 'props': [("text-align", "center"), ("width", "250px")]},
                    {'selector': 'td', 'props': [("text-align", "center"), ("width", "250px"), ("word-wrap", "break-word")]}
                ],
                "Time Allocation (%)": [
                    {'selector': 'th', 'props': [("text-align", "center")]},
                    {'selector': 'td', 'props': [("text-align", "center")]}
                ],
                "AI Impact": [
                    {'selector': 'th', 'props': [("text-align", "center")]},
                    {'selector': 'td', 'props': [("text-align", "center")]}
                ],
                None: [
                    {'selector': 'th.col_heading', 'props': [("text-align", "center")]}
                ]
            }
        )
        
        st.dataframe(styled_df)

    col1, col2, col3 = st.columns([7, 1, 1])
    with col2:
        st.button("Back", on_click=lambda: go_to_step(2))

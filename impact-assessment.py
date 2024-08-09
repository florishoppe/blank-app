import streamlit as st
import pandas as pd
from data import data  # Importing the data from the separate file

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_roles' not in st.session_state:
    st.session_state.selected_roles = []
if 'role_data' not in st.session_state:
    st.session_state.role_data = {}

# Function to change steps
def go_to_step(step):
    st.session_state.step = step

# Custom CSS to center content and align text to the right
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .right-align {
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Breadcrumb-like Navigation
st.sidebar.title("Navigation")
if st.session_state.step >= 1:
    if st.sidebar.button("Step 1: Select Roles"):
        go_to_step(1)
if st.session_state.step >= 2:
    if st.sidebar.button("Step 2: Verify Role Details"):
        go_to_step(2)
if st.session_state.step == 3:
    if st.sidebar.button("Step 3: Summary"):
        go_to_step(3)

# Formatting function for currency (European format, e.g., €55.000)
def format_currency(value):
    return f"€{value:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".")

# Return the step description text
def step_text():
    step_descriptions = {
        1: "Step 1. Select Job Roles",
        2: "Step 2. Verify Role Details",
        3: "Step 3. Summary"
    }
    return step_descriptions.get(st.session_state.step)

# Main container to center content
with st.container():
    st.markdown('<div class="center">', unsafe_allow_html=True)
    
    # Step 1: Select Roles
    if st.session_state.step == 1:
        st.title(step_text())
        available_roles = list(data.keys())
        selected_roles = st.multiselect("Choose roles to include", available_roles, st.session_state.selected_roles)
        
        if set(selected_roles) != set(st.session_state.selected_roles):
            st.session_state.selected_roles = selected_roles
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
            
            # Input fields for salary and number of employees
            cols = st.columns(2)
            with cols[0]:
                salary_str = st.text_input(
                    "Salary (€)", value=format_currency(st.session_state.role_data[role]['salary']), key=f"{role}-salary")
                try:
                    st.session_state.role_data[role]['salary'] = int(salary_str.replace("€", "").replace(".", "").replace(",", ""))
                except ValueError:
                    st.error("Please enter a valid salary amount")
            
            with cols[1]:
                employees_str = st.text_input(
                    "Number of employees", value=str(st.session_state.role_data[role].get('employees', 1)), key=f"{role}-employees")
                if employees_str != str(st.session_state.role_data[role].get('employees', 1)):
                    try:
                        st.session_state.role_data[role]['employees'] = int(employees_str)
                    except ValueError:
                        st.error("Please enter a valid number of employees")
            
            total_time_allocation = 0
            for idx, task in enumerate(st.session_state.role_data[role]['tasks']):
                cols = st.columns([1, 1])
                with cols[0]:
                    st.markdown(f"**{task['sub_task']}**")
                    st.markdown(f"*{task['description']}*", unsafe_allow_html=True)
                with cols[1]:
                    time_allocation_str = st.text_input("Time allocation (%)", value=str(task["time_allocation"]), key=f"{role}-{idx}-time_allocation")
                    try:
                        time_allocation = int(time_allocation_str)
                        total_time_allocation += time_allocation
                        if time_allocation != task["time_allocation"]:
                            task["time_allocation"] = time_allocation
                    except ValueError:
                        st.error("Please enter a valid time allocation percentage")
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='right-align'><strong>Total Time Allocation:</strong> {total_time_allocation}%</div>", unsafe_allow_html=True)
            if total_time_allocation < 100:
                st.markdown(f"<div class='right-align'><strong>Other:</strong> {100 - total_time_allocation}%</div>", unsafe_allow_html=True)
            elif total_time_allocation > 100:
                st.markdown(f"<div class='right-align' style='color: red'><strong>Total time allocation exceeds 100%</strong></div>", unsafe_allow_html=True)
            
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Navigation buttons
        col1, col2, col3 = st.columns([7, 1, 1])
        with col2:
            st.button("Back", on_click=lambda: go_to_step(1))
        with col3:
            if valid_time_allocation and total_time_allocation <= 100:
                st.button("Next", on_click=lambda: go_to_step(3))
    
    # Step 3: Summary
    elif st.session_state.step == 3:
        st.title(step_text())
        
        total_org_cost_saving = 0
        
        for role in st.session_state.role_data.keys():
            st.subheader(role)
            salary = st.session_state.role_data[role]['salary']
            employees = st.session_state.role_data[role].get('employees', 1)
            
            st.markdown(f"**Salary**: {format_currency(salary)}")
            st.markdown(f"**Number of Employees**: {employees}")
            
            table_data = {
                "Description": [],
                "Time Allocation (%)": [],
                "AI Impact Score (1-5)": [],
                "Cost Saving (€)": []
            }
            
            total_role_cost_saving = 0
            for task in st.session_state.role_data[role]['tasks']:
                table_data["Description"].append(task['description'])
                table_data["Time Allocation (%)"].append(task['time_allocation'])
                table_data["AI Impact Score (1-5)"].append(task['ai_impact'])
                
                task_cost = salary * (task['time_allocation'] / 100) * (task['ai_impact'] / 5) * employees
                table_data["Cost Saving (€)"].append(format_currency(task_cost))
                total_role_cost_saving += task_cost
            
            df = pd.DataFrame(table_data)
            total_org_cost_saving += total_role_cost_saving
            
            # Hide index and format dataframe
            styled_df = df.style.hide(axis='index').set_table_styles({
                "Description": [
                    {'selector': 'th', 'props': [("text-align", "center"), ("width", "250px")]},
                    {'selector': 'td', 'props': [("text-align", "center"), ("width", "250px"), ("word-wrap", "break-word")]}
                ],
                "Time Allocation (%)": [
                    {'selector': 'th', 'props': [("text-align", "center")]},
                    {'selector': 'td', 'props': [("text-align", "center")]}
                ],
                "AI Impact Score (1-5)": [
                    {'selector': 'th', 'props': [("text-align", "center")]},
                    {'selector': 'td', 'props': [("text-align", "center")]}
                ],
                "Cost Saving (€)": [
                    {'selector': 'th', 'props': [("text-align", "center")]},
                    {'selector': 'td', 'props': [("text-align", "center")]}
                ],
                None: [
                    {'selector': 'th.col_heading', 'props': [("text-align", "center")]}
                ]
            })
            
            st.dataframe(styled_df)
            st.markdown(f"**Total Cost Saving for {role}**: {format_currency(total_role_cost_saving)}")
            st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"## Total Cost Saving for the Organization: {format_currency(total_org_cost_saving)}")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.empty()
        with col2:
            st.button("Back", on_click=lambda: go_to_step(2))
    
    st.markdown('</div>', unsafe_allow_html=True)

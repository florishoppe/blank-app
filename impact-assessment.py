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

def go_to_step(step):
    st.session_state.step = step

# Custom CSS to center content
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# Formatting function for currency
def format_currency(value):
    return f"€{value:,.0f}".replace(",", ".").replace(".", ",")

# Step text
def step_text():
    if st.session_state.step == 1:
        return "Step 1. Select Job Roles"
    elif st.session_state.step == 2:
        return "Step 2. Verify Role Details"
    elif st.session_state.step == 3:
        return "Step 3. Summary"

# Container to center content
with st.container():
    st.markdown('<div class="center">', unsafe_allow_html=True)
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
                cols = st.columns([1, 1])  # Adjust the layout
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

                st.markdown("<br>", unsafe_allow_html=True)  # Add space between tasks

            if total_time_allocation < 100:
                st.markdown(f"**Other**: {100 - total_time_allocation}%")
            elif total_time_allocation > 100:
                st.error("Total time allocation exceeds 100%")

            st.markdown(f"**Total Time Allocation**: {total_time_allocation}%")
        
        st.markdown("<br>", unsafe_allow_html=True)  # Add more space between roles

        # Correctly define and use the columns for navigation buttons
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
            salary = int(st.session_state.role_data[role]['salary'])
            employees = int(st.session_state.role_data[role].get('employees', 1))
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
                }
            )

            st.dataframe(styled_df)
            st.markdown(f"**Total Cost Saving for {role}**: {format_currency(total_role_cost_saving)}")
            st.markdown("<br>", unsafe_allow_html=True)  # Add space between roles

        st.markdown(f"## Total Cost Saving for the Organization: {format_currency(total_org_cost_saving)}")

        col1, col2, col3 = st.columns([6, 1, 1])
        with col2:
            st.button("Back", on_click=lambda: go_to_step(2))
        
    st.markdown('</div>', unsafe_allow_html=True)

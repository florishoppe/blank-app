import streamlit as st

# Sample data
   job_roles = {
       "Copywriter": [
           {"task": "Research and Analysis", "time_allocation": 25, "ai_impact": "High"},
           {"task": "Planning and Strategy Development", "time_allocation": 30, "ai_impact": "Medium"}
       ],
       # Add more roles and tasks
   }

   # Page 1: Role Selection
   st.title("Job Roles App")
   st.header("Select Job Roles")
   
   selected_roles = st.multiselect("Choose job roles:", list(job_roles.keys()))

   if selected_roles:
       # Page 2: View/Edit Data
       st.header("View and Edit Task Data")
       for role in selected_roles:
           st.subheader(f"Role: {role}")
           for task in job_roles[role]:
               task_name = st.text_input(f"Task Name ({role})", task["task"])
               task["task"] = task_name
               time_allocation = st.slider(f"Time Allocation (%) ({role}/{task_name})", 0, 100, task["time_allocation"])
               task["time_allocation"] = time_allocation
               ai_impact = st.selectbox(f"AI Impact ({role}/{task_name})", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["ai_impact"]))
               task["ai_impact"] = ai_impact
   
       # Page 3: Summary
       st.header("Summary of Tasks")
       for role in selected_roles:
           st.subheader(f"Role: {role}")
           total_time_allocation = 0
           for task in job_roles[role]:
               st.text(f"Task: {task['task']} - Time Allocation: {task['time_allocation']}% - AI Impact: {task['ai_impact']}")
               total_time_allocation += task["time_allocation"]
           st.text(f"Total Time Allocation for {role}: {total_time_allocation}%")

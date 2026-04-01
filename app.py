import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your pet care management system.

This app helps you plan and organize your pet's daily routine with intelligent task scheduling.
"""
)

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

if "pets" not in st.session_state:
    st.session_state.pets = []

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 0

# Owner Setup
st.subheader("👤 Owner Information")
col1, col2, col3, col4 = st.columns(4)

with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    owner_email = st.text_input("Email", value="jordan@example.com")
with col3:
    owner_phone = st.text_input("Phone", value="555-0000")
with col4:
    owner_address = st.text_input("Address", value="123 Main St")

if st.button("Initialize Owner & Scheduler"):
    st.session_state.owner = Owner(
        name=owner_name,
        email=owner_email,
        phone=owner_phone,
        address=owner_address
    )
    st.session_state.scheduler = Scheduler(
        scheduler_id="sched_001",
        owner=st.session_state.owner
    )
    st.success(f"✅ Owner '{owner_name}' and Scheduler initialized!")

if st.session_state.owner:
    st.info(f"Owner: **{st.session_state.owner.name}** | Email: {st.session_state.owner.email}")

st.divider()

# Pet Management
st.subheader("🐕 Manage Pets")

if st.session_state.owner:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        pet_species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"])
    with col3:
        pet_breed = st.text_input("Breed", value="Labrador")
    with col4:
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    
    pet_health = st.text_area("Health info", value="Healthy, up to date on vaccinations")
    
    if st.button("Add Pet"):
        # Check if pet name already exists
        existing_names = [p.name.lower() for p in st.session_state.owner.pets]
        if pet_name.lower() in existing_names:
            st.error(f"❌ A pet named '{pet_name}' already exists! Choose a different name.")
        else:
            # Create new pet with unique ID
            st.session_state.pet_counter += 1
            pet = Pet(
                pet_id=f"pet_{st.session_state.pet_counter:03d}",
                name=pet_name,
                species=pet_species,
                breed=pet_breed,
                age=pet_age,
                health_info=pet_health,
                owner=st.session_state.owner
            )
            
            # Use the add_pet() method with duplicate checking
            if st.session_state.owner.add_pet(pet):
                st.session_state.pets = st.session_state.owner.pets
                st.success(f"✅ Pet '{pet_name}' added successfully!")
            else:
                st.error(f"❌ Could not add pet '{pet_name}'. A pet with this ID or name may already exist.")
    
    if st.session_state.pets:
        st.markdown("### Current Pets")
        for pet in st.session_state.pets:
            st.info(f"🐾 **{pet.name}** ({pet.species}, {pet.breed}, {pet.age} years) - {pet.health_info}")
else:
    st.warning("⚠️ Please initialize an Owner first.")

st.divider()

# Task Scheduling
st.subheader("📋 Schedule Tasks")

if st.session_state.owner and st.session_state.pets:
    st.markdown("### Add a Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_pet = st.selectbox(
            "Select pet",
            options=st.session_state.pets,
            format_func=lambda p: f"{p.name} ({p.species})"
        )
        task_type = st.selectbox(
            "Task type",
            options=[t.value for t in TaskType],
            format_func=lambda x: x.upper()
        )
        task_description = st.text_input("Task description", value="Feed pet")
    
    with col2:
        task_time = st.time_input("Time", value=datetime.now().time())
        task_priority = st.slider("Priority (1=Low, 5=High)", min_value=1, max_value=5, value=3)
    
    if st.button("Schedule Task"):
        due_datetime = datetime.combine(datetime.now().date(), task_time)
        
        task = Task(
            task_id=f"task_{len(st.session_state.scheduler.tasks) + 1:03d}",
            task_type=TaskType(task_type),
            pet=selected_pet,
            due_time=due_datetime,
            priority=task_priority,
            description=task_description,
            completed=False
        )
        
        st.session_state.scheduler.add_task(task)
        st.success(f"✅ Task '{task_description}' scheduled for {selected_pet.name} at {task_time}!")
    
    if st.session_state.scheduler.tasks:
        st.markdown("### 📅 Current Schedule (Chronological Order)")
        
        # Use Scheduler.sort_by_time() method
        sorted_tasks = st.session_state.scheduler.sort_by_time()
        
        # Display as table
        task_data = []
        for task in sorted_tasks:
            task_data.append({
                "Status": "✅ Done" if task.completed else "⏳ Pending",
                "Time": task.due_time.strftime('%H:%M'),
                "Pet": task.pet.name,
                "Type": task.task_type.value.capitalize(),
                "Description": task.description,
                "Priority": "⭐" * task.priority
            })
        
        st.table(task_data)
        
        # Conflict Detection Section
        st.markdown("### ⚠️ Schedule Conflicts")
        conflicts = st.session_state.scheduler.detect_conflicts()
        
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("✅ No scheduling conflicts detected!")
        
        st.divider()
        
        # Task Filtering Section
        st.markdown("### 🔍 Filter Tasks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            filter_pet = st.selectbox(
                "Filter by Pet (select 'All' to show all)",
                options=["All"] + [p.name for p in st.session_state.pets],
                key="filter_pet_select"
            )
        
        with col2:
            filter_status = st.selectbox(
                "Filter by Status",
                options=["All", "Pending", "Completed"],
                key="filter_status_select"
            )
        
        # Apply filters using Scheduler.filter_tasks()
        filtered_tasks = st.session_state.scheduler.tasks
        
        if filter_pet != "All":
            filtered_tasks = st.session_state.scheduler.filter_tasks(pet_name=filter_pet)
        
        if filter_status == "Pending":
            filtered_tasks = [t for t in filtered_tasks if not t.completed]
        elif filter_status == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t.completed]
        
        if filtered_tasks:
            st.markdown(f"**Found {len(filtered_tasks)} task(s)**")
            
            for task in filtered_tasks:
                with st.expander(
                    f"{'✅' if task.completed else '⏳'} {task.pet.name} - {task.task_type.value.upper()} at {task.due_time.strftime('%H:%M')}"
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Description:** {task.description}")
                        st.write(f"**Due:** {task.due_time.strftime('%Y-%m-%d %H:%M')}")
                    
                    with col2:
                        st.write(f"**Priority:** {'⭐' * task.priority}")
                        st.write(f"**Status:** {'✅ Completed' if task.completed else '⏳ Pending'}")
                    
                    with col3:
                        if not task.completed:
                            if st.button("✓ Mark Complete", key=f"complete_{task.task_id}"):
                                task.mark_complete(st.session_state.scheduler)
                                st.success(f"Task marked complete! {'📌 Next occurrence created.' if task.recurrence else ''}")
                                st.rerun()
        else:
            st.info("No tasks match your filters.")
        
        st.divider()
        
        # Task Summary Section
        st.markdown("### 📊 Task Summary")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        pending_count = len([t for t in st.session_state.scheduler.tasks if not t.completed])
        completed_count = len([t for t in st.session_state.scheduler.tasks if t.completed])
        recurring_count = len([t for t in st.session_state.scheduler.tasks if t.recurrence])
        
        with summary_col1:
            st.metric("Total Tasks", len(st.session_state.scheduler.tasks))
        with summary_col2:
            st.metric("Pending", pending_count)
        with summary_col3:
            st.metric("Completed", completed_count)
        with summary_col4:
            st.metric("Recurring", recurring_count)

    else:
        st.info("No tasks scheduled yet. Add one above.")

elif st.session_state.owner:
    st.warning("⚠️ Please add at least one pet before scheduling tasks.")

else:
    st.warning("⚠️ Please initialize an Owner first.")

import os
import streamlit as st
from huggingface_hub import InferenceClient
from datetime import datetime, timedelta
import json

# Hugging Face token (securely stored in Streamlit secrets)
LUCI_API1 = st.secrets["LUCI_API1"]
client = InferenceClient("meta-llama/Meta-Llama-3-8B", token=LUCI_API1)

# Page configuration
st.set_page_config(
    page_title="🌍 AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "trips" not in st.session_state:
    st.session_state.trips = {}
if "current_trip" not in st.session_state:
    st.session_state.current_trip = None
if "itinerary" not in st.session_state:
    st.session_state.itinerary = {}
if "budget" not in st.session_state:
    st.session_state.budget = {}
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "packing_list" not in st.session_state:
    st.session_state.packing_list = {}
if "travel_notes" not in st.session_state:
    st.session_state.travel_notes = []

# Sidebar: Trip Management
st.sidebar.header("✈️ Trip Management")

# Create or select trip
trip_name = st.sidebar.text_input("Trip Name", placeholder="e.g., Paris Vacation 2026")

if st.sidebar.button("+ New Trip"):
    if trip_name and trip_name not in st.session_state.trips:
        st.session_state.trips[trip_name] = {
            "destination": "",
            "start_date": None,
            "end_date": None,
            "budget": 1000,
            "travelers": 1,
        }
        st.session_state.current_trip = trip_name
        st.session_state.itinerary[trip_name] = {}
        st.session_state.budget[trip_name] = []
        st.session_state.packing_list[trip_name] = []
        st.success(f"✅ Trip '{trip_name}' created!")
    elif trip_name in st.session_state.trips:
        st.warning("Trip already exists!")
    else:
        st.warning("Enter a trip name!")

# Select existing trip
if st.session_state.trips:
    selected_trip = st.sidebar.selectbox(
        "Select Trip",
        list(st.session_state.trips.keys()),
        index=0 if st.session_state.current_trip is None else list(st.session_state.trips.keys()).index(st.session_state.current_trip) if st.session_state.current_trip in st.session_state.trips else 0
    )
    st.session_state.current_trip = selected_trip

# Display current trip info
if st.session_state.current_trip:
    trip_info = st.session_state.trips[st.session_state.current_trip]
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📍 {st.session_state.current_trip}")
    
    if trip_info["destination"]:
        st.sidebar.write(f"**Destination:** {trip_info['destination']}")
    if trip_info["start_date"]:
        st.sidebar.write(f"**Start:** {trip_info['start_date']}")
    if trip_info["end_date"]:
        st.sidebar.write(f"**End:** {trip_info['end_date']}")
    if trip_info["budget"]:
        st.sidebar.write(f"**Budget:** ${trip_info['budget']}")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["🗺️ Plan", "📅 Itinerary", "💰 Budget", "❤️ Favorites", "🎒 Packing", "💬 Travel AI"]
)

# AI Travel Advice Function
def get_travel_advice(destination, trip_type, travelers, interests):
    system_prompt = (
        "You are an expert travel planner AI. "
        "Give practical tips, must-visit attractions, local food recommendations, transportation advice, and travel hacks."
    )
    
    user_context = (
        f"Destination: {destination}\n"
        f"Trip Type: {trip_type}\n"
        f"Travelers: {travelers}\n"
        f"Interests: {interests}"
    )
    
    full_prompt = f"""<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|>
<|start_header_id|>user<|end_header_id|>

{user_context}

Plan my perfect trip!<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""
    
    response = client.text_generation(
        full_prompt, 
        max_new_tokens=500, 
        temperature=0.8,
        do_sample=True
    )
    return response.strip()

# ==================== TAB 1: PLAN ====================
with tab1:
    st.title("🗺️ Trip Planning")
    
    if st.session_state.current_trip:
        trip = st.session_state.trips[st.session_state.current_trip]
        
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.text_input("Destination", value=trip.get("destination", ""), placeholder="e.g., Paris, Tokyo, Barcelona")
            travelers = st.number_input("Number of Travelers", min_value=1, max_value=20, value=trip.get("travelers", 1))
            trip_type = st.selectbox("Trip Type", ["Adventure", "Relaxation", "Cultural", "Beach", "Mountain", "City", "Food Tour"])
        
        with col2:
            start_date = st.date_input("Start Date", value=trip.get("start_date") or datetime.now())
            end_date = st.date_input("End Date", value=trip.get("end_date") or (datetime.now() + timedelta(days=7)))
            # FIXED: Ensure value >= min_value
            budget_value = max(100, trip.get("budget", 1000))
            budget = st.number_input("Total Budget ($)", min_value=100, value=budget_value, step=100)
        
        if st.button("💾 Save Trip Details"):
            trip["destination"] = destination
            trip["start_date"] = start_date
            trip["end_date"] = end_date
            trip["budget"] = budget
            trip["travelers"] = travelers
            st.success("✅ Trip details saved!")
        
        st.markdown("---")
        
        # AI Travel Recommendation
        if destination:
            st.subheader("🤖 AI Travel Recommendations")
            interests = st.multiselect(
                "What are your interests?",
                ["History", "Food", "Nature", "Adventure", "Shopping", "Nightlife", "Museums", "Beaches"],
                default=["History", "Food"]
            )
            
            if st.button("🎯 Get Personalized Recommendations"):
                with st.spinner("🔍 Planning your perfect trip..."):
                    advice = get_travel_advice(destination, trip_type, travelers, ", ".join(interests))
                    st.markdown(advice)
    else:
        st.info("👈 Create or select a trip from the sidebar to start planning!")

# ==================== TAB 2: ITINERARY ====================
with tab2:
    st.title("📅 Day-by-Day Itinerary")
    
    if st.session_state.current_trip:
        trip = st.session_state.trips[st.session_state.current_trip]
        start_date = trip.get("start_date")
        end_date = trip.get("end_date")
        
        if start_date and end_date:
            num_days = (end_date - start_date).days + 1
            
            for day in range(1, num_days + 1):
                current_date = start_date + timedelta(days=day - 1)
                
                with st.expander(f"Day {day} - {current_date.strftime('%A, %B %d')}"):
                    day_key = f"day_{day}"
                    
                    morning = st.text_area(f"Morning Activity", key=f"{day_key}_morning", height=80)
                    afternoon = st.text_area(f"Afternoon Activity", key=f"{day_key}_afternoon", height=80)
                    evening = st.text_area(f"Evening Activity", key=f"{day_key}_evening", height=80)
                    
                    if st.button(f"Save Day {day}", key=f"save_day_{day}"):
                        if st.session_state.current_trip not in st.session_state.itinerary:
                            st.session_state.itinerary[st.session_state.current_trip] = {}
                        
                        st.session_state.itinerary[st.session_state.current_trip][day] = {
                            "date": str(current_date),
                            "morning": morning,
                            "afternoon": afternoon,
                            "evening": evening,
                        }
                        st.success(f"✅ Day {day} saved!")
        else:
            st.warning("⚠️ Set start and end dates in the Plan tab first!")
    else:
        st.info("👈 Create or select a trip from the sidebar!")

# ==================== TAB 3: BUDGET ====================
with tab3:
    st.title("💰 Budget Tracker")
    
    if st.session_state.current_trip:
        trip = st.session_state.trips[st.session_state.current_trip]
        total_budget = trip.get("budget", 1000)
        
        st.metric("Total Budget", f"${total_budget}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox(
                "Category",
                ["Accommodation", "Food", "Transportation", "Activities", "Shopping", "Other"],
                key="expense_category"
            )
        
        with col2:
            amount = st.number_input("Amount ($)", min_value=0.0, step=10.0, key="expense_amount")
        
        with col3:
            description = st.text_input("Description", placeholder="e.g., Hotel 3 nights", key="expense_desc")
        
        if st.button("➕ Add Expense"):
            if st.session_state.current_trip not in st.session_state.budget:
                st.session_state.budget[st.session_state.current_trip] = []
            
            st.session_state.budget[st.session_state.current_trip].append({
                "category": category,
                "amount": amount,
                "description": description,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("✅ Expense added!")
        
        st.markdown("---")
        
        # Display expenses
        if st.session_state.current_trip in st.session_state.budget and st.session_state.budget[st.session_state.current_trip]:
            expenses = st.session_state.budget[st.session_state.current_trip]
            
            # Summary by category
            st.subheader("📊 Budget Summary")
            category_totals = {}
            total_spent = 0
            
            for expense in expenses:
                cat = expense["category"]
                amt = expense["amount"]
                category_totals[cat] = category_totals.get(cat, 0) + amt
                total_spent += amt
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Spent", f"${total_spent:.2f}")
            with col2:
                remaining = max(0, total_budget - total_spent)
                st.metric("Remaining", f"${remaining:.2f}")
            with col3:
                percentage = (total_spent / total_budget * 100) if total_budget > 0 else 0
                st.metric("Budget Used", f"{percentage:.1f}%")
            
            st.markdown("**By Category:**")
            for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- **{cat}:** ${total:.2f}")
            
            st.markdown("---")
            st.subheader("📝 All Expenses")
            for i, expense in enumerate(expenses):
                with st.expander(f"{expense['category']} - ${expense['amount']} ({expense['date']})"):
                    st.write(f"**Description:** {expense['description']}")
                    if st.button("🗑️ Delete", key=f"delete_expense_{i}"):
                        expenses.pop(i)
                        st.rerun()
    else:
        st.info("👈 Create or select a trip from the sidebar!")

# ==================== TAB 4: FAVORITES ====================
with tab4:
    st.title("❤️ Favorite Destinations & Places")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        favorite = st.text_input("Add a Favorite Place", placeholder="e.g., Eiffel Tower, Tokyo Disneyland")
    
    with col2:
        if st.button("❤️ Add"):
            if favorite and favorite not in st.session_state.favorites:
                st.session_state.favorites.append(favorite)
                st.success("✅ Added to favorites!")
            elif favorite in st.session_state.favorites:
                st.warning("Already in favorites!")
    
    st.markdown("---")
    
    if st.session_state.favorites:
        st.subheader("Your Favorite Places")
        for i, fav in enumerate(st.session_state.favorites):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"⭐ {fav}")
            with col2:
                if st.button("✕", key=f"remove_fav_{i}"):
                    st.session_state.favorites.pop(i)
                    st.rerun()
    else:
        st.info("Start adding your favorite places!")

# ==================== TAB 5: PACKING ====================
with tab5:
    st.title("🎒 Packing Checklist")
    
    if st.session_state.current_trip:
        trip_key = st.session_state.current_trip
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            item = st.text_input("Add Item to Packing List", placeholder="e.g., Passport, Sunscreen")
        
        with col2:
            if st.button("➕"):
                if item:
                    if trip_key not in st.session_state.packing_list:
                        st.session_state.packing_list[trip_key] = []
                    st.session_state.packing_list[trip_key].append({"item": item, "packed": False})
                    st.success("✅ Added to packing list!")
        
        st.markdown("---")
        
        if trip_key in st.session_state.packing_list and st.session_state.packing_list[trip_key]:
            st.subheader("Packing Items")
            
            for i, pack_item in enumerate(st.session_state.packing_list[trip_key]):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    new_status = st.checkbox(
                        pack_item["item"],
                        value=pack_item["packed"],
                        key=f"pack_{i}"
                    )
                    st.session_state.packing_list[trip_key][i]["packed"] = new_status
                
                with col2:
                    if st.button("🗑️", key=f"delete_pack_{i}"):
                        st.session_state.packing_list[trip_key].pop(i)
                        st.rerun()
            
            # Progress
            packed_count = sum(1 for item in st.session_state.packing_list[trip_key] if item["packed"])
            total_count = len(st.session_state.packing_list[trip_key])
            st.progress(packed_count / total_count if total_count > 0 else 0, text=f"Packed: {packed_count}/{total_count}")
        
        else:
            st.info("Start adding items to your packing list!")
    else:
        st.info("👈 Create or select a trip from the sidebar!")

# ==================== TAB 6: TRAVEL AI ====================
with tab6:
    st.title("💬 Travel AI Assistant")
    st.markdown("Ask me anything about your travel! Get tips, recommendations, and advice.")
    
    if st.session_state.current_trip:
        trip = st.session_state.trips[st.session_state.current_trip]
        destination = trip.get("destination", "your destination")
        
        travel_question = st.text_area(
            "Ask your travel question:",
            placeholder=f"e.g., Best time to visit {destination}? What's the local currency? Best restaurants?"
        )
        
        if st.button("🤖 Get AI Response"):
         if travel_question:
           with st.spinner("🔍 Thinking..."):
            system_prompt = (
                "You are a helpful travel assistant. Answer travel questions concisely "
                f"with context: Destination={destination}. "
                "Use bullet points when possible."
            )
            
            # SIMPLE prompt format - no complex tokens
            full_prompt = f"{system_prompt}\n\nQ: {travel_question}\nA: "
            
            response = client.text_generation(
                full_prompt,
                max_new_tokens=300,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )
            st.markdown(response.strip())
    
    else:
        st.info("👈 Create or select a trip from the sidebar!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    🌍 **AI Travel Planner** | Plan your perfect trip with AI assistance | ✈️
    </div>
    """,
    unsafe_allow_html=True
)
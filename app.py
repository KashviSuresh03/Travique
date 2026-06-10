import streamlit as st
import pandas as pd

data=pd.read_csv("data/destination.csv")

st.title("Travique AI")
st.write("Student Budget Travel Planner")

source=st.text_input("From:")
destination=st.text_input("To:")

budget=st.number_input("Budget:", min_value=1000, step=500)

days= st.number_input("Number of days:", min_value=1, step=1)

interests = st.multiselect("Interests:", ["Nature", "Culture", "Adventure", "Food", "Relaxation"])

female_mode=st.checkbox("solo female traveler")

if st.button("Plan My Trip"):

    if not source or not destination:
        st.error("Please enter both source and destination.")
        st.stop()
    filtered_places=data[data["City"].str.lower()==destination.lower()]

    st.subheader("📍 Recommended Attractions")

    for place in filtered_places["Name"].head(5):
        st.write(f"- {place}")

    st.success("Travique AI is planning your trip!.....")

    st.subheader("Trip Summary")

    st.write(f"📍 From: {source}")
    st.write(f"📍 To: {destination}")
    st.write(f"💰 Budget: ₹{budget}")
    st.write(f"📅 Days: {days}")
    st.write(f"🎯 Interests: {', '.join(interests)}")

    if female_mode:
        st.success(f"Solo female traveler Mode Acived! We will ensure your safety and comfort throughout the trip.")

    hotel_budget = budget * 0.4
    food_budget = budget * 0.3
    travel_budget = budget * 0.3

    st.subheader("Budget Allocation")

    col1, col2, col3 = st.columns(3)

    with col1:
     st.metric("🏨 Stay", f"₹{hotel_budget:.0f}")

    with col2:
        st.metric("🍽 Food", f"₹{food_budget:.0f}")

    with col3:
        st.metric("🚌 Travel", f"₹{travel_budget:.0f}")
    interest = interests[0] if interests else "general sightseeing"
    if interest=="Nature":
        st.write("Botanical Garden")
        st.write("Nature Trail")
        st.write("Waterfall Hike")

    elif interest=="Culture":
        st.write("Local Museum")
        st.write("Historical Site")
        st.write("Cultural Show")
    
    elif interest=="Adventure":
        st.write("Ziplining")
        st.write("Kayaking")
        st.write("Rock Climbing")
    
    elif interest=="Food":
        st.write("Street Food Tour")
        st.write("Cooking Class")
        st.write("Food Market Visit")

    st.write("Suggested Itinerary")
  
    for day in range(1, days + 1):
        st.write(f"Day {day}:")
        st.write(f"- Activity 1: Explore local attractions related to {interest}")
        st.write(f"- Activity 2: Try local cuisine at a popular restaurant")
        st.write(f"- Activity 3: Relax at a recommended spot")
        st.write("Take photos and share your experience on social media with #TraviqueAI")

    if female_mode:
        st.write("Safety Tips for Solo")
        st.write("- Always stay in well-reviewed accommodations.")
        st.write("- Keep emergency contacts handy.")
        st.write("- Prefer verified transportation options.")


st.subheader("Emergency Information")

st.write("Police: 100")
st.write("Ambulance: 102")
st.write("Fire Department: 101")

if female_mode:
    st.write("Women Help Line: 1091")






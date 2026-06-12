import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    top_places=filtered_places.sort_values(by="Google review rating",ascending=False)

    st.subheader("📍 Recommended Attractions")

    
    for _, row in filtered_places.head(5).iterrows():
        st.write(f"- {row['Name']} | ⭐ {row['Google review rating']}")

    trip_places=top_places.head(days*2)["Name"]
    place_index=0

    for day in range(1, days+1):
        st.write(f"Day {day}")
        for i in range(2):
            if place_index < len(trip_places):
                st.write(f"{trip_places[place_index]}")
                place_index+=1

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

    budget_data={
    "Stay":hotel_budget,
    "Food":food_budget,
    "Travel":travel_budget
}
    fig,ax=plt.subplots()
    ax.pie(budget_data.values(), labels=budget_data.keys(), autopct="%1.1f%%")
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
     st.metric("🏨 Stay", f"₹{hotel_budget:.0f}")

    with col2:
        st.metric("🍽 Food", f"₹{food_budget:.0f}")

    with col3:
        st.metric("🚌 Travel", f"₹{travel_budget:.0f}")
    interest = interests[0] if interests else "general sightseeing"
    

    st.write("Suggested Itinerary")
  
  

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










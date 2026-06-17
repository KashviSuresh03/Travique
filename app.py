import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from google import genai


data=pd.read_csv("data/destination.csv")

with open("travique_model.pkl", "rb") as f:
    model = pickle.load(f)
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
    
st.title("Travique AI")
st.write("Student Budget Travel Planner")

source=st.text_input("From:")
destination=st.text_input("To:")

budget=st.number_input("Budget:", min_value=1000, step=500)

days= st.number_input("Number of days:", min_value=1, step=1)

interests = st.multiselect("Interests:", ["Nature", "Culture", "Adventure", "Food", "Relaxation"])
travel_style = st.selectbox(
    "Travel Style",
    ["Budget", "Balanced", "Luxury"]
)

female_mode=st.checkbox("solo female traveler")

if st.button("Plan My Trip"):

    if not source or not destination:
        st.error("Please enter both source and destination.")
        st.stop()
    filtered_places=data[data["City"].str.lower()==destination.lower()]
    if filtered_places.empty:
        st.error("Destination not found in database.")
        st.stop()
    top_places=filtered_places.sort_values(by="Google review rating",ascending=False)

    st.divider()
    st.subheader("📍 Recommended Attractions")

    
    for _, row in top_places.head(5).iterrows():
        st.write(f"- {row['Name']} | ⭐ {row['Google review rating']}")

    if not top_places.empty:
        first_place=top_places.iloc[0]

        sample=pd.DataFrame({
            "Type":[first_place["Type"]],
            "Entrance Fee in INR": [first_place["Entrance Fee in INR"]],
            "time needed to visit in hrs": [first_place["time needed to visit in hrs"]],
            "DSLR Allowed": [first_place["DSLR Allowed"]],
            "Best Time to visit": [first_place["Best Time to visit"]]

        })

        predicted_rating=model.predict(sample)
        
        st.subheader("🤖 AI Attraction Score")
        st.success( f"Predicted Rating: ⭐ {predicted_rating[0]:.2f}/5")

    trip_places=top_places.head(days*2)["Name"].tolist()
    place_index=0

    for day in range(1, days+1):
        st.subheader(f"📅 Day {day}")
        for i in range(2):
            if place_index < len(trip_places):
                st.write(f"{trip_places[place_index]}")
                place_index+=1

    st.success("Travique AI is planning your trip!.....")
    st.divider()
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
    st.divider()
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
    daily_budget = budget / days
    st.subheader("💵 Daily Budget")
    st.metric("Budget Per Day",f"₹{daily_budget:.0f}")
    
    st.subheader("🎓 Student Budget Analysis")

    if daily_budget < 1000:
        st.warning("Budget is quite tight for this trip.")

    elif daily_budget < 2500:
        st.info("Good student budget. Plan spending carefully.")

    else:
        st.success("Comfortable budget for a student trip.")



    st.subheader("💡 Student Travel Tips")

    if daily_budget < 1000:
        st.write("• Prefer hostels or dorm stays")
        st.write("• Use local buses instead of cabs")
        st.write("• Prioritize free attractions")

    elif daily_budget < 2500:
        st.write("• Mix free and paid attractions")
        st.write("• Book accommodation in advance")
        st.write("• Use public transport when possible")

    else:
        st.write("• Comfortable budget for sightseeing")
        st.write("• Consider guided tours")
        st.write("• Explore local food experiences")

    st.divider()
    st.subheader("🤖 AI Travel Assistant")

    prompt = f"""
    Create a detailed travel itinerary.

    Source: {source}
    Destination: {destination}
    Budget: ₹{budget}
    Days: {days}
    Travel Style: {travel_style}

    Interests:
    {', '.join(interests)}

    Solo Female Traveler:
    {female_mode}

    Include:

    1. Day-wise itinerary
    2. Estimated daily spending
    3. Local food recommendations
    4. Packing checklist
    5. Safety advice
    6. Student budget tips

    Format clearly using headings.
    """

    with st.spinner("Travique AI is planning your trip..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            ai_reply = response.text

            st.markdown(ai_reply)

            st.download_button( 
                "📄 Download Itinerary",
                ai_reply,
                file_name=f"{destination}_itinerary.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"AI Error: {e}")


    
        

    if female_mode:
        st.subheader("🛡 Safety Checklist")

        st.write("✓ Share live location with trusted contacts")
        st.write("✓ Stay in well-reviewed accommodations")
        st.write("✓ Use verified transportation services")
        st.write("✓ Avoid isolated areas at night")
        st.write("✓ Keep emergency contacts handy")

st.subheader("Emergency Information")

st.write("Police: 100")
st.write("Ambulance: 102")
st.write("Fire Department: 101")

if female_mode:
    st.write("Women Help Line: 1091")










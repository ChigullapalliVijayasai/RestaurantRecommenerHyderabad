import streamlit as st
import pandas as pd

# ----------------------------
# 🟢 Load and clean dataset
# ----------------------------
try:
    df = pd.read_csv("restaurants.csv")
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    st.success("✅ Restaurant data loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# ----------------------------
# 🎨 Page Config and Styling
# ----------------------------
st.set_page_config(page_title="Hyderabad Restaurant Recommender", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: lavender;
        color: #FFD700; /* dark yellow text */
        font-family: 'Arial';
    }
    .stApp {
        background-color: lavender;
        color: #FFD700;
    }
    .stTextInput > div > div > input {
        color: #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 🔍 Filter Function
# ----------------------------
def filter_restaurants(df, query):
    query = query.lower()
    if "city" in df.columns:
        df = df[df["city"].str.lower().str.contains("hyderabad", na=False)]

    if "restaurant" in query or "hyderabad" in query:
        results = df.copy()
    else:
        results = df[df.apply(lambda row: query in str(row).lower(), axis=1)]

    return results.head(20)  # limit to first 20 for display


# ----------------------------
# 💬 Streamlit UI
# ----------------------------
st.title("🍴 Hyderabad Restaurant Recommender")

query = st.text_input("Ask me about Hyderabad restaurants:", placeholder="e.g., best biryani in Hyderabad")

if st.button("Find Restaurants"):
    if query.strip() == "":
        st.warning("Please enter a search query.")
    else:
        results = filter_restaurants(df, query)
        if not results.empty:
            st.write(f"### 🍽️ Found {len(results)} restaurants:")
            st.dataframe(results)
        else:
            st.error("No restaurants found for your query.")

# ----------------------------
# 📊 Extra Info
# ----------------------------
if st.checkbox("Show data sample"):
    st.dataframe(df.head(10))

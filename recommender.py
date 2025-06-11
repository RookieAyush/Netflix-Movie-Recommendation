import streamlit as st
from recommender import recommend, fetch_poster

st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.markdown("<h1 style='color:red;'>🍿 Netflix Recommendation Engine</h1>", unsafe_allow_html=True)

movie_input = st.text_input("Enter a Netflix title or genre (e.g., Comedy, Horror, Romance)", "")

if movie_input:
    results = recommend(movie_input)

    if isinstance(results, list) or results is None or len(results) == 0:
        st.error("Sorry, no matching results found.")
    else:
        st.success("Here are some titles you might like:")
        cols = st.columns(2)

        for idx, row in results.iterrows():
            poster_url = fetch_poster(row['title'])

            with cols[idx % 2]:
                st.image(poster_url, width=160)
                st.subheader(row['title'])
                st.write(f"**Genre:** {row['listed_in']}")
                st.caption(row['description'][:200] + "...")
        
        st.markdown("---")

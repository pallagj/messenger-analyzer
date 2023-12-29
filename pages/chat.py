import altair as alt
import streamlit as st
from storage import MessageStorage
import plotly.express as px

if 'messages' in st.session_state:
    messages = st.session_state['messages']  # type: MessageStorage

    st.write("## Messages by Date")

    title = st.sidebar.selectbox("Select chat:", messages.get_titles())

    daily_interval = st.number_input("Count by day:", min_value=1, step=1, value=7)
    st.line_chart(messages.get_messages_by_time(title, daily_interval))

    messages_by_time = messages.get_messages_by_time_by_sender(title, daily_interval)
    chart = alt.Chart(messages_by_time).mark_area().encode(
        x="datetime:T",
        y=alt.Y("message_count:Q", stack="normalize"),
        color="sender_name:N"
    )
    st.altair_chart(chart, use_container_width=True)

    st.write("## Reactions")

    reaction_matrix = messages.get_reaction_matrix(title)
    fig = px.imshow(reaction_matrix, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    participants = messages.get_participants(title)
    st.bar_chart(messages.get_reaction_counts_by_participant(title))

    reactions = messages.get_all_reactions(title)
    reaction = [s.split(" ")[0] for s in st.multiselect("Reaction:", reactions, default=reactions[:3])]
    reaction_matrix = messages.get_reaction_matrix(title, reaction)
    fig = px.imshow(reaction_matrix, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.write("## Count by Participant")
    st.bar_chart(messages.get_participant_count(title))






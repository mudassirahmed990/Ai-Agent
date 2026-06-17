import altair as alt
import pandas as pd
import streamlit as st

def render_category_chart(df: pd.DataFrame):
    if df.empty or 'category' not in df.columns:
        st.info("No data available.")
        return

    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']

    chart = alt.Chart(category_counts).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X('Category:N', sort='-y', axis=alt.Axis(
            labelAngle=-35,
            labelColor='#7c83a8',
            labelFont='Inter',
            labelFontSize=11,
            tickColor='transparent',
            domainColor='transparent',
            titleColor='#7c83a8'
        )),
        y=alt.Y('Count:Q', axis=alt.Axis(
            labelColor='#7c83a8',
            labelFont='Inter',
            gridColor='rgba(124,58,237,0.08)',
            domainColor='transparent',
            tickColor='transparent'
        )),
        color=alt.Color('Category:N',
            scale=alt.Scale(
                range=['#7c3aed','#06b6d4','#a78bfa','#f43f5e',
                       '#f59e0b','#10b981','#3b82f6','#ec4899',
                       '#8b5cf6','#14b8a6']
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip('Category:N', title='Crime Type'),
            alt.Tooltip('Count:Q', title='Total Reports')
        ]
    ).properties(
        height=300,
        background='transparent'
    ).configure_view(
        strokeWidth=0,
        fill='transparent'
    )

    st.altair_chart(chart, use_container_width=True)


def render_priority_pie_chart(df: pd.DataFrame):
    if df.empty or 'priority' not in df.columns:
        st.info("No data available.")
        return

    priority_counts = df['priority'].value_counts().reset_index()
    priority_counts.columns = ['Priority', 'Count']

    chart = alt.Chart(priority_counts).mark_arc(innerRadius=60, outerRadius=120).encode(
        theta=alt.Theta('Count:Q'),
        color=alt.Color('Priority:N',
            scale=alt.Scale(
                domain=['High Priority', 'Medium Priority', 'Low Priority'],
                range=['#f43f5e', '#f59e0b', '#10b981']
            ),
            legend=alt.Legend(
                labelColor='#c4c9e8',
                labelFont='Inter',
                labelFontSize=12,
                titleColor='#7c83a8',
                orient='bottom'
            )
        ),
        tooltip=[
            alt.Tooltip('Priority:N', title='Priority'),
            alt.Tooltip('Count:Q', title='Reports')
        ]
    ).properties(
        height=300,
        background='transparent'
    ).configure_view(
        strokeWidth=0,
        fill='transparent'
    )

    st.altair_chart(chart, use_container_width=True)

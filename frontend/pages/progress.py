import streamlit as st
from datetime import datetime, timedelta, date
from typing import Dict, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from styles.theme import get_theme_colors
from components.cards import render_metric_card
from utils.api import get_user_progress, get_categories_breakdown
from utils.state import is_authenticated

def create_weekly_facts_chart(progress_data: Dict, colors: Dict) -> Optional[go.Figure]:
    """Create a bar chart for facts learned this week."""
    try:
        facts_this_week = progress_data.get("facts_this_week", 0)
        total_facts = progress_data.get("total_facts", 0)
        
        # Create mock daily data for the week based on facts_this_week
        # In a real implementation, you'd get daily breakdown from backend
        today = date.today()
        week_days = []
        daily_facts = []
        
        for i in range(7):
            day_date = today - timedelta(days=6-i)
            week_days.append(day_date.strftime("%a"))
            
            # Distribute facts across the week (mock data based on total)
            if i == 6:  # Today
                daily_facts.append(max(0, facts_this_week - sum(daily_facts)))
            else:
                # Random distribution for demo (in reality, this would come from backend)
                import random
                daily_facts.append(random.randint(0, max(1, facts_this_week // 4)))
        
        # Ensure we don't exceed facts_this_week
        total_distributed = sum(daily_facts)
        if total_distributed > facts_this_week:
            # Scale down proportionally
            scale_factor = facts_this_week / total_distributed if total_distributed > 0 else 0
            daily_facts = [int(fact * scale_factor) for fact in daily_facts]
        
        df = pd.DataFrame({
            "day": week_days,
            "facts": daily_facts
        })
        
        fig = px.bar(
            df, 
            x="day", 
            y="facts", 
            title="📚 Facts Learned This Week",
            color_discrete_sequence=[colors['accent']]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            title_font_color=colors['text'],
            title_font_size=18,
            height=400,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        
        fig.update_xaxes(
            gridcolor='rgba(128,128,128,0.2)', 
            zerolinecolor='rgba(128,128,128,0.2)',
            title_text="Day of Week"
        )
        fig.update_yaxes(
            gridcolor='rgba(128,128,128,0.2)', 
            zerolinecolor='rgba(128,128,128,0.2)',
            title_text="Facts Learned"
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating facts chart: {e}")
        return None

def create_categories_pie_chart(categories_data: Dict, colors: Dict) -> Optional[go.Figure]:
    """Create a pie chart for categories breakdown."""
    try:
        if not categories_data:
            st.error("No categories data provided")
            return None
        categories = categories_data.get("categories", {})
        
        if not categories:
            # Create a placeholder chart
            fig = go.Figure(data=[go.Pie(
                labels=["No Data"],
                values=[1],
                hole=0.4,
                marker_colors=[colors['border']]
            )])
            
            fig.update_layout(
                title="🏷️ Facts by Category",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=colors['text']),
                title_font_color=colors['text'],
                title_font_size=18,
                height=400,
                showlegend=True,
                annotations=[dict(text='No facts yet', x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            
            return fig
        
        # Prepare data
        labels = list(categories.keys())
        values = list(categories.values())
        
        # Create color palette using available theme colors
        color_palette = [
            colors['accent'],      # #6366F1 - indigo
            colors['secondary'],   # #8B5CF6 - violet  
            colors['success'],     # #10B981 - emerald
            colors['warning'],     # #F59E0B - amber
            colors['error'],       # #EF4444 - red
            '#F97316',  # orange
            '#84CC16',  # lime
            '#06B6D4',  # cyan
            '#EC4899',  # pink
            '#8B5CF6'   # violet (repeat)
        ]
        
        # Extend colors if needed
        while len(color_palette) < len(labels):
            color_palette.extend(color_palette)
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=color_palette[:len(labels)]
        )])
        
        fig.update_layout(
            title="🏷️ Facts by Category",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            title_font_color=colors['text'],
            title_font_size=18,
            height=400,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Facts: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating categories chart: {e}")
        return None

def render_progress() -> None:
    """Render the progress page with charts and metrics"""
    if not is_authenticated():
        st.error("🔐 Please log in to view your progress.")
        return
    
    colors = get_theme_colors()
    
    st.subheader("📊 Your Progress")
    
    # Fetch data from backend
    with st.spinner("📊 Loading your progress data..."):
        progress_data = get_user_progress()
        categories_data = get_categories_breakdown()
    
    if not progress_data:
        st.error("❌ Could not load progress data. Please try again later.")
        return
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card(
            str(progress_data.get("total_facts", 0)), 
            "Total Facts Learned"
        )
    
    with col2:
        render_metric_card(
            f"{progress_data.get('current_streak', 0)} days", 
            "Current Streak"
        )
    
    with col3:
        render_metric_card(
            f"{progress_data.get('longest_streak', 0)} days", 
            "Longest Streak"
        )
    
    st.markdown("---")
    
    # Create charts section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### 📊 Weekly Activity")
        
        # Facts learned this week chart
        facts_chart = create_weekly_facts_chart(progress_data, colors)
        if facts_chart:
            st.plotly_chart(facts_chart, use_container_width=True, key="facts_chart")
        else:
            st.info("📊 Unable to display facts chart. Data may be unavailable.")
        
        # Weekly stats
        facts_this_week = progress_data.get("facts_this_week", 0)
        st.metric(
            "Facts This Week", 
            facts_this_week,
            delta=f"+{facts_this_week} this week" if facts_this_week > 0 else "No activity this week"
        )
    
    with chart_col2:
        st.markdown("### 🏷️ Category Breakdown")
        
        # Categories pie chart
        if categories_data:
            categories_chart = create_categories_pie_chart(categories_data, colors)
            if categories_chart:
                st.plotly_chart(categories_chart, use_container_width=True, key="categories_chart")
            else:
                st.info("🏷️ Unable to display categories chart.")
        else:
            st.info("🏷️ No category data available yet. Start learning to see your progress!")
        
        # Category details
        if categories_data and categories_data.get("categories"):
            st.markdown("#### 📋 Details")
            categories = categories_data["categories"]
            total = categories_data.get("total", sum(categories.values()))
            
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total * 100) if total > 0 else 0
                st.write(f"**{category}:** {count} facts ({percentage:.1f}%)")
        else:
            st.write("No categories yet. Start exploring health topics!")
    
    # Additional insights
    st.markdown("---")
    st.markdown("### 🎯 Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        last_activity = progress_data.get("last_activity")
        if last_activity:
            try:
                last_date = datetime.strptime(last_activity, "%Y-%m-%d").date()
                days_ago = (date.today() - last_date).days
                
                if days_ago == 0:
                    st.success("🔥 You're active today! Keep it up!")
                elif days_ago == 1:
                    st.info("📅 Last activity: Yesterday")
                else:
                    st.warning(f"📅 Last activity: {days_ago} days ago")
            except ValueError:
                st.info("📅 Activity tracking available")
        else:
            st.info("📅 Start your learning journey today!")
    
    with col2:
        total_facts = progress_data.get("total_facts", 0)
        current_streak = progress_data.get("current_streak", 0)
        
        if total_facts >= 50:
            st.success("🏆 Health Expert! You've learned 50+ facts!")
        elif total_facts >= 20:
            st.success("🌟 Health Enthusiast! Keep learning!")
        elif total_facts >= 5:
            st.info("📚 Getting started! You're on your way!")
        else:
            st.info("🚀 Begin your health learning journey!")
        
        if current_streak >= 7:
            st.success(f"🔥 Amazing! {current_streak}-day streak!")
        elif current_streak >= 3:
            st.info(f"💪 Great! {current_streak}-day streak!")
    
    # Learning suggestions
    if total_facts < 5:
        st.markdown("---")
        st.markdown("### 💡 Get Started")
        st.info("""
        🔍 **Search** for health topics you're curious about
        
        🧠 **Take quizzes** to test your knowledge
        
        🏷️ **Explore categories** like Nutrition, Exercise, and Mental Health
        """)
    elif current_streak == 0:
        st.markdown("---")
        st.markdown("### 🎯 Come Back Tomorrow")
        st.info("Keep your learning streak alive! Come back tomorrow to continue your health education journey.")
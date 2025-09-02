import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="JEE/NEET Institute Finder",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("🎯 JEE/NEET Institute Finder Dashboard")
st.markdown("### Find the perfect coaching institute for your competition exam preparation!")

# Sample data for institutes
@st.cache_data
def load_institute_data():
    institutes = {
        'Institute_Name': [
            'Aakash Institute', 'Physics Wallah', 'Allen Career Institute', 
            'Unacademy', 'BYJU\'S', 'Vedantu', 'Resonance', 'FIITJEE',
            'Narayana', 'Sri Chaitanya', 'Kota Factory', 'Career Point',
            'Bansal Classes', 'VMC (Vidyamandir Classes)', 'B2E Learning'
        ],
        'JEE_Success_Rate': [85, 78, 92, 75, 70, 72, 88, 90, 82, 80, 86, 83, 89, 87, 74],
        'NEET_Success_Rate': [88, 82, 94, 78, 74, 76, 85, 83, 86, 84, 81, 85, 84, 82, 77],
        'Online_Available': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Limited', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Limited', 'Yes', 'Yes'],
        'Location': ['Pan India', 'Online', 'Rajasthan/UP', 'Online', 'Online', 'Online', 'Rajasthan', 'Delhi/NCR', 'South India', 'South India', 'Rajasthan', 'Rajasthan', 'Rajasthan', 'Pan India', 'Online'],
        'Study_Material_Rating': [9, 8, 10, 8, 7, 7, 9, 9, 8, 8, 9, 8, 9, 9, 7],
        'Faculty_Rating': [8.5, 9.2, 9.0, 8.0, 7.5, 7.8, 8.8, 8.7, 8.2, 8.0, 8.9, 8.3, 8.9, 8.6, 7.9],
        'Infrastructure_Rating': [9, 7, 9, 8, 8, 7, 8, 9, 8, 8, 7, 8, 8, 8, 8],
        'Batch_Size': ['Medium', 'Large', 'Small', 'Large', 'Large', 'Medium', 'Small', 'Small', 'Medium', 'Medium', 'Small', 'Medium', 'Small', 'Small', 'Large']
    }
    return pd.DataFrame(institutes)

# Load data
df = load_institute_data()

# Sidebar for filters
st.sidebar.header("🔍 Filter Your Search")

# Basic filters
exam_type = st.sidebar.selectbox(
    "Select Exam Type:", 
    ["Both JEE & NEET", "JEE Main/Advanced", "NEET"]
)

online_preference = st.sidebar.radio(
    "Learning Mode Preference:", 
    ["No Preference", "Online Only", "Offline Available", "Limited Online OK"]
)

location_preference = st.sidebar.multiselect(
    "Preferred Locations:", 
    ["Pan India", "Online", "Rajasthan/UP", "Delhi/NCR", "South India"],
    default=["Pan India", "Online"]
)

batch_size_pref = st.sidebar.selectbox(
    "Preferred Batch Size:",
    ["No Preference", "Small", "Medium", "Large"]
)

minimum_success_rate = st.sidebar.slider(
    "Minimum Success Rate Required (%)",
    50, 95, 75
)

# Apply filters
filtered_df = df.copy()

# Filter by online availability
if online_preference == "Online Only":
    filtered_df = filtered_df[filtered_df['Online_Available'] == 'Yes']
elif online_preference == "Offline Available":
    filtered_df = filtered_df[filtered_df['Online_Available'].isin(['Yes', 'Limited'])]
elif online_preference == "Limited Online OK":
    filtered_df = filtered_df[filtered_df['Online_Available'].isin(['Yes', 'Limited'])]

# Filter by location
if location_preference:
    filtered_df = filtered_df[filtered_df['Location'].isin(location_preference)]

# Filter by batch size
if batch_size_pref != "No Preference":
    filtered_df = filtered_df[filtered_df['Batch_Size'] == batch_size_pref]

# Filter by success rate based on exam type
if exam_type == "JEE Main/Advanced":
    filtered_df = filtered_df[filtered_df['JEE_Success_Rate'] >= minimum_success_rate]
    filtered_df = filtered_df.sort_values('JEE_Success_Rate', ascending=False)
elif exam_type == "NEET":
    filtered_df = filtered_df[filtered_df['NEET_Success_Rate'] >= minimum_success_rate]
    filtered_df = filtered_df.sort_values('NEET_Success_Rate', ascending=False)
else:
    # For both exams, use average success rate
    filtered_df['Avg_Success_Rate'] = (filtered_df['JEE_Success_Rate'] + filtered_df['NEET_Success_Rate']) / 2
    filtered_df = filtered_df[filtered_df['Avg_Success_Rate'] >= minimum_success_rate]
    filtered_df = filtered_df.sort_values('Avg_Success_Rate', ascending=False)

# Display results
st.markdown("---")
st.header(f"📋 Search Results ({len(filtered_df)} institutes found)")

if len(filtered_df) > 0:
    # Display top recommendations
    st.subheader("🏆 Top Recommendations")
    
    for idx, (_, institute) in enumerate(filtered_df.head(5).iterrows()):
        with st.expander(f"#{idx+1} {institute['Institute_Name']}", expanded=(idx < 3)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**📍 Location:** {institute['Location']}")
                st.write(f"**🌐 Online Available:** {institute['Online_Available']}")
                st.write(f"**👥 Batch Size:** {institute['Batch_Size']}")
                if exam_type == "JEE Main/Advanced":
                    st.write(f"**🎯 JEE Success Rate:** {institute['JEE_Success_Rate']}%")
                elif exam_type == "NEET":
                    st.write(f"**🏥 NEET Success Rate:** {institute['NEET_Success_Rate']}%")
                else:
                    st.write(f"**🎯 JEE Success Rate:** {institute['JEE_Success_Rate']}%")
                    st.write(f"**🏥 NEET Success Rate:** {institute['NEET_Success_Rate']}%")
            
            with col2:
                st.write(f"**👨‍🏫 Faculty Rating:** {institute['Faculty_Rating']}/10")
                st.write(f"**📚 Study Material:** {institute['Study_Material_Rating']}/10")
                st.write(f"**🏢 Infrastructure:** {institute['Infrastructure_Rating']}/10")
                
                # Overall rating calculation
                overall_rating = (institute['Faculty_Rating'] + institute['Study_Material_Rating'] + institute['Infrastructure_Rating']) / 3
                st.write(f"**⭐ Overall Rating:** {overall_rating:.1f}/10")

    # Complete list in table format
    st.markdown("---")
    st.subheader("📊 Complete Institute List")
    
    # Prepare display dataframe
    display_columns = ['Institute_Name', 'Location', 'Online_Available', 'Batch_Size']
    
    if exam_type == "JEE Main/Advanced":
        display_columns.extend(['JEE_Success_Rate', 'Faculty_Rating', 'Study_Material_Rating'])
    elif exam_type == "NEET":
        display_columns.extend(['NEET_Success_Rate', 'Faculty_Rating', 'Study_Material_Rating'])
    else:
        display_columns.extend(['JEE_Success_Rate', 'NEET_Success_Rate', 'Faculty_Rating', 'Study_Material_Rating'])
    
    # Display the table
    st.dataframe(
        filtered_df[display_columns].reset_index(drop=True),
        use_container_width=True,
        height=400
    )
    
    # Quick stats
    st.markdown("---")
    st.subheader("📈 Quick Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_faculty = filtered_df['Faculty_Rating'].mean()
        st.metric("Average Faculty Rating", f"{avg_faculty:.1f}/10")
    
    with col2:
        online_count = len(filtered_df[filtered_df['Online_Available'] == 'Yes'])
        st.metric("Institutes with Online Classes", f"{online_count}/{len(filtered_df)}")
    
    with col3:
        if exam_type == "JEE Main/Advanced":
            avg_success = filtered_df['JEE_Success_Rate'].mean()
            st.metric("Average JEE Success Rate", f"{avg_success:.1f}%")
        elif exam_type == "NEET":
            avg_success = filtered_df['NEET_Success_Rate'].mean()
            st.metric("Average NEET Success Rate", f"{avg_success:.1f}%")
        else:
            avg_success = filtered_df[['JEE_Success_Rate', 'NEET_Success_Rate']].mean().mean()
            st.metric("Average Success Rate", f"{avg_success:.1f}%")

else:
    st.warning("🚫 No institutes match your current criteria. Please try adjusting your filters.")
    st.info("💡 **Suggestions:**")
    st.write("• Lower the minimum success rate requirement")
    st.write("• Expand location preferences")
    st.write("• Change batch size preference to 'No Preference'")
    st.write("• Modify learning mode preference")

# Institute comparison feature
if len(filtered_df) >= 2:
    st.markdown("---")
    st.subheader("🔍 Compare Institutes")
    
    # Select institutes to compare
    institutes_to_compare = st.multiselect(
        "Select institutes to compare (max 3):",
        filtered_df['Institute_Name'].tolist(),
        max_selections=3
    )
    
    if len(institutes_to_compare) >= 2:
        comparison_df = filtered_df[filtered_df['Institute_Name'].isin(institutes_to_compare)]
        
        # Display comparison
        st.write("**Comparison Table:**")
        comparison_columns = ['Institute_Name', 'JEE_Success_Rate', 'NEET_Success_Rate', 
                            'Faculty_Rating', 'Study_Material_Rating', 'Infrastructure_Rating', 
                            'Online_Available', 'Batch_Size']
        
        st.dataframe(
            comparison_df[comparison_columns].set_index('Institute_Name'),
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>📚 JEE/NEET Institute Finder | Built with Streamlit</p>
    <p>💡 Use the filters on the left to customize your search results</p>
</div>
""", unsafe_allow_html=True)
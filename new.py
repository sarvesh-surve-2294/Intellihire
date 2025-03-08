# import streamlit as st
# import os
# import time
# import cv2
# import numpy as np
# from deepface import DeepFace
# import firebase_admin
# from firebase_admin import credentials, firestore
# import cohere
# import base64
# import pandas as pd
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from PIL import Image
# import pyautogui  # For screen capture

# # Fix for DeepFace compatibility issues with TensorFlow
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# # Custom CSS for a more modern and clean appearance
# st.markdown("""
# <style>
#     /* Main UI colors and styling */
#     :root {
#         --primary-color: #2E3B55;
#         --secondary-color: #4A6FBF;
#         --accent-color: #3498db;
#         --text-color: #333;
#         --background-color: #F7F9FC;
#         --card-background: #FFFFFF;
#         --success-color: #28a745;
#         --warning-color: #ffc107;
#         --danger-color: #dc3545;
#     }
    
#     /* Main container styling */
#     .main {
#         background-color: var(--background-color);
#         padding: 1.5rem;
#     }
    
#     /* Header styling */
#     .main-header {
#         color: var(--primary-color);
#         font-weight: 700;
#         margin-bottom: 1.5rem;
#         padding-bottom: 1rem;
#         border-bottom: 2px solid var(--secondary-color);
#     }
    
#     /* Section styling */
#     .section-header {
#         background-color: var(--primary-color);
#         color: white;
#         padding: 1rem;
#         border-radius: 8px 8px 0 0;
#         font-weight: 600;
#         margin-top: 2rem;
#     }
    
#     .section-content {
#         background-color: var(--card-background);
#         padding: 1.5rem;
#         border-radius: 0 0 8px 8px;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
    
#     /* Buttons styling */
#     .stButton > button {
#         background-color: var(--primary-color);
#         color: white;
#         border-radius: 6px;
#         padding: 0.5rem 1rem;
#         font-weight: 500;
#         border: none;
#         transition: all 0.3s ease;
#     }
    
#     .stButton > button:hover {
#         background-color: var(--secondary-color);
#         transform: translateY(-2px);
#     }
    
#     /* Profile card styling */
#     .profile-card {
#         background-color: #f0f2f6;
#         padding: 15px;
#         border-radius: 10px;
#         border-left: 4px solid var(--accent-color);
#         margin-top: 10px;
#     }
    
#     .profile-card h4 {
#         color: var(--primary-color);
#         border-bottom: 1px solid #ccc;
#         padding-bottom: 8px;
#         margin-bottom: 12px;
#     }
    
#     /* Table styling */
#     .styled-table {
#         width: 100%;
#         border-collapse: collapse;
#         margin: 1rem 0;
#         font-size: 0.9em;
#         border-radius: 6px;
#         overflow: hidden;
#         box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
#     }
    
#     .styled-table thead tr {
#         background-color: var(--primary-color);
#         color: white;
#         text-align: left;
#     }
    
#     .styled-table th,
#     .styled-table td {
#         padding: 12px 15px;
#     }
    
#     .styled-table tbody tr {
#         border-bottom: 1px solid #dddddd;
#     }
    
#     .styled-table tbody tr:nth-of-type(even) {
#         background-color: #f3f3f3;
#     }
    
#     .styled-table tbody tr:last-of-type {
#         border-bottom: 2px solid var(--primary-color);
#     }
    
#     /* Status indicators */
#     .status-indicator {
#         display: inline-block;
#         width: 12px;
#         height: 12px;
#         border-radius: 50%;
#         margin-right: 8px;
#     }
    
#     .status-high {
#         background-color: var(--danger-color);
#     }
    
#     .status-medium {
#         background-color: var(--warning-color);
#     }
    
#     .status-low {
#         background-color: var(--success-color);
#     }
    
#     /* Question card styling */
#     .question-card {
#         background-color: #f8f9fa;
#         padding: 12px;
#         border-radius: 6px;
#         margin-bottom: 12px;
#         border-left: 3px solid var(--accent-color);
#     }
    
#     /* Responsive iframe */
#     .responsive-iframe {
#         position: relative;
#         width: 100%;
#         height: 0;
#         padding-bottom: 56.25%;
#         margin-bottom: 1rem;
#     }
    
#     .responsive-iframe iframe {
#         position: absolute;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         border: none;
#         border-radius: 6px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # 1. Firebase Initialization
# # -----------------------------
# if not firebase_admin._apps:
#     cred = credentials.Certificate(
#         r"C:\\Users\\aadik\\Downloads\\assessai-44afc-firebase-adminsdk-fbsvc-4e13d0986d.json"
#     )  # Replace with your Firebase credentials path
#     firebase_admin.initialize_app(cred)
# db = firestore.client()

# # -----------------------------
# # 2. Initialize Cohere
# # -----------------------------
# COHERE_API_KEY = st.secrets["cohere"]["api_key"]
# co = cohere.Client(COHERE_API_KEY)

# # -----------------------------
# # 3. Google Sheets Integration
# # -----------------------------
# def setup_google_sheets_api():
#     # Set up Google Sheets API connection using service account
#     credentials = service_account.Credentials.from_service_account_file(
#         'C:\\Users\\aadik\\OneDrive\\Documents\\Desktop\\codewHari.py\\moonlit-haven-452014-i4-248bff09d735.json',
#         scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
#     )
#     service = build('sheets', 'v4', credentials=credentials)
#     return service

# def fetch_sheet_data(service, spreadsheet_id):
#     """Fetch data from Google Sheets"""
#     try:
#         # Get the first sheet
#         sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#         sheet_name = sheet_metadata['sheets'][0]['properties']['title']
        
#         # Get all values from the sheet
#         result = service.spreadsheets().values().get(
#             spreadsheetId=spreadsheet_id,
#             range=sheet_name
#         ).execute()
        
#         rows = result.get('values', [])
        
#         if not rows:
#             st.error("No data found in the spreadsheet.")
#             return []
            
#         # Assume first row is the header
#         headers = rows[0]
        
#         # Create a list of candidates
#         candidates = []
#         for row in rows[1:]:  # Skip header row
#             # Extend row with empty strings if it's shorter than headers
#             row_data = row + [''] * (len(headers) - len(row))
            
#             # Find the exact indices for each column
#             name_idx = headers.index("Name") if "Name" in headers else -1
#             email_idx = headers.index("Email") if "Email" in headers else -1
#             edu_idx = -1
#             for i, h in enumerate(headers):
#                 if "Education" in h:
#                     edu_idx = i
#                     break
#             role_idx = -1
#             for i, h in enumerate(headers):
#                 if "Job role" in h:
#                     role_idx = i
#                     break
#             skills_idx = -1
#             for i, h in enumerate(headers):
#                 if "Skills" in h:
#                     skills_idx = i
#                     break
#             exp_idx = -1
#             for i, h in enumerate(headers):
#                 if "Years" in h and "experience" in h:
#                     exp_idx = i
#                     break
            
#             # Create profile using found indices
#             profile_data = {
#                 "name": row_data[name_idx] if name_idx >= 0 and name_idx < len(row_data) else "Unknown",
#                 "email": row_data[email_idx] if email_idx >= 0 and email_idx < len(row_data) else "Unknown",
#                 "education": row_data[edu_idx] if edu_idx >= 0 and edu_idx < len(row_data) else "Unknown",
#                 "role": row_data[role_idx] if role_idx >= 0 and role_idx < len(row_data) else "Unknown",
#                 "skills": row_data[skills_idx] if skills_idx >= 0 and skills_idx < len(row_data) else "Unknown",
#                 "experience": row_data[exp_idx] if exp_idx >= 0 and exp_idx < len(row_data) else "Unknown"
#             }
            
#             # Only add candidates with a name
#             if profile_data["name"] and profile_data["name"] != "Unknown":
#                 # Store in Firebase
#                 db.collection("candidates").document(profile_data["name"]).set(profile_data)
#                 candidates.append(profile_data)
        
#         return candidates
#     except Exception as e:
#         st.error(f"Error fetching spreadsheet data: {str(e)}")
#         return []

# def extract_spreadsheet_id(sheet_url):
#     """Extract the spreadsheet ID from a Google Sheets URL"""
#     import re
#     # Pattern to match the ID in a Google Sheets URL
#     pattern = r"/d/([a-zA-Z0-9-_]+)"
#     match = re.search(pattern, sheet_url)
#     if match:
#         return match.group(1)
#     return None

# # -----------------------------
# # App Title & Layout
# # -----------------------------
# st.markdown('<h1 class="main-header">Recruiter Dashboard - AI Interview Assistant</h1>', unsafe_allow_html=True)

# # Create a two-column layout for the main content
# left_col, right_col = st.columns([1, 3])

# # -----------------------------
# # Left Column: Candidate Management
# # -----------------------------
# with left_col:
#     st.markdown('<div class="section-header">Candidate Profiles</div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
#     # Google Sheets URL input
#     sheet_url = st.text_input(
#         "Google Sheets URL", 
#         value="https://docs.google.com/spreadsheets/d/1ePTP7QhzLZvf5YJI2qTX78wOeSupfmagBzOZ_MvpywQ/edit?usp=sharing",
#         help="URL of the Google Sheet containing candidate information"
#     )
    
#     # Initialize candidates list in session state if it doesn't exist
#     if "candidates" not in st.session_state:
#         st.session_state["candidates"] = []
    
#     if st.button("Sync Candidate Profiles"):
#         if sheet_url:
#             with st.spinner("Syncing profiles from Google Sheets..."):
#                 try:
#                     # Extract the spreadsheet ID from the URL
#                     spreadsheet_id = extract_spreadsheet_id(sheet_url)
                    
#                     if not spreadsheet_id:
#                         st.error("Invalid Google Sheets URL. Please check and try again.")
#                     else:
#                         service = setup_google_sheets_api()
#                         candidates = fetch_sheet_data(service, spreadsheet_id)
                        
#                         if candidates:
#                             st.success(f"Successfully synced {len(candidates)} candidate profiles!")
#                             # Store the candidates in session state for display
#                             st.session_state["candidates"] = candidates
#                         else:
#                             st.warning("No candidate profiles found in the spreadsheet.")
#                 except Exception as e:
#                     st.error(f"Error syncing profiles: {str(e)}")
#         else:
#             st.warning("Please enter a Google Sheets URL")
    
#     # Display list of candidates
#     st.subheader("Available Candidates")
#     if st.session_state["candidates"]:
#         # Fix: Make sure we have actual names in the dropdown
#         candidate_names = [candidate["name"] for candidate in st.session_state["candidates"] if candidate["name"] != "Unknown"]
        
#         if candidate_names:
#             selected_candidate = st.selectbox(
#                 "Select a candidate",
#                 options=candidate_names,
#                 index=0,
#                 key="candidate_select"
#             )
            
#             # Fix: Find the selected candidate's profile in session state
#             selected_profile = next((c for c in st.session_state["candidates"] if c["name"] == selected_candidate), None)
            
#             if selected_profile:
#                 st.session_state["current_profile"] = selected_profile
            
#                 # Display the selected candidate profile in a card format
#                 st.markdown("""
#                 <div class="profile-card">
#                     <h4>Selected Candidate</h4>
#                 """, unsafe_allow_html=True)
                
#                 st.markdown(f"""
#                     <p><strong>Name:</strong> {selected_profile.get('name', 'N/A')}</p>
#                     <p><strong>Email:</strong> {selected_profile.get('email', 'N/A')}</p>
#                     <p><strong>Role:</strong> {selected_profile.get('role', 'N/A')}</p>
#                     <p><strong>Education:</strong> {selected_profile.get('education', 'N/A')}</p>
#                     <p><strong>Skills:</strong> {selected_profile.get('skills', 'N/A')}</p>
#                     <p><strong>Experience:</strong> {selected_profile.get('experience', 'N/A')} years</p>
#                 </div>
#                 """, unsafe_allow_html=True)
#         else:
#             st.info("No valid candidate names found in the data. Please check your Google Sheet format.")
#     else:
#         st.info("No candidates synced yet. Click 'Sync Candidate Profiles' to fetch data from Google Sheets.")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# # -----------------------------
# # Right Column: Interview Tools
# # -----------------------------
# with right_col:
#     # Generate interview questions function
#     def generate_interview_questions(profile):
#         if not profile:
#             return ["Please select a candidate profile first."]
#         prompt = f"Generate five interview questions for a candidate applying as {profile.get('role', 'N/A')} with {profile.get('experience', 'N/A')} years of experience and skills in {profile.get('skills', 'N/A')}."
#         response = co.generate(
#             model="command",
#             prompt=prompt,
#             max_tokens=150,
#             temperature=0.7
#         )
#         questions = response.generations[0].text.strip().split("\n")
#         questions = [q.strip() for q in questions if q.strip()]
#         return questions[:5]
    
#     # Function to detect facial expression and stress level
#     def detect_stress(image):
#         try:
#             img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#             result = DeepFace.analyze(img_bgr, actions=['emotion'], enforce_detection=False)

#             if isinstance(result, list) and len(result) > 0:
#                 emotion = result[0].get('dominant_emotion', 'Neutral')
#             else:
#                 emotion = 'Neutral'

#             # Stress level logic based on emotions
#             if emotion in ['fear', 'sad', 'angry']:
#                 stress_level = "High"
#             elif emotion in ['neutral', 'surprise']:
#                 stress_level = "Medium"
#             else:
#                 stress_level = "Low"

#             return emotion, stress_level
#         except Exception as e:
#             return f"Error detecting expression: {str(e)}", "Unknown"

#     # Function to capture screenshot and analyze stress level
#     def capture_and_analyze_stress():
#         # Capture screenshot of the meeting window
#         screenshot = pyautogui.screenshot()
#         screenshot = np.array(screenshot)
#         screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

#         # Analyze stress level
#         emotion, stress_level = detect_stress(screenshot)
#         return screenshot, emotion, stress_level
    
#     # -----------------------------
#     # Interview Question Generator
#     # -----------------------------
#     st.markdown('<div class="section-header">📝 AI Interview Question Generator</div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
#     if st.button("Generate Interview Questions", key="generate_questions"):
#         if "current_profile" in st.session_state:
#             with st.spinner("Generating relevant interview questions..."):
#                 st.session_state["questions"] = generate_interview_questions(st.session_state["current_profile"])
#                 st.success("Generated interview questions!")
#         else:
#             st.warning("No candidate selected. Please sync and select a candidate first.")

#     if "questions" in st.session_state:
#         for i, question in enumerate(st.session_state["questions"], 1):
#             st.markdown(f"""
#             <div class="question-card">
#                 <strong>Q{i}:</strong> {question}
#             </div>
#             """, unsafe_allow_html=True)
    
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # -----------------------------
#     # Video Interview Room
#     # -----------------------------
#     st.markdown('<div class="section-header">🎥 Video Interview Room</div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
#     # Input box for Digital Samba meeting room link
#     meeting_link = st.text_input("Enter Digital Samba Meeting Room Link:", key="meeting_link")

#     # Embed the meeting room using an iframe if a link is provided
#     if meeting_link:
#         st.markdown(
#             f"""
#             <div class="responsive-iframe">
#                 <iframe
#                     src="{meeting_link}"
#                     allow="camera; microphone; fullscreen; display-capture"
#                 ></iframe>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
        
#         # Add interview controls
#         cols = st.columns(3)
#         with cols[0]:
#             if st.button("Start Interview", key="start_interview"):
#                 st.session_state["interview_active"] = True
#                 st.success("Interview started!")
#         with cols[1]:
#             if st.button("Pause Interview", key="pause_interview"):
#                 st.session_state["interview_active"] = False
#                 st.info("Interview paused.")
#         with cols[2]:
#             if st.button("End Interview", key="end_interview"):
#                 st.session_state["interview_active"] = False
#                 st.error("Interview ended.")
#     else:
#         st.warning("Please enter a valid Digital Samba meeting room link to start the video interview.")
    
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # -----------------------------
#     # Stress Level Analysis
#     # -----------------------------
#     st.markdown('<div class="section-header">📊 Automated Stress Level Detection</div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
#     # Add custom interval option
#     col1, col2 = st.columns(2)
#     with col1:
#         interval = st.slider(
#             "Screenshot Interval (seconds)", 
#             min_value=10, 
#             max_value=120, 
#             value=60, 
#             step=10,
#             key="interval_slider"
#         )
    
#     with col2:
#         num_captures = st.number_input(
#             "Number of Captures", 
#             min_value=1, 
#             max_value=10, 
#             value=5,
#             key="num_captures"
#         )

#     # Button to start automated stress level analysis
#     if st.button("Start Automated Stress Level Analysis", key="start_stress_analysis"):
#         if "current_profile" not in st.session_state:
#             st.warning("Please select a candidate first.")
#         else:
#             st.subheader("Stress Level Analysis Results:")
            
#             # Create a placeholder for the results table
#             results_table = st.empty()
            
#             # Initialize the results list
#             if "analysis_results" not in st.session_state:
#                 st.session_state["analysis_results"] = []
            
#             # Capture and analyze screenshots for the specified number of iterations
#             for i in range(num_captures):
#                 with st.spinner(f"Capturing and analyzing screenshot {i+1}/{num_captures}..."):
#                     screenshot, emotion, stress_level = capture_and_analyze_stress()
                    
#                     # Create a timestamp
#                     timestamp = time.strftime("%H:%M:%S", time.localtime())
                    
#                     # Add result to session state
#                     st.session_state["analysis_results"].append({
#                         "capture": i+1,
#                         "timestamp": timestamp,
#                         "emotion": emotion,
#                         "stress_level": stress_level
#                     })
                    
#                     # Display the screenshot
#                     st.image(
#                         cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB), 
#                         caption=f"Capture {i+1} - {timestamp}", 
#                         use_column_width=True
#                     )
                    
#                     # Display the updated results table
#                     results_table.markdown(
#                         """
#                         <table class="styled-table">
#                             <thead>
#                                 <tr>
#                                     <th>Capture</th>
#                                     <th>Time</th>
#                                     <th>Emotion</th>
#                                     <th>Stress Level</th>
#                                 </tr>
#                             </thead>
#                             <tbody>
#                         """ + 
#                         ''.join([
#                             f"""
#                             <tr>
#                                 <td>{result['capture']}</td>
#                                 <td>{result['timestamp']}</td>
#                                 <td>{result['emotion']}</td>
#                                 <td>
#                                     <span class="status-indicator status-{'high' if result['stress_level'] == 'High' else 'medium' if result['stress_level'] == 'Medium' else 'low'}"></span>
#                                     {result['stress_level']}
#                                 </td>
#                             </tr>
#                             """ for result in st.session_state["analysis_results"]
#                         ]) +
#                         """
#                             </tbody>
#                         </table>
#                         """,
#                         unsafe_allow_html=True
#                     )
                    
#                     # Provide insights based on the result
#                     if stress_level == "High":
#                         st.error("The candidate appears highly stressed. Consider providing reassurance.")
#                     elif stress_level == "Medium":
#                         st.warning("The candidate appears moderately stressed. Monitor their behavior.")
#                     else:
#                         st.success("The candidate appears relaxed. Great job!")

#                     # Save the captured image and analysis result to Firebase
#                     timestamp_unix = int(time.time())
#                     selected_name = st.session_state["current_profile"]["name"]
#                     analysis_data = {
#                         "timestamp": timestamp_unix,
#                         "emotion": emotion,
#                         "stress_level": stress_level,
#                         "image": base64.b64encode(cv2.imencode('.jpg', screenshot)[1]).decode("utf-8")
#                     }
#                     db.collection("stress_analysis").document(selected_name).set(analysis_data, merge=True)
                    
#                     # Wait for the specified interval before the next capture
#                     if i < num_captures - 1:  # Don't wait after the last capture
#                         time.sleep(interval)
            
#             # Show summary after all captures
#             emotions_count = {}
#             for result in st.session_state["analysis_results"]:
#                 emotion = result["emotion"]
#                 emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
            
#             dominant_emotion = max(emotions_count.items(), key=lambda x: x[1])[0]
            
#             st.markdown(
#                 f"""
#                 <div class="profile-card">
#                     <h4>Analysis Summary</h4>
#                     <p>Dominant emotion: <strong>{dominant_emotion}</strong></p>
#                     <p>Total captures: <strong>{num_captures}</strong></p>
#                     <p>Average stress level: <strong>
#                         {"High" if sum(1 for r in st.session_state["analysis_results"] if r["stress_level"] == "High") > num_captures/2 else 
#                          "Medium" if sum(1 for r in st.session_state["analysis_results"] if r["stress_level"] == "Medium") > num_captures/2 else 
#                          "Low"}
#                     </strong></p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
    
#     st.markdown('</div>', unsafe_allow_html=True)

# # Footer
# st.markdown("""
# <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ccc; color: #777;">
#     <p>© 2025 Recruiter Dashboard - AI Interview Assistant. All rights reserved.</p>
# </div>
# """, unsafe_allow_html=True)
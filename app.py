# ==============================================================================
# IMPORT NECESSARY LIBRARIES
# ==============================================================================
import streamlit as st
import requests
import datetime
import streamlit.components.v1 as components

# ==============================================================================
# GLOBAL CONFIGURATION
# ==============================================================================
RETURNED_BASE_URL = "https://silvio0-product-return-api.hf.space"

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION & UI SETUP
# ==============================================================================
st.set_page_config(
    page_title="Product Return AI Predictor", 
    page_icon="📦", 
    layout="centered"
)

# Custom CSS & Hero Section for a Modern Dashboard Look
st.markdown(
    """
    <style>
    /* Main Container */
    .hero-container { 
        text-align: center; 
        padding-bottom: 2rem; 
    }

    /* Gradient Title - Tech/E-commerce Theme */
    .gradient-text { 
        font-size: 2.8rem; 
        font-weight: 800; 
        background: -webkit-linear-gradient(45deg, #FF416C, #FF4B2B); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        margin-bottom: 0.5rem; 
    }

    /* Sub-hook styling */
    .sub-hook { 
        font-size: 1.2rem; 
        font-weight: 500; 
        color: #A0AEC0; 
        margin-bottom: 2rem; 
    }

    /* Description Box with Accent Border */
    .description-box { 
        background-color: #1E1E2E; 
        padding: 1.5rem 2rem; 
        border-radius: 8px; 
        border-left: 4px solid #FF4B2B; 
        text-align: left; 
        font-size: 1rem; 
        line-height: 1.6; 
        color: #E2E8F0; 
        margin-top: 1.5rem; 
    }
    </style>

    <div class="hero-container">
        <div class="gradient-text">📦 Product Return Dashboard</div>
        <div class="sub-hook">Predicting e-commerce returns before and after delivery.</div>
        <div class="description-box">
            Input the customer's order details below. Our advanced Machine Learning pipeline 
            will estimate the probability of the product being returned, allowing you to optimize logistics and customer satisfaction.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# SIDEBAR CONFIGURATION
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Model Configuration")
    
    prediction_mode = st.selectbox(
        "Select Prediction Phase",
        options=["pre", "post"],
        index=0,
        format_func=lambda phase: "🚚 Pre-Delivery (Checkout Phase)" if phase == "pre" else "📦 Post-Delivery (Received Phase)",
        help="Choose 'Pre-Delivery' to evaluate return risk at checkout. Choose 'Post-Delivery' to evaluate risk after the item arrives and is rated."
    )
    
    st.markdown("---")
    
    # Tech Stack Section
    st.markdown("### 🛠️ Built With")
    st.markdown(
        """
        - **Frontend UI:** Streamlit
        - **Backend API:** FastAPI
        - **Machine Learning:** Scikit-Learn
        - **Explainable AI:** LIME
        - **Data Processing:** Pandas & Numpy
        """
    )
    
    st.markdown("---")
    
    # Author Section
    st.markdown("### 👨‍💻 Developed By")
    st.markdown("**Silvio Christian Joe**")
    st.markdown("[🔗 GitHub (@viochris)](https://github.com/viochris)")
    
    st.markdown("---")
    st.markdown(f"**API Target:**\n`{RETURNED_BASE_URL}`")


# ==============================================================================
# PRE-DELIVERY PREDICTION FORM
# ==============================================================================
if prediction_mode == "pre":
    with st.form("pre_delivery_form"):
        st.markdown("### 🛒 Order Details (Checkout Phase)")
        
        # Split the input form into two visually balanced columns
        col1, col2 = st.columns(2)

        with col1:
            customer_age = st.number_input(
                "Customer Age",
                min_value=18, 
                max_value=69, 
                value=25,
                help="The age of the customer placing the order."
            )

            product_category = st.selectbox(
                "Product Category",
                options=['Groceries', 'Home & Living', 'Sports', 'Electronics', 'Beauty', 'Fashion'],
                index=3,
                help="The main category of the item being purchased."
            )

            payment_method = st.selectbox(
                "Payment Method",
                options=['Wallet', 'UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery'],
                index=0,
                help="The payment method selected by the customer at checkout."
            )

        with col2:
            order_value_usd = st.number_input(
                "Order Value (USD)",
                min_value=10.01,
                max_value=718.73,
                value=50.00,
                step=1.0,
                help="The total transaction amount in US Dollars."
            )

            order_date = st.date_input(
                "Order Date",
                value="today",
                min_value=datetime.date(2023, 1, 1),
                max_value=datetime.date(2025, 12, 30),
                help="The date the order is being placed."
            )

        # The submit button that triggers the API call
        submitted = st.form_submit_button("Analyze Pre-Delivery Risk 🚀", use_container_width=True)

    # ==============================================================================
    # API INTEGRATION & RESULTS RENDERING (PRE-DELIVERY)
    # ==============================================================================
    if submitted:
        # Prepare the payload using the Form Data format expected by FastAPI
        payload = {
            "customer_age": customer_age,
            "product_category": product_category,
            "payment_method": payment_method,
            "order_value_usd": order_value_usd,
            "order_date": str(order_date)
        }

        try:
            # ---------------------------------------------------------
            # 1. FETCH PREDICTION
            # ---------------------------------------------------------
            with st.spinner("🤖 AI is analyzing order details for return risk..."):
                response_pred = requests.post(f"{RETURNED_BASE_URL}/predict/pre", data=payload)

                if response_pred.status_code == 200:
                    pred_data = response_pred.json()
                    
                    # Safely extract data with default fallbacks
                    prediction_text = pred_data.get("prediction", "")
                    churn_proba = pred_data.get("returned_proba", "")
                    conf = pred_data.get("prediction_conf", "")

                    # Data integrity check: Ensure all required fields were returned
                    if not all([prediction_text, churn_proba, conf]):
                        st.error("🚨 **[DATA ERROR]** The API returned an incomplete prediction response. Missing key metrics.")
                        st.stop()
                    
                    # Display the results in a modern, customized HTML card
                    st.markdown(
                        f"""
                        <div style='background-color: #1E1E1E; padding: 25px; border-radius: 12px; border-left: 6px solid #FF416C; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-top: 20px;'>
                            <h3 style='color: #FF416C; margin-top: 0; font-family: sans-serif;'>🎉 Analysis Complete!</h3>
                            <p style='font-size: 16px; color: #E0E0E0; margin-bottom: 5px; font-family: sans-serif;'>Predicted Order Status:</p>
                            <p style='font-size: 32px; font-weight: bold; color: #FFD700; margin-top: 0; margin-bottom: 15px; font-family: monospace;'>
                                {prediction_text}
                            </p>
                            <hr style='border-color: #333333;'>
                            <p style='color: #A0A0A0; margin-bottom: 5px; font-size: 14px; font-family: sans-serif;'>
                                📊 <strong>Probability of Return:</strong> {churn_proba}
                            </p>
                            <p style='color: #A0A0A0; margin-bottom: 0; font-size: 14px; font-family: sans-serif;'>
                                🤖 <strong>Model Confidence Score:</strong> {conf}
                            </p>
                        </div>
                        <br><br>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"🚨 **API Error [{response_pred.status_code}]:** {response_pred.text}")
                    st.stop()

            # ---------------------------------------------------------
            # 2. FETCH LIME EXPLANATION
            # ---------------------------------------------------------
            with st.spinner("🔍 AI is generating the reasoning behind this prediction..."):
                response_explain = requests.post(f"{RETURNED_BASE_URL}/explain/pre", data=payload)

                if response_explain.status_code == 200:
                    explain_data = response_explain.json()
                    html_data = explain_data.get("explanation_html", "")

                    # Data integrity check: Ensure HTML was actually generated
                    if not html_data:
                        st.error("🚨 **[EXPLANATION ERROR]** The API successfully responded, but the LIME HTML string is empty.")
                        st.stop()

                    # Wrap the raw HTML inside a premium custom container using inline CSS
                    # Adjusted border color to match the Pre-Delivery theme
                    lime_html_with_bg = f"""
                    <div style='background-color: #1E1E1E; padding: 25px; border-radius: 12px; 
                                box-shadow: 0 8px 16px rgba(0,0,0,0.5); border-top: 6px solid #FF416C; 
                                font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;'>
                        <style>
                            /* Override LIME's default black text elements for dark mode compatibility */
                            svg text {{ fill: #E0E0E0 !important; }}
                            table {{ color: #E0E0E0 !important; }}
                            .lime-table th, .lime-table td {{ border-color: #444444 !important; }}
                        </style>
                        <h2 style='color: #FFFFFF; margin-top: 0; margin-bottom: 5px; font-weight: 700;'>
                            🧠 AI Decision Breakdown
                        </h2>
                        <p style='color: #A0AEC0; font-size: 15px; margin-top: 0; margin-bottom: 25px; font-weight: 500;'>
                            A transparent view of which specific order features positively or negatively impacted the return probability.
                        </p>
                        {html_data}
                    </div>
                    """
                    # Render the generated LIME HTML output directly inside the Streamlit UI
                    components.html(lime_html_with_bg, height=850, scrolling=True)

                else:
                    st.error(f"🚨 **Explanation API Error [{response_explain.status_code}]:** {response_explain.text}")
                    st.stop()

        # ---------------------------------------------------------
        # EXCEPTION HANDLING & ERROR ROUTING (CLIENT LEVEL)
        # ---------------------------------------------------------
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e).lower()
            error_raw = str(e)

            # 1. Handling Network / Connection Issues
            if error_type == "ConnectionError" or "connection" in error_msg:
                st.error(f"🚨 **[NETWORK ERROR]** Could not connect to the API server at `{RETURNED_BASE_URL}`. Please ensure the FastAPI server is online and reachable.")
            
            # 2. Handling Timeout Issues (e.g., LIME taking too long)
            elif error_type == "Timeout" or "timeout" in error_msg:
                st.error("🚨 **[TIMEOUT ERROR]** The API request took too long and timed out. The server might be overloaded or experiencing high latency. Please try again.")
            
            # 3. Handling Invalid API Responses
            elif error_type == "JSONDecodeError" or "json" in error_msg:
                st.error(f"🚨 **[DATA ERROR]** Failed to parse the API response. The server might have returned an HTML error page instead of JSON. Details: `{error_raw}`")
            
            # 4. Handling Missing Data in the Response Dictionary
            elif error_type == "KeyError" or "key" in error_msg:
                st.error(f"🚨 **[PAYLOAD ERROR]** The API returned an unexpected JSON structure. Missing key. Details: `{error_raw}`")
            
            # 5. Fallback for any other Streamlit UI errors
            else:
                st.error(f"🚨 **[UNKNOWN ERROR]** An unexpected system error occurred during the request execution. Type: `{error_type}`. Details: `{error_raw}`")
            
            # Halt further execution to prevent cascading UI crashes
            st.stop()

    else:
        st.info("💡 Fill out the customer profile and order details above, then click **Analyze Pre-Delivery Risk 🚀** to generate AI insights.")
    

# ==============================================================================
# POST-DELIVERY PREDICTION FORM
# ==============================================================================
elif prediction_mode == "post":
    with st.form("post_delivery_form"):
        st.markdown("### 📦 Order & Post-Delivery Details (Received Phase)")
        
        # Split the input form into two visually balanced columns
        col1, col2 = st.columns(2)

        with col1:
            customer_age = st.number_input(
                "Customer Age",
                min_value=18, 
                max_value=69, 
                value=25,
                help="The age of the customer who received the order."
            )

            product_category = st.selectbox(
                "Product Category",
                options=['Groceries', 'Home & Living', 'Sports', 'Electronics', 'Beauty', 'Fashion'],
                index=3,
                help="The main category of the received item."
            )

            payment_method = st.selectbox(
                "Payment Method",
                options=['Wallet', 'UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery'],
                index=0,
                help="The payment method used for this transaction."
            )
            
            order_date = st.date_input(
                "Order Date",
                value="today",
                min_value=datetime.date(2023, 1, 1),
                max_value=datetime.date(2025, 12, 30),
                help="The original date the order was placed."
            )

        with col2:
            order_value_usd = st.number_input(
                "Order Value (USD)",
                min_value=10.01,
                max_value=718.73,
                value=50.00,
                step=1.0,
                help="The total transaction amount in US Dollars."
            )

            delivery_time_days = st.number_input(
                "Delivery Time (Days)",
                min_value=1,
                max_value=14,
                value=3,
                help="The number of days it took for the product to reach the customer."
            )

            customer_rating = st.number_input(
                "Customer Rating",
                min_value=1.0,
                max_value=5.0,
                value=4.0,
                step=0.1,
                help="The rating given by the customer after receiving the product (1.0 to 5.0)."
            )

        # The submit button that triggers the API call
        submitted = st.form_submit_button("Analyze Post-Delivery Risk 🚀", use_container_width=True)

# ==============================================================================
# API INTEGRATION & RESULTS RENDERING (POST-DELIVERY)
# ==============================================================================
    if submitted:
        # Prepare the payload using the Form Data format expected by FastAPI
        # Note the addition of post-delivery specific metrics
        payload = {
            "customer_age": customer_age,
            "product_category": product_category,
            "payment_method": payment_method,
            "order_value_usd": order_value_usd,
            "delivery_time_days": delivery_time_days,
            "customer_rating": customer_rating,
            "order_date": str(order_date)
        }

        try:
            # ---------------------------------------------------------
            # 1. FETCH PREDICTION
            # ---------------------------------------------------------
            with st.spinner("🤖 AI is analyzing post-delivery metrics for return risk..."):
                response_pred = requests.post(f"{RETURNED_BASE_URL}/predict/post", data=payload)

                if response_pred.status_code == 200:
                    pred_data = response_pred.json()
                    
                    # Safely extract data with default fallbacks
                    prediction_text = pred_data.get("prediction", "")
                    churn_proba = pred_data.get("returned_proba", "")
                    conf = pred_data.get("prediction_conf", "")

                    # Data integrity check: Ensure all required fields were returned
                    if not all([prediction_text, churn_proba, conf]):
                        st.error("🚨 **[DATA ERROR]** The API returned an incomplete prediction response. Missing key metrics.")
                        st.stop()

                    # Display the results in a modern, customized HTML card
                    # Using #FF4B2B accent color to match the Post-Delivery dashboard theme
                    st.markdown(
                        f"""
                        <div style='background-color: #1E1E1E; padding: 25px; border-radius: 12px; border-left: 6px solid #FF4B2B; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-top: 20px;'>
                            <h3 style='color: #FF4B2B; margin-top: 0; font-family: sans-serif;'>🎉 Post-Delivery Analysis Complete!</h3>
                            <p style='font-size: 16px; color: #E0E0E0; margin-bottom: 5px; font-family: sans-serif;'>Predicted Return Status:</p>
                            <p style='font-size: 32px; font-weight: bold; color: #FFD700; margin-top: 0; margin-bottom: 15px; font-family: monospace;'>
                                {prediction_text}
                            </p>
                            <hr style='border-color: #333333;'>
                            <p style='color: #A0A0A0; margin-bottom: 5px; font-size: 14px; font-family: sans-serif;'>
                                📊 <strong>Probability of Return:</strong> {churn_proba}
                            </p>
                            <p style='color: #A0A0A0; margin-bottom: 0; font-size: 14px; font-family: sans-serif;'>
                                🤖 <strong>Model Confidence Score:</strong> {conf}
                            </p>
                        </div>
                        <br><br>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"🚨 **API Error [{response_pred.status_code}]:** {response_pred.text}")
                    st.stop()

            # ---------------------------------------------------------
            # 2. FETCH LIME EXPLANATION
            # ---------------------------------------------------------
            with st.spinner("🔍 AI is generating the reasoning behind this post-delivery prediction..."):
                response_explain = requests.post(f"{RETURNED_BASE_URL}/explain/post", data=payload)

                if response_explain.status_code == 200:
                    explain_data = response_explain.json()
                    explain_html = explain_data.get("explanation_html", "")

                    # Data integrity check: Ensure HTML was actually generated
                    if not explain_html:
                        st.error("🚨 **[EXPLANATION ERROR]** The API successfully responded, but the LIME HTML string is empty.")
                        st.stop()

                    # Wrap the raw HTML inside a premium custom container using inline CSS
                    lime_html_with_bg = f"""
                    <div style='background-color: #1E1E1E; padding: 25px; border-radius: 12px; 
                                box-shadow: 0 8px 16px rgba(0,0,0,0.5); border-top: 6px solid #FF4B2B; 
                                font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;'>
                        <style>
                            /* Override LIME's default black text elements for dark mode compatibility */
                            svg text {{ fill: #E0E0E0 !important; }}
                            table {{ color: #E0E0E0 !important; }}
                            .lime-table th, .lime-table td {{ border-color: #444444 !important; }}
                        </style>
                        <h2 style='color: #FFFFFF; margin-top: 0; margin-bottom: 5px; font-weight: 700;'>
                            🧠 AI Decision Breakdown
                        </h2>
                        <p style='color: #A0AEC0; font-size: 15px; margin-top: 0; margin-bottom: 25px; font-weight: 500;'>
                            A transparent view of how delivery time, customer rating, and order details impacted the final return probability.
                        </p>
                        {explain_html}
                    </div>
                    """
                    # Render the generated LIME HTML output directly inside the Streamlit UI
                    components.html(lime_html_with_bg, height=850, scrolling=True)

                else:
                    st.error(f"🚨 **Explanation API Error [{response_explain.status_code}]:** {response_explain.text}")
                    st.stop()

        # ---------------------------------------------------------
        # EXCEPTION HANDLING & ERROR ROUTING (CLIENT LEVEL)
        # ---------------------------------------------------------
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e).lower()
            error_raw = str(e)

            # 1. Handling Network / Connection Issues
            if error_type == "ConnectionError" or "connection" in error_msg:
                st.error(f"🚨 **[NETWORK ERROR]** Could not connect to the API server at `{RETURNED_BASE_URL}`. Please ensure the FastAPI server is online and reachable.")
            
            # 2. Handling Timeout Issues (e.g., LIME taking too long)
            elif error_type == "Timeout" or "timeout" in error_msg:
                st.error("🚨 **[TIMEOUT ERROR]** The API request took too long and timed out. The server might be overloaded or experiencing high latency. Please try again.")
            
            # 3. Handling Invalid API Responses
            elif error_type == "JSONDecodeError" or "json" in error_msg:
                st.error(f"🚨 **[DATA ERROR]** Failed to parse the API response. The server might have returned an HTML error page instead of JSON. Details: `{error_raw}`")
            
            # 4. Handling Missing Data in the Response Dictionary
            elif error_type == "KeyError" or "key" in error_msg:
                st.error(f"🚨 **[PAYLOAD ERROR]** The API returned an unexpected JSON structure. Missing key. Details: `{error_raw}`")
            
            # 5. Fallback for any other Streamlit UI errors
            else:
                st.error(f"🚨 **[UNKNOWN ERROR]** An unexpected system error occurred during the request execution. Type: `{error_type}`. Details: `{error_raw}`")
            
            # Halt further execution to prevent cascading UI crashes
            st.stop()

    else:
        st.info("💡 Fill out the post-delivery metrics and order details above, then click **Analyze Post-Delivery Risk 🚀** to generate AI insights.")
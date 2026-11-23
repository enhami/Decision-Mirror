import streamlit as st
import pandas as pd
import numpy as np

from ui.styles import apply_styles
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# ---------------------------------
# REUSABLE FEATURE TESTING FUNCTION
# ---------------------------------

def run_feature_test(model, original_row, feature, test_values, original_prediction):

    results = []

    for value in test_values:

        changed_row = original_row.copy()
        changed_row[feature] = float(value)

        prediction = model.predict(changed_row)[0]

        results.append({
            "Feature Value": round(float(value), 3),
            "Prediction": str(prediction),
            "Prediction Flipped": prediction != original_prediction
        })

    return pd.DataFrame(results)


# ---------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="DecisionMirror",
    page_icon="🔍",
    layout="wide"
)
apply_styles()
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-tag">AI • MACHINE LEARNING • MODEL ANALYSIS</div>
        <div class="hero-title">🔍 DecisionMirror</div>
        <div class="hero-description">
            Understand how reliable your machine learning decisions really are.
            Test prediction sensitivity, explore decision boundaries, and discover
            which features influence your model's predictions.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------
# 2. DATASET UPLOAD
# ---------------------------------

st.markdown(
    """
    <div class="section-card">
        <div class="section-label">STEP 01 • DATA INPUT</div>
        <div class="section-title">📂 Upload your dataset</div>
        <div class="section-description">
            Start by uploading a CSV file. DecisionMirror will inspect
            your dataset before training the machine learning model.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Choose your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])

        col3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

        st.subheader("Column Information")

        col_info_df = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values
        })
        st.dataframe(col_info_df, use_container_width=True, hide_index=True)


        st.divider()


        # ---------------------------------
        # 3. MODEL TRAINING
        # ---------------------------------

        st.markdown(
            """
            <div class="section-card">
                <div class="section-label">STEP 02 • MODEL TRAINING</div>
                <div class="section-title">🧠 Train your machine learning model</div>
                <div class="section-description">
                    Select your target column and train a Random Forest model
                    to evaluate its predictive performance.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        target_column = st.selectbox(
            "Select Target Column",
            df.columns
        )

        if st.button("Train Machine Learning Model"):

            clean_df = df.dropna(subset=[target_column])

            X = clean_df.drop(columns=[target_column])
            y = clean_df[target_column]

            if X.shape[1] == 0:

                st.error("At least one feature is required.")

            elif y.nunique() < 2:

                st.error(
                    "The target must contain at least "
                    "two different classes."
                )

            elif len(clean_df) < 4:

                st.error("Please upload more dataset rows.")

            else:

                numeric_features = X.select_dtypes(
                    include=["number"]
                ).columns.tolist()

                categorical_features = X.select_dtypes(
                    exclude=["number"]
                ).columns.tolist()

                transformers = []

                if numeric_features:

                    numeric_pipeline = Pipeline([
                        (
                            "imputer",
                            SimpleImputer(strategy="median")
                        )
                    ])

                    transformers.append(
                        ("numeric", numeric_pipeline, numeric_features)
                    )

                if categorical_features:

                    categorical_pipeline = Pipeline([
                        (
                            "imputer",
                            SimpleImputer(strategy="most_frequent")
                        ),
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore")
                        )
                    ])

                    transformers.append(
                        (
                            "categorical",
                            categorical_pipeline,
                            categorical_features
                        )
                    )

                preprocessor = ColumnTransformer(
                    transformers=transformers
                )

                model = Pipeline([
                    ("preprocessor", preprocessor),
                    (
                        "classifier",
                        RandomForestClassifier(
                            n_estimators=100,
                            random_state=42
                        )
                    )
                ])

                class_counts = y.value_counts()

                use_stratify = (
                    class_counts.min() >= 2
                    and int(np.ceil(len(y) * 0.25)) >= y.nunique()
                )

                try:

                    X_train, X_test, y_train, y_test = train_test_split(
                        X,
                        y,
                        test_size=0.25,
                        random_state=42,
                        stratify=y if use_stratify else None
                    )

                    model.fit(X_train, y_train)

                    predictions = model.predict(X_test)

                    accuracy = accuracy_score(
                        y_test,
                        predictions
                    )

                    # Clear previous analysis results after training a new model
                    st.session_state.pop("dm_stress_results", None)
                    st.session_state.pop("dm_stress_boundary_changes", None)
                    st.session_state.pop("dm_stress_feature", None)
                    st.session_state.pop("dm_stress_prediction", None)
                    st.session_state.pop("dm_sensitivity_results", None)
                    st.session_state.pop("dm_training_rows", None)
                    st.session_state.pop("dm_testing_rows", None)
                    st.session_state.pop("dm_training_accuracy", None)
                    st.session_state.pop("dm_training_confusion_matrix", None)
                    st.session_state.pop("dm_training_small_dataset", None)

                    # Save model and reference data

                    st.session_state["dm_model"] = model
                    st.session_state["dm_X_test"] = X_test.copy()
                    st.session_state["dm_X_reference"] = X.copy()
                    st.session_state["dm_target"] = target_column

                    # Confusion Matrix

                    labels = list(
                        pd.unique(
                            pd.concat([
                                y_test.reset_index(drop=True),
                                pd.Series(predictions)
                            ])
                        )
                    )

                    matrix = confusion_matrix(
                        y_test,
                        predictions,
                        labels=labels
                    )

                    matrix_df = pd.DataFrame(
                        matrix,
                        index=labels,
                        columns=labels
                    )

                    matrix_df.index.name = "Actual"
                    matrix_df.columns.name = "Predicted"

                    # SAVE MODEL PERFORMANCE RESULTS
                    st.session_state["dm_training_rows"] = len(X_train)
                    st.session_state["dm_testing_rows"] = len(X_test)
                    st.session_state["dm_training_accuracy"] = accuracy
                    st.session_state["dm_training_confusion_matrix"] = matrix_df
                    st.session_state["dm_training_small_dataset"] = len(clean_df) < 30

                except Exception as error:

                    st.error(f"Training error: {error}")

        # DISPLAY SAVED MODEL PERFORMANCE
        if "dm_training_accuracy" in st.session_state:

            st.success("Model trained successfully!")

            st.subheader("Model Performance")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Training Rows",
                st.session_state["dm_training_rows"]
            )

            col2.metric(
                "Testing Rows",
                st.session_state["dm_testing_rows"]
            )

            col3.metric(
                "Accuracy",
                f"{st.session_state['dm_training_accuracy'] * 100:.2f}%"
            )

            st.subheader("Confusion Matrix")

            st.dataframe(
                st.session_state["dm_training_confusion_matrix"]
            )

            if st.session_state["dm_training_small_dataset"]:

                st.warning(
                    "Very small dataset: performance "
                    "results may be unstable."
                )

    except Exception as error:

        st.error(f"Could not process dataset: {error}")

else:

    st.info("Please upload a CSV dataset to get started.")

# ---------------------------------
# 4. AUTOMATED DECISION FLIP LAB
# ---------------------------------

if "dm_model" in st.session_state:

    st.divider()

    st.markdown(
        """
        <div class="section-card">
            <div class="section-label">STEP 03 • ROBUSTNESS TESTING</div>
            <div class="section-title">🔬 Automated Decision Flip Lab</div>
            <div class="section-description">
                Change one feature at a time and observe when the model's
                prediction changes. Explore how sensitive individual
                decisions are to input variations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write(
        "Automatically test different input values "
        "and investigate prediction stability."
    )

    model = st.session_state["dm_model"]

    X_test = st.session_state["dm_X_test"]

    X_reference = st.session_state["dm_X_reference"]

    # Find numeric features

    numeric_columns = X_test.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if numeric_columns and len(X_test) > 0:

        # Select test example

        row_number = st.selectbox(
            "Choose a test example",
            range(len(X_test)),
            key="auto_row"
        )

        original_row = X_test.iloc[[row_number]].copy()

        # Select feature

        feature = st.selectbox(
            "Choose a feature to stress-test",
            numeric_columns,
            key="auto_feature"
        )

        # Get original prediction

        original_prediction = model.predict(
            original_row
        )[0]

        # Get feature range

        min_value = float(
            X_reference[feature].min()
        )

        max_value = float(
            X_reference[feature].max()
        )

        original_value = float(
            original_row[feature].iloc[0]
        )

        st.write(
            f"Original feature value: {original_value}"
        )

        st.write(
            f"Original prediction: {original_prediction}"
        )

        st.divider()

        st.subheader("⚙️ Automated Stress Test")

        st.write(
            "DecisionMirror will test 21 evenly spaced values "
            "across the observed dataset range, plus the "
            "original value if it isn't already included."
        )

        if st.button("Run Automated Stress Test"):

            if min_value == max_value:

                st.warning(
                    "This feature has only one observed value. "
                    "Choose another feature."
                )

            else:

                # Generate test values
                unique_values = np.sort(
                X_reference[feature].dropna().unique()
                )
                
                if len(unique_values) <= 10:
                     test_values = unique_values
                else:
                     test_values = np.linspace(min_value,max_value,21)
                     test_values = np.unique(np.append(test_values, original_value))

                # Run reusable feature test
                results_df = run_feature_test(
                    model,
                    original_row,
                    feature,
                    test_values,
                    original_prediction
                    )
                # ---------------------------------
                # 5. DECISION BOUNDARY DETECTION
                # ---------------------------------
                boundary_changes = []
                
                for i in range(1, len(results_df)):
                    previous_prediction = results_df.iloc[i - 1]["Prediction"]
                    current_prediction = results_df.iloc[i]["Prediction"]
                    
                    if previous_prediction != current_prediction:
                        lower_value = results_df.iloc[i - 1]["Feature Value"]
                        upper_value = results_df.iloc[i]["Feature Value"]
                        approximate_boundary = (lower_value + upper_value) / 2
                        
                        boundary_changes.append({
                            "Prediction Change": (f"{previous_prediction} → {current_prediction}"),
                            "Between Values": (f"{lower_value} and {upper_value}"),
                            "Approximate Switch Point": round(approximate_boundary, 3)
                            })
                st.session_state["dm_stress_results"] = results_df
                st.session_state["dm_stress_boundary_changes"] = boundary_changes
                st.session_state["dm_stress_feature"] = feature
                st.session_state["dm_stress_prediction"] = original_prediction
                st.session_state["dm_stress_row"] = row_number
                st.session_state["dm_stress_selected_feature"] = feature

        if (
            "dm_stress_results" in st.session_state
            and st.session_state.get("dm_stress_row") == row_number
            and st.session_state.get("dm_stress_selected_feature") == feature
        ):
            results_df = st.session_state["dm_stress_results"]
            boundary_changes = st.session_state["dm_stress_boundary_changes"]
            
            total_tests = len(results_df)
            flip_count = int(
                results_df["Prediction Flipped"].sum()
                )
            flip_rate = (flip_count / total_tests) * 100
            # Display results
            st.success("Automated stress test completed!")
            
            st.subheader("📊 Stress Test Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Values Tested",total_tests)
            col2.metric("Prediction Flips",flip_count)
            col3.metric("Flip Rate",f"{flip_rate:.2f}%")
            
            st.subheader("Prediction Results")
            st.dataframe(results_df, use_container_width=True)
            
            # Display detected boundaries
            st.subheader("🎯 Decision Boundary Detection")
            if boundary_changes:
                boundary_df = pd.DataFrame(boundary_changes)
                st.write(
                    "The model changed its prediction at "
                    "the following approximate feature boundaries:"
                )
                st.dataframe(
                    boundary_df,
                    use_container_width=True
                )
            else:
                st.success(
                    "No prediction boundaries were detected "
                    "within the tested feature range."
                )

            # Prediction distribution

            st.subheader("Prediction Distribution")

            prediction_counts = (
                results_df["Prediction"]
                .value_counts()
                .sort_index()
            )

            st.bar_chart(prediction_counts)
            
            # Interpretation
            if flip_count > 0:
                st.warning(
                    f"The model changed its original "
                    f"prediction for {flip_count} out of "
                    f"{total_tests} tested values."
                )

            else:
                st.success(
                    "The model maintained its original "
                    "prediction across all tested values."
                )

            st.caption(
                "Flip rate = percentage of tested input "
                "values that produced a different prediction "
                "from the original input."
            )

    else:

        st.info(
            "The dataset needs at least one numeric "
            "input feature to run this test."
        )

else:

    st.info(
        "Upload a dataset and train a model to use "
        "the Decision Flip Lab."
    )

# ---------------------------------
# 6. FEATURE SENSITIVITY COMPARISON
# ---------------------------------

if "dm_model" in st.session_state:

    st.divider()

    st.markdown(
    """
    <div class="section-card">
        <div class="section-label">STEP 04 • FEATURE ANALYSIS</div>
        <div class="section-title">📊 Feature Sensitivity Comparison</div>
        <div class="section-description">
            Compare how much each numerical feature influences
            the model's predictions. Identify which inputs have
            the greatest impact on decision stability.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    st.write(
        "Compare how changes in different numerical "
        "features affect the model's predictions."
    )

    model = st.session_state["dm_model"]

    X_test = st.session_state["dm_X_test"]

    X_reference = st.session_state["dm_X_reference"]

    numeric_columns = [
        col for col in X_test.select_dtypes(
            include=["number"]
            ).columns
            if col != "PassengerId"
    ]

    if numeric_columns and len(X_test) > 0:

        sensitivity_row_number = st.selectbox(
            "Choose a test example for comparison",
            range(len(X_test)),
            key="sensitivity_row"
        )

        original_row = X_test.iloc[
            [sensitivity_row_number]
        ].copy()

        original_prediction = model.predict(
            original_row
        )[0]

        st.write(
            f"Original prediction: {original_prediction}"
        )

        if st.button("Compare Feature Sensitivity"):

            sensitivity_results = []

            for feature in numeric_columns:

                min_value = float(X_reference[feature].min())
                max_value = float(X_reference[feature].max())

                original_value = float(
                    original_row[feature].iloc[0]
                )

                if min_value == max_value:
                    continue

                unique_values = np.sort(X_reference[feature].dropna().unique())
                if len(unique_values) <= 10:
                     test_values = unique_values
                else:
                     test_values = np.linspace(min_value, max_value, 21)
                     test_values = np.unique(np.append(test_values, original_value))

                # Run reusable feature test
                feature_results = run_feature_test(
                    model,
                    original_row,
                    feature,
                    test_values,
                    original_prediction
                )

                feature_flips = int(
                    feature_results["Prediction Flipped"].sum()
                )

                total_tests = len(feature_results)

                feature_flip_rate = (
                    feature_flips / total_tests
                ) * 100

                sensitivity_results.append({
                    "Feature": feature,
                    "Values Tested": total_tests,
                    "Prediction Flips": feature_flips,
                    "Flip Rate (%)": round(feature_flip_rate, 2)
                })

            if sensitivity_results:

                sensitivity_df = pd.DataFrame(
                    sensitivity_results
                )

                sensitivity_df = sensitivity_df.sort_values(
                    by="Flip Rate (%)",
                    ascending=False
                )

                # SAVE RESULTS
                st.session_state["dm_sensitivity_results"] = sensitivity_df
                st.session_state["dm_sensitivity_row"] = sensitivity_row_number

            else:
                st.session_state.pop(
                    "dm_sensitivity_results", None
                )

                st.warning(
                    "No numerical features with varying values "
                    "were available for comparison."
                )

        # DISPLAY SAVED RESULTS
        if (
            "dm_sensitivity_results" in st.session_state
            and st.session_state.get("dm_sensitivity_row") == sensitivity_row_number
        ):

            sensitivity_df = st.session_state[
                "dm_sensitivity_results"
            ]

            st.success(
                "Feature sensitivity comparison completed!"
            )

            st.subheader("Sensitivity Results")

            st.dataframe(
                sensitivity_df,
                use_container_width=True
            )

            st.subheader("Feature Sensitivity Chart")

            if sensitivity_df["Flip Rate (%)"].max() == 0:
                st.info(
                    "No prediction changes were observed for this test row "
                    "across the tested feature values."
                    )
            else:
                chart_df = sensitivity_df.set_index(
                    "Feature"
                    )[["Flip Rate (%)"]]
                
                st.bar_chart(chart_df)

            highest_rate = sensitivity_df["Flip Rate (%)"].max()

            top_features = sensitivity_df.loc[
                sensitivity_df["Flip Rate (%)"] == highest_rate,
                "Feature"
            ].tolist()

            st.info(
                f"Most sensitive feature(s): {', '.join(top_features)} "
                f"({highest_rate}% flip rate)."
            )

            st.caption(
                "Flip rates are calculated separately for "
                "each feature by changing that feature while "
                "keeping the other inputs constant. Results "
                "depend on the selected test example and "
                "the observed feature ranges."
            )

    else:

        st.info(
            "At least one numerical input feature is "
            "required for this comparison."
        )
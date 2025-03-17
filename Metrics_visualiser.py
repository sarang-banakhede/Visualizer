import streamlit as st
import pandas as pd
import plotly.express as px
import json

def load_json(uploaded_file):
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        return data
    return None

def json_to_df(data, data_type):
    metrics = []
    for epoch, values in data.items():
        values['epoch'] = int(epoch)
        values['type'] = data_type  
        metrics.append(values)
    return pd.DataFrame(metrics)

def main():
    st.title("Performance Metrics Visualization")
    st.sidebar.header("Upload JSON Files")
    train_file = st.sidebar.file_uploader("Upload Training JSON", type=["json"])
    test_file = st.sidebar.file_uploader("Upload Testing JSON", type=["json"])
    
    if train_file or test_file:
        train_data = load_json(train_file) if train_file else None
        test_data = load_json(test_file) if test_file else None
        
        train_df = json_to_df(train_data, "Training") if train_data else None
        test_df = json_to_df(test_data, "Testing") if test_data else None
        
        combined_df = pd.concat([df for df in [train_df, test_df] if df is not None])
        
        st.sidebar.header("Settings")
        mode = st.sidebar.radio("Mode", ["Combined", "Individual"])
        
        metrics = [col for col in combined_df.columns if col not in ['epoch', 'type']]
        selected_metrics = st.sidebar.multiselect("Choose Metrics", metrics, default=metrics)
        
        if selected_metrics:
            if mode == "Combined":
                melted_df = combined_df.melt(id_vars=['epoch', 'type'], value_vars=selected_metrics, 
                                             var_name='metric', value_name='value')
                fig = px.line(melted_df, x='epoch', y='value', color='metric', line_dash='type',
                              title="Performance Metrics Over Epochs",
                              labels={'value': 'Metric Value', 'epoch': 'Epoch', 'metric': 'Metric', 'type': 'Type'})
                st.plotly_chart(fig)
            else:
                for metric in selected_metrics:
                    fig = px.line(combined_df, x='epoch', y=metric, color='type',
                                  title=f"{metric} Over Epochs",
                                  labels={'epoch': 'Epoch', metric: metric, 'type': 'Type'})
                    st.plotly_chart(fig)
        else:
            st.warning("Please select at least one metric to plot.")
    else:
        st.info("Please upload at least one JSON file to proceed.")

if __name__ == "__main__":
    main()

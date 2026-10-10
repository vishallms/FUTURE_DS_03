import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

def generate_funnel_data():
    """Generate structured marketing funnel dataset."""
    np.random.seed(42)
    channels = ['Paid Search', 'Social Media', 'Organic Search', 'Email Marketing', 'Direct']
    data = []
    
    for channel in channels:
        impressions = np.random.randint(50000, 100000)
        clicks = int(impressions * np.random.uniform(0.12, 0.25))
        product_views = int(clicks * np.random.uniform(0.50, 0.70))
        cart_adds = int(product_views * np.random.uniform(0.25, 0.45))
        purchases = int(cart_adds * np.random.uniform(0.30, 0.60))
        
        data.append({
            'Channel': channel,
            'Impressions': impressions,
            'Clicks': clicks,
            'Product_Views': product_views,
            'Cart_Adds': cart_adds,
            'Purchases': purchases
        })
        
    df = pd.DataFrame(data)
    df.to_csv('marketing_funnel.csv', index=False)
    print("Dataset 'marketing_funnel.csv' created successfully!\n")
    return df

def analyze_marketing_funnel(df):
    print("==========================================")
    print("  MARKETING FUNNEL & CONVERSION REPORT    ")
    print("==========================================")
    
    # Aggregated Funnel Stages
    stages = ['Impressions', 'Clicks', 'Product_Views', 'Cart_Adds', 'Purchases']
    totals = [df[stage].sum() for stage in stages]
    
    funnel_df = pd.DataFrame({
        'Stage': stages,
        'Users': totals
    })
    
    # Calculate Conversion Rates relative to first stage (Impressions)
    funnel_df['Overall_Conversion_%'] = (funnel_df['Users'] / funnel_df['Users'].iloc[0]) * 100
    
    # Calculate Step-by-Step Conversion Rates
    funnel_df['Step_Conversion_%'] = (funnel_df['Users'] / funnel_df['Users'].shift(1)).fillna(1.0) * 100
    
    print("--- Overall Funnel Performance ---")
    print(funnel_df.to_string(index=False), "\n")
    
    # Create directory for charts
    os.makedirs("output_charts", exist_ok=True)
    
    # 1. Overall Marketing Funnel (Horizontal Bar Chart)
    plt.figure(figsize=(9, 5))
    palette = sns.color_palette("Blues_r", len(stages))
    ax = sns.barplot(data=funnel_df, x='Users', y='Stage', palette=palette, hue='Stage', legend=False)
    
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{int(width):,}',
                    (width, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center',
                    xytext=(5, 0),
                    textcoords='offset points',
                    fontsize=10, fontweight='bold')
                    
    plt.title('Overall Conversion Funnel Stages', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Users')
    plt.tight_layout()
    plt.savefig('output_charts/funnel_overview.png', dpi=300)
    plt.close()

    # 2. Channel Conversion Rate Comparison
    df['Conversion_Rate_%'] = (df['Purchases'] / df['Clicks']) * 100
    print("--- Performance by Marketing Channel ---")
    print(df[['Channel', 'Clicks', 'Purchases', 'Conversion_Rate_%']].to_string(index=False), "\n")
    
    plt.figure(figsize=(9, 5))
    sns.barplot(data=df.sort_values(by='Conversion_Rate_%', ascending=False), 
                x='Channel', y='Conversion_Rate_%', palette='viridis', hue='Channel', legend=False)
    plt.title('Click-to-Purchase Conversion Rate by Channel (%)', fontsize=14, fontweight='bold')
    plt.ylabel('Conversion Rate (%)')
    plt.xlabel('Marketing Channel')
    plt.tight_layout()
    plt.savefig('output_charts/channel_conversion_rates.png', dpi=300)
    plt.close()

    # 3. Stage Drop-Off Analysis
    funnel_df['Drop_Off_%'] = 100 - funnel_df['Step_Conversion_%']
    plt.figure(figsize=(8, 4))
    sns.barplot(data=funnel_df.iloc[1:], x='Stage', y='Drop_Off_%', palette='Reds', hue='Stage', legend=False)
    plt.title('Percentage Drop-Off at Each Funnel Transition', fontsize=14, fontweight='bold')
    plt.ylabel('Drop-Off Rate (%)')
    plt.xlabel('Funnel Transition Stage')
    plt.tight_layout()
    plt.savefig('output_charts/stage_dropoff_rates.png', dpi=300)
    plt.close()

    print("Analysis complete! All visual charts saved in 'output_charts/' folder.")

if __name__ == "__main__":
    df_funnel = generate_funnel_data()
    analyze_marketing_funnel(df_funnel)
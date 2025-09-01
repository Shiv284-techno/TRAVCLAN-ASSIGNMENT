"""
Simple Chart Generation - No Text Overlap Issues
Fast execution with clean, readable visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set clean style
plt.style.use('default')
sns.set_style("whitegrid")

def create_simple_charts():
    """Create simple, clean visualizations without text overlap"""
    
    print("Loading data...")
    df = pd.read_csv('Hotel_bookings_final.csv')
    
    # Create figure with better spacing
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('Hotel Booking Analysis - Key Insights', fontsize=18, fontweight='bold', y=0.98)
    
    # 1. Booking Channel Distribution (Clean Pie Chart)
    ax1 = plt.subplot(2, 3, 1)
    channel_counts = df['booking_channel'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Simple pie chart with better spacing
    wedges, texts, autotexts = ax1.pie(channel_counts.values, 
                                      labels=channel_counts.index,
                                      autopct='%1.1f%%', 
                                      colors=colors,
                                      startangle=90,
                                      textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    ax1.set_title('Booking Channels', fontsize=14, fontweight='bold', pad=15)
    
    # 2. Star Rating Distribution (Simple Bar Chart)
    ax2 = plt.subplot(2, 3, 2)
    star_counts = df['star_rating'].value_counts().sort_index()
    
    bars = ax2.bar(star_counts.index, star_counts.values, 
                   color='skyblue', alpha=0.8, edgecolor='navy')
    ax2.set_title('Hotel Star Ratings', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Rating')
    ax2.set_ylabel('Bookings')
    
    # Add simple value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    # 3. Cancellation Analysis (Clean comparison)
    ax3 = plt.subplot(2, 3, 3)
    
    # Calculate cancellation rates
    total_bookings = len(df)
    cancelled = len(df[df['booking_status'].str.contains('cancel', case=False, na=False)])
    confirmed = total_bookings - cancelled
    
    # Simple pie chart for status
    status_data = [confirmed, cancelled]
    status_labels = ['Confirmed', 'Cancelled']
    colors_status = ['lightgreen', 'lightcoral']
    
    ax3.pie(status_data, labels=status_labels, autopct='%1.1f%%', 
            colors=colors_status, startangle=90,
            textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax3.set_title('Booking Status', fontsize=14, fontweight='bold', pad=15)
    
    # 4. Revenue by Channel (Horizontal bars for clarity)
    ax4 = plt.subplot(2, 3, 4)
    revenue_by_channel = df.groupby('booking_channel')['selling_price'].sum() / 1000000
    
    bars = ax4.barh(revenue_by_channel.index, revenue_by_channel.values, 
                    color='green', alpha=0.7)
    ax4.set_title('Revenue by Channel', fontsize=14, fontweight='bold', pad=15)
    ax4.set_xlabel('Revenue ($M)')
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax4.text(width + 5, bar.get_y() + bar.get_height()/2.,
                f'${width:.0f}M', ha='left', va='center', fontsize=10, fontweight='bold')
    
    # 5. Monthly Trends (Simple line plot)
    ax5 = plt.subplot(2, 3, 5)
    
    # Convert dates and get monthly data
    df['booking_date'] = pd.to_datetime(df['booking_date'], errors='coerce')
    df['month'] = df['booking_date'].dt.month
    monthly_bookings = df['month'].value_counts().sort_index()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    ax5.plot(monthly_bookings.index, monthly_bookings.values, 
             marker='o', linewidth=2, markersize=6, color='purple')
    ax5.set_title('Monthly Booking Trends', fontsize=14, fontweight='bold', pad=15)
    ax5.set_xlabel('Month')
    ax5.set_ylabel('Bookings')
    ax5.set_xticks(range(1, 13))
    ax5.set_xticklabels([months[i-1] for i in range(1, 13)], rotation=45)
    ax5.grid(True, alpha=0.3)
    
    # 6. Room Types (Simple horizontal bars)
    ax6 = plt.subplot(2, 3, 6)
    room_counts = df['room_type'].value_counts()
    
    bars = ax6.barh(room_counts.index, room_counts.values, 
                    color='orange', alpha=0.7)
    ax6.set_title('Room Type Preferences', fontsize=14, fontweight='bold', pad=15)
    ax6.set_xlabel('Bookings')
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width + 200, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}', ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Adjust layout for better spacing
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    
    # Save with high quality
    plt.savefig('hotel_insights_clean.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print("Charts saved to: hotel_insights_clean.png")
    plt.show()
    
    # Create a summary metrics chart
    fig2, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig2.suptitle('Key Business Metrics Summary', fontsize=16, fontweight='bold')
    
    # Calculate key metrics
    total_revenue = df['selling_price'].sum() / 1000000
    avg_booking = df['selling_price'].mean()
    cancellation_rate = (cancelled / total_bookings) * 100
    unique_customers = df['customer_id'].nunique()
    
    # Create metrics display
    metrics = ['Total Revenue\n($M)', 'Avg Booking\n($)', 'Cancel Rate\n(%)', 'Customers']
    values = [total_revenue, avg_booking, cancellation_rate, unique_customers]
    colors_metrics = ['green', 'blue', 'red', 'purple']
    
    bars = ax.bar(metrics, values, color=colors_metrics, alpha=0.7)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, values)):
        height = bar.get_height()
        if i == 0:  # Revenue
            label = f'${value:.0f}M'
        elif i == 1:  # Avg booking
            label = f'${value:,.0f}'
        elif i == 2:  # Cancel rate
            label = f'{value:.1f}%'
        else:  # Customers
            label = f'{int(value):,}'
            
        ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.02,
                label, ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_title('Hotel Booking Performance Metrics', fontsize=14, pad=20)
    ax.set_ylabel('Values')
    
    # Remove y-axis for cleaner look
    ax.set_ylim(0, max(values) * 1.15)
    
    plt.tight_layout()
    plt.savefig('business_metrics_summary.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    
    print("Metrics summary saved to: business_metrics_summary.png")
    plt.show()
    
    print("\n" + "="*50)
    print("SIMPLE CHARTS GENERATED SUCCESSFULLY!")
    print("="*50)
    print("Files created:")
    print("• hotel_insights_clean.png - Main analysis dashboard")
    print("• business_metrics_summary.png - Key metrics summary") 
    print("\nFeatures:")
    print("• No overlapping text")
    print("• Clean, readable labels")
    print("• Professional appearance") 
    print("• Fast execution time")

if __name__ == "__main__":
    create_simple_charts()
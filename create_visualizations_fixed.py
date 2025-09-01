"""
Create Key Visualizations for Hotel Booking Analysis - Fixed Version
Addresses text overlap and improves chart readability
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style with better defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.style.use('default')
sns.set_palette("husl")
sns.set_style("whitegrid")

def create_visualizations():
    """Create key visualizations with proper spacing and no text overlap"""
    
    # Load data
    df = pd.read_csv('Hotel_bookings_final.csv')
    
    # Data preprocessing
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Create derived features
    if 'booking_date' in df.columns and 'check_in_date' in df.columns:
        df['booking_lead_time'] = (df['check_in_date'] - df['booking_date']).dt.days
    
    if 'selling_price' in df.columns and 'costprice' in df.columns:
        df['profit_margin'] = ((df['selling_price'] - df['costprice']) / df['selling_price']) * 100
    
    if 'booking_date' in df.columns:
        df['booking_month'] = df['booking_date'].dt.month
    
    # Create visualizations with better spacing
    fig = plt.figure(figsize=(24, 18))  # Increased size for better spacing
    fig.suptitle('Hotel Booking Data Analysis - Key Insights', fontsize=22, fontweight='bold', y=0.98)
    
    # 1. Booking Channel Distribution
    ax1 = plt.subplot(2, 3, 1)
    channel_counts = df['booking_channel'].value_counts()
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = ax1.pie(channel_counts.values, labels=channel_counts.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    # Improve pie chart text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    ax1.set_title('Booking Channel Distribution', fontsize=14, fontweight='bold', pad=20)
    
    # 2. Star Rating vs Booking Volume
    ax2 = plt.subplot(2, 3, 2)
    star_booking = df.groupby('star_rating').size()
    bars = ax2.bar(star_booking.index, star_booking.values, color='skyblue', 
                   edgecolor='navy', alpha=0.8, width=0.6)
    ax2.set_title('Bookings by Hotel Star Rating', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Star Rating', fontsize=12)
    ax2.set_ylabel('Number of Bookings', fontsize=12)
    ax2.set_ylim(0, max(star_booking.values) * 1.15)  # Add space for labels
    
    # Add value labels with better positioning
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(star_booking.values) * 0.02,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 3. Cancellation Rates by Channel
    ax3 = plt.subplot(2, 3, 3)
    cancel_by_channel = df.groupby('booking_channel')['booking_status'].apply(
        lambda x: (x.str.contains('cancel', case=False, na=False).sum() / len(x)) * 100
    ).sort_values(ascending=False)
    
    bars = ax3.bar(range(len(cancel_by_channel)), cancel_by_channel.values, 
                   color='coral', alpha=0.8, width=0.6)
    ax3.set_xticks(range(len(cancel_by_channel)))
    ax3.set_xticklabels(cancel_by_channel.index, rotation=0, ha='center')  # No rotation
    ax3.set_title('Cancellation Rate by Channel', fontsize=14, fontweight='bold', pad=20)
    ax3.set_ylabel('Cancellation Rate (%)', fontsize=12)
    ax3.set_ylim(0, max(cancel_by_channel.values) * 1.2)  # Add space for labels
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + max(cancel_by_channel.values) * 0.02,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 4. Revenue by Channel
    ax4 = plt.subplot(2, 3, 4)
    revenue_by_channel = df.groupby('booking_channel')['selling_price'].sum() / 1000000
    bars = ax4.bar(range(len(revenue_by_channel)), revenue_by_channel.values, 
                   color='green', alpha=0.8, width=0.6)
    ax4.set_xticks(range(len(revenue_by_channel)))
    ax4.set_xticklabels(revenue_by_channel.index, rotation=0, ha='center')
    ax4.set_title('Total Revenue by Channel', fontsize=14, fontweight='bold', pad=20)
    ax4.set_ylabel('Revenue (Millions $)', fontsize=12)
    ax4.set_ylim(0, max(revenue_by_channel.values) * 1.2)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + max(revenue_by_channel.values) * 0.02,
                f'${height:.0f}M', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 5. Monthly Booking Trends
    ax5 = plt.subplot(2, 3, 5)
    monthly_bookings = df.groupby('booking_month').size()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    ax5.plot(monthly_bookings.index, monthly_bookings.values, marker='o', 
             linewidth=3, markersize=10, color='purple', markerfacecolor='white', 
             markeredgecolor='purple', markeredgewidth=2)
    ax5.set_title('Monthly Booking Trends', fontsize=14, fontweight='bold', pad=20)
    ax5.set_xlabel('Month', fontsize=12)
    ax5.set_ylabel('Number of Bookings', fontsize=12)
    ax5.set_xticks(range(1, 13))
    ax5.set_xticklabels([months[i-1] for i in range(1, 13)], rotation=45, ha='right')
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(min(monthly_bookings.values) * 0.9, max(monthly_bookings.values) * 1.1)
    
    # 6. Room Type Distribution
    ax6 = plt.subplot(2, 3, 6)
    room_counts = df['room_type'].value_counts()
    bars = ax6.barh(range(len(room_counts)), room_counts.values, 
                    color='orange', alpha=0.8, height=0.6)
    ax6.set_yticks(range(len(room_counts)))
    ax6.set_yticklabels(room_counts.index)
    ax6.set_title('Room Type Distribution', fontsize=14, fontweight='bold', pad=20)
    ax6.set_xlabel('Number of Bookings', fontsize=12)
    ax6.set_xlim(0, max(room_counts.values) * 1.15)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width + max(room_counts.values) * 0.02, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}', ha='left', va='center', fontweight='bold', fontsize=10)
    
    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for main title
    plt.subplots_adjust(hspace=0.35, wspace=0.25)  # Increase spacing between subplots
    
    plt.savefig('hotel_booking_insights_fixed.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()
    
    # Create a second figure for profitability analysis
    fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig2.suptitle('Hotel Booking Profitability Analysis', fontsize=20, fontweight='bold', y=0.98)
    
    # Profit Margin Distribution
    profit_data = df['profit_margin'].dropna()
    ax1.hist(profit_data, bins=30, color='purple', alpha=0.7, edgecolor='black', density=False)
    ax1.axvline(profit_data.mean(), color='red', linestyle='--', linewidth=3,
               label=f'Mean: {profit_data.mean():.1f}%')
    ax1.set_title('Profit Margin Distribution', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Profit Margin (%)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Average Revenue by Star Rating
    revenue_by_rating = df.groupby('star_rating')['selling_price'].mean()
    bars = ax2.bar(revenue_by_rating.index, revenue_by_rating.values, 
                   color='gold', alpha=0.9, edgecolor='black', width=0.6)
    ax2.set_title('Average Revenue by Star Rating', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Star Rating', fontsize=12)
    ax2.set_ylabel('Average Revenue ($)', fontsize=12)
    ax2.set_ylim(0, max(revenue_by_rating.values) * 1.15)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(revenue_by_rating.values) * 0.02,
                f'${height:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Booking Status Overview
    status_counts = df['booking_status'].value_counts()
    colors_pie = ['lightgreen', 'lightcoral', 'lightblue', 'lightyellow']
    wedges, texts, autotexts = ax3.pie(status_counts.values, labels=status_counts.index, 
                                      autopct='%1.1f%%', colors=colors_pie[:len(status_counts)],
                                      startangle=90)
    # Improve pie chart text
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    ax3.set_title('Booking Status Distribution', fontsize=16, fontweight='bold', pad=20)
    
    # Customer Value Analysis
    customer_value = df.groupby('customer_id')['selling_price'].sum()
    ax4.hist(customer_value/1000, bins=25, color='teal', alpha=0.8, edgecolor='black')
    ax4.set_title('Customer Total Spend Distribution', fontsize=16, fontweight='bold', pad=20)
    ax4.set_xlabel('Total Customer Spend (Thousands $)', fontsize=12)
    ax4.set_ylabel('Number of Customers', fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    # Add summary statistics
    mean_spend = customer_value.mean() / 1000
    ax4.axvline(mean_spend, color='red', linestyle='--', linewidth=3,
               label=f'Mean: ${mean_spend:.0f}K')
    ax4.legend(fontsize=12)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(hspace=0.3, wspace=0.25)
    
    plt.savefig('hotel_profitability_fixed.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    
    print("Fixed visualizations created successfully!")
    print("Generated files:")
    print("• hotel_booking_insights_fixed.png")
    print("• hotel_profitability_fixed.png")
    print("• Improved text spacing and readability")
    print("• No overlapping labels or text")

if __name__ == "__main__":
    create_visualizations()
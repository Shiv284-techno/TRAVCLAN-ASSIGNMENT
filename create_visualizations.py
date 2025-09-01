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
    """Create key visualizations for the hotel booking analysis"""
    
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
    
    # Create visualizations
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('Hotel Booking Data Analysis - Key Insights', fontsize=20, fontweight='bold')
    
    # 1. Booking Channel Distribution
    ax1 = plt.subplot(2, 3, 1)
    channel_counts = df['booking_channel'].value_counts()
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    ax1.pie(channel_counts.values, labels=channel_counts.index, autopct='%1.1f%%', colors=colors)
    ax1.set_title('Booking Channel Distribution', fontsize=14, fontweight='bold')
    
    # 2. Star Rating vs Booking Volume
    ax2 = plt.subplot(2, 3, 2)
    star_booking = df.groupby('star_rating').size()
    bars = ax2.bar(star_booking.index, star_booking.values, color='skyblue', edgecolor='navy', alpha=0.7)
    ax2.set_title('Bookings by Hotel Star Rating', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Star Rating')
    ax2.set_ylabel('Number of Bookings')
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height):,}', ha='center', va='bottom')
    
    # 3. Cancellation Rates by Channel
    ax3 = plt.subplot(2, 3, 3)
    cancel_by_channel = df.groupby('booking_channel')['booking_status'].apply(
        lambda x: (x.str.contains('cancel', case=False, na=False).sum() / len(x)) * 100
    ).sort_values(ascending=False)
    
    bars = ax3.bar(range(len(cancel_by_channel)), cancel_by_channel.values, color='coral', alpha=0.8)
    ax3.set_xticks(range(len(cancel_by_channel)))
    ax3.set_xticklabels(cancel_by_channel.index, rotation=45)
    ax3.set_title('Cancellation Rate by Booking Channel', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Cancellation Rate (%)')
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom')
    
    # 4. Revenue by Channel
    ax4 = plt.subplot(2, 3, 4)
    revenue_by_channel = df.groupby('booking_channel')['selling_price'].sum() / 1000000  # Convert to millions
    bars = ax4.bar(range(len(revenue_by_channel)), revenue_by_channel.values, color='green', alpha=0.7)
    ax4.set_xticks(range(len(revenue_by_channel)))
    ax4.set_xticklabels(revenue_by_channel.index, rotation=45)
    ax4.set_title('Total Revenue by Booking Channel', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Revenue (Millions $)')
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'${height:.1f}M', ha='center', va='bottom')
    
    # 5. Monthly Booking Trends
    ax5 = plt.subplot(2, 3, 5)
    monthly_bookings = df.groupby('booking_month').size()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax5.plot(monthly_bookings.index, monthly_bookings.values, marker='o', linewidth=3, markersize=8, color='purple')
    ax5.set_title('Monthly Booking Trends', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Month')
    ax5.set_ylabel('Number of Bookings')
    ax5.set_xticks(range(1, 13))
    ax5.set_xticklabels([months[i-1] for i in range(1, 13)], rotation=45)
    ax5.grid(True, alpha=0.3)
    
    # 6. Room Type Distribution
    ax6 = plt.subplot(2, 3, 6)
    room_counts = df['room_type'].value_counts()
    bars = ax6.barh(range(len(room_counts)), room_counts.values, color='orange', alpha=0.7)
    ax6.set_yticks(range(len(room_counts)))
    ax6.set_yticklabels(room_counts.index)
    ax6.set_title('Booking Distribution by Room Type', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Number of Bookings')
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width + 200, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}', ha='left', va='center')
    
    plt.tight_layout()
    plt.savefig('hotel_booking_key_insights.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create a second figure for profit analysis
    plt.figure(figsize=(16, 10))
    plt.suptitle('Hotel Booking Profitability Analysis', fontsize=18, fontweight='bold')
    
    # Profit Margin Distribution
    plt.subplot(2, 2, 1)
    plt.hist(df['profit_margin'].dropna(), bins=30, color='purple', alpha=0.7, edgecolor='black')
    plt.axvline(df['profit_margin'].mean(), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {df["profit_margin"].mean():.1f}%')
    plt.title('Profit Margin Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Profit Margin (%)')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Average Revenue by Star Rating
    plt.subplot(2, 2, 2)
    revenue_by_rating = df.groupby('star_rating')['selling_price'].mean()
    bars = plt.bar(revenue_by_rating.index, revenue_by_rating.values, color='gold', alpha=0.8, edgecolor='black')
    plt.title('Average Revenue per Booking by Star Rating', fontsize=14, fontweight='bold')
    plt.xlabel('Star Rating')
    plt.ylabel('Average Revenue ($)')
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'${height:.0f}', ha='center', va='bottom')
    
    # Booking Status Overview
    plt.subplot(2, 2, 3)
    status_counts = df['booking_status'].value_counts()
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow']
    plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
           colors=colors[:len(status_counts)])
    plt.title('Overall Booking Status Distribution', fontsize=14, fontweight='bold')
    
    # Customer Booking Frequency
    plt.subplot(2, 2, 4)
    customer_bookings = df.groupby('customer_id').size()
    booking_freq = customer_bookings.value_counts().sort_index()
    plt.bar(booking_freq.index[:10], booking_freq.values[:10], color='teal', alpha=0.7)
    plt.title('Customer Booking Frequency (Top 10)', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Bookings per Customer')
    plt.ylabel('Number of Customers')
    
    plt.tight_layout()
    plt.savefig('hotel_booking_profitability.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualizations created successfully!")
    print("Generated files:")
    print("• hotel_booking_key_insights.png")
    print("• hotel_booking_profitability.png")

if __name__ == "__main__":
    create_visualizations()
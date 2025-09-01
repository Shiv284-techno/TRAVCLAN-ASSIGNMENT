"""
Quick Visualization Test - Minimal Charts for Testing
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def quick_test():
    """Create minimal charts to test visualization functionality"""
    
    print("Loading data for visualization test...")
    df = pd.read_csv('Hotel_bookings_final.csv')
    
    # Create simple 2x2 grid
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('TravClan Hotel Booking Analysis - Quick Test', fontsize=16, fontweight='bold')
    
    # 1. Simple Channel Distribution
    channel_counts = df['booking_channel'].value_counts()
    ax1.pie(channel_counts.values, labels=channel_counts.index, autopct='%1.1f%%')
    ax1.set_title('Booking Channels', fontweight='bold')
    
    # 2. Star Rating Bars
    star_counts = df['star_rating'].value_counts().sort_index()
    ax2.bar(star_counts.index, star_counts.values, color='skyblue')
    ax2.set_title('Star Ratings', fontweight='bold')
    ax2.set_xlabel('Rating')
    ax2.set_ylabel('Count')
    
    # 3. Booking Status
    cancelled = len(df[df['booking_status'].str.contains('cancel', case=False, na=False)])
    confirmed = len(df) - cancelled
    ax3.pie([confirmed, cancelled], labels=['Confirmed', 'Cancelled'], 
           colors=['lightgreen', 'lightcoral'], autopct='%1.1f%%')
    ax3.set_title('Booking Status', fontweight='bold')
    
    # 4. Room Types
    room_counts = df['room_type'].value_counts()
    ax4.barh(room_counts.index, room_counts.values, color='orange')
    ax4.set_title('Room Types', fontweight='bold')
    ax4.set_xlabel('Bookings')
    
    plt.tight_layout()
    plt.savefig('quick_test_charts.png', dpi=200, bbox_inches='tight')
    print("Test charts saved to: quick_test_charts.png")
    plt.show()
    
    # Print quick stats
    print(f"\n=== QUICK STATS ===")
    print(f"Total Bookings: {len(df):,}")
    print(f"Cancellation Rate: {(cancelled/len(df)*100):.1f}%")
    print(f"Average Booking Value: ${df['selling_price'].mean():,.2f}")
    print(f"Top Channel: {channel_counts.index[0]} ({channel_counts.iloc[0]/len(df)*100:.1f}%)")
    print(f"Visualization test completed successfully!")

if __name__ == "__main__":
    quick_test()
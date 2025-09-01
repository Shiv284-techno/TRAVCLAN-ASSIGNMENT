"""
Quick Chart Generation for README Documentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('Hotel_bookings_final.csv')

# Set style
plt.style.use('default')
sns.set_style("whitegrid")

# Create a simple architecture diagram visualization
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.text(0.5, 0.9, 'HOTEL BOOKING ANALYSIS ARCHITECTURE', 
        ha='center', va='center', fontsize=16, fontweight='bold')

# Draw architecture layers
layers = [
    'Data Layer: CSV → Validation → Feature Engineering',
    'Analysis Layer: EDA → Statistics → Patterns → Trends', 
    'Visualization Layer: Charts → Dashboards → Graphics',
    'Intelligence Layer: Segmentation → Revenue → Predictions',
    'Reporting Layer: Summary → Findings → Recommendations'
]

colors = ['lightblue', 'lightgreen', 'orange', 'lightcoral', 'lightyellow']

for i, (layer, color) in enumerate(zip(layers, colors)):
    y_pos = 0.75 - i * 0.15
    ax.add_patch(plt.Rectangle((0.1, y_pos-0.05), 0.8, 0.08, 
                              facecolor=color, edgecolor='black', alpha=0.7))
    ax.text(0.5, y_pos, layer, ha='center', va='center', fontsize=10, fontweight='bold')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.title('Project Architecture Overview', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('project_architecture.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a simple metrics summary chart
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Hotel Booking Analysis - Key Metrics Summary', fontsize=16, fontweight='bold')

# 1. Channel Distribution
channel_counts = df['booking_channel'].value_counts()
ax1.pie(channel_counts.values, labels=channel_counts.index, autopct='%1.1f%%', 
        colors=['lightblue', 'lightgreen', 'orange'])
ax1.set_title('Booking Channel Distribution', fontweight='bold')

# 2. Cancellation Overview
cancelled = len(df[df['booking_status'].str.contains('cancel', case=False, na=False)])
confirmed = len(df) - cancelled
ax2.pie([confirmed, cancelled], labels=['Confirmed', 'Cancelled'], autopct='%1.1f%%',
        colors=['lightgreen', 'lightcoral'])
ax2.set_title('Booking Status Overview', fontweight='bold')

# 3. Star Rating Distribution
star_counts = df['star_rating'].value_counts().sort_index()
ax3.bar(star_counts.index, star_counts.values, color='gold', alpha=0.7)
ax3.set_title('Hotel Star Rating Distribution', fontweight='bold')
ax3.set_xlabel('Star Rating')
ax3.set_ylabel('Number of Bookings')

# 4. Revenue Metrics
revenue_data = [df['selling_price'].sum()/1000000, df['selling_price'].mean()/1000]
labels = ['Total Revenue\n($M)', 'Average Booking\n($K)']
ax4.bar(labels, revenue_data, color=['green', 'blue'], alpha=0.7)
ax4.set_title('Revenue Metrics', fontweight='bold')
ax4.set_ylabel('Value')

plt.tight_layout()
plt.savefig('metrics_summary_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("Quick charts generated successfully!")
print("Files created:")
print("• project_architecture.png")
print("• metrics_summary_dashboard.png")
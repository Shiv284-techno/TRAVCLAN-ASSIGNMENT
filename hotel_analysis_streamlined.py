"""
Hotel Booking Data Analysis - TravClan Business Analyst Intern Assignment
Streamlined version for quick analysis and insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def analyze_hotel_bookings():
    """Comprehensive hotel booking analysis"""
    
    print("="*60)
    print("HOTEL BOOKING DATA ANALYSIS - TRAVCLAN ASSIGNMENT")
    print("="*60)
    
    # Load data
    try:
        df = pd.read_csv('Hotel_bookings_final.csv')
        print(f"Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # 1. DATASET OVERVIEW
    print("\n1. DATASET OVERVIEW")
    print("-" * 30)
    print(f"Dataset shape: {df.shape}")
    print("\nColumn Information:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col:<20} ({df[col].dtype})")
    
    # 2. MISSING VALUES ANALYSIS
    print("\n2. MISSING VALUES ANALYSIS")
    print("-" * 30)
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_percent.values
    }).sort_values('Missing_Count', ascending=False)
    
    print(missing_df[missing_df['Missing_Count'] > 0])
    
    # 3. DATA PREPROCESSING
    print("\n3. DATA PREPROCESSING")
    print("-" * 30)
    
    # Handle missing values for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Handle missing values for categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Convert date columns
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Create derived features
    if 'booking_date' in df.columns and 'check_in_date' in df.columns:
        df['booking_lead_time'] = (df['check_in_date'] - df['booking_date']).dt.days
    
    if 'check_in_date' in df.columns and 'check_out_date' in df.columns:
        df['stay_duration'] = (df['check_out_date'] - df['check_in_date']).dt.days
    
    if 'selling_price' in df.columns and 'costprice' in df.columns:
        df['profit_margin'] = ((df['selling_price'] - df['costprice']) / df['selling_price']) * 100
    
    if 'booking_date' in df.columns:
        df['booking_month'] = df['booking_date'].dt.month
    
    print("Data preprocessing completed")
    print("Created derived features: booking_lead_time, stay_duration, profit_margin")
    
    # 4. KEY OBSERVATIONS - BOOKING PATTERNS
    print("\n4. KEY OBSERVATIONS - BOOKING PATTERNS")
    print("-" * 40)
    
    # Booking Channel Analysis
    if 'booking_channel' in df.columns:
        print("\nA. BOOKING CHANNEL ANALYSIS:")
        channel_counts = df['booking_channel'].value_counts()
        channel_percentages = (channel_counts / len(df)) * 100
        for channel, count in channel_counts.head().items():
            pct = channel_percentages[channel]
            print(f"   {channel}: {count:,} bookings ({pct:.1f}%)")
    
    # Star Rating Analysis
    if 'star_rating' in df.columns:
        print("\nB. HOTEL STAR RATING ANALYSIS:")
        rating_counts = df['star_rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            pct = (count / len(df)) * 100
            print(f"   {rating}-star hotels: {count:,} bookings ({pct:.1f}%)")
    
    # Room Type Analysis
    if 'room_type' in df.columns:
        print("\nC. ROOM TYPE PREFERENCES:")
        room_counts = df['room_type'].value_counts()
        for room, count in room_counts.head().items():
            pct = (count / len(df)) * 100
            print(f"   {room}: {count:,} bookings ({pct:.1f}%)")
    
    # 5. CANCELLATION ANALYSIS
    print("\n5. CANCELLATION BEHAVIOR ANALYSIS")
    print("-" * 40)
    
    if 'booking_status' in df.columns:
        # Overall cancellation rate
        total_bookings = len(df)
        cancelled_bookings = len(df[df['booking_status'].str.contains('cancel', case=False, na=False)])
        cancellation_rate = (cancelled_bookings / total_bookings) * 100
        
        print(f"\nOverall Cancellation Rate: {cancellation_rate:.2f}%")
        
        # Cancellation by channel
        if 'booking_channel' in df.columns:
            print("\nCANCELLATION RATES BY CHANNEL:")
            cancel_by_channel = df.groupby('booking_channel')['booking_status'].apply(
                lambda x: (x.str.contains('cancel', case=False, na=False).sum() / len(x)) * 100
            ).sort_values(ascending=False)
            
            for channel, rate in cancel_by_channel.head().items():
                print(f"   {channel}: {rate:.1f}%")
        
        # Cancellation by star rating
        if 'star_rating' in df.columns:
            print("\nCANCELLATION RATES BY STAR RATING:")
            cancel_by_rating = df.groupby('star_rating')['booking_status'].apply(
                lambda x: (x.str.contains('cancel', case=False, na=False).sum() / len(x)) * 100
            )
            
            for rating in sorted(cancel_by_rating.index):
                rate = cancel_by_rating[rating]
                print(f"   {rating}-star hotels: {rate:.1f}%")
    
    # 6. REVENUE & PROFITABILITY ANALYSIS
    print("\n6. REVENUE & PROFITABILITY ANALYSIS")
    print("-" * 40)
    
    if 'selling_price' in df.columns:
        total_revenue = df['selling_price'].sum()
        avg_booking_value = df['selling_price'].mean()
        median_booking_value = df['selling_price'].median()
        
        print(f"\nREVENUE METRICS:")
        print(f"   Total Revenue: ${total_revenue:,.2f}")
        print(f"   Average Booking Value: ${avg_booking_value:.2f}")
        print(f"   Median Booking Value: ${median_booking_value:.2f}")
        
        # Revenue by channel
        if 'booking_channel' in df.columns:
            print(f"\nREVENUE BY BOOKING CHANNEL:")
            revenue_by_channel = df.groupby('booking_channel')['selling_price'].agg(['sum', 'mean']).round(2)
            revenue_by_channel = revenue_by_channel.sort_values('sum', ascending=False)
            
            for channel in revenue_by_channel.index[:5]:
                total_rev = revenue_by_channel.loc[channel, 'sum']
                avg_rev = revenue_by_channel.loc[channel, 'mean']
                print(f"   {channel}: Total ${total_rev:,.2f}, Avg ${avg_rev:.2f}")
        
        # Profit margin analysis
        if 'profit_margin' in df.columns:
            avg_profit_margin = df['profit_margin'].mean()
            median_profit_margin = df['profit_margin'].median()
            print(f"\nPROFIT MARGINS:")
            print(f"   Average Profit Margin: {avg_profit_margin:.2f}%")
            print(f"   Median Profit Margin: {median_profit_margin:.2f}%")
    
    # 7. TEMPORAL ANALYSIS
    print("\n7. TEMPORAL TRENDS ANALYSIS")
    print("-" * 40)
    
    if 'booking_month' in df.columns:
        print("\nBOOKINGS BY MONTH:")
        monthly_bookings = df['booking_month'].value_counts().sort_index()
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        
        for month, count in monthly_bookings.items():
            pct = (count / len(df)) * 100
            print(f"   {month_names.get(month, month)}: {count:,} bookings ({pct:.1f}%)")
    
    if 'stay_duration' in df.columns:
        avg_stay = df['stay_duration'].mean()
        median_stay = df['stay_duration'].median()
        print(f"\nSTAY DURATION:")
        print(f"   Average Stay: {avg_stay:.1f} days")
        print(f"   Median Stay: {median_stay:.1f} days")
    
    if 'booking_lead_time' in df.columns:
        avg_lead_time = df['booking_lead_time'].mean()
        median_lead_time = df['booking_lead_time'].median()
        print(f"\nBOOKING LEAD TIME:")
        print(f"   Average Lead Time: {avg_lead_time:.1f} days")
        print(f"   Median Lead Time: {median_lead_time:.1f} days")
    
    # 8. CUSTOMER SEGMENTATION
    print("\n8. CUSTOMER SEGMENTATION INSIGHTS")
    print("-" * 40)
    
    if 'customer_id' in df.columns:
        # Customer booking frequency
        customer_bookings = df.groupby('customer_id').size()
        repeat_customers = (customer_bookings > 1).sum()
        total_customers = len(customer_bookings)
        repeat_rate = (repeat_customers / total_customers) * 100
        
        print(f"\nCUSTOMER BEHAVIOR:")
        print(f"   Total Unique Customers: {total_customers:,}")
        print(f"   Repeat Customers: {repeat_customers:,} ({repeat_rate:.1f}%)")
        print(f"   Average Bookings per Customer: {customer_bookings.mean():.1f}")
        
        # High-value customers
        if 'selling_price' in df.columns:
            customer_value = df.groupby('customer_id')['selling_price'].sum()
            high_value_threshold = customer_value.quantile(0.9)
            high_value_customers = (customer_value >= high_value_threshold).sum()
            
            print(f"   High-Value Customers (top 10%): {high_value_customers:,}")
            print(f"   High-Value Threshold: ${high_value_threshold:.2f}")
    
    # 9. BUSINESS RECOMMENDATIONS
    print("\n9. BUSINESS RECOMMENDATIONS")
    print("=" * 40)
    
    recommendations = [
        "REDUCE CANCELLATIONS:",
        "• Implement flexible booking policies for high-cancellation channels",
        "• Offer incentives for non-refundable bookings",
        "• Send booking reminders closer to check-in date",
        "",
        "IMPROVE PROFITABILITY:",
        "• Focus marketing on high-value customer segments",
        "• Optimize pricing for peak seasons and popular room types",
        "• Increase direct booking initiatives",
        "",
        "CHANNEL OPTIMIZATION:",
        "• Invest more in top-performing booking channels",
        "• Negotiate better rates with high-volume channels",
        "• Monitor and improve underperforming channels",
        "",
        "CUSTOMER RETENTION:",
        "• Create loyalty programs for repeat customers",
        "• Personalize offers based on booking history",
        "• Implement post-stay follow-up campaigns"
    ]
    
    for rec in recommendations:
        print(rec)
    
    # 10. KEY METRICS SUMMARY
    print("\n10. EXECUTIVE SUMMARY - KEY METRICS")
    print("=" * 40)
    
    summary_metrics = []
    
    if 'booking_status' in df.columns:
        cancelled = df[df['booking_status'].str.contains('cancel', case=False, na=False)]
        cancel_rate = (len(cancelled) / len(df)) * 100
        summary_metrics.append(f"Cancellation Rate: {cancel_rate:.1f}%")
    
    if 'selling_price' in df.columns:
        avg_revenue = df['selling_price'].mean()
        summary_metrics.append(f"Average Booking Value: ${avg_revenue:.2f}")
    
    if 'booking_channel' in df.columns:
        top_channel = df['booking_channel'].value_counts().index[0]
        channel_share = (df['booking_channel'].value_counts().iloc[0] / len(df)) * 100
        summary_metrics.append(f"Top Channel: {top_channel} ({channel_share:.1f}%)")
    
    if 'customer_id' in df.columns:
        unique_customers = df['customer_id'].nunique()
        summary_metrics.append(f"Unique Customers: {unique_customers:,}")
    
    for metric in summary_metrics:
        print(f"• {metric}")
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")

if __name__ == "__main__":
    analyze_hotel_bookings()
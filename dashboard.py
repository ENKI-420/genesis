#!/usr/bin/env python3
"""
Enterprise Acquisition Dashboard
Simple console-based dashboard for viewing key metrics
"""
import json
import sqlite3
from datetime import datetime
from enhanced_enterprise_acquisition import EnhancedEnterpriseClientAcquisition

class Dashboard:
    def __init__(self):
        self.acquisition = EnhancedEnterpriseClientAcquisition()
        
    def display_header(self):
        """Display dashboard header"""
        print("🎯 ENTERPRISE CLIENT ACQUISITION DASHBOARD")
        print("=" * 60)
        print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
    def display_summary_metrics(self):
        """Display summary metrics"""
        analytics = self.acquisition.generate_advanced_analytics()
        summary = analytics['summary']
        
        print("📊 SUMMARY METRICS")
        print("-" * 30)
        print(f"Total Leads:           {summary['total_leads']:>8}")
        print(f"Qualified Leads:       {summary['qualified_leads']:>8}")
        print(f"Pipeline Value:        ${summary['total_pipeline_value']:>12,.0f}")
        print(f"Qualification Rate:    {summary['qualification_rate']:>8.1f}%")
        print(f"Average Deal Size:     ${summary['average_deal_size']:>12,.0f}")
        print(f"Weekly Leads:          {summary['weekly_leads']:>8}")
        print()
        
    def display_source_performance(self):
        """Display source performance breakdown"""
        analytics = self.acquisition.generate_advanced_analytics()
        sources = analytics['source_performance']
        
        print("🎯 SOURCE PERFORMANCE")
        print("-" * 30)
        print(f"{'Source':<20} {'Leads':<8} {'Value':<12} {'Avg Score':<10}")
        print("-" * 50)
        
        for source, data in sources.items():
            source_name = source.replace('_', ' ').title()
            print(f"{source_name:<20} {data['count']:<8} ${data['total_value']:<11,.0f} {data['avg_qualification_score']:<10.1f}")
        print()
        
    def display_industry_insights(self):
        """Display industry insights"""
        analytics = self.acquisition.generate_advanced_analytics()
        industries = analytics['industry_insights']
        
        if industries:
            print("🏭 INDUSTRY INSIGHTS")
            print("-" * 30)
            print(f"{'Industry':<20} {'Leads':<8} {'Avg Deal':<12}")
            print("-" * 40)
            
            for industry, data in industries.items():
                print(f"{industry:<20} {data['count']:<8} ${data['avg_deal_size']:<11,.0f}")
            print()
        
    def display_conversion_funnel(self):
        """Display conversion funnel"""
        analytics = self.acquisition.generate_advanced_analytics()
        funnel = analytics['conversion_funnel']
        
        print("🔄 CONVERSION FUNNEL")
        print("-" * 30)
        total_leads = sum(funnel.values())
        
        for status, count in funnel.items():
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            status_name = status.replace('_', ' ').title()
            print(f"{status_name:<20} {count:<8} {percentage:<8.1f}%")
        print()
        
    def display_recommendations(self):
        """Display AI recommendations"""
        analytics = self.acquisition.generate_advanced_analytics()
        recommendations = analytics['recommendations']
        
        print("🤖 AI RECOMMENDATIONS")
        print("-" * 30)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        print()
        
    def display_top_leads(self):
        """Display top leads by value"""
        conn = sqlite3.connect(self.acquisition.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT company_name, deal_size, qualification_score, lead_source, status
            FROM leads 
            ORDER BY deal_size DESC 
            LIMIT 5
        """)
        top_leads = cursor.fetchall()
        conn.close()
        
        print("🏆 TOP LEADS BY VALUE")
        print("-" * 30)
        print(f"{'Company':<25} {'Deal Size':<12} {'Score':<8} {'Source':<15}")
        print("-" * 60)
        
        for company, deal_size, score, source, status in top_leads:
            source_name = source.replace('_', ' ').title()[:14]
            status_icon = "✅" if status == "qualified" else "⏳"
            print(f"{company[:24]:<25} ${deal_size:<11,.0f} {score:<8} {source_name:<15} {status_icon}")
        print()
        
    def display_recent_activity(self):
        """Display recent activity"""
        conn = sqlite3.connect(self.acquisition.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT company_name, created_at, lead_source, deal_size
            FROM leads 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent_leads = cursor.fetchall()
        conn.close()
        
        print("🕒 RECENT ACTIVITY")
        print("-" * 30)
        print(f"{'Company':<25} {'Date':<12} {'Source':<15}")
        print("-" * 52)
        
        for company, created_at, source, deal_size in recent_leads:
            date_str = created_at.split(' ')[0] if created_at else "N/A"
            source_name = source.replace('_', ' ').title()[:14]
            print(f"{company[:24]:<25} {date_str:<12} {source_name:<15}")
        print()
        
    def display_database_stats(self):
        """Display database statistics"""
        conn = sqlite3.connect(self.acquisition.db_path)
        cursor = conn.cursor()
        
        # Get table counts
        cursor.execute("SELECT COUNT(*) FROM leads")
        leads_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM opportunities")
        opportunities_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM conversion_tracking")
        conversions_count = cursor.fetchone()[0]
        
        # Get database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()[0]
        
        conn.close()
        
        print("🗄️ DATABASE STATISTICS")
        print("-" * 30)
        print(f"Leads Table:           {leads_count:>8} records")
        print(f"Opportunities Table:   {opportunities_count:>8} records")
        print(f"Conversions Table:     {conversions_count:>8} records")
        print(f"Database Size:         {db_size/1024:>8.1f} KB")
        print()
        
    def run_dashboard(self):
        """Run the complete dashboard"""
        self.display_header()
        self.display_summary_metrics()
        self.display_source_performance()
        self.display_industry_insights()
        self.display_conversion_funnel()
        self.display_top_leads()
        self.display_recent_activity()
        self.display_recommendations()
        self.display_database_stats()
        
        print("=" * 60)
        print("🎯 Dashboard complete! Use 'python3 dashboard.py' to refresh.")
        
def main():
    """Main function"""
    dashboard = Dashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
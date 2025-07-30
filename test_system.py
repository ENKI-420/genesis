#!/usr/bin/env python3
"""
Test script for Enterprise Client Acquisition System
Demonstrates various features and capabilities
"""
import json
import sqlite3
from enhanced_enterprise_acquisition import EnhancedEnterpriseClientAcquisition, LeadData, LeadSource

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Testing Basic Functionality")
    print("=" * 50)
    
    # Initialize system
    acquisition = EnhancedEnterpriseClientAcquisition()
    
    # Test email validation
    test_emails = [
        "valid@company.com",
        "invalid-email",
        "test@10minutemail.com",  # Disposable
        "user@domain.org"
    ]
    
    print("📧 Email Validation Test:")
    for email in test_emails:
        is_valid = acquisition.validate_email(email)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"  {email}: {status}")
    
    print()

def test_lead_generation():
    """Test lead generation capabilities"""
    print("🎯 Testing Lead Generation")
    print("=" * 50)
    
    acquisition = EnhancedEnterpriseClientAcquisition()
    
    # Generate some test leads
    test_leads = [
        LeadData(
            company="Test Corp",
            contact="John Doe",
            email="john@testcorp.com",
            deal_size=75000,
            source=LeadSource.CONTENT_MARKETING.value,
            industry="Technology",
            company_size="500+",
            budget_authority="Manager",
            timeline="Q3 2024"
        ),
        LeadData(
            company="Demo Inc",
            contact="Jane Smith",
            email="jane@demoinc.com",
            deal_size=150000,
            source=LeadSource.REFERRAL_PROGRAM.value,
            industry="Finance",
            company_size="1000+",
            budget_authority="C-Level",
            timeline="Q2 2024"
        )
    ]
    
    print("📝 Adding Test Leads:")
    for lead in test_leads:
        lead_id = acquisition.add_enhanced_lead_to_database(lead)
        if lead_id:
            print(f"  ✅ Added: {lead.company} - ${lead.deal_size:,}")
        else:
            print(f"  ❌ Failed: {lead.company}")
    
    print()

def test_analytics():
    """Test analytics and reporting"""
    print("📊 Testing Analytics")
    print("=" * 50)
    
    acquisition = EnhancedEnterpriseClientAcquisition()
    
    # Generate analytics
    analytics = acquisition.generate_advanced_analytics()
    
    print("📈 Key Metrics:")
    print(f"  Total Leads: {analytics['summary']['total_leads']}")
    print(f"  Qualified Leads: {analytics['summary']['qualified_leads']}")
    print(f"  Pipeline Value: ${analytics['summary']['total_pipeline_value']:,}")
    print(f"  Qualification Rate: {analytics['summary']['qualification_rate']:.1f}%")
    print(f"  Average Deal Size: ${analytics['summary']['average_deal_size']:,.0f}")
    
    print("\n🎯 Recommendations:")
    for rec in analytics['recommendations']:
        print(f"  {rec}")
    
    print()

def test_database_queries():
    """Test database query capabilities"""
    print("🗄️ Testing Database Queries")
    print("=" * 50)
    
    conn = sqlite3.connect("enhanced_enterprise_acquisition.db")
    cursor = conn.cursor()
    
    # Get lead statistics
    cursor.execute("SELECT COUNT(*), SUM(deal_size) FROM leads")
    total_leads, total_value = cursor.fetchone()
    
    # Get qualified leads
    cursor.execute("SELECT company_name, deal_size, qualification_score FROM leads WHERE status = 'qualified'")
    qualified_leads = cursor.fetchall()
    
    # Get source breakdown
    cursor.execute("SELECT lead_source, COUNT(*), AVG(deal_size) FROM leads GROUP BY lead_source")
    source_breakdown = cursor.fetchall()
    
    print(f"📊 Database Summary:")
    print(f"  Total Leads: {total_leads}")
    print(f"  Total Value: ${total_value or 0:,.0f}")
    
    print(f"\n✅ Qualified Leads:")
    for company, deal_size, score in qualified_leads:
        print(f"  {company}: ${deal_size:,.0f} (Score: {score})")
    
    print(f"\n📊 Source Breakdown:")
    for source, count, avg_deal in source_breakdown:
        print(f"  {source}: {count} leads, avg ${avg_deal or 0:,.0f}")
    
    conn.close()
    print()

def test_configuration():
    """Test configuration system"""
    print("⚙️ Testing Configuration")
    print("=" * 50)
    
    # Test with default config
    acquisition_default = EnhancedEnterpriseClientAcquisition()
    print(f"Default qualification threshold: {acquisition_default.config['qualification_threshold']}")
    
    # Test with custom config
    custom_config = {
        "qualification_threshold": 30,
        "source_weights": {
            "industry_challenges": 30,
            "content_marketing": 25
        }
    }
    
    # Save custom config
    with open("test_config.json", "w") as f:
        json.dump(custom_config, f, indent=2)
    
    acquisition_custom = EnhancedEnterpriseClientAcquisition("test_config.json")
    print(f"Custom qualification threshold: {acquisition_custom.config['qualification_threshold']}")
    print(f"Custom industry_challenges weight: {acquisition_custom.config['source_weights']['industry_challenges']}")
    
    print()

def main():
    """Run all tests"""
    print("🚀 Enterprise Client Acquisition System - Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_basic_functionality()
        test_lead_generation()
        test_analytics()
        test_database_queries()
        test_configuration()
        
        print("✅ All tests completed successfully!")
        print("\n📄 Generated Files:")
        print("  - enhanced_enterprise_acquisition.db (Database)")
        print("  - enhanced_enterprise_acquisition_report.json (Analytics Report)")
        print("  - enterprise_acquisition.log (Log File)")
        print("  - test_config.json (Test Configuration)")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
import streamlit as bar
import pandas as pd
import numpy as np

# পেজ কনফিগারেশন
bar.set_page_config(page_title="দোকান খাতা - স্পেশাল ERP", page_icon="🏪", layout="wide")

# ডামি সেশন স্টেট (লগইন ও ডেটার জন্য)
if "logged_in" not in bar.session_state:
    bar.session_state.logged_in = False
if "shop_name" not in bar.session_state:
    bar.session_state.shop_name = "আমার স্বপ্নের দোকান"

# --- সাইন-আপ ও সাইন-ইন পেজ ---
if not bar.session_state.logged_in:
    bar.title("🏪 দোকান খাতা (Dokan Khata) - এ স্বাগত")
    
    tab1, tab2 = bar.tabs(["লগইন (Sign In)", "নিবন্ধন (Sign Up)"])
    
    with tab1:
        bar.subheader("আপনার অ্যাকাউন্টে প্রবেশ করুন")
        username = bar.text_input("ইউজারনেম বা মোবাইল")
        password = bar.text_input("পাসওয়ার্ড", type="password")
        if bar.button("লগইন করুন"):
            if username and password:
                bar.session_state.logged_in = True
                bar.success("লগইন সফল হয়েছে!")
                bar.rerun()
            else:
                bar.error("অনুগ্রহ করে সঠিক তথ্য দিন।")
                
    with tab2:
        bar.subheader("নতুন দোকান অ্যাকাউন্ট তৈরি করুন")
        new_shop = bar.text_input("দোকানের নাম")
        new_owner = bar.text_input("মালিকের নাম")
        phone = bar.text_input("মোবাইল নাম্বার")
        new_pass = bar.text_input("নতুন পাসওয়ার্ড", type="password")
        logo = bar.file_uploader("দোকানের লোগো আপলোড করুন", type=["jpg", "png", "jpeg"])
        
        if bar.button("অ্যাকাউন্ট তৈরি করুন"):
            if new_shop and phone and new_pass:
                bar.session_state.shop_name = new_shop
                bar.session_state.logged_in = True
                bar.success("রেজিস্ট্রেশন সফল হয়েছে!")
                bar.rerun()
            else:
                bar.error("সবগুলো ঘর পূরণ করুন।")

# --- মূল অ্যাপ (লগইন করার পর) ---
else:
    # সাইডবার / নেভিগেশন
    bar.sidebar.title(f"🏪 {bar.session_state.shop_name}")
    bar.sidebar.write("স্ট্যাটাস: প্রফেশনাল ইউজার")
    
    menu = bar.sidebar.radio("মেনু সিলেক্ট করুন", [
        "📊 ড্যাশবোর্ড ও শেয়ার ভ্যালু", 
        "💰 বেচা-কিনা ও খরচ হিসাব", 
        "👥 দেনাদার ও পাওনাদার", 
        "👔 স্টাফ ও ইনভেন্টরি", 
        "🏦 ব্যাংক ও ক্যাশ হিসাব",
        "⚙️ দোকানের প্রোফাইল"
    ])
    
    if bar.sidebar.button("লগআউট"):
        bar.session_state.logged_in = False
        bar.rerun()

    # --- ১. ড্যাশবোর্ড ও শেয়ার ভ্যালু ---
    if menu == "📊 ড্যাশবোর্ড ও শেয়ার ভ্যালু":
        bar.title("📊 দোকানের রিয়েল-টাইম ড্যাশবোর্ড")
        
        # প্রধান মেট্রিক্স (KPI)
        col1, col2, col3, col4 = bar.columns(4)
        with col1:
            bar.metric(label="আজকের মোট বিক্রি", value="৳ ২৫,৫০০", delta="+১২%")
        with col2:
            bar.metric(label="আজকের মোট খরচ", value="৳ ৩,২০০", delta="-৫%")
        with col3:
            bar.metric(label="নিট লাভ/ক্ষতি", value="৳ ২২,৩০০", delta="লাভজনক", delta_color="normal")
        with col4:
            # বিক্রির ওপর ভিত্তি করে আনুমানিক শেয়ার ভ্যালু হিসাব
            bar.metric(label="দোকানের শেয়ার ভ্যালু (Est.)", value="৳ ১৫,৫০,০০০", delta="+৳ ৫০,০০০")
            
        bar.markdown("---")
        bar.subheader("📈 বিক্রি ও লাভের গ্রাফিক্স রিপোর্ট")
        
        # গ্রাফের জন্য ডামি ডেটা
        chart_data = pd.DataFrame(
            np.random.randn(7, 2) * [2000, 500],
            columns=['দৈনিক বিক্রি (৳)', 'দৈনিক লাভ (৳)'],
            index=['সোম', 'মঙ্গল', 'বুধ', 'বৃহঃ', 'শুক্র', 'শনি', 'রবি']
        )
        bar.line_chart(chart_data)

    # --- ২. বেচা-কিনা ও খরচ হিসাব ---
    elif menu == "💰 বেচা-কিনা ও খরচ হিসাব":
        bar.title("💰 দৈনিক বেচা-কিনা ও খরচ এন্ট্রি")
        
        col1, col2 = bar.columns(2)
        with col1:
            bar.subheader("🛒 নতুন বিক্রয় এন্ট্রি")
            prod_name = bar.text_input("পণ্যের নাম/আইডি")
            qty = bar.number_input("পরিমাণ (Quantity)", min_value=1)
            price = bar.number_input("বিক্রয় মূল্য (৳)", min_value=0.0)
            pay_method = bar.selectbox("পেমেন্ট মাধ্যম", ["ক্যাশ", "বিকাশ", "কার্ড", "ব্যাংক"])
            if bar.button("বিক্রি সেভ করুন"):
                bar.success(f"৳ {qty*price} এর বিক্রি সফলভাবে সংরক্ষিত হয়েছে।")
                
        with col2:
            bar.subheader("💸 খরচ এন্ট্রি")
            expense_cause = bar.text_input("খরচের বিবরণ (যেমন: কারেন্ট বিল, ভাড়া)")
            expense_amt = bar.number_input("খরচের পরিমাণ (৳)", min_value=0.0)
            if bar.button("খরচ সেভ করুন"):
                bar.success(f"৳ {expense_amt} খরচ এন্ট্রি হয়েছে।")

    # --- ৩. দেনাদার ও পাওনাদার ---
    elif menu == "👥 দেনাদার ও পাওনাদার":
        bar.title("👥 দেনাদার ও পাওনাদার (বাকি খাতা)")
        
        tab1, tab2 = bar.tabs(["🔴 দেনাদার (গ্রাহক বাকি)", "🟢 পাওনাদার (মহাজন বাকি)"])
        
        with tab1:
            bar.subheader("কাস্টমারের বাকির হিসাব")
            c_name = bar.text_input("গ্রাহকের নাম")
            c_amount = bar.number_input("বাকির পরিমাণ (৳)", key="customer_due")
            if bar.button("দেনাদার যোগ করুন"):
                bar.warning(f"{c_name} এর নামে ৳ {c_amount} বাকি লেখা হলো।")
                
        with tab2:
            bar.subheader("মহাজনের পাওনার হিসাব")
            s_name = bar.text_input("মহাজন/সাপ্লায়ারের নাম")
            s_amount = bar.number_input("পাওনার পরিমাণ (৳)", key="supplier_due")
            if bar.button("পাওনাদার যোগ করুন"):
                bar.error(f"{s_name} আপনার কাছে ৳ {s_amount} পাবে।")

    # --- ৪. স্টাফ ও ইনভেন্টরি ---
    elif menu == "👔 স্টাফ ও ইনভেন্টরি":
        bar.title("👔 স্টাফ ম্যানেজমেন্ট ও মালপত্র (ইনভেন্টরি)")
        
        bar.subheader("👔 স্টাফের বেতন ও হাজিরা")
        staff_name = bar.text_input("স্টাফের নাম")
        salary = bar.number_input("মাসিক বেতন (৳)", min_value=0)
        attendance = bar.radio("আজকের হাজিরা", ["উপস্থিত", "অনুপস্থিত"])
        if bar.button("স্টাফ তথ্য আপডেট করুন"):
            bar.success("স্টাফ রেকর্ড আপডেট হয়েছে।")
            
        bar.markdown("---")
        bar.subheader("📦 মালের স্টকিং (Inventory)")
        bar.text_input("নতুন মালের নাম")
        bar.number_input("ক্রয় মূল্য (পাইকারি দাম)", min_value=0)
        bar.number_input("বর্তমান স্টক সংখ্যা", min_value=0)
        if bar.button("স্টক আপডেট"):
            bar.success("স্টক সফলভাবে যুক্ত হয়েছে।")

    # --- ৫. ব্যাংক ও ক্যাশ হিসাব ---
    elif menu == "🏦 ব্যাংক ও ক্যাশ হিসাব":
        bar.title("🏦 ব্যাংক, বিকাশ ও ক্যাশ ব্যালেন্স")
        
        # বর্তমান ব্যালেন্স কার্ড
        c1, c2, c3 = bar.columns(3)
        c1.metric("💵 হাতে ক্যাশ টাকা", "৳ ৪৫,০০০")
        c2.metric("📱 বিকাশ মার্চেন্ট ব্যালেন্স", "৳ ৮৮,৫০০")
        c3.metric("🏦 ব্যাংক অ্যাকাউন্ট ব্যালেন্স", "৳ ৫,২০,০০০")
        
        bar.markdown("---")
        bar.subheader("🔄 লেনদেন ও উত্তোলন (Transaction & Withdrawal)")
        
        trans_type = bar.selectbox("লেনদেনের ধরণ", [
            "ব্যাংক থেকে ক্যাশ উত্তোলন", 
            "বিকাশ থেকে ক্যাশ উত্তোলন", 
            "ক্যাশ থেকে ব্যাংকে জমা", 
            "কার্ড পেমেন্ট সেটেলমেন্ট"
        ])
        amount = bar.number_input("টাকার পরিমাণ (৳)", min_value=0.0)
        if bar.button("লেনদেন সম্পন্ন করুন"):
            bar.success(f"সফলভাবে '{trans_type}' বাবদ ৳ {amount} অ্যাডজাস্ট করা হয়েছে।")

    # --- ৬. দোকানের প্রোফাইল ---
    elif menu == "⚙️ দোকানের প্রোফাইল":
        bar.title("⚙️ দোকানের প্রোফাইল এবং সেটিংস")
        bar.write(f"**দোকানের নাম:** {bar.session_state.shop_name}")
        bar.write("**ঠিকানা:** ঢাকা, বাংলাদেশ।")
        bar.write("**মোবাইল:** ০১XXXXXXXXX")
        bar.image("https://via.placeholder.com/150", caption="দোকানের লোগো (Sample)")
        
        new_title = bar.text_input("দোকানের নাম পরিবর্তন করুন", bar.session_state.shop_name)
        if bar.button("নাম আপডেট করুন"):
            bar.session_state.shop_name = new_title
            bar.rerun()

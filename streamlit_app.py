import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip", "install", "plotly"], capture_output=True)

import streamlit as st
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="NED's App", page_icon="💳", layout="wide")

st.markdown("""
<style>
    .stButton > button {
        background-color: #00A6A6; color: white;
        border: none; border-radius: 8px;
        width: 100%; font-weight: 600;
    }
    .stButton > button:hover { background-color: #007d7d; color: white; }
</style>
""", unsafe_allow_html=True)

USERS = {
    'user1':  {'password': 'pass1',    'balance': 5000},
    'user2':  {'password': 'pass2',    'balance': 3000},
    'admin':  {'password': 'admin123', 'balance': 10000},
}

if 'logged_in'    not in st.session_state: st.session_state.logged_in    = False
if 'username'     not in st.session_state: st.session_state.username     = ''
if 'balance'      not in st.session_state: st.session_state.balance      = 0
if 'transactions' not in st.session_state: st.session_state.transactions = []

def fmt(n): return f"PKR {n:,.2f}"

def do_logout():
    st.session_state.logged_in    = False
    st.session_state.username     = ''
    st.session_state.balance      = 0
    st.session_state.transactions = []

# ── LOGIN ──
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 💳 NED's App")
        st.markdown("*EasyPaisa-style Banking Dashboard*")
        st.markdown("---")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("Login"):
            if username in USERS and USERS[username]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.balance   = USERS[username]['balance']
                st.session_state.transactions = []
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        st.caption("💡 Try: user1/pass1 · user2/pass2 · admin/admin123")

# ── DASHBOARD ──
else:
    user  = st.session_state.username
    trans = st.session_state.transactions

    col_title, col_user, col_logout = st.columns([3, 1, 1])
    with col_title: st.markdown("### 💳 NED's App")
    with col_user:  st.markdown(f"<br>👤 **{user.upper()}**", unsafe_allow_html=True)
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Logout"):
            do_logout()
            st.rerun()

    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Dashboard", "📈 Reports"])

    # ── TAB 1 ──
    with tab1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#00A6A6,#007d7d);color:white;
                    border-radius:12px;padding:20px;margin-bottom:16px;">
            <p style="font-size:13px;opacity:.8;margin-bottom:4px;">CURRENT BALANCE</p>
            <p style="font-size:32px;font-weight:700;margin:0;">{fmt(st.session_state.balance)}</p>
            <p style="font-size:13px;opacity:.8;margin-top:4px;">Welcome, {user.upper()}</p>
        </div>
        """, unsafe_allow_html=True)

        total_sent  = sum(t['amount'] for t in trans if t['type'] == 'Send')
        total_bills = sum(t['amount'] for t in trans if t['type'] == 'Bill Payment')
        c1, c2, c3 = st.columns(3)
        c1.metric("💸 Total Sent",   fmt(total_sent))
        c2.metric("🧾 Bills Paid",   fmt(total_bills))
        c3.metric("🔢 Transactions", len(trans))

        st.markdown("---")
        col_send, col_bill = st.columns(2)

        with col_send:
            st.markdown("#### ➤ Send Money")
            s_amt = st.number_input("Amount", min_value=1.0, step=100.0, key="s_amt", label_visibility="collapsed")
            s_rec = st.text_input("Recipient", placeholder="Recipient name", key="s_rec", label_visibility="collapsed")
            if st.button("Send Money 💸"):
                if not s_rec:
                    st.warning("Enter a recipient name.")
                elif s_amt > st.session_state.balance:
                    st.error("❌ Insufficient balance")
                else:
                    st.session_state.balance -= s_amt
                    st.session_state.transactions.append({
                        'date': datetime.datetime.now().strftime('%d/%m %H:%M'),
                        'type': 'Send', 'amount': s_amt, 'to_from': s_rec
                    })
                    st.success(f"✅ Sent {fmt(s_amt)} to {s_rec}!")
                    st.rerun()

        with col_bill:
            st.markdown("#### 🧾 Pay Bills")
            b_amt  = st.number_input("Bill Amount", min_value=1.0, step=100.0, key="b_amt", label_visibility="collapsed")
            b_type = st.selectbox("Bill Type", ["Electricity", "Water", "Internet", "Mobile"], key="b_type", label_visibility="collapsed")
            if st.button("Pay Bill ⚡"):
                if b_amt > st.session_state.balance:
                    st.error("❌ Insufficient balance")
                else:
                    st.session_state.balance -= b_amt
                    st.session_state.transactions.append({
                        'date': datetime.datetime.now().strftime('%d/%m %H:%M'),
                        'type': 'Bill Payment', 'amount': b_amt, 'to_from': b_type
                    })
                    st.success(f"✅ {b_type} bill of {fmt(b_amt)} paid!")
                    st.rerun()

        st.markdown("---")
        st.markdown("#### 🕒 Recent Transactions")
        if trans:
            for t in list(reversed(trans[-5:])):
                c1, c2, c3, c4 = st.columns([2, 1.5, 2, 2])
                c1.caption(t['date'])
                c2.write(t['type'])
                c3.markdown(f"<span style='color:#e74c3c;font-weight:600;'>-{fmt(t['amount'])}</span>", unsafe_allow_html=True)
                c4.caption(t['to_from'])
        else:
            st.info("No transactions yet. Send money or pay a bill to get started!")

    # ── TAB 2 ──
    with tab2:
        st.markdown("#### 📊 Spending Summary")
        total_sent  = sum(t['amount'] for t in trans if t['type'] == 'Send')
        total_bills = sum(t['amount'] for t in trans if t['type'] == 'Bill Payment')
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Spent", fmt(total_sent + total_bills))
        m2.metric("Money Sent",  fmt(total_sent))
        m3.metric("Bills Paid",  fmt(total_bills))
        st.markdown("---")

        if trans:
            types = {}
            for t in trans:
                types[t['type']] = types.get(t['type'], 0) + t['amount']
            fig = go.Figure(data=[go.Bar(
                x=list(types.keys()), y=list(types.values()),
                marker_color='#00A6A6', marker_line_width=0,
                text=[fmt(v) for v in types.values()], textposition='outside',
            )])
            fig.update_layout(
                title="Spending by Category", xaxis_title="",
                yaxis_title="Amount (PKR)", template="plotly_white", height=350,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### 📋 All Transactions")
            st.markdown("| Date | Type | Amount | Details |")
            st.markdown("|------|------|--------|---------|")
            for t in reversed(trans):
                st.markdown(f"| {t['date']} | {t['type']} | {fmt(t['amount'])} | {t['to_from']} |")
        else:
            st.info("Make some transactions to see your reports here!")

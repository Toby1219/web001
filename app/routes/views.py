from flask import render_template, Blueprint, redirect, url_for, request, flash, g, session
from ..model.models import UserAccSchema, UserAccount, Transactions, TransactionSchema, Admin
from ..utils.handlers import (query_db_only, query_db_many, gen_referral_link, 
                              filter_transactions, change_data_handler, calculateInterest)
from ..utils.extension import is_auth
from datetime import datetime
from ..model.forms import ChangePsswordForm, ChangeWalletForm

view_bp = Blueprint("views", __name__)

@view_bp.route("/")
def homepage():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template('landing/lpage.html', signup_success=signup_success, webs=webs), 200
    return render_template('landing/lpage.html', webs=webs), 200

@view_bp.route("/about")
def aboutpage():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template('landing/about.html', signup_success=signup_success, webs=webs), 200
    return render_template("landing/about.html", webs=webs), 200

@view_bp.route("/financial-instrument")
def financial_instruments():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template('landing/f_instru.html', signup_success=signup_success, webs=webs), 200   
    return render_template("landing/f_instru.html", webs=webs), 200

@view_bp.route("/live-payout")
def live_payout():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template("landing/l_payout.html", signup_success=signup_success, webs=webs), 200
    return render_template("landing/l_payout.html", webs=webs), 200

@view_bp.route("/t-and-c")
def term_condi():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template("landing/t_u.html", signup_success=signup_success, webs=webs), 200
    return render_template("landing/t_u.html", webs=webs), 200

@view_bp.route("/privacy-policy")
def privacy_policy():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template("landing/privacy.html", signup_success=signup_success, webs=webs), 200
    return render_template("landing/privacy.html", webs=webs), 200

@view_bp.route("/loc")
def location_():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template("landing/location.html", signup_success=signup_success, webs=webs), 200
    return render_template("landing/location.html", webs=webs), 200

@view_bp.route('/terms-and-privacy-policy')
def terms():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if is_auth():
        signup_success = True
        return render_template("landing/terms.html", signup_success=signup_success, webs=webs), 200
    return render_template("auth/terms.html", webs=webs), 200

@view_bp.route('/user-account/user')
def account_page():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if session.get('role') != 'user' or g.user == None:
        return redirect(url_for('auth.login'))
    flash(f"{g.user.username.capitalize()} account page")
    args = ["id", "username", "email", "ref_count", "referral_code", 'ref_by', 'balance', 
            'earned', 'invested', 'active_deposits', 'ref_earings']
    data = query_db_only(UserAccount, UserAccSchema, g.user.username, onlys=args)
    referral_link, ref_n = gen_referral_link(data)
    user = UserAccount.query.filter_by(username=g.user.username).first()
    transacObj = Transactions.query.filter_by(username=g.user.username)
    transac = query_db_many(Transactions, TransactionSchema, g.user.username)
    transactions = [t for t in transac if t['status'] == 'Success']
    tr = None
    if transactions:
        tr = transactions[-1]
    else:
        tr = {'plan': '-', 'plan_perc': '_'}
    calculateInterest(user, transacObj)
    return render_template("user_account/acct_page.html", data=data, referral_link=referral_link, ref_n=ref_n, tr=tr, webs=webs), 200

@view_bp.route('/user-account/deposit')
def deposit_page():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if session.get('role') != 'user' or g.user == None:
        return redirect(url_for('auth.login'))
    args = ["username", "email", "walletType", "walletAddress", "earned", 'referral_code',
            "withdrawn", "active_deposits", "a_w_type", "a_w_address", "ref_by"]
    data = query_db_only(UserAccount, UserAccSchema, g.user.username, onlys=args)
    return render_template("user_account/deposit.html", data=data, webs=webs), 200

@view_bp.route('/user-account/withdraw', methods=['GET', 'POST'])
def withdraw_page():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if session.get('role') != 'user' or g.user == None:
        return redirect(url_for('auth.login'))  
    args = ["username", "email", "walletType", "walletAddress", "withdrawn", "balance", "a_w_type", "a_w_address"]
    data = query_db_only(UserAccount, UserAccSchema, g.user.username, onlys=args)
    return render_template("user_account/withdraw.html", data=data, webs=webs), 200

@view_bp.route('/user-account/transctions', methods=['GET', 'POST'])
def transaction():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if session.get('role') != 'user' or g.user == None:
        return redirect(url_for('auth.login'))  
    args = ["id", "username", "email", "walletType", "walletAddress", 
        "balance", "withdrawn", "active_deposits", "a_w_type", "a_w_address"]
    data = query_db_only(UserAccount, UserAccSchema, g.user.username, onlys=args)
    transactions = []
    if request.method == "POST":
        date_from = request.form.get("from")
        date_to = request.form.get("to")
        status = request.form.get("status")
        ttype = request.form.get("ttype")
        transactions = filter_transactions(date_from, date_to, status, ttype)
    if request.method == "GET":
        t_schema = query_db_many(Transactions, TransactionSchema, g.user.username)
        return render_template("user_account/transac.html", webs=webs, data=data,  transaction=sorted(t_schema, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"), reverse=True)), 200
    return render_template("user_account/transac.html", data=data,  transaction=transactions, webs=webs), 200

@view_bp.route('/user-account/setting', methods=['GET', 'POST'])
def settings():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    if session.get('role') != 'user' or g.user == None:
        return redirect(url_for('auth.login'))
    args = ["username", "email", "walletType", "walletAddress", "referral_code", 'phone', "a_w_type", "a_w_address"]
    data = query_db_only(UserAccount, UserAccSchema, g.user.username, onlys=args)
    form_password = ChangePsswordForm()
    form_wallet = ChangeWalletForm()
    if request.method == "POST":
        email = request.form.get("e")
        phone = request.form.get('pn')
        pay_method = form_wallet.walletType.data
        wallet_a = form_wallet.walletAdress.data
        cur_passw = form_password.Currentpassword.data
        new_passw = form_password.NewPassword.data
        co_new_passw = form_password.ComfirmPassword.data
        user = UserAccount.query.get(g.user.id)        
        msg = change_data_handler(user, email, phone, pay_method, wallet_a, cur_passw, new_passw, co_new_passw)
        flash(msg)
        return redirect(url_for('views.settings'))
    return render_template('user_account/setting.html', data=data,  form_password=form_password, form_wallet=form_wallet, webs=webs)




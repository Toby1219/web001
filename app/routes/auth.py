from flask import Blueprint, render_template, flash, redirect, url_for, request, session, jsonify
from ..model.forms import RegisterForm, LoginForm, ChangePsswordForm, ResetPassword
from ..model.models import UserAccount, Admin
from ..utils.extension import (validate_wallet, add_session, 
                               countries_data, generate_otp, is_valid_phone, assign_userWallet)
from zxcvbn import zxcvbn
from ..utils.handlers import deposit_handler, withdraw_handler, change_data_handler

from datetime import datetime, timedelta
import time, random

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    ref_code_req = request.args.get('ref')
    form = RegisterForm()
    if form.validate_on_submit():
        account_name = UserAccount.query.filter_by(username=form.username.data).first()
        email = UserAccount.query.filter_by(email=form.email.data).first()
        password =form.password.data
        re_password = form.retype_password.data
        wallet_type = form.walletType.data
        wallet_address = form.walletAdress.data
        referred_by = form.ref_code.data
        password_result = zxcvbn(password)
        if account_name:
            flash(f"❌ User name already exist", "error")
            return redirect(url_for('auth.register'))
        if email:
            flash("❌ Email already exist", "error")
            return redirect(url_for('auth.register'))
        if password != re_password:
            flash("❌ Password does not match", "error")
            return redirect(url_for('auth.register'))
        if password_result['score'] < 1:
            flash("❌ Password not secure use secure password", "error")
            return redirect(url_for('auth.register'))
        if len(form.username.data) < 3:
            flash("❌ username too short", "error")
            return redirect(url_for('auth.register'))
        if not validate_wallet(wallet_type.replace("Wallet", "").strip(), wallet_address):
            flash("❌ Invalid or wrong wallet address", "error")
            return redirect(url_for('auth.register'))
        if not is_valid_phone(form.phone.data, form.phone_region.data):
            flash("❌ Invalid or wrong phone number", "error")
            return redirect(url_for('auth.register'))
        else:
            if referred_by != None:
                referrer = UserAccount.query.filter_by(referral_code=referred_by).first()
                if referrer:
                    referrer.ref_count = int(referrer.ref_count) + 1
            
            user = UserAccount(username=form.username.data, email=form.email.data, walletType=wallet_type, 
                               walletAddress=wallet_address, ref_by=referred_by, phone=form.phone.data)
            address, type_, = assign_userWallet(wallet_type)
            user.a_w_address = address
            user.a_w_type = type_
            user.set_password(password=password)
            user.generate_referral_code()
            user.create_user()
            add_session(user.id)
            
            return redirect(url_for('views.account_page'))
    else:
        flash("".join(f"{r}: {x[0]}" for r, x in form.errors.items()))
    
    return render_template("auth/register.html", form=form, ref_code_req=ref_code_req or "", c_datas=countries_data, webs=webs), 200

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data.strip()).first()
        if admin and admin.check_password(form.password.data):
            add_session(admin.id, 'admin_')
            return redirect(url_for('admin.homepage_admin'))
        
        user = UserAccount.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            add_session(user.id)
            return redirect(url_for('views.account_page'))
        else:
            if not user or not admin:
                flash("❌ Invalid log in details (Username) or (Password)", "error")
                return redirect(url_for('auth.login'))           
    else:
        flash("".join(x[0] for _, x in form.errors.items()))
      
    return render_template("auth/login.html", form=form, webs=webs)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route('/reset-password/otp')
def reset_fuc():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]

    return render_template("auth/fpass.html", webs=webs), 200


@auth_bp.route('/otp', methods=['GET', 'POST'])
def request_otp():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]
    time.sleep(random.randint(5, 10))
    input_args = request.args.get('b')
    user = UserAccount.query.filter_by(email=input_args).first()
    if not user:
        user = UserAccount.query.filter_by(phone=f"+{input_args}").first()
    if input_args and user:
        otp = generate_otp()
        user.otp = otp
        user.otp_expiry = datetime.now() + timedelta(seconds=30)
        user.create_user()
        return jsonify([{"otp": otp}])
    else:
        return jsonify([{"otp": " faild invalid user details"}])


@auth_bp.route('/reset', methods=['GET', 'POST'])
def reset_password():
    ad = Admin.query.get(1)
    webs = [ad.PhoneNumberWhatsapp, ad.PhoneNumberTelegram, ad.email]

    form_password = ResetPassword()
    otp = request.args.get('otp')
    userinput = request.args.get('u')
    new_passw = form_password.NewPassword.data
    
    if request.method == 'POST':
        user = UserAccount.query.filter_by(email=userinput).first()
        
        if user and user.otp == otp and user.otp_expiry > datetime.now():       
            user.otp = None
            user.otp_expiry = None
            user.set_password(new_passw)
            user.create_user()  
            return redirect(url_for('auth.login'))
        else:
            flash("OTP expired")
    return render_template('auth/resetp.html', form_password=form_password, webs=webs)


def give_gift(code, cucode, amt, plan):
    import json
    user = UserAccount.query.filter_by(referral_code=code).first()
    user2 = UserAccount.query.filter_by(referral_code=cucode).first()
    ad = Admin.query.get(1)
    plans = json.loads(ad.ref_gift)
    percent = [v for k, v in plans.items() if k.lower() == plan.lower()]
    if user and percent and user2.is_first_payment:
        gift = percent[0] / 100 * float(amt)
        user2.is_first_payment = False
        user.ref_earings = "{:,.2f}".format(gift + float(user.ref_earings))
        user.create_user()
           

@auth_bp.route('/user-account/payment', methods=['POST'])
def payment_handler():
    if session.get('role') != 'user':
        return redirect(url_for('auth.login'))
    data = request.get_json()    
    t_t = data['tt']
    match t_t:
        case "deposit":
            selected_plan = data['plan']
            selected_ammount = data['planamt']
            w_address = data['wa']
            w_type = data['wt']
            plan_perc = data['pp']
            plan_hours = data['ph']
            refBy = data['refby']
            ref_code = data['refcode']
            give_gift(refBy, ref_code, selected_ammount, selected_plan)
            response_ = deposit_handler(w_address, w_type, selected_ammount, 
                                        selected_plan, t_t, plan_perc, plan_hours)
            return jsonify({"nextUrl":f'{request.base_url}/user-account/user'})
        case "withdraw":
            amt = data['amt']
            w_a = data['wa']
            w_t = data['wt']
            s = data["st"]
            response_ = withdraw_handler(w_a, w_t, amt, t_t, s)
            return jsonify({"nextUrl":f'{request.base_url}/user-account/user'})

from datetime import datetime, timedelta, timezone
import mysql.connector
import timeago
import hashlib
from slugify import slugify
from flask import Flask, url_for, render_template, redirect, request, session, Response
from flask_sitemapper import Sitemapper
import os
import sys
import socket
import random
import re

import backend
from backend import *

event_names = {}

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__


def categories():
    sql = "SELECT * FROM categories ORDER BY category_name ASC"
    cursor.execute(sql)
    cats = cursor.fetchall()
    return cats


def hasTitle(title):
    sql = "SELECT ens_title FROM urls WHERE ens_title = %s"
    cursor.execute(sql, (title,))
    title = cursor.fetchone()
    return title


def hasCatTitle(title):
    sql = "SELECT category_name FROM categories WHERE category_name = %s"
    cursor.execute(sql, (title,))
    title = cursor.fetchone()
    return title


def hasCatUrl(url):
    sql = "SELECT category_url FROM categories WHERE category_url = %s"
    cursor.execute(sql, (url,))
    url = cursor.fetchone()
    return url


def hasUser(email):
    encemail = f"{backend.ucdencrypt(email, backend.key)}"
    sql = "SELECT user_id FROM users WHERE user_email = %s"
    cursor.execute(sql, (encemail,))
    post = cursor.fetchone()
    return post


def tel_no_check(number):
    pattern = r'^90\d{10}$'

    # Düzenli ifadeyi kullanarak kontrol yapma
    if re.match(pattern, number):
        return True
    else:
        return False

def tel_no_user_check(number):
    number = backend.ucddecrypt(eval(str(number)), backend.key)
    sql = "SELECT * FROM users WHERE user_cep_tel_no = %s"
    cursor.execute(sql, (number, ))
    user_tel_no = cursor.fetchall()
    if user_tel_no:
        return False
    else:
        return True

def timeAgo(date):
    return timeago.format(date, datetime.now(), 'tr')


sitemapper = Sitemapper()
app = Flask(__name__)
app.secret_key = b',\xbd\x0b\xa6qr\x8f\xb95*Z\xe9+w\x9c\xfb'
app.jinja_env.globals.update(categories=categories)
app.jinja_env.filters['timeAgo'] = timeAgo
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
app.config['SESSION_PERMANENT'] = False
sitemapper.init_app(app)

@sitemapper.include(lastmod="2022-02-08")
@app.route('/', methods=['GET', 'POST'])
def home():
    success = ''
    error = ''
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)
        durum = durums['user_statu']

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        if durum == 1:

            user_details = backend.user_detail()

            dec_userdetails = [
                {'user_statu': i['user_statu'], 'user_id': i['user_id'],
                 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
                 'user_create_date': i['user_create_date'],
                 'user_update_date': i['user_update_date'], 'user_total_count': i['user_total_count']}
                for i in user_details]

            if request.method == "GET":
                success = request.args.get('success')
                error = request.args.get('error')

                last_activity_key = f'last_activity_{user_id}'
                last_activity = session.get(last_activity_key)
                now = datetime.now(timezone.utc)
                session[last_activity_key] = now
                if last_activity:
                    expiry_time = last_activity + timedelta(
                        minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                    if expiry_time < now:
                        return redirect(url_for('logout', id=user_id))

                return render_template('administrator/index.html', error=error, success=success, durum=durums,
                                       onlineuser=dec_datakul,
                                       users=dec_userdetails)

            elif request.method == "POST":

                last_activity_key = f'last_activity_{user_id}'
                last_activity = session.get(last_activity_key)
                now = datetime.now(timezone.utc)
                session[last_activity_key] = now

                if last_activity:
                    expiry_time = last_activity + timedelta(
                        minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                    if expiry_time < now:
                        # Oturum süresi doldu, çıkış yapmaya yönlendir
                        return redirect(url_for('logout', id=user_id))

                if request.form['kuladi'] == '':
                    error = 'Aranacak kullanıcı adını veya kullanıcı emaili girmediniz..!'
                else:

                    kuladi = f"{backend.ucdencrypt(request.form['kuladi'], backend.key)}"

                    user_details = backend.user_detail_search(kuladi)

                    dec_userdetails2 = [
                        {'user_statu': i['user_statu'], 'user_id': i['user_id'],
                         'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
                         'user_create_date': i['user_create_date'],
                         'user_update_date': i['user_update_date'], 'user_total_count': i['user_total_count']}
                        for i in user_details]

                    if user_details:
                        kulanici = request.form['kuladi']
                        success = f'Aranan Kelime : {kulanici} Kullanıcı verisi sistemde mevcuttur.'
                        user_details = user_details
                    else:
                        kulanici = request.form['kuladi']
                        error = f"Aranan Kelime : {kulanici} Kullanıcı verisi sistemde mevcut değildir...!"

                return render_template('administrator/index.html', error=error, success=success, durum=durums,
                                       onlineuser=dec_datakul, users=dec_userdetails2)

        elif durum == 0:

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now

            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/index.html', durum=durums, onlineuser=dec_datakul)
    else:
        durums = 3
        return render_template('views/index.html', durum=durums)


################################################ Giriş İşlemleri Başlangıç #############################################################################

@sitemapper.include(lastmod="2022-02-08")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    error = ''
    durums = 3

    if request.method == 'POST':
        if request.form['username'] == '':
            error = 'Kullanıcı adı veya E-posta adresinizi belirtin.'
        elif request.form['password'] == '':
            error = 'Şifrenizi belirtin.'
        else:

            encusername = f"{backend.ucdencrypt(request.form['username'], backend.key)}"

            encsifre = f"{backend.ucdencrypt(request.form['password'], backend.key)}"

            user = backend.login(encusername, encusername, encusername, encsifre)
            if user:
                giris = user['user_giris']

                if giris == 0:
                    host = request.remote_addr
                    bugun = datetime.now()
                    tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                    backend.login_update(tarih, "1", host, user['user_id'])

                    session['user_id'] = user['user_id']

                    rand_num = random.randint(1000, 9999)
                    event_name = f"cikis_etkinligi_{rand_num}"
                    event_names[session['user_id']] = event_name
                    session['last_activity_{user_id}'] = datetime.now()

                    backend.event_start(event_name, user['user_id'])

                    session.permanent = True
                    return redirect(url_for('home'))
                elif giris == 1:
                    error = 'Bu kullanıcı zaten giriş yapmıştır.'
            else:
                error = 'Girdiğiniz bilgilere ait kullanıcı bulunamadı.'

    return render_template('views/login.html', error=error, durum=durums)


@sitemapper.include(lastmod="2022-02-08")
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    durums = 3
    if request.method == 'POST':
        if request.form['username'] == '':
            error = 'Username belirtin.'
        elif request.form['firstname'] == '':
            error = 'Adınızı belirtin.'
        elif request.form['firstname'] == '':
            error = 'Soyadınızı belirtin.'
        elif request.form['telno'] == '':
            error = 'Telefon numarası belirtiniz.'
        elif tel_no_check(request.form['telno']) == False:
            error = 'Telefon biçimi yanlıştır.'
        elif tel_no_user_check(request.form['telno']) == False:
            error = 'Daha önce bu numarayla kayıt olunmuştur.'
        elif request.form['email'] == '':
            error = 'E-posta adresinizi belirtin'
        elif request.form['password'] == '' or request.form['re_password'] == '':
            error = 'Şifrenizi belirtin.'
        elif request.form['password'] != request.form['re_password']:
            error = 'Girdiğiniz şifreler birbiriyle uyuşmuyor'
        elif hasUser(request.form['email']):
            error = 'Bu e-posta ile birisi zaten kayıtlı, başka bir tane deneyin'
        else:
            encusername = f"{backend.ucdencrypt(request.form['username'], backend.key)}"

            encfirstname = f"{backend.ucdencrypt(request.form['firstname'], backend.key)}"

            enclastname = f"{backend.ucdencrypt(request.form['lastname'], backend.key)}"

            enctelno = f"{backend.ucdencrypt(request.form['telno'], backend.key)}"

            encemail = f"{backend.ucdencrypt(request.form['email'], backend.key)}"

            encsifre = f"{backend.ucdencrypt(request.form['password'], backend.key)}"

            user_statu = 0
            host = request.remote_addr
            user_giris = 0
            bugun = datetime.now()
            tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

            backend.register_insert(encusername, encfirstname, enclastname, enctelno, encemail, encsifre, user_statu, user_giris, host, tarih, tarih)

            if backend.cursor.rowcount:
                session['user_id'] = backend.cursor.lastrowid
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                backend.login_update(tarih, "1", host, session['user_id'])

                return redirect(url_for('home'))
            else:
                error = 'Teknik bir problemden dolayı kaydınız oluşturulamadı'

    return render_template('views/register.html', error=error, durum=durums)


@sitemapper.include(lastmod="2022-02-08")
@app.route('/logout/<id>')
def logout(id):
    backend.logout_update("0", id)
    event_name = event_names.pop(int(id), None)
    if event_name:
        backend.event_update(event_name)
    session.permanent = False
    session.clear()
    return redirect(url_for('home'))


@sitemapper.include(lastmod="2022-02-08")
@app.route('/profil2/<id>', methods=['POST', 'GET'])
def profil2(id):
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user_durum(user_id)
        durum = durums['user_statu']

        if durum == 1:
            kul = backend.users(user_id)

            onlinekul = backend.online_users()

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            dec_datakul = [
                {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
                 'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
                 'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
                 'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
                 'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
                 'user_update_date': i['user_update_date']}
                for i in onlinekul]

            return render_template('administrator/profil2.html', durum=durums, kul=kul, onlineuser=dec_datakul)

        else:

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            kul = backend.users(user_id)

            onlinekul = backend.online_users()

            dec_datakul = [
                {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
                 'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
                 'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
                 'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
                 'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
                 'user_update_date': i['user_update_date']}
                for i in onlinekul]

            return render_template('views/profil2.html', durum=durums, kul=kul, onlineuser=dec_datakul)

    return redirect(url_for('home'))


################################################ Giriş İşlemleri Bitiş #############################################################################

################################################ Admin Ensturamanlar Bölümü Başlangıç#############################################################################

@app.route('/ensturamans', methods=['GET', 'POST'])
def ensturamans():
    if 'user_id' in session:
        user_id = session['user_id']
        success = request.args.get('success')
        error = request.args.get('error')

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        ens_details = backend.ens_detail()

        dec_data = [{'ens_statu': i['ens_statu'], 'ens_id': i['ens_id'],
                     'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                     'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key)} for
                    i in ens_details]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('administrator/ensturamans.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   urls=dec_data)

        if request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if request.form['urlname'] == '':
                error = "Aranacak Bot İsmi veya Kategori ID'sini veya Müşteri Numara'sı yazmadınız...!"
            else:

                kelime = f"{backend.encrypt(request.form['urlname'], backend.key)}"
                ens_details = backend.ens_detail_search(kelime)

                dec_data2 = [{'ens_statu': i['ens_statu'], 'ens_id': i['ens_id'],
                              'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                              'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key)} for
                             i in ens_details]

                if ens_details:
                    ens = request.form['urlname']
                    ens_details = ens_details
                    success = f'Aranan Kelime : {ens} Eş değer sonuçlar bulunmuştur. '
                else:
                    ens = request.form['urlname']
                    error = f'Aranan Kelime {ens} Eş değer veri sistemde mevcut değildir...!'
            return render_template('administrator/ensturamans.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   urls=dec_data2)
    else:
        durums = 3
        return redirect(url_for('home'))


@app.route('/newensturamans', methods=['GET', 'POST'])
def newensturamans():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        error = ''
        success = ''

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('administrator/newensturamans.html', durum=durums, onlineuser=dec_datakul)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if (backend.searc_user_packets_log(user_id) == False):
                error = 'Satın Alınmış Paketiniz Bulunmadığı için bot ekleyemezsiniz...!'

            elif request.form['title'] == '':
                error = 'Bot başlığı girmediniz...!'
            elif hasTitle(request.form['title']):
                error = 'Bu başlıkta Bot kayıt edilmiştir...!'
            elif request.form['category_id'] == '':
                error = 'Katgeori Seçmediniz...!'
            elif request.form['mustelno'] == '':
                error = 'Müşteri telefon numarası alanını boş bıraktınız...!'
            elif (tel_no_check(request.form['mustelno']) == False):
                error = 'Geçerli telefon numarası giriniz...!'
            elif request.form['musno'] == '':
                error = 'Müşteri numarası alanını boş bıraktınız...!'
            elif request.form['mussifre'] == '':
                error = 'Müşteri şifresi alanını boş bıraktınız...!'
            elif request.form['yuzdefiyat'] == '':
                error = 'Paranızın Yüzde Kaçı Kullanılacak girmediniz...!'
            elif request.form['ensturamanlar'] == '':
                error = 'Ensturamanlar alanını boş bıraktınız...!'
            else:
                enctitle = f"{backend.encrypt(request.form['title'], backend.key)}"
                encmustelno = f"{backend.encrypt(request.form['mustelno'], backend.key)}"
                encmusno = f"{backend.encrypt(request.form['musno'], backend.key)}"
                encmussifre = f"{backend.encrypt(request.form['mussifre'], backend.key)}"
                encyuzdefiyat = f"{backend.encrypt(request.form['yuzdefiyat'], backend.key)}"
                encensturamanlar = f"{backend.encrypt(request.form['ensturamanlar'], backend.key)}"
                paclogid = backend.searc_user_packets_log_id_data(user_id)
                for row in paclogid:
                    pacid = row['pac_log_id']
                paclogid = pacid
                statu = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"
                backend.add_ensturaman(enctitle, request.form['category_id'], encmustelno, encmusno, encmussifre,
                                       encyuzdefiyat, encensturamanlar, user_id, paclogid, tarih, tarih, statu)
                success = 'Bot Başarıyla Eklendi..'

        return render_template('administrator/newensturamans.html', error=error, success=success, durum=durums,
                               onlineuser=dec_datakul)

    else:
        return redirect(url_for('home'))


@app.route('/duzenle/<id>', methods=['GET', 'POST'])
def duzenle(id):
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            ens = backend.edit_ensturaman_checking(id)

            dec_data = [{'ens_id': i['ens_id'], 'ens_statu': i['ens_statu'],
                         'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                         'ens_category': i['ens_category'],
                         'ens_mustelno': backend.decrypt(eval(str(i['ens_mustelno'])), backend.key),
                         'ens_musno': backend.decrypt(eval(str(i['ens_musno'])), backend.key),
                         'ens_mussifre': backend.decrypt(eval(str(i['ens_mussifre'])), backend.key),
                         'ens_yuzdefiyat': backend.decrypt(eval(str(i['ens_yuzdefiyat'])), backend.key),
                         'ens_ensturamanlar': backend.decrypt(eval(str(i['ens_ensturamanlar'])), backend.key),
                         'ens_user': i['ens_user'],
                         'ens_create_date': i['ens_create_date'], 'ens_update_date': i['ens_update_date']}
                        for i in ens]

            return render_template('administrator/duzenleensturaman.html', durum=durums, onlineuser=dec_datakul,
                                   ens=dec_data)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            ens = backend.edit_ensturaman_checking(id)
            dec_data = [{'ens_id': i['ens_id'], 'ens_statu': i['ens_statu'],
                         'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                         'ens_category': i['ens_category'],
                         'ens_mustelno': backend.decrypt(eval(str(i['ens_mustelno'])), backend.key),
                         'ens_musno': backend.decrypt(eval(str(i['ens_musno'])), backend.key),
                         'ens_mussifre': backend.decrypt(eval(str(i['ens_mussifre'])), backend.key),
                         'ens_yuzdefiyat': backend.decrypt(eval(str(i['ens_yuzdefiyat'])), backend.key),
                         'ens_ensturamanlar': backend.decrypt(eval(str(i['ens_ensturamanlar'])), backend.key),
                         'ens_user': i['ens_user'],
                         'ens_create_date': i['ens_create_date'], 'ens_update_date': i['ens_update_date']}
                        for i in ens]

            error = ''
            success = ''
            if (backend.searc_user_packets_log(user_id) == False):
                error = 'Satın Alınmış Paketiniz Bulunmadığı için bot ekleyemezsiniz veya düzenleyemezsiniz...!'
            elif request.form['title'] == '':
                error = 'Bot başlığı girmediniz...!'
            elif hasTitle(request.form['title']):
                error = 'Bu başlıkta Bot kayıt edilmiştir...!'
            elif request.form['category_id'] == '':
                error = 'Katgeori Seçmediniz...!'
            elif request.form['mustelno'] == '':
                error = 'Müşteri telefon numarası alanını boş bıraktınız...!'
            elif (tel_no_check(request.form['mustelno']) == False):
                error = 'Geçerli telefon numarası giriniz...!'
            elif request.form['musno'] == '':
                error = 'Müşteri numarası alanını boş bıraktınız...!'
            elif request.form['mussifre'] == '':
                error = 'Müşteri şifresi alanını boş bıraktınız...!'
            elif request.form['yuzdefiyat'] == '':
                error = 'Paranızın Yüzde Kaçı Kullanılacak girmediniz...!'
            elif request.form['ensturamanlar'] == '':
                error = 'Ensturamanlar alanını boş bıraktınız...!'
            else:
                enctitle = f"{encrypt(request.form['title'], key)}"
                encmustelno = f"{encrypt(request.form['mustelno'], key)}"
                encmusno = f"{encrypt(request.form['musno'], key)}"
                encmussifre = f"{encrypt(request.form['mussifre'], key)}"
                encyuzdefiyat = f"{encrypt(request.form['yuzdefiyat'], key)}"
                encensturamanlar = f"{encrypt(request.form['ensturamanlar'], key)}"
                paclogid = backend.searc_user_packets_log_id_data(user_id)
                for row in paclogid:
                    pacid = row['pac_log_id']

                paclogid = pacid
                statu = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                backend.edit_ensturaman(enctitle, request.form['category_id'], encmustelno, encmusno, encmussifre,
                                        encyuzdefiyat, encensturamanlar, user_id, paclogid, tarih, tarih, statu, id)

                success = 'Bot Başarıyla Güncellendi..'

            return render_template('administrator/duzenleensturaman.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul, ens=dec_data)

    else:
        return redirect(url_for('home'))


@app.route('/sil/<id>')
def sil(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = backend.edit_ensturaman_checking(id)
        if ensid:

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            backend.delete_ensturaman(id)
            return redirect(url_for('ensturamans'))
    else:
        return redirect(url_for('home'))


@app.route('/aktifyap/<id>')
def aktifyap(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = backend.edit_ensturaman_checking(id)
        if ensid:
            for row in ensid:
                ustatu = row['ens_statu']
                if ustatu == 0:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    statu = 1

                    backend.ens_statu_update(statu, id)

                    success = 'Bot aktif yapılmıştır.'
                    return redirect(url_for('ensturamans', error=None, success=success))
                elif ustatu == 1:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    error = 'Bot daha önce aktif yapılmıştır...!'
                    return redirect(url_for('ensturamans', error=error, success=None))
    else:
        return redirect(url_for('home'))


@app.route('/pasifyap/<id>')
def pasifyap(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = backend.edit_ensturaman_checking(id)
        if ensid:
            for row in ensid:
                ustatu = row['ens_statu']
                if ustatu == 0:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    error = 'Bot daha önce pasif yapılmıştır...!'
                    return redirect(url_for('ensturamans', error=error, success=None))
                elif ustatu == 1:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    statu = 0

                    backend.ens_statu_update(statu, id)

                    success = 'Bot pasif yapılmıştır...!'
                    return redirect(url_for('ensturamans', error=None, success=success))
    else:
        return redirect(url_for('home'))


################################################ Admin Ensturaman Bölümü Bitiş #############################################################################

################################################ Admin Kategoriler Bölümü Başlangıç #############################################################################

@app.route('/category', methods=['GET', 'POST'])
def category():
    if 'user_id' in session:

        user_id = session['user_id']
        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        error = ''
        success = ''

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            kategori = backend.categories_data()

            return render_template('administrator/category.html', durum=durums, onlineuser=dec_datakul, cats=kategori)

        elif request.method == "POST":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            kategori = backend.categories_data()

            if request.form['katadi'] == '':
                error = 'Aranacak kategori adı girmediniz..!'
            else:
                kategori = backend.categories_search(request.form['katadi'])

                if kategori:
                    kat = request.form['katadi']
                    success = f'Aranan Kelime : {kat} Katgeori verisi sistemde mevuttur.'
                    kategori = kategori
                else:
                    kat = request.form['katadi']
                    error = f"Aranan Kelime : {kat} Kategori verisi sistemde bulunamadı...!"

            return render_template('administrator/category.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   cats=kategori)
    else:
        return redirect(url_for('home'))


@app.route('/newcat', methods=['GET', 'POST'])
def newcat():
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        error = ''
        success = ''

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('administrator/newkategori.html', durum=durums, onlineuser=dec_datakul)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if request.form['title'] == '':
                error = 'Kategori ismi girmediniz...!'
            elif hasCatTitle(request.form['title']):
                error = 'Bu isimde kategori kayıt edilmiştir...!'
            elif request.form['url'] == '':
                error = 'Kategori adres alanını boş bıraktınız...!'
            elif hasCatUrl(request.form['url']):
                error = 'Kategori adresi daha önce kayıt edilmiştir...!'
            else:

                backend.add_categories(request.form['title'], request.form['url'])

                success = 'Kategori Başarıyla Eklendi..'

        return render_template('administrator/newkategori.html', error=error, success=success, durum=durums,
                               onlineuser=dec_datakul)

    else:
        return redirect(url_for('home'))


@app.route('/catduzenle/<id>', methods=['GET', 'POST'])
def catduzenle(id):
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            cats = backend.cats(id)

            ens = backend.search_categories_and_ensturamans(id)

            dec_urls = [{'ens_statu': i['ens_statu'], 'ens_id': i['ens_id'],
                         'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                         'total_url_count': i['total_url_count']}
                        for i in ens]

            return render_template('administrator/duzenlecategory.html', durum=durums, onlineuser=dec_datakul,
                                   cats=cats,
                                   urls=dec_urls)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            cats = backend.cats(id)

            ens = backend.search_categories_and_ensturamans(id)

            dec_urls = [
                {'ens_statu': i['ens_statu'], 'ens_id': i['ens_id'],
                 'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                 'total_url_count': i['total_url_count']}
                for i in ens]

            error = ''
            success = ''

            if request.form['title'] == '':
                error = 'Link başlığı girmediniz...!'
            elif hasCatTitle(request.form['title']):
                error = 'Bu başlıkta kategori kayıt edilmiştir...!'
            elif request.form['url'] == '':
                error = 'Kategorinin Bağlantı adres alanını boş bıraktınız...!'
            elif hasCatUrl(request.form['url']):
                error = 'Kategorinin bağlantı adresi daha önce kayıt edilmiştir...!'
            else:

                backend.update_categories(request.form['title'], request.form['url'], id)

                success = 'Kategori Başarıyla Güncellendi..'

            return render_template('administrator/duzenlecategory.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul, cats=cats, urls=dec_urls)

    else:
        return redirect(url_for('home'))


@app.route('/catsil/<id>')
def catsil(id):
    if 'user_id' in session:
        user_id = session['user_id']

        katid = backend.cats(id)

        last_activity_key = f'last_activity_{user_id}'
        last_activity = session.get(last_activity_key)
        now = datetime.now(timezone.utc)
        session[last_activity_key] = now
        if last_activity:
            expiry_time = last_activity + timedelta(
                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
            if expiry_time < now:
                # Oturum süresi doldu, çıkış yapmaya yönlendir
                return redirect(url_for('logout', id=user_id))

        if katid:
            for row in katid:
                kid = row['category_id']

                ens_id = backend.ens_detail_categories(kid)
                if ens_id:
                    backend.delete_ensturaman_categories(kid)

                backend.delete_categories(id)

                return redirect(url_for('category'))
    else:
        return redirect(url_for('home'))


################################################ Admin Kategoriler Bölümü Bitiş #############################################################################

################################################ Admin Kullanıcı Ayarları Bölümü Bitiş #############################################################################

@app.route('/users', methods=['GET', 'POST'])
def users():
    success = ''
    error = ''

    if 'user_id' in session:

        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        user_details = backend.user_detail()

        dec_userdetails = [
            {'user_statu': i['user_statu'], 'user_id': i['user_id'],
             'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date'], 'user_total_count': i['user_total_count']}
            for i in user_details]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            success = request.args.get('success')
            error = request.args.get('error')
            return render_template('administrator/users.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   users=dec_userdetails)

        elif request.method == "POST":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if request.form['kuladi'] == '':
                error = 'Aranacak kullanıcı adını veya kullanıcı emaili girmediniz..!'
            else:
                kuladi = f"{backend.ucdencrypt(request.form['kuladi'], backend.key)}"

                user_details = backend.user_detail_search(kuladi)

                dec_userdetails2 = [
                    {'user_statu': i['user_statu'], 'user_id': i['user_id'],
                     'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
                     'user_create_date': i['user_create_date'],
                     'user_update_date': i['user_update_date'], 'user_total_count': i['user_total_count']}
                    for i in user_details]

                if user_details:
                    kulanici = request.form['kuladi']
                    success = f'Aranan Kelime : {kulanici} Kullanıcı verisi sistemde mevcuttur.'
                    user_details = user_details
                else:
                    kulanici = request.form['kuladi']
                    error = f"Aranan Kelime : {kulanici} Kullanıcı verisi sistemde mevcut değildir...!"

            return render_template('administrator/users.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   users=dec_userdetails2)
    else:
        return redirect(url_for('home'))


@app.route('/userduzenle/<id>', methods=['GET', 'POST'])
def userduzenle(id):
    if 'user_id' in session:

        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return redirect(url_for('home', durum=durums, onlineuser=dec_datakul))
    else:
        durums = 0
        return redirect(url_for('home'))


@app.route('/usersil/<id>', methods=['GET', 'POST'])
def usersil(id):
    if 'user_id' in session:

        user_id = session['user_id']

        last_activity_key = f'last_activity_{user_id}'
        last_activity = session.get(last_activity_key)
        now = datetime.now(timezone.utc)
        session[last_activity_key] = now
        if last_activity:
            expiry_time = last_activity + timedelta(
                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
            if expiry_time < now:
                # Oturum süresi doldu, çıkış yapmaya yönlendir
                return redirect(url_for('logout', id=user_id))

        if request.method == "GET":
            user = backend.users(id)
            if user:
                backend.delete_user(id)
                return redirect(url_for('home'))
    else:
        durums = 0
        return redirect(url_for('home'))


@app.route('/useradminyap/<id>', methods=['GET', 'POST'])
def useradminyap(id):
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == "GET":
            userid = backend.users(id)
            if userid:
                for row in userid:
                    ustatu = row['user_statu']
                    uname = f"{backend.ucddecrypt(eval(str(row['user_name'])), backend.key)}"
                    if ustatu == 1:

                        last_activity_key = f'last_activity_{user_id}'
                        last_activity = session.get(last_activity_key)
                        now = datetime.now(timezone.utc)
                        session[last_activity_key] = now
                        if last_activity:
                            expiry_time = last_activity + timedelta(
                                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                            if expiry_time < now:
                                # Oturum süresi doldu, çıkış yapmaya yönlendir
                                return redirect(url_for('logout', id=user_id))

                        error = 'Üye daha önce admin statüsüne yükseltilmiştir...!'
                        return redirect(url_for('users', error=error, success=None))
                    elif ustatu == 0:

                        last_activity_key = f'last_activity_{user_id}'
                        last_activity = session.get(last_activity_key)
                        now = datetime.now(timezone.utc)
                        session[last_activity_key] = now
                        if last_activity:
                            expiry_time = last_activity + timedelta(
                                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                            if expiry_time < now:
                                # Oturum süresi doldu, çıkış yapmaya yönlendir
                                return redirect(url_for('logout', id=user_id))

                        statu = 1
                        backend.update_statu_user(statu, id)
                        success = f'{uname} Statüsü Adminliğe Yükseltilmiştir.'
                        return redirect(url_for('users', error=None, success=success))
    else:
        durums = 0
        return redirect(url_for('home'), durum=durums)


@app.route('/useruyeyap/<id>', methods=['GET', 'POST'])
def useruyeyap(id):
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == "GET":
            userid = backend.users(id)
            if userid:
                for row in userid:
                    ustatu = row['user_statu']
                    uname = f"{backend.ucddecrypt(eval(str(row['user_name'])), backend.key)}"
                    if ustatu == 0:

                        last_activity_key = f'last_activity_{user_id}'
                        last_activity = session.get(last_activity_key)
                        now = datetime.now(timezone.utc)
                        session[last_activity_key] = now
                        if last_activity:
                            expiry_time = last_activity + timedelta(
                                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                            if expiry_time < now:
                                # Oturum süresi doldu, çıkış yapmaya yönlendir
                                return redirect(url_for('logout', id=user_id))

                        error = 'Kullanıcı daha önce Üyeliğe düşürülmüştür...!'
                        return redirect(url_for('users', error=error))
                        # return render_template('users.html', error=error,success=success, durum=durums, users=user_details)
                    elif ustatu == 1:

                        last_activity_key = f'last_activity_{user_id}'
                        last_activity = session.get(last_activity_key)
                        now = datetime.now(timezone.utc)
                        session[last_activity_key] = now
                        if last_activity:
                            expiry_time = last_activity + timedelta(
                                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                            if expiry_time < now:
                                # Oturum süresi doldu, çıkış yapmaya yönlendir
                                return redirect(url_for('logout', id=user_id))

                        statu = 0
                        backend.update_statu_user(statu, id)
                        error = None
                        success = f'{uname} Statüsü Üyeliğe Düşürülmüştür.'
                        return redirect(url_for('users', success=success))
                        # return render_template('users.html', error=error,success=success, durum=durums, users=user_details)
    else:
        durums = 3
        return redirect(url_for('home'), durum=durums)


################################################ Admin Kullanıcı Ayarları Bölümü Bitiş #############################################################################

################################################ Admin Packets Bölümü Başlangıç #############################################################################

@app.route('/packets', methods=['GET', 'POST'])
def packets():
    if 'user_id' in session:
        user_id = session['user_id']
        success = request.args.get('success')
        error = request.args.get('error')

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        pac_details = backend.pac_detail()

        dec_data = [{'pac_statu': i['pac_statu'], 'pac_id': i['pac_id'],
                     'pac_title': backend.decrypt(eval(str(i['pac_title'])), backend.key)} for
                    i in pac_details]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('administrator/paketler.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   pakets=dec_data)

        if request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if request.form['paketname'] == '':
                error = "Aranacak Bot İsmi veya Kategori ID'sini veya Müşteri Numara'sı yazmadınız...!"
            else:

                kelime = f"{backend.encrypt(request.form['paketname'], backend.key)}"
                pac_details = backend.pac_detail_search(kelime)

                dec_data2 = [{'pac_statu': i['pac_statu'], 'pac_id': i['pac_id'],
                              'pac_title': backend.decrypt(eval(str(i['pac_title'])), backend.key)} for
                             i in pac_details]

                if pac_details:
                    pac = request.form['paketname']
                    pac_details = pac_details
                    success = f'Aranan Kelime : {pac} Eş değer sonuçlar bulunmuştur. '
                else:
                    pac = request.form['paketname']
                    error = f'Aranan Kelime {pac} Eş değer veri sistemde mevcut değildir...!'
            return render_template('administrator/paketler.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   pakets=dec_data2)
    else:
        durums = 3
        return redirect(url_for('home'))


@app.route('/newpackets', methods=['GET', 'POST'])
def newpackets():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        error = ''
        success = ''

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('administrator/newpaket.html', durum=durums, onlineuser=dec_datakul)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if request.files['image'] == '':
                error = 'Resim Seçmediniz...!'
            elif request.form['title'] == '':
                error = 'Paket başlığı girmediniz...!'
            elif request.form['description'] == '':
                error = 'Açıklama girmediniz...!'
            elif request.form['price'] == '':
                error = 'Fiyat girmediniz...!'
            else:

                file = request.files['image']
                file.save('static/uploads/' + file.filename)

                gelen_veri = request.form['description']
                cumleler = gelen_veri.split(' ')
                ilk_yirmi_cumle = ' '.join(cumleler[:15])
                ilk_yirmi_cumle = f"{ilk_yirmi_cumle}..."

                encimg = f"{backend.encrypt(file.filename, backend.key)}"
                enctitle = f"{backend.encrypt(request.form['title'], backend.key)}"
                encdescription = f"{backend.encrypt(request.form['description'], backend.key)}"
                encdescription2 = f"{backend.encrypt(ilk_yirmi_cumle, backend.key)}"
                encprice = f"{backend.encrypt(request.form['price'], backend.key)}"

                statu = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"
                backend.add_packets(statu, encimg, enctitle, encdescription, encdescription2, encprice, tarih, tarih)
                success = 'Paket Başarıyla Eklendi..'

        return render_template('administrator/newpaket.html', error=error, success=success, durum=durums,
                               onlineuser=dec_datakul)

    else:
        return redirect(url_for('home'))


@app.route('/editpackets/<id>', methods=['GET', 'POST'])
def editpackets(id):
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            pac = backend.edit_packets_checking(id)

            dec_data = [{'pac_id': i['pac_id'], 'pac_statu': i['pac_statu'],
                         'pac_img': backend.decrypt(eval(str(i['pac_img'])), backend.key),
                         'pac_title': backend.decrypt(eval(str(i['pac_title'])), backend.key),
                         'pac_content': backend.decrypt(eval(str(i['pac_content'])), backend.key),
                         'pac_fiyat': backend.decrypt(eval(str(i['pac_fiyat'])), backend.key),
                         'pac_create_date': i['pac_create_date'], 'pac_update_date': i['pac_update_date']}
                        for i in pac]

            return render_template('administrator/duzenlepaket.html', durum=durums, onlineuser=dec_datakul,
                                   paketler=dec_data)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            pac = backend.edit_packets_checking(id)

            dec_data = [{'pac_id': i['pac_id'], 'pac_statu': i['pac_statu'],
                         'pac_img': backend.decrypt(eval(str(i['pac_img'])), backend.key),
                         'pac_title': backend.decrypt(eval(str(i['pac_title'])), backend.key),
                         'pac_content': backend.decrypt(eval(str(i['pac_content'])), backend.key),
                         'pac_fiyat': backend.decrypt(eval(str(i['pac_fiyat'])), backend.key),
                         'pac_create_date': i['pac_create_date'], 'pac_update_date': i['pac_update_date']}
                        for i in pac]

            error = ''
            success = ''

            if request.files['image'] == '':
                error = 'Resim Seçmediniz...!'
            elif request.form['title'] == '':
                error = 'Paket başlığı girmediniz...!'
            elif request.form['description'] == '':
                error = 'Açıklama girmediniz...!'
            elif request.form['price'] == '':
                error = 'Fiyat girmediniz...!'
            else:

                affterImgName = f"{dec_data[0]['pac_img']}"

                file_path = os.path.join('static/uploads', affterImgName)
                if os.path.exists(file_path):
                    os.remove(file_path)

                file = request.files['image']
                file.save('static/uploads/' + file.filename)

                gelen_veri = request.form['description']
                cumleler = gelen_veri.split(' ')
                ilk_yirmi_cumle = ' '.join(cumleler[:15])
                ilk_yirmi_cumle = f"{ilk_yirmi_cumle}..."

                encimg = f"{backend.encrypt(file.filename, backend.key)}"
                enctitle = f"{backend.encrypt(request.form['title'], backend.key)}"
                encdescription = f"{backend.encrypt(request.form['description'], backend.key)}"
                encdescription2 = f"{backend.encrypt(ilk_yirmi_cumle, backend.key)}"
                encprice = f"{backend.encrypt(request.form['price'], backend.key)}"

                statu = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                backend.edit_packets(statu, encimg, enctitle, encdescription, encdescription2, encprice, tarih, tarih, id)

                success = 'Paket Başarıyla Güncellendi..'

            return render_template('administrator/duzenlepaket.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul, paketler=dec_data)

    else:
        return redirect(url_for('home'))


@app.route('/deletepackets/<id>')
def deletepackets(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = backend.edit_packets_checking(id)
        if ensid:

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            backend.delete_packets(id)
            return redirect(url_for('packets'))
    else:
        return redirect(url_for('home'))


@app.route('/aktifyappackets/<id>')
def aktifyappackets(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = backend.edit_packets_checking(id)
        if ensid:
            for row in ensid:
                ustatu = row['pac_statu']
                if ustatu == 0:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    statu = 1

                    backend.pac_statu_update(statu, id)

                    success = 'Paket aktif yapılmıştır.'
                    return redirect(url_for('packets', error=None, success=success))
                elif ustatu == 1:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    error = 'Paket daha önce aktif yapılmıştır...!'
                    return redirect(url_for('packets', error=error, success=None))
    else:
        return redirect(url_for('home'))


@app.route('/pasifyappackets/<id>')
def pasifyappackets(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = backend.edit_packets_checking(id)
        if ensid:
            for row in ensid:
                ustatu = row['pac_statu']
                if ustatu == 0:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    error = 'Paket daha önce pasif yapılmıştır...!'
                    return redirect(url_for('packets', error=error, success=None))
                elif ustatu == 1:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    statu = 0

                    backend.ens_statu_update(statu, id)

                    success = 'Paket pasif yapılmıştır...!'
                    return redirect(url_for('packets', error=None, success=success))
    else:
        return redirect(url_for('home'))


################################################ Admin Packets Bölümü Bitiş #############################################################################

################################################ User Packets Bölümü Başlangıç #############################################################################
@app.route('/userpackets', methods=['GET', 'POST'])
def userpackets():
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        pac_details = backend.pac_details()

        dec_data = [{'pac_id': i['pac_id'], 'pac_statu': i['pac_statu'],
                     'pac_img': backend.decrypt(eval(str(i['pac_img'])), backend.key),
                     'pac_title': backend.decrypt(eval(str(i['pac_title'])), backend.key),
                     'pac_content': backend.decrypt(eval(str(i['pac_content'])), backend.key),
                     'pac_contentiki': backend.decrypt(eval(str(i['pac_contentiki'])), backend.key),
                     'pac_fiyat': backend.decrypt(eval(str(i['pac_fiyat'])), backend.key),
                     'pac_create_date': i['pac_create_date'], 'pac_update_date': i['pac_update_date']} for
                    i in pac_details]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/paketler.html', durum=durums,
                                   onlineuser=dec_datakul,
                                   pakets=dec_data)

        if request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/paketler.html', durum=durums,
                                   onlineuser=dec_datakul,
                                   pakets=dec_data)
    else:
        durums = 3
        return redirect(url_for('home'))


@app.route('/userpacketsdetay/<id>', methods=['GET', 'POST'])
def userpacketsdetay(id):
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        pac_details = backend.pac_detailstwo(id)

        dec_data = [{'pac_id': i['pac_id'], 'pac_statu': i['pac_statu'],
                     'pac_img': backend.decrypt(eval(str(i['pac_img'])), backend.key),
                     'pac_title': backend.decrypt(eval(str(i['pac_title'])), backend.key),
                     'pac_content': backend.decrypt(eval(str(i['pac_content'])), backend.key),
                     'pac_contentiki': backend.decrypt(eval(str(i['pac_contentiki'])), backend.key),
                     'pac_fiyat': backend.decrypt(eval(str(i['pac_fiyat'])), backend.key),
                     'pac_create_date': i['pac_create_date'], 'pac_update_date': i['pac_update_date']} for
                    i in pac_details]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/paketler.html', durum=durums,
                                   onlineuser=dec_datakul,
                                   paketss=dec_data, pakets=None)

        if request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/paketler.html', durum=durums,
                                   onlineuser=dec_datakul,
                                   paketss=dec_data, pakets=None)
    else:
        durums = 3
        return redirect(url_for('home'))

################################################ User Packets Bölümü Bitiş #############################################################################


################################################ User Ensturamanlar Bölümü Başlangıç#############################################################################

@app.route('/userensturamans', methods=['GET', 'POST'])
def userensturamans():
    if 'user_id' in session:

        success = request.args.get('success')
        error = request.args.get('error')

        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        ens_details = backend.ens_detail_user(user_id)

        dec_data = [{'ens_statu': i['ens_statu'], 'ens_id': i['ens_id'],
                     'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key)} for
                    i in ens_details]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/ensturamans.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   urls=dec_data)

        if request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if request.form['urlname'] == '':
                error = "Aranacak Bot İsmi veya Kategori ID'sini veya Müşteri Numarası yazmadınız...!"
            else:

                kelime = f"{backend.encrypt(request.form['urlname'], backend.key)}"

                ens_details = backend.ens_detail_user_search(kelime, user_id)

                dec_data2 = [{'ens_statu': i['ens_statu'], 'ens_id': i['ens_id'],
                              'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key)} for
                             i in ens_details]

                if ens_details:
                    urls = request.form['urlname']
                    ens_details = ens_details
                    success = f'Aranan Kelime : {urls} Eş değer sonuçlar bulunmuştur. '
                else:
                    urls = request.form['urlname']
                    error = f'Aranan Kelime {urls} Eş değer veri sistemde mevcut değildir...!'
            return render_template('views/ensturamans.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul,
                                   urls=dec_data2)
    else:
        durums = 3
        return redirect(url_for('home'))


@app.route('/userensnewensturamans', methods=['GET', 'POST'])
def userensnewensturamans():
    if 'user_id' in session:
        user_id = session['user_id']

        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        error = ''
        success = ''

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            return render_template('views/newensturamans.html', durum=durums, onlineuser=dec_datakul)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            if (backend.searc_user_packets_log(user_id) == False):
                error = 'Satın Alınmış Paketiniz Bulunmadığı için bot ekleyemezsiniz...!'
            elif request.form['title'] == '':
                error = 'Bot başlığı girmediniz...!'
            elif hasTitle(request.form['title']):
                error = 'Bu başlıkta Bot kayıt edilmiştir...!'
            elif request.form['category_id'] == '':
                error = 'Katgeori Seçmediniz...!'
            elif request.form['mustelno'] == '':
                error = 'Müşteri telefon numarası alanını boş bıraktınız...!'
            elif (tel_no_check(request.form['mustelno']) == False):
                error = 'Geçerli telefon numarası giriniz...!'
            elif request.form['musno'] == '':
                error = 'Müşteri numarası alanını boş bıraktınız...!'
            elif request.form['mussifre'] == '':
                error = 'Müşteri şifresi alanını boş bıraktınız...!'
            elif request.form['yuzdefiyat'] == '':
                error = 'Paranızın Yüzde Kaçı Kullanılacak girmediniz...!'
            elif request.form['ensturamanlar'] == '':
                error = 'Ensturamanlar alanını boş bıraktınız...!'
            else:
                enctitle = f"{backend.encrypt(request.form['title'], backend.key)}"
                encmustelno = f"{backend.encrypt(request.form['mustelno'], backend.key)}"
                encmusno = f"{backend.encrypt(request.form['musno'], backend.key)}"
                encmussifre = f"{backend.encrypt(request.form['mussifre'], backend.key)}"
                encyuzdefiyat = f"{backend.encrypt(request.form['yuzdefiyat'], backend.key)}"
                encensturamanlar = f"{backend.encrypt(request.form['ensturamanlar'], backend.key)}"
                paclogid = backend.searc_user_packets_log_id_data(user_id)
                for row in paclogid:
                    pacid = row['pac_log_id']

                paclogid = int(pacid)
                statu = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                backend.add_ensturaman(enctitle, request.form['category_id'], encmustelno, encmusno, encmussifre,
                                       encyuzdefiyat, encensturamanlar, user_id, paclogid, tarih, tarih, statu)

                success = 'Bot Başarıyla Eklendi..'

        return render_template('views/newensturamans.html', error=error, success=success, durum=durums,
                               onlineuser=dec_datakul)

    else:
        return redirect(url_for('home'))


@app.route('/userensduzenle/<id>', methods=['GET', 'POST'])
def userensduzenle(id):
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user_durum(user_id)

        onlinekul = backend.online_users()

        dec_datakul = [
            {'user_id': i['user_id'], 'user_name': backend.ucddecrypt(eval(str(i['user_name'])), backend.key),
             'user_email': backend.ucddecrypt(eval(str(i['user_email'])), backend.key),
             'user_password': backend.ucddecrypt(eval(str(i['user_password'])), backend.key),
             'user_statu': i['user_statu'], 'user_giris': i['user_giris'],
             'user_ip_adress': i['user_ip_adress'], 'user_create_date': i['user_create_date'],
             'user_update_date': i['user_update_date']}
            for i in onlinekul]

        if request.method == "GET":

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            ens = backend.edit_ensturaman_checking_user(id, user_id)
            dec_data = [{'ens_id': i['ens_id'], 'ens_statu': i['ens_statu'],
                         'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                         'ens_category': i['ens_category'],
                         'ens_mustelno': backend.decrypt(eval(str(i['ens_mustelno'])), backend.key),
                         'ens_musno': backend.decrypt(eval(str(i['ens_musno'])), backend.key),
                         'ens_mussifre': backend.decrypt(eval(str(i['ens_mussifre'])), backend.key),
                         'ens_yuzdefiyat': backend.decrypt(eval(str(i['ens_yuzdefiyat'])), backend.key),
                         'ens_ensturamanlar': backend.decrypt(eval(str(i['ens_ensturamanlar'])), backend.key),
                         'ens_user': i['ens_user'],
                         'ens_create_date': i['ens_create_date'], 'ens_update_date': i['ens_update_date']}
                        for i in ens]

            return render_template('views/duzenleensturaman.html', durum=durums, onlineuser=dec_datakul,
                                   ens=dec_data)

        elif request.method == 'POST':

            last_activity_key = f'last_activity_{user_id}'
            last_activity = session.get(last_activity_key)
            now = datetime.now(timezone.utc)
            session[last_activity_key] = now
            if last_activity:
                expiry_time = last_activity + timedelta(
                    minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                if expiry_time < now:
                    # Oturum süresi doldu, çıkış yapmaya yönlendir
                    return redirect(url_for('logout', id=user_id))

            ens = backend.edit_ensturaman_checking_user(id, user_id)

            dec_data = [{'ens_id': i['ens_id'], 'ens_statu': i['ens_statu'],
                         'ens_title': backend.decrypt(eval(str(i['ens_title'])), backend.key),
                         'ens_category': i['ens_category'],
                         'ens_mustelno': backend.decrypt(eval(str(i['ens_mustelno'])), backend.key),
                         'ens_musno': backend.decrypt(eval(str(i['ens_musno'])), backend.key),
                         'ens_mussifre': backend.decrypt(eval(str(i['ens_mussifre'])), backend.key),
                         'ens_yuzdefiyat': backend.decrypt(eval(str(i['ens_yuzdefiyat'])), backend.key),
                         'ens_ensturamanlar': backend.decrypt(eval(str(i['ens_ensturamanlar'])), backend.key),
                         'ens_user': i['ens_user'],
                         'ens_create_date': i['ens_create_date'], 'ens_update_date': i['ens_update_date']}
                        for i in ens]

            error = ''
            success = ''

            if (backend.searc_user_packets_log(user_id) == False):
                error = 'Satın Alınmış Paketiniz Bulunmadığı için bot ekleyemezsiniz veya düzenleyemezsiniz...!'

            elif request.form['title'] == '':
                error = 'Bot başlığı girmediniz...!'
            elif hasTitle(request.form['title']):
                error = 'Bu başlıkta Bot kayıt edilmiştir...!'
            elif request.form['category_id'] == '':
                error = 'Katgeori Seçmediniz...!'
            elif request.form['mustelno'] == '':
                error = 'Müşteri telefon numarası alanını boş bıraktınız...!'
            elif (tel_no_check(request.form['mustelno']) == False):
                error = 'Geçerli telefon numarası giriniz...!'
            elif request.form['musno'] == '':
                error = 'Müşteri numarası alanını boş bıraktınız...!'
            elif request.form['mussifre'] == '':
                error = 'Müşteri şifresi alanını boş bıraktınız...!'
            elif request.form['yuzdefiyat'] == '':
                error = 'Paranızın Yüzde Kaçı Kullanılacak girmediniz...!'
            elif request.form['ensturamanlar'] == '':
                error = 'Ensturamanlar alanını boş bıraktınız...!'
            else:
                enctitle = f"{encrypt(request.form['title'], key)}"
                encmustelno = f"{encrypt(request.form['mustelno'], key)}"
                encmusno = f"{encrypt(request.form['musno'], key)}"
                encmussifre = f"{encrypt(request.form['mussifre'], key)}"
                encyuzdefiyat = f"{encrypt(request.form['yuzdefiyat'], key)}"
                encensturamanlar = f"{encrypt(request.form['ensturamanlar'], key)}"
                paclogid = backend.searc_user_packets_log_id_data(user_id)
                for row in paclogid:
                    pacid = row['pac_log_id']

                paclogid = int(pacid)

                statu = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                backend.edit_ensturaman_user(enctitle, request.form['category_id'], encmustelno, encmusno, encmussifre,
                                             encyuzdefiyat, encensturamanlar, user_id, paclogid, tarih, tarih, statu, user_id,
                                             id, )
                success = 'Bot Adresi Başarıyla Güncellendi..'

            return render_template('views/duzenleensturaman.html', error=error, success=success, durum=durums,
                                   onlineuser=dec_datakul, ens=dec_data)

    else:
        return redirect(url_for('home'))


@app.route('/userenssil/<id>')
def userenssil(id):
    ensid = backend.edit_ensturaman_checking(id)
    if ensid:

        backend.delete_ensturaman(id)

        return redirect(url_for('userensturamans'))
    else:
        return redirect(url_for('home'))


@app.route('/userensaktifyap/<id>')
def userensaktifyap(id):
    if 'user_id' in session:
        user_id = session['user_id']
        ensid = edit_ensturaman_checking_user(id, user_id)
        if ensid:
            for row in ensid:
                ustatu = row['ens_statu']
                if ustatu == 0:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    statu = 1

                    backend.ens_statu_update(statu, id)

                    success = 'Bot aktif yapılmıştır.'
                    return redirect(url_for('userensturamans', error=None, success=success))
                elif ustatu == 1:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    error = 'Bot daha önce aktif yapılmıştır...!'
                    return redirect(url_for('userensturamans', error=error, success=None))
    else:
        return redirect(url_for('home'))


@app.route('/userenspasifyap/<id>')
def userenspasifyap(id):
    if 'user_id' in session:

        user_id = session['user_id']
        ensid = backend.edit_ensturaman_checking_user(id, user_id)
        if ensid:
            for row in ensid:
                ustatu = row['ens_statu']
                if ustatu == 0:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    error = 'Bot daha önce pasif yapılmıştır...!'
                    return redirect(url_for('userensturamans', error=error, success=None))
                elif ustatu == 1:

                    last_activity_key = f'last_activity_{user_id}'
                    last_activity = session.get(last_activity_key)
                    now = datetime.now(timezone.utc)
                    session[last_activity_key] = now
                    if last_activity:
                        expiry_time = last_activity + timedelta(
                            minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
                        if expiry_time < now:
                            # Oturum süresi doldu, çıkış yapmaya yönlendir
                            return redirect(url_for('logout', id=user_id))

                    statu = 0

                    backend.ens_statu_update(statu, id)

                    success = 'Bot pasif yapılmıştır...!'
                    return redirect(url_for('userensturamans', error=None, success=success))
    else:
        return redirect(url_for('home'))

################################################ User Ensturaman Bölümü Bitiş #############################################################################

################################################ Hatalı Sayfa Başlangıç #############################################################################

@app.errorhandler(404)
def page_not_found(error):
    if 'user_id' in session:
        user_id = session['user_id']

        last_activity_key = f'last_activity_{user_id}'
        last_activity = session.get(last_activity_key)
        now = datetime.now(timezone.utc)
        session[last_activity_key] = now
        if last_activity:
            expiry_time = last_activity + timedelta(
                minutes=app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() // 60)
            if expiry_time < now:
                # Oturum süresi doldu, çıkış yapmaya yönlendir
                return redirect(url_for('logout', id=user_id))

        durums = backend.user_durum(user_id)
        return render_template('not-found.html', durum=durums), 404
    else:
        durums = 0
        return render_template('not-found.html', durum=durums), 404


################################################ Hatalı Sayfa Bitiş #############################################################################

########################### ROBOTS TEXT #################################
@app.route('/robots.txt')
def robots():
    r = Response(response="""# robots.txt İHS Telekom tarafından oluşturuldu\n
User-agent: Googlebot\n
Disallow: /adminpanel\n
User-agent: googlebot-image\n
Disallow: /adminpanel\n
User-agent: googlebot-mobile\n
Disallow: /adminpanel\n
User-agent: Slurp\n
Disallow: /adminpanel\n
User-agent: Teoma\n
Disallow: /adminpanel\n
User-agent: yahoo-mmcrawler\n
Disallow: /adminpanel\n
User-agent: *\n
Disallow: /adminpanel\n
Crawl-delay: 120\n
Disallow: /adminpanel\n
Sitemap: http://78.186.138.86/sitemap.xml\n
""", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

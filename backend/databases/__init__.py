import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="barron4335",
    password="1968Hram",
    database="alsatbot"
)

cursor = db.cursor(dictionary=True)


def login(email, user, ceptelno, password):
    sql = "SELECT * FROM users WHERE (user_email = %s AND user_password = %s) OR (user_name = %s AND user_password = %s) OR (user_cep_tel_no = %s AND user_password = %s)"
    cursor.execute(sql, (email, password, user, password, ceptelno, password))
    user = cursor.fetchone()
    return user


def login_update(tarih, sayi, host, user):
    sql = "UPDATE users SET user_update_date = %s,  user_giris = %s, user_ip_adress=%sWHERE user_id = %s"
    cursor.execute(sql, (tarih, sayi, host, user,))
    db.commit()


def event_start(eventname, user):
    sql = f"CREATE EVENT `{eventname}`ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 15 MINUTE ON COMPLETION NOT PRESERVE DO UPDATE `users`SET `user_giris` = 0 WHERE `user_id` = %s;"
    cursor.execute(sql, (user,))
    db.commit()


def register_insert(user, firstname, lastname, telno, email, password, statu, giris, host, tarih, tarih2):
    sql = "INSERT INTO users SET user_name = %s, user_firstname = %s, user_lastname = %s, user_cep_tel_no = %s, user_email = %s, user_password = %s, user_statu = %s, user_giris = %s, user_ip_adress = %s, user_create_date = %s, user_update_date = %s"
    cursor.execute(sql, (user, firstname, lastname, telno, email, password, statu, giris, host, tarih, tarih2))
    db.commit()


def logout_update(sayi, user):
    sql = "UPDATE users SET user_giris = %s WHERE user_id = %s"
    cursor.execute(sql, (sayi, user,))
    db.commit()


def event_update(eventname):
    sql = f"DROP EVENT IF EXISTS `{eventname}`;"
    cursor.execute(sql)
    db.commit()


def user_durum(user):
    sql = "SELECT user_statu FROM users WHERE user_id = %s"
    cursor.execute(sql, (user,))
    durums = cursor.fetchone()
    return durums


def users(user):
    sql = "SELECT * FROM users WHERE user_id= %s"
    cursor.execute(sql, (user,))
    kul = cursor.fetchall()
    return kul


def delete_user(user):
    sql = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(sql, (user,))
    db.commit()


def update_statu_user(statu, user):
    sql = "UPDATE users SET user_statu = %s WHERE user_id = %s"
    cursor.execute(sql, (statu, user,))
    db.commit()


def online_users():
    cursor.execute("SELECT * FROM users WHERE user_giris = 1")
    onlinekul = cursor.fetchall()
    return onlinekul


def user_detail():
    sql = "SELECT users.user_statu, users.user_id, users.user_name, users.user_create_date, users.user_update_date, (SELECT COUNT(*) FROM users) AS user_total_count FROM users"
    cursor.execute(sql, )
    user_details = cursor.fetchall()
    return user_details


def user_detail_search(kuladi):
    sql = "SELECT users.user_statu, users.user_id, users.user_name, users.user_create_date, users.user_update_date, (SELECT COUNT(*) FROM users) AS user_total_count FROM users WHERE user_name = %s or user_email = %s"
    cursor.execute(sql, (kuladi, kuladi,))
    user_details = cursor.fetchall()
    return user_details


def ens_detail():
    sql = "SELECT urls.ens_statu, urls.ens_id, urls.ens_title, users.user_name FROM urls LEFT JOIN users ON urls.ens_user = users.user_id;"
    cursor.execute(sql, )
    ens_details = cursor.fetchall()
    return ens_details


def pac_detail():
    sql = "SELECT packets.pac_statu, packets.pac_id, packets.pac_title FROM packets"
    cursor.execute(sql, )
    pac_details = cursor.fetchall()
    return pac_details


def pac_details():
    sql = "SELECT * FROM packets"
    cursor.execute(sql, )
    pacs = cursor.fetchall()
    return pacs


def pac_detailstwo(pac_id):
    sql = "SELECT * FROM packets WHERE pac_id = %s"
    cursor.execute(sql, (pac_id,))
    pacs = cursor.fetchall()
    return pacs


def ens_detail_user(user):
    sql = "SELECT urls.ens_statu, urls.ens_id, urls.ens_title FROM urls WHERE ens_user = %s"
    cursor.execute(sql, (user,))
    ens_details = cursor.fetchall()
    return ens_details


def ens_detail_categories(catid):
    sql = "SELECT * FROM urls WHERE ens_category = %s"
    cursor.execute(sql, (catid,))
    ensid = cursor.fetchall()
    return ensid


def ens_detail_search(kelime):
    sql = "SELECT urls.ens_statu, urls.ens_id, urls.ens_title, users.user_name FROM urls JOIN users ON urls.ens_user = users.user_id WHERE ens_category = %s OR ens_title = %s OR ens_musno = %s"
    cursor.execute(sql, (kelime, kelime, kelime))
    ens_details = cursor.fetchall()
    return ens_details


def pac_detail_search(kelime):
    sql = "SELECT packets.pac_statu, packets.pac_id, packets.pac_title FROM packets WHERE pac_title = %s"
    cursor.execute(sql, (kelime,))
    pac_details = cursor.fetchall()
    return pac_details


def ens_detail_user_search(kelime, user):
    sql = "SELECT urls.ens_statu, urls.ens_id, urls.ens_title FROM urls WHERE (ens_category = %s AND ens_user = %s) OR  (ens_title = %s AND ens_user = %s) or (ens_musno = %s AND ens_user = %s)"
    cursor.execute(sql, (kelime, user, kelime, user, kelime, user))
    ens_details = cursor.fetchall()
    return ens_details


def searc_user_packets_log(user):
    sql = "SELECT * FROM pac_log WHERE pac_log_user_id = %s"
    cursor.execute(sql, (user,))
    pac_log_search = cursor.fetchall()
    if pac_log_search:
        return True
    else:
        return False


def searc_user_packets_log_id_data(user):
    sql = "SELECT * FROM pac_log WHERE pac_log_user_id = %s"
    cursor.execute(sql, (user,))
    pac_log_search = cursor.fetchall()
    return pac_log_search


def add_ensturaman(title, category, mustelno, musno, mussifre, yuzdefiyat, ensturamanlar, user, paclogid, tarih, tarih2,
                   statu):
    sql = "INSERT INTO urls SET ens_title = %s,ens_category = %s, ens_mustelno = %s, ens_musno = %s, ens_mussifre = %s, ens_yuzdefiyat = %s, ens_ensturamanlar = %s, ens_user = %s, pac_logs_id = %s, ens_create_date = %s, ens_update_date = %s, ens_statu = %s"
    cursor.execute(sql, (title, category, mustelno, musno, mussifre,
                         yuzdefiyat, ensturamanlar, user, paclogid, tarih, tarih2, statu))
    db.commit()


def add_packets(statu, img, title, description, description2, price, tarih, tarih2):
    sql = "INSERT INTO packets SET pac_statu = %s,pac_img = %s, pac_title = %s, pac_content = %s, pac_contentiki = %s, pac_fiyat = %s, pac_create_date = %s, pac_update_date = %s"
    cursor.execute(sql, (statu, img, title, description, description2, price, tarih, tarih2,))
    db.commit()


def edit_ensturaman_checking(ens_id):
    sql = "SELECT * FROM urls WHERE ens_id = %s"
    cursor.execute(sql, (ens_id,))
    ens = cursor.fetchall()
    return ens


def edit_packets_checking(pac_id):
    sql = "SELECT * FROM packets WHERE pac_id = %s"
    cursor.execute(sql, (pac_id,))
    ens = cursor.fetchall()
    return ens


def edit_packets_checking(pac_id):
    sql = "SELECT * FROM packets WHERE pac_id = %s"
    cursor.execute(sql, (pac_id,))
    pacs = cursor.fetchall()
    return pacs


def edit_ensturaman_checking_user(ens_id, user_id):
    sql = "SELECT * FROM urls WHERE ens_id = %s AND ens_user = %s"
    cursor.execute(sql, (ens_id, user_id,))
    ens = cursor.fetchall()
    return ens


def edit_ensturaman(title, category, mustelno, musno, mussifre, yuzdefiyat, ensturamanlar, user, paclogid, tarih, tarih2, statu,
                    ensid):
    sql = "UPDATE urls SET ens_title = %s,ens_category = %s,ens_mustelno = %s, ens_musno = %s, ens_mussifre = %s, ens_yuzdefiyat = %s, ens_ensturamanlar = %s, ens_user = %s, pac_logs_id = %s, ens_create_date = %s, ens_update_date = %s, ens_statu = %s WHERE ens_id = %s"
    cursor.execute(sql, (
        title, category, mustelno, musno, mussifre, yuzdefiyat, ensturamanlar, user, paclogid, tarih, tarih2, statu, ensid,))
    db.commit()


def edit_packets(statu, img, title, content, convert2, fiyat, tarih, tarih2, patid):
    sql = "UPDATE packets SET pac_statu = %s, pac_img = %s, pac_title = %s, pac_content = %s, pac_contentiki = %s, pac_fiyat = %s, pac_create_date = %s, pac_update_date = %s WHERE pac_id = %s"
    cursor.execute(sql, (statu, img, title, content, convert2, fiyat, tarih, tarih2, patid))
    db.commit()


def edit_ensturaman_user(title, category, mustelno, musno, mussifre, yuzdefiyat, ensturamanlar, user, paclogid, tarih,
                         tarih2,
                         statu, user2, ensid):
    sql = "UPDATE urls SET ens_title = %s,ens_category = %s,ens_mustelno = %s, ens_musno = %s, ens_mussifre = %s, ens_yuzdefiyat = %s, ens_ensturamanlar = %s, ens_user = %s, pac_logs_id = %s, ens_create_date = %s, ens_update_date = %s, ens_statu = %s WHERE ens_user = %s AND ens_id = %s"
    cursor.execute(sql, (
        title, category, mustelno, musno, mussifre, yuzdefiyat, ensturamanlar, user, paclogid, tarih, tarih2, statu,
        user2,
        ensid,))
    db.commit()


def delete_ensturaman(ensid):
    sql = "DELETE FROM urls WHERE ens_id = %s"
    cursor.execute(sql, (ensid,))
    db.commit()


def delete_packets(pacid):
    sql = "DELETE FROM packets WHERE pac_id = %s"
    cursor.execute(sql, (pacid,))
    db.commit()


def delete_ensturaman_categories(catid):
    sql = "DELETE FROM urls WHERE ens_category = %s"
    cursor.execute(sql, (catid,))
    db.commit()


def ens_statu_update(statu, ensid):
    sql = "UPDATE urls SET ens_statu = %s WHERE ens_id = %s"
    cursor.execute(sql, (statu, ensid,))
    db.commit()


def pac_statu_update(statu, pacid):
    sql = "UPDATE packets SET pac_statu = %s WHERE pac_id = %s"
    cursor.execute(sql, (statu, pacid,))
    db.commit()


def categories_data():
    sql = "SELECT categories.category_id, categories.category_name, categories.category_url, SUM(CASE WHEN urls.ens_statu = 0 THEN 1 ELSE 0 END) as total_status_0_count, SUM(CASE WHEN urls.ens_statu = 1 THEN 1 ELSE 0 END) as total_status_1_count FROM categories LEFT JOIN urls ON categories.category_id = urls.ens_category GROUP BY categories.category_id, categories.category_url, categories.category_name"
    cursor.execute(sql)
    kategori = cursor.fetchall()
    return kategori


def categories_search(katadi):
    sql = "SELECT categories.category_id, categories.category_name, categories.category_url, SUM(CASE WHEN urls.ens_statu = 0 THEN 1 ELSE 0 END) as total_status_0_count, SUM(CASE WHEN urls.ens_statu = 1 THEN 1 ELSE 0 END) as total_status_1_count FROM categories LEFT JOIN urls ON categories.category_id = urls.ens_category WHERE categories.category_name = %s GROUP BY categories.category_id, categories.category_url, categories.category_name"
    cursor.execute(sql, (katadi,))
    kategori = cursor.fetchall()
    return kategori


def add_categories(title, url):
    sql = "INSERT INTO categories SET category_name = %s, category_url = %s"
    cursor.execute(sql, (title, url,))
    db.commit()


def delete_categories(catid):
    sql = "DELETE FROM categories WHERE category_id = %s"
    cursor.execute(sql, (catid,))
    db.commit()


def update_categories(title, url, catid):
    sql = "UPDATE categories SET category_name = %s, category_url = %s WHERE category_id = %s"
    cursor.execute(sql, (title, url, catid,))
    db.commit()


def cats(catid):
    sql = "SELECT * FROM categories WHERE category_id = %s"
    cursor.execute(sql, (catid,))
    cat = cursor.fetchall()
    return cat


def search_categories_and_ensturamans(catid):
    sql = "SELECT urls.ens_statu, urls.ens_id, urls.ens_title, (SELECT COUNT(*) FROM urls WHERE ens_category = %s) AS total_url_count FROM urls WHERE urls.ens_category = %s"
    cursor.execute(sql, (catid, catid,))
    catens = cursor.fetchall()
    return catens

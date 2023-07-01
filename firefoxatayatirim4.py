# !/usr/bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from threading import Thread

# Application Class

global mesaj
mesaj = ''


class WhatsappApplications():
    def __init__(self):
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['binary'] = '/usr/bin/firefox'
        self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
        self.driver.get("https://web.whatsapp.com/send/?phone=905333904681&text&type=phone_number&app_absent=0%2F")

        time.sleep(35)
        while True:
            try:
                gelenmesaj = self.driver.find_element(By.CSS_SELECTOR,
                                                      '#main > div._3B19s > div > div._5kRIK > div.n5hs2j7m.oq31bsqd.gx1rr48f.qh5tioqs > div:nth-child(3) > div > div > div > div._1BOF7._2AOIt > div.cm280p3y.to2l77zo.n1yiu2zv.c6f98ldp.ooty25bp.oq31bsqd > div.copyable-text > div > span._11JPr.selectable-text.copyable-text > span').text
                global mesaj
                mesaj = gelenmesaj
            except Exception as e:
                pass


global hisseList
hisseList = []


class Applications():
    def __init__(self):
        try:

            self.musno = '119396'
            self.sifre = '1968'
            self.nakit = ''

            firefox_capabilities = DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True
            firefox_capabilities['binary'] = '/usr/bin/firefox'
            self.driver = webdriver.Firefox(capabilities=firefox_capabilities)

            self.driver.get('https://web.ataonline.com.tr/SanalSube/tr/Account/Login')

            musno = self.driver.find_element(By.XPATH, '//*[@id="InputCustomerNo"]')
            musno.send_keys(f"{self.musno}")

            password = self.driver.find_element(By.XPATH, '//*[@id="Password"]')
            password.send_keys(f"{self.sifre}")

            login = self.driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
            login.click()

            time.sleep(50)  # 50

            global mesaj
            print(mesaj)

            myaz = self.driver.find_element(By.CSS_SELECTOR, '#SMSPassword')
            myaz.send_keys(f'{mesaj}')

            time.sleep(3)

            giristamamla = self.driver.find_element(By.CSS_SELECTOR, '#btnSMS1')
            giristamamla.click()

            time.sleep(10)

            self.nakit = self.driver.find_element(By.XPATH,
                                                  '//*[@id="widget1_portfoy"]/div/div/div/div[11]/div[2]').text
            self.nakit1 = self.nakit.split(".")
            self.nakit2 = self.nakit1[0]
            self.nakit3 = self.nakit2.replace(",", ".")
            self.nakit4 = str(int(self.nakit3) * 50 / 100).split('.')
            self.nakit5 = self.nakit4[0]
            self.nakit6 = int(self.nakit5)

            self.i = 0

            scroll_amount = 100  # Kaydırma miktarı (pixel olarak)
            for _ in range(4):
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(1)

            global hisseList

            if len(hisseList) == 0:

                # div1

                div1 = self.driver.find_element(By.CSS_SELECTOR, '#col_2')

                # div2

                div2 = div1.find_element(By.CSS_SELECTOR, '#portlet_2')

                # div3

                div3 = div2.find_element(By.CSS_SELECTOR, '#container_WidgetWatchList')

                # div4

                div4 = div3.find_element(By.CSS_SELECTOR, '#container_WidgetWatchList > div.widget_favorite')

                # div5

                div5 = div4.find_element(By.CSS_SELECTOR, '#EquityList')

                # div6

                div6 = div5.find_element(By.CSS_SELECTOR, '#EquityList > div')

                # div7

                div7 = div6.find_element(By.CSS_SELECTOR, '#EquityList > div > div')

                # div8

                div8 = div7.find_element(By.CSS_SELECTOR, '#EquityList > div > div > div.WrapperPadding15')

                # div9

                div9 = div8.find_element(By.CSS_SELECTOR, '#mainSortingContainer')

                # row sortable-watchlist ts-data div elementlerini bul
                div_elements = div9.find_elements(By.CLASS_NAME, "row")
                div_elements = [div for div in div_elements if
                                div.get_attribute("class") == "row sortable-watchlist ts-data"]

                # Her bir div elementi için döngü oluştur
                for div_element in div_elements:
                    hisse1 = div_element
                    hisse = div_element.text
                    hisse = hisse.split("\n")
                    hisseadi = hisse[0]
                    hissefiyat = hisse[1]
                    hisseyuzdelik1 = float(hisse[4])
                    hisseyuzdelik = "{:.2f}".format(hisseyuzdelik1)
                    adet = 0

                    yuzdeartis = float(hisseyuzdelik) + 0.15
                    yuzdeartis = "{:.2f}".format(yuzdeartis)
                    yuzdeazalis = float(hisseyuzdelik) + (-0.10)
                    yuzdeazalis = "{:.2f}".format(yuzdeazalis)

                    # İşlemlerinizi burada yapabilirsiniz
                    print(f"|" + "-" * 50)
                    print(f"| [+] Hisse Adı: {hisseadi}")
                    print(f"| [+] Hisse Fiyat : {hissefiyat}")
                    print(f"| [+] Hisse Yüzdelik : {hisseyuzdelik}")
                    print(f"| [+] Hisse Hedef Artış Yüzdelik : {yuzdeartis}")
                    hesap1 = (float(float(hissefiyat) / 100) * float(yuzdeartis)) + float(hissefiyat)
                    hesap1 = "{:.3f}".format(hesap1)
                    print(f"| [+] Hisse Hedef Artış Fiyat : {hesap1}")
                    print(f"| [+] Hisse Hedef Düşüş Yüzdelik {yuzdeazalis}")
                    hesap2 = float(hissefiyat) - (float(float(hissefiyat) / 100) * float(yuzdeartis))
                    hesap2 = "{:.3f}".format(hesap2)
                    print(f"| [+] Hisse Hedef Düşüş Fiyat {hesap2}")
                    print(f"| [+] Adet : {adet}")
                    print(f"|" + "-" * 50)

                    hisseList.append(
                        [hisseadi, hissefiyat, hisseyuzdelik, yuzdeartis, yuzdeazalis, adet, hisse1, hesap1, hesap2])

            else:
                for i in range(0, len(hisseList)):
                    # İşlemlerinizi burada yapabilirsiniz
                    print(f"|" + "-" * 50)
                    print(f"| [+] Hisse Adı: {hisseList[i][0]}")
                    print(f"| [+] Hisse Fiyat : {hisseList[i][1]}")
                    print(f"| [+] Hisse Yüzdelik : {hisseList[i][2]}")
                    print(f"| [+] Hisse Hedef Artış Yüzdelik : {hisseList[i][3]}")
                    hesap1 = float(
                        (float(float(hisseList[i][1]) / 100) * float(hisseList[i][3])) + float(hisseList[i][1]))
                    hesap1 = "{:.3f}".format(hesap1)
                    hisseList[i][7] = f"{hesap1}"
                    print(f"| [+] Hisse Hedef Artış Fiyat : {hisseList[i][7]}")
                    print(f"| [+] Hisse Hedef Azalış Yüzdelik {hisseList[i][4]}")
                    hesap2 = float(
                        float(hisseList[i][1]) - (float(float(hisseList[i][1]) / 100) * float(hisseList[i][4])))
                    hesap2 = "{:.3f}".format(hesap2)
                    hisseList[i][8] = f"{hesap2}"
                    print(f"| [+] Hisse Hedef Azalış Fiyat {hisseList[i][8]}")
                    print(f"| [+] Adet : {hisseList[i][5]}")
                    print(f"|" + "-" * 50)

            self.controlcenter()

            time.sleep(1000000000)

        except Exception as e:
            print(f"Hata : {e}")
            self.driver.close()
            Applications()

    def controlcenter(self):
        while True:
            try:

                # scroll down

                self.driver.execute_script(f"window.scrollBy(0, document.body.scrollHeight);")

                # Bakiye
                nyenile = self.driver.find_element(By.XPATH, '//*[@id="btn-WidgetPortfolio-refresh"]')
                nyenile.click()

                time.sleep(1)

                # scroll down

                scroll_amount = 100  # Kaydırma miktarı (pixel olarak)
                for _ in range(2):
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(1)

                # işlem bölümü

                self.nakit = self.driver.find_element(By.XPATH,
                                                      '//*[@id="widget1_portfoy"]/div/div/div/div[11]/div[2]').text
                self.nakit1 = self.nakit.split(".")
                self.nakit2 = self.nakit1[0]
                self.nakit3 = self.nakit2.replace(",", ".")
                self.nakit4 = str(int(self.nakit3) * 50 / 100).split('.')
                self.nakit5 = self.nakit4[0]
                self.nakit6 = int(self.nakit5)

                print(f"| [+] Şuan ki nakit : {self.nakit3}")
                # div1

                div1 = self.driver.find_element(By.CSS_SELECTOR, '#col_2')

                # div2

                div2 = div1.find_element(By.CSS_SELECTOR, '#portlet_2')

                # div3

                div3 = div2.find_element(By.CSS_SELECTOR, '#container_WidgetWatchList')

                # div4

                div4 = div3.find_element(By.CSS_SELECTOR, '#container_WidgetWatchList > div.widget_favorite')

                # div5

                div5 = div4.find_element(By.CSS_SELECTOR, '#EquityList')

                # div6

                div6 = div5.find_element(By.CSS_SELECTOR, '#EquityList > div')

                # div7

                div7 = div6.find_element(By.CSS_SELECTOR, '#EquityList > div > div')

                # div8

                div8 = div7.find_element(By.CSS_SELECTOR, '#EquityList > div > div > div.WrapperPadding15')

                # div9

                div9 = div8.find_element(By.CSS_SELECTOR, '#mainSortingContainer')

                # row sortable-watchlist ts-data div elementlerini bul
                div_elements = div9.find_elements(By.CLASS_NAME, "row")
                div_elements = [div for div in div_elements if
                                div.get_attribute("class") == "row sortable-watchlist ts-data"]

                # Her bir div elementi için döngü oluştur
                for div_element in div_elements:
                    hisse = div_element.text
                    hisse = hisse.split("\n")
                    self.hisseadi = hisse[0]
                    self.hissefiyat = float(hisse[1])
                    self.hissefiyat2 = "{:.3f}".format(self.hissefiyat)
                    self.hisseyuzdelik = float(hisse[4])

                    # self.hisseyuzdelik = "{:.2f}".format(hisseyuzdelik1)

                    print("|" + "-" * 72 + "|")
                    print(
                        f"|   Hisse Adı: {self.hisseadi} - Hisse Fiyat : {self.hissefiyat}  - Hisse Yüzdelik : {self.hisseyuzdelik}")
                    print("|" + "-" * 72 + "|")

                    listadet = len(hisseList)

                    for i in range(0, listadet):

                        hisseadi2 = hisseList[i][0]

                        if self.hisseadi == hisseadi2:

                            hisseyuzdelik2 = float(hisseList[i][2])
                            yuzdeartis = float(hisseList[i][3])
                            yuzdeazalis = float(hisseList[i][4])
                            self.adet = hisseList[i][5]
                            self.alsat = hisseList[i][6]

                            time.sleep(1)

                            if self.hisseyuzdelik > yuzdeartis:

                                if int(self.adet) == 0:
                                    print(f"|                  Yeterli lootunuz bulunmamaktadır...                   |")
                                    print("|" + "-" * 72 + "|")

                                else:
                                    print("|" + "-" * 72 + "|")
                                    print("|                     Sat emir işlemi uygulanıyor...                     |")
                                    print("|" + "-" * 72 + "|")
                                    try:
                                        print("| SAT EMRİ ŞARTI OLUŞTU ")
                                        hizlisat = self.alsat.find_element(By.XPATH, '//*[@id="Sell"]')
                                        hizlisat.click()

                                        time.sleep(5)

                                        try:
                                            self.driver.find_element(By.XPATH,
                                                                     "//input[@type='radio' and @id='ShortFall' and @checked]")
                                            print("| [-] Liste Düzeltiliyor...")

                                            hisseList[i][5] = f"{self.adet}"

                                            print(
                                                f"| [+] Adet : {hisseList[i][5]} alım emrin gerçekleşmesi bekleniliyordur.")

                                            try:

                                                kapat3 = self.driver.find_element(By.XPATH, '//*[@id="hizli_emir_row_div"]/div[1]/div[2]/p/a')
                                                kapat3.click()

                                            except:
                                                pass

                                        except NoSuchElementException:

                                            adetc = self.driver.find_element(By.XPATH, '//*[@id="equityMaxUnit"] ').text
                                            adetc = adetc

                                            print(adetc)

                                            hisseadiyaz = Select(
                                                self.driver.find_element(By.XPATH, '//*[@id="ddlEquityOrderSales"]'))
                                            hisseadiyaz.select_by_visible_text(f'{hisseadi2}')

                                            hissefiyatyaz = self.driver.find_element(By.XPATH, '//*[@id="ddlPrice"]')
                                            hissefiyatyaz.send_keys(f"{self.hissefiyat2}")

                                            adetyaz = self.driver.find_element(By.XPATH, '//*[@id="Unit"]')
                                            adetyaz.send_keys(f"{adetc}")

                                            alemirgonder = self.driver.find_element(By.XPATH,
                                                                                    '//*[@id="btn-send-mini-addorder"]')
                                            alemirgonder.click()

                                            time.sleep(3)

                                            kapat = self.driver.find_element(By.XPATH, '//*[@id="AlertBoxCloseButton"]')
                                            kapat.click()

                                            time.sleep(1)

                                            kapat2 = self.driver.find_element(By.XPATH,
                                                                              '//*[@id="hizli_emir_row_div"]/div[1]/div[2]/p/a')
                                            kapat2.click()

                                            # Bakiye

                                            sonuc = float(self.hissefiyat2) * int(adetc)
                                            print(
                                                f"| Hisse Adı : {hisseadi2} - Tane Fiyatı : {self.hissefiyat2} * Satılacak Adet Sayısı : {adetc} : {sonuc}")

                                            hisseList[i][5] = int(hisseList[i][5]) - int(adetc)
                                            adet2 = hisseList[i][5]
                                            hisseList[i][3] = float(hisseList[i][3]) + 0.10
                                            hisseyüzdelikartis = "{:.2f}".format(hisseList[i][3])
                                            print(f"| [+] Adet : {adetc} satma emri verilmiştir.")
                                            print(f"| [+] Hisse Adı : {hisseadi2} - Adet : {adet2} olmuştur.")
                                            print(f"| [+] Hisse Yüzdelik Artış Hedef : {hisseyüzdelikartis} olmuştur.")
                                            hesap1 = (float(float(self.hissefiyat) / 100) * float(
                                                hisseList[i][3])) + float(self.hissefiyat)
                                            hesap1 = "{:.3f}".format(hesap1)
                                            hisseList[i][7] = f"{hesap1}"
                                            print(f"| [+] Hisse Hedef Artış Fiyat : {hisseList[i][7]}")


                                    except Exception as e:

                                        print(f"Hata : {e}")

                                        pass

                            elif self.hisseyuzdelik < yuzdeazalis:
                                print("|" + "-" * 72 + "|")
                                print("|                      Adet Limit Kontrol Ediliyor                       |")
                                print("|" + "-" * 72 + "|")

                                if int(self.adet) >= 100:
                                    print(
                                        f"|                 Adet : {self.adet} / Limit : 100'e ulaşmış veya aşmıştır.                 |")
                                    print("|                     Sat emir işlemi uygulanıyor...                     |")
                                    print("|" + "-" * 72 + "|")
                                    try:
                                        print("| SAT EMRİ ŞARTI OLUŞTU ")
                                        hizlisat = self.alsat.find_element(By.XPATH, '//*[@id="Sell"]')
                                        hizlisat.click()

                                        time.sleep(5)

                                        try:
                                            self.driver.find_element(By.XPATH,
                                                                     "//input[@type='radio' and @id='ShortFall' and @checked]")
                                            print("| [-] Liste Düzeltiliyor...")

                                            hisseList[i][5] = f"{self.adet}"

                                            print(
                                                f"| [+] Adet : {hisseList[i][5]} alım emrin gerçekleşmesi bekleniliyordur.")


                                        except NoSuchElementException:

                                            adetc = self.driver.find_element(By.XPATH, '//*[@id="equityMaxUnit"] ').text
                                            adetc = adetc

                                            print(adetc)

                                            hisseadiyaz = Select(
                                                self.driver.find_element(By.XPATH, '//*[@id="ddlEquityOrderSales"]'))
                                            hisseadiyaz.select_by_visible_text(f'{hisseadi2}')

                                            hissefiyatyaz = self.driver.find_element(By.XPATH, '//*[@id="ddlPrice"]')
                                            hissefiyatyaz.send_keys(f"{self.hissefiyat2}")

                                            adetyaz = self.driver.find_element(By.XPATH, '//*[@id="Unit"]')
                                            adetyaz.send_keys(f"{adetc}")

                                            alemirgonder = self.driver.find_element(By.XPATH,
                                                                                    '//*[@id="btn-send-mini-addorder"]')
                                            alemirgonder.click()

                                            time.sleep(3)

                                            kapat = self.driver.find_element(By.XPATH, '//*[@id="AlertBoxCloseButton"]')
                                            kapat.click()

                                            time.sleep(1)

                                            kapat2 = self.driver.find_element(By.XPATH,
                                                                              '//*[@id="hizli_emir_row_div"]/div[1]/div[2]/p/a')
                                            kapat2.click()

                                            # Bakiye

                                            sonuc = float(self.hissefiyat2) * int(adetc)
                                            print(
                                                f"| Hisse Adı : {hisseadi2} - Tane Fiyatı : {self.hissefiyat2} * Satılacak Adet Sayısı : {adetc} : {sonuc}")

                                            hisseList[i][5] = int(hisseList[i][5]) - int(adetc)
                                            adet2 = hisseList[i][5]
                                            hisseList[i][3] = float(hisseList[i][3]) + 0.10
                                            hisseyüzdelikartis = "{:.2f}".format(hisseList[i][3])
                                            print(f"| [+] Adet : {adetc} satma emri verilmiştir.")
                                            print(f"| [+] Hisse Adı : {hisseadi2} - Adet : {adet2} olmuştur.")
                                            print(f"| [+] Hisse Yüzdelik Artış Hedef : {hisseyüzdelikartis} olmuştur.")
                                            hesap1 = (float(float(self.hissefiyat) / 100) * float(
                                                hisseList[i][3])) + float(self.hissefiyat)
                                            hesap1 = "{:.3f}".format(hesap1)
                                            hisseList[i][7] = f"{hesap1}"
                                            print(f"| [+] Hisse Hedef Artış Fiyat : {hisseList[i][7]}")

                                    except Exception as e:
                                        print(f"Hata : {e}")
                                        pass

                                else:
                                    print("|" + "-" * 72 + "|")
                                    print("|                Al emir için bakiye kontrol ediliyor...                 |")

                                    if float(self.nakit) < 10.00:
                                        print(
                                            "|                         [-] Bakiye Yetersiz..!                         |")
                                        print("|" + "-" * 72 + "|")
                                    else:
                                        print("|" + "-" * 72 + "|")
                                        print(
                                            "|                     Al emir işlemi uygulanıyor...                      |")
                                        print("|" + "-" * 72 + "|")

                                        self.alinacak_Adet = int(int(self.nakit6) / self.hissefiyat)

                                        if self.alinacak_Adet <= 0:
                                            print("| [-] Alım için yetersiz bakiye")

                                        else:
                                            self.adet = int(self.adet) + self.alinacak_Adet
                                            print(
                                                f"|                         [+] Alıncak Adet : {self.alinacak_Adet}                          |")

                                            try:
                                                print("| AL EMRİ ŞARTI OLUŞTU ")

                                                hizlial = self.alsat.find_element(By.XPATH, '//*[@id="Buy"]')
                                                hizlial.click()

                                                time.sleep(5)
                                                hisseadiyaz = Select(
                                                    self.driver.find_element(By.XPATH, '//*[@id="ddlEquityOrderBuy"]'))
                                                hisseadiyaz.select_by_visible_text(f'{hisseadi2}')

                                                hissefiyatyaz = self.driver.find_element(By.XPATH,
                                                                                         '//*[@id="ddlPrice"]')
                                                hissefiyatyaz.send_keys(f"{self.hissefiyat2}")

                                                adetyaz = self.driver.find_element(By.XPATH, '//*[@id="Unit"]')
                                                adetyaz.send_keys(f"{self.alinacak_Adet}")

                                                alemirgonder = self.driver.find_element(By.XPATH,
                                                                                        '//*[@id="btn-send-mini-addorder"]')
                                                alemirgonder.click()

                                                time.sleep(3)

                                                kapat = self.driver.find_element(By.XPATH,
                                                                                 '//*[@id="AlertBoxCloseButton"]')
                                                kapat.click()

                                                time.sleep(1)

                                                kapat2 = self.driver.find_element(By.XPATH,
                                                                                  '//*[@id="hizli_emir_row_div"]/div[1]/div[2]/p/a')
                                                kapat2.click()

                                                sonuc = float(self.hissefiyat2) * self.alinacak_Adet
                                                print(
                                                    f"| Hisse Adı : {hisseadi2} - Tane Fiyatı : {self.hissefiyat2} * Alınacak Adet Sayısı : {self.alinacak_Adet} : {sonuc}")

                                                hisseList[i][5] = int(hisseList[i][5]) + int(self.alinacak_Adet)
                                                adet2 = hisseList[i][5]
                                                hisseList[i][3] = float(hisseList[i][3]) + 0.10
                                                hisseyüzdelikartis = "{:.2f}".format(hisseList[i][3])
                                                hisseList[i][4] = float(hisseList[i][4]) + (-0.10)
                                                hisseyüzdelikazalis = "{:.2f}".format(hisseList[i][4])
                                                print(f"| [+] Adet: {self.alinacak_Adet} satın alma emri verilmiştir.")
                                                print(f"| [+] Hisse Adı : {hisseadi2} - Adet : {adet2} olmuştur.")
                                                print(
                                                    f"| [+] Hisse Yüzdelik Artış Hedef : {hisseyüzdelikartis} olmuştur.")
                                                hesap1 = float((float(float(self.hissefiyat) / 100) * float(
                                                    hisseList[i][3])) + float(self.hissefiyat))
                                                hesap1 = "{:.3f}".format(hesap1)
                                                hisseList[i][7] = f"{hesap1}"
                                                print(f"| [+] Hisse Hedef Artış Fiyat : {hisseList[i][7]}")
                                                print(
                                                    f"| [+] Hisse Yüzdelik Azalış Hedef : {hisseyüzdelikazalis} olmuştur.")
                                                hesap2 = float(float(self.hissefiyat) - (
                                                            float(float(self.hissefiyat) / 100) * float(
                                                        hisseList[i][4])))
                                                hesap2 = "{:.3f}".format(hesap2)
                                                hisseList[i][8] = f"{hesap2}"
                                                print(f"| [+] Hisse Hedef Azalış Fiyat {hisseList[i][8]}")

                                            except:
                                                pass

                            elif self.hisseyuzdelik == hisseyuzdelik2:
                                print("|" + "-" * 72 + "|")
                                print("|                 Hisse oranın değişmesi bekleniliyor...                 |")
                                print("|" + "-" * 72 + "|")

            except Exception as e:
                print(f"Hata : {e}")
                self.driver.close()
                Applications()

    # def alemir(self, hisseadi, adet, fiyat, alsat):
    #     try:
    #         print("| AL EMRİ ŞARTI OLUŞTU ")
    #
    #         hizlial = alsat.find_element(By.XPATH, '//*[@id="Buy"]')
    #         hizlial.click()
    #
    #         time.sleep(5)
    #         hisseadiyaz = Select(self.driver.find_element(By.XPATH, '//*[@id="ddlEquityOrderBuy"]'))
    #         hisseadiyaz.select_by_visible_text(f'{hisseadi}')
    #
    #         hissefiyatyaz = self.driver.find_element(By.XPATH, '//*[@id="ddlPrice"]')
    #         hissefiyatyaz.send_keys(f"{fiyat}")
    #
    #         adetyaz = self.driver.find_element(By.XPATH, '//*[@id="Unit"]')
    #         adetyaz.send_keys(f"{adet}")
    #
    #         alemirgonder = self.driver.find_element(By.XPATH, '//*[@id="btn-send-mini-addorder"]')
    #         alemirgonder.click()
    #
    #         time.sleep(3)
    #
    #         kapat = self.driver.find_element(By.XPATH, '//*[@id="AlertBoxCloseButton"]')
    #         kapat.click()
    #
    #         time.sleep(1)
    #
    #         kapat2 = self.driver.find_element(By.XPATH, '//*[@id="hizli_emir_row_div"]/div[1]/div[2]/p/a')
    #         kapat2.click()
    #
    #         sonuc = float(fiyat) * adet
    #         print(f"| Hisse Adı : {hisseadi} - Tane Fiyatı : {fiyat} * Alınacak Adet Sayısı : {adet} : {sonuc}")
    #
    #         self.adetDuzelt(islem="Arttır", hisseadi=hisseadi, adet=adet)
    #
    #     except Exception as e:
    #
    #         print(f"Hata : {e}")
    #         self.driver.close()
    #         Applications()
    #
    # def satemir(self, hisseadi, adet, fiyat, alsat):
    #     try:
    #         print("| SAT EMRİ ŞARTI OLUŞTU ")
    #         hizlisat = alsat.find_element(By.XPATH, '//*[@id="Sell"]')
    #         hizlisat.click()
    #
    #         time.sleep(5)
    #
    #         try:
    #             self.driver.find_element(By.XPATH, "//input[@type='radio' and @id='ShortFall' and @checked]")
    #             print("| [-] Liste Düzeltiliyor...")
    #
    #             self.adetDuzelt(islem="Düzelt", hisseadi=hisseadi, adet=adet)
    #
    #         except NoSuchElementException:
    #
    #             adetc = self.driver.find_element(By.XPATH, '//*[@id="equityMaxUnit"] ').text
    #             adetc = adetc
    #
    #             print(adetc)
    #
    #             hisseadiyaz = Select(self.driver.find_element(By.XPATH, '//*[@id="ddlEquityOrderSales"]'))
    #             hisseadiyaz.select_by_visible_text(f'{hisseadi}')
    #
    #             hissefiyatyaz = self.driver.find_element(By.XPATH, '//*[@id="ddlPrice"]')
    #             hissefiyatyaz.send_keys(f"{fiyat}")
    #
    #             adetyaz = self.driver.find_element(By.XPATH, '//*[@id="Unit"]')
    #             adetyaz.send_keys(f"{adetc}")
    #
    #             alemirgonder = self.driver.find_element(By.XPATH, '//*[@id="btn-send-mini-addorder"]')
    #             alemirgonder.click()
    #
    #             time.sleep(3)
    #
    #             kapat = self.driver.find_element(By.XPATH, '//*[@id="AlertBoxCloseButton"]')
    #             kapat.click()
    #
    #             time.sleep(1)
    #
    #             kapat2 = self.driver.find_element(By.XPATH, '//*[@id="hizli_emir_row_div"]/div[1]/div[2]/p/a')
    #             kapat2.click()
    #
    #             # Bakiye
    #
    #             sonuc = float(fiyat) * int(adetc)
    #             print(
    #                 f"| Hisse Adı : {hisseadi} - Tane Fiyatı : {fiyat} * Satılacak Adet Sayısı : {adetc} : {sonuc}")
    #
    #             self.adetDuzelt(islem="çıkart", hisseadi=hisseadi, adet=adetc)
    #
    #     except Exception as e:
    #
    #         print(f"Hata : {e}")
    #         self.driver.close()
    #         Applications()
    #
    # def adetDuzelt(self, islem, hisseadi, adet):
    #     global hisseList
    #
    #     if islem == "Düzelt":
    #
    #         listadet = len(hisseList)
    #
    #         for i in range(0, listadet):
    #
    #             hisseadi2 = hisseList[i][0]
    #
    #             if hisseadi == hisseadi2:
    #                 hisseList[i][5] = f"{adet}"
    #
    #                 print(f"| [+] Adet : {hisseList[i][5]} alım emrin gerçekleşmesi bekleniliyordur.")
    #
    #                 self.controlcenter()
    #
    #     if islem == "Arttır":
    #
    #         listadet = len(hisseList)
    #
    #         for i in range(0, listadet):
    #
    #             hisseadi2 = hisseList[i][0]
    #
    #             if hisseadi == hisseadi2:
    #
    #                 hisseList[i][5] = int(hisseList[i][5]) + int(adet)
    #                 adet2 = hisseList[i][5]
    #                 hisseList[i][3] = float(hisseList[i][3]) + 0.05
    #                 hisseyüzdelikartis = "{:.2f}".format(hisseList[i][3])
    #                 hisseList[i][4] = float(hisseList[i][4]) + (-0.05)
    #                 hisseyüzdelikazalis = "{:.2f}".format(hisseList[i][4])
    #                 print(f"| [+] Adet: {adet} satın alma emri verilmiştir.")
    #                 print(f"| [+] Hisse Adı : {hisseadi} - Adet : {adet2} olmuştur.")
    #                 print(f"| [+] Hisse Yüzdelik Artış Hedef : {hisseyüzdelikartis} olmuştur.")
    #                 print(f"| [+] Hisse Yüzdelik Azalış Hedef : {hisseyüzdelikazalis} olmuştur.")
    #
    #                 self.controlcenter()
    #
    #     if islem == "Çıkart":
    #
    #         listadet = len(hisseList)
    #
    #         for i in range(0, listadet):
    #
    #             hisseadi2 = hisseList[i][0]
    #
    #             if hisseadi == hisseadi2:
    #
    #                 hisseList[i][5] = int(hisseList[i][5]) - int(adet)
    #                 adet2 = hisseList[i][5]
    #                 hisseList[i][3] = float(hisseList[i][3]) + 0.10
    #                 hisseyüzdelikartis = "{:.2f}".format(hisseList[i][3])
    #                 print(f"| [+] Adet : {adet} satma emri verilmiştir.")
    #                 print(f"| [+] Hisse Adı : {hisseadi} - Adet : {adet2} olmuştur.")
    #                 print(f"| [+] Hisse Yüzdelik Artış Hedef : {hisseyüzdelikartis} olmuştur.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    t1 = Thread(target=WhatsappApplications)
    t1.start()
    Applications()

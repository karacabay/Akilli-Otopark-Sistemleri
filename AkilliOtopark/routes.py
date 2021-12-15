from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from AkilliOtopark import app, db
from AkilliOtopark.forms import UserForm, LoginForm, PlakaEkle, PlakaSil, KullaniciSil
from AkilliOtopark.models import User, Plaka

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Zaten giriş yaptınız.', 'warning')  
        return redirect(url_for('kullanici_paneli'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)    
            flash(f"Akıllı Otopark Sistemlerine hoşgeldin '{form.username.data}'", 'success')
            return redirect(url_for('kullanici_paneli'))
        else:
            flash(f'Kullanıcı adı veya şifre hatalı.', 'danger')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/kullanici-ekle', methods=['GET', 'POST'])
def kullanici_ekle():
    if not current_user.is_authenticated:
        flash(f'Lütfen giriş yapınız.', 'danger')  
        return redirect(url_for('login'))
    if current_user.id != 1:
        flash(f'Bu alanı görüntüleme yetkiniz bulunmamakta.', 'danger')  
        return redirect(url_for('kullanici_paneli'))
    
    form = UserForm()
    if request.method == 'POST':
        if not form.password.data == form.password2.data:
            flash(f'Şifreler eşleşmemekte.', 'danger')
            return render_template('kullanici-ekle.html', 
                    form=form, admin=True, user=True)

        db.session.add( User(
            username=form.username.data,  
            password=form.password.data))
        db.session.commit()
        flash('Kullanıcı başarıyla kaydedildi.', 'success')
        return redirect(url_for('kullanici_paneli'))

    else:
        return render_template('kullanici-ekle.html', form=form, 
                                                      admin=True, 
                                                      user=True)

@app.route('/kullanici-sil', methods=['GET', 'POST'])
def kullanici_sil():
    if not current_user.is_authenticated:    
        flash(f'Lütfen giriş yapınız.', 'danger')  
        return redirect(url_for('login'))
    if current_user.id != 1:
        flash(f'Bu alanı görüntüleme yetkiniz bulunmamakta.', 'danger')  
        return redirect(url_for('kullanici_paneli'))
    
    form = KullaniciSil()
    all_users = User.query.all()
    form.selectbox.choices = [('false', 'Seçiniz')] + [(u.id, u.username) for u in all_users if u.id!=1]
    if request.method == 'POST':     
        if form.selectbox.data != 'false':
            x = User.query.get(int(form.selectbox.data))
            plakas = Plaka.query.filter_by(user_id=x.id)
            for p in plakas:
                db.session.delete(p)
                db.session.commit()

            db.session.delete(x)
            db.session.commit()
            

            flash('Kullanıcı ve kayıtlı plakaları başarıyla silindi.', 'success')
            return redirect(url_for('kullanici_paneli'))
        else:
            flash('Kullanıcı silinemedi.', 'danger')
            return redirect(url_for('kullanici_paneli'))
    else:
        return render_template('kullanici-sil.html', form=form, user=True, admin=True)

@app.route('/kullanici-paneli', methods=['GET', 'POST'])
def kullanici_paneli():
    if not current_user.is_authenticated:
        flash('Lütfen giriş yapınız.', 'danger')
        return redirect(url_for('login'))
    admin = current_user.id == 1
    all_plakas = Plaka.query.filter_by(user_id=current_user.id)
    return render_template('kullanici-paneli.html',plakas=all_plakas, 
                                                   user=current_user.is_authenticated, 
                                                   admin=admin)

@app.route('/about')
def about():
    if current_user.is_authenticated:
        admin = current_user.id == 1
    else :
        admin=False
    return render_template('about.html', user=current_user.is_authenticated, admin=admin)

@app.route('/plaka-ekle', methods=['GET', 'POST'])
def plaka_ekle():
    if not current_user.is_authenticated:
        flash('Lütfen giriş yapınız.', 'danger')
        return redirect(url_for('login'))
    admin = current_user.id == 1
    form = PlakaEkle()
    if request.method == 'POST':     
        db.session.add( Plaka(
            name=form.name.data.title(), 
            surname=form.surname.data.title(), 
            plaka=form.plaka.data.upper().replace(' ', ''), 
            user_id=current_user.id))
        db.session.commit()
        flash('Plaka başarıyla kaydedildi.', 'success')
        return redirect(url_for('kullanici_paneli'))

    else:
        return render_template('plaka-ekle.html', form=form, user=current_user.is_authenticated, admin=admin)

@app.route('/plaka-sil', methods=['GET', 'POST'])
def plaka_sil():
    if not current_user.is_authenticated:
        flash('Lütfen giriş yapınız.', 'danger')
        return redirect(url_for('login'))
    admin = current_user.id == 1
    form = PlakaSil()
    all_plakas = Plaka.query.filter_by(user_id=current_user.id)
    if current_user.id == 1:
        all_plakas = Plaka.query.all()

    form.selectbox.choices = [('false', 'Seçiniz')] + [(plaka.id, plaka.plaka+' '+plaka.name+' '+plaka.surname) for plaka in all_plakas]
    if request.method == 'POST':     
        if form.selectbox.data != 'false':
            x = Plaka.query.get(int(form.selectbox.data))
            db.session.delete(x)
            db.session.commit()
            flash('Plaka başarıyla silindi.', 'success')
            return redirect(url_for('kullanici_paneli'))
        else:
            flash('Plaka silinemedi.', 'danger')
            return redirect(url_for('kullanici_paneli'))
    else:
        return render_template('plaka-sil.html', form=form, user=current_user.is_authenticated, admin=admin)

@app.route('/butun-plakalar')
def butun_plakalar():
    all_plakas = Plaka.query.all()
    isimler = [p.name for p in all_plakas]
    soyisimler = [p.surname for p in all_plakas]
    plakalar = [p.plaka for p in all_plakas]
    sonuc = [isim+'***'+soyisim+'***'+plaka for (isim, soyisim, plaka) in zip(isimler,
    soyisimler, plakalar)]
    sonuc = ('---').join(sonuc)
    print(sonuc)
    return sonuc

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        flash('Lütfen giriş yapınız', 'danger')
    else:
        logout_user()
    return redirect(url_for('login'))
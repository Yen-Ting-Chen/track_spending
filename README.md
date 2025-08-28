
# 📒 記帳系統（Budget Tracker）

這是一個基於 **Django** 框架開發的記帳系統，支援多使用者登入、記帳紀錄、新增消費類型、帳務分析、圖表顯示等功能，可部署於 **AWS EC2**。
<!-- ，並整合 **第三方登入（Google / Facebook）** -->


## 🔧 專案功能特色

### 🧾 記帳紀錄
- 顯示當月記帳資料（可篩選其他月份與年份）
- 顯示每筆的類別、消費方式、備註等
- 支援新增 / 編輯 / 刪除記帳資料
- 每月統計總收入、總支出與結餘

### ➕ 新增記帳
- 可選擇消費類型與方式（如：現金、信用卡、行動支付等）
- 日期預設為今天，可手動選擇
- 支援類別管理（新增與刪除）

### 📊 帳務分析
- 使用 Chart.js 呈現：
  - 月收入 / 支出 / 結餘比較圖
  - 分類消費總覽（圓餅圖）
- 顯示每類別花費明細，並標示消費日期
- 可篩選分析的時間區間（預設當年度）

<!-- ### 🔐 使用者管理
- 使用 Django Allauth 整合：
  - 本地帳號（Email + 密碼）
  - Facebook / Google 第三方登入
- 每位使用者的帳務資料獨立存放 -->

### 💅 前端美化
- 採用 **Bootstrap 5**
- 支援響應式版面
- 自訂樣式與字體（Noto Sans TC）
- 表格與卡片風格統一，清晰美觀

## 🛠️ 開發與部署

### 📦 技術棧
- Backend：Django 4.0.4
- Frontend：Bootstrap 5 + Chart.js
- Database：sqlite3
<!-- - Auth：Django Allauth（Email / Google / Facebook）
- 部署：支援 AWS EC2 / Nginx / Gunicorn -->

## 🚀 快速開始

### 1️⃣ 環境安裝

```bash
git clone https://github.com/your-username/budget-tracker.git
cd budget-tracker

python -m venv venv
source venv/bin/activate  # Windows 用 venv\Scripts\activate

pip install -r requirements.txt
```

<!-- ### 2️⃣ 建立資料庫設定（MySQL）

請於 `settings.py` 中配置你的 MySQL 連線設定：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
} -->
```

### 3️⃣ 套用資料庫

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ 建立管理員帳號

```bash
python manage.py createsuperuser
```

### 5️⃣ 執行開發伺服器

```bash
python manage.py runserver
```

開啟瀏覽器進入 [http://localhost:8000](http://localhost:8000)

<!-- ## 🔑 第三方登入設定（可選）

請至 Google / Facebook 建立應用程式，並在 `.env` 或 `settings.py` 設定以下變數：

```env
SOCIAL_AUTH_GOOGLE_CLIENT_ID=
SOCIAL_AUTH_GOOGLE_SECRET=
SOCIAL_AUTH_FACEBOOK_KEY=
SOCIAL_AUTH_FACEBOOK_SECRET=
``` -->

## 📁 專案結構

```
budget_tracker/
├── spend_record/         # 記帳功能 app
│   ├── models.py         # 資料模型
│   ├── views.py          # 各頁面邏輯
│   ├── forms.py          # 表單定義
│   ├── templates/        # HTML 模板
├── templates/
│   └── base.html         # 共用基礎模板
├── static/               # 靜態資源
├── manage.py
├── requirements.txt
```

## 🧑‍💻 開發者資訊

作者：`陳彥廷 / tom840321zx`  
E-mail：tom840321zx@gmail.com

## 📄 License

本專案採用 MIT 授權，歡迎自由使用與修改。

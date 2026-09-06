# KiwiAI — شمارش کیوی ردیفی

این پروژهٔ محلی برای ویدئوی موبایل از یک ردیف باغ است:

`YOLOv5m → ByteTrack → Two-Container Verification (TCV) → شمارش`

## اجرا

```powershell
cd KiwiAI
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

فعلاً باید وزن آموزش‌دیدهٔ `best.pt` را انتخاب کنی. بدون برچسب، مدل قابل آموزش نیست؛ برای آموزش باید دو کلاس را برچسب بزنیم: `0=kiwifruit` و `1=support-post`.

## مرحلهٔ برچسب‌گذاری

تصاویر GitHub را داخل پوشه‌ای به نام `images` قرار بده و اجرا کن:

```powershell
python labeler.py
```

با ماوس دور هر میوه یا پایه باکس بکش؛ کلید `۱` برای کیوی، `۲` برای پایه و `Enter` برای ذخیره و رفتن به عکس بعدی است. فایل‌های YOLO خودکار در پوشهٔ `labels` کنار `images` ساخته می‌شوند.

## نکتهٔ مهم

این نسخه موتور واقعیِ تشخیص، ByteTrack و TCV را دارد. مرحلهٔ بعدی که من ادامه می‌دهم، ابزار برچسب‌گذاری و آموزش YOLOv5m روی RTX 3070 است؛ بعد فیلتر ردیف بر اساس support-post را به آن اضافه می‌کنیم.

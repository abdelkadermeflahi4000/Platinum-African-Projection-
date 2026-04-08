--- beyond_the_facade/README.md (原始)


+++ beyond_the_facade/README.md (修改后)
# 🌌 Beyond the Facade

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-blue)]()

## تجربة تفاعلية لكسر الإغلاق الفكري | An Interactive Experience to Break Intellectual Closure

**ما وراء الواجهة** هو مشروع مفتوح المصدر يجمع بين الفلسفة، الفن الرقمي، والتقنية المتقدمة لاستكشاف فكرة أن واقعنا الحالي هو مجرد طبقة واحدة من طبقات متعددة.

---

## 📜 البيان التأسيسي

اقرأ [البيان الكامل](MANIFESTO.md) لفهم الفلسفة والأهداف العميقة للمشروع.

> *"القيود ليست في العالم، بل في منظورنا له."*

---

## 🎯 الأهداف

### فلسفية:
- إثبات وجود طبقات واقع مخفية عبر التجربة التفاعلية
- كسر مفهوم الزمن الخطي والإدراك المحدود
- استكشاف فكرة "الأراضي الأخرى" خلف حدود المنظور الحالي

### تقنية:
- بناء محرك منظور (Perspective Engine) باستخدام Three.js/WebXR
- تطوير نظام إغلاق زمني (Temporal Closure API)
- خلق واجهة مستخدم 360° تحول الشاشة إلى "عين" ترى كل شيء

---

## 🏗️ البنية التقنية

```
beyond_the_facade/
├── src/                    # الكود المصدري الأساسي
│   ├── perspective_engine/  # محرك العرض والمنظور
│   ├── temporal_closure/    # نظام الإغلاق الزمني
│   └── core/               # النواة الأساسية
├── web_interface/          # واجهة الويب (Three.js, WebXR)
├── docs/                   # الوثائق والخارطة
├── tests/                  # اختبارات النظام
└── MANIFESTO.md           # البيان التأسيسي
```

### التقنيات المستخدمة:
- **Python/Rust**: للنواة والخوارزميات الأساسية
- **Three.js**: للعرض ثلاثي الأبعاد في المتصفح
- **WebXR**: لتجارب الواقع الافتراضي والمعزز
- **WebSocket**: للاتصال اللحظي بين المكونات

---

## 🚀 البدء السريع

### المتطلبات:
- Python 3.9+
- Node.js 18+
- Rust (اختياري للأداء العالي)

### التثبيت:

```bash
# استنساخ المشروع
git clone https://github.com/yourusername/beyond_the_facade.git
cd beyond_the_facade

# تثبيت تبعيات بايثون
pip install -r requirements.txt

# تثبيت تبعيات الواجهة
cd web_interface
npm install

# تشغيل الخادم التجريبي
python src/main.py
```

---

## 📖 الاستخدام الأساسي

```python
from src.perspective_engine import RealityEngine

# إنشاء واقع مقيد
reality = RealityEngine(perspective="linear", bounds="atmosphere")

# عرض الحالة الحالية
print(reality.describe())

# كسر الإغلاق بتغيير المنظور
reality.expand_awareness(mode="omnidirectional")

# الكشف عن الأراضي المخفية
hidden_lands = reality.reveal_hidden_layers()
print(f"تم اكتشاف {len(hidden_lands)} طبقات واقع جديدة")
```

---

## 🗺️ خارطة الطريق

| المرحلة | الحالة | الهدف |
|--------|--------|-------|
| **التأسيس** | 🟡 قيد التطوير | بناء النواة وتعريف حدود الإغلاق الأولي |
| **التوسيع** | ⚪ قادم | إضافة طبقات مخفية تظهر بتغيير الزاوية |
| **التحرر** | ⚪ مستقبلي | التكامل مع نظارات VR ومنظور 360° كامل |

اقرأ [الخارطة التفصيلية](docs/ROADMAP.md) للمزيد.

---

## 🤝 المساهمة

نحن نرحب بالمساهمين من جميع الخلفيات:
- 💻 المطورون (Python, Rust, JavaScript)
- 🎨 الفنانون الرقميون ومصممو التجارب الغامرة
- 🧠 الفلاسفة والباحثون في نظرية الواقع
- 📝 الكتاب وصانعو المحتوى

اقرأ [دليل المساهمة](docs/CONTRIBUTING.md) للبدء.

---

## 📄 الرخصة

مشروع مرخص تحت [MIT License](LICENSE) - حرية كاملة للتعديل والمشاركة والبناء.

---

## 🌐 روابط ذات صلة

- [الوثائق الكاملة](docs/)
- [البيان التأسيسي](MANIFESTO.md)
- [قائمة المساهمين](CONTRIBUTORS.md)

---

*"الأراضي الأخرى لا تُكتشف بالهروب، بل بتغيير النظر."*
*"Other lands are not discovered by escaping, but by changing how we see."*
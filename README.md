# e-qaime-pdf-to-excel
[e-taxes.gov.az portalından yüklənmiş e-qaimə pdf fayllarındakı məlumatları avtomatik olaraq excel reyestrinə yığan python skript]

# E-Qaimə PDF to Excel Parser 🚀

Bu Python skripti, [new.e-taxes.gov.az](https://new.e-taxes.gov.az) portalından yüklənmiş istənilən sayda e-qaimə PDF fayllarını oxuyur və daxilindəki məlumatları avtomatik olaraq vahid bir Excel reyestrinə (yəni sizin kreditor üzrə ödəməli olacağınız məlumatları) yığır.

Mexaniki köçürmə xətalarının qarşısını almaq və hesabatlıq proseslərini sürətləndirmək üçün faydalı bir alətdir.

### 📋 Çıxarılan Məlumatlar:
- 📄 E-qaimənin seriya nömrəsi
- 🏢 Göndərən VÖEN
- 🤝 Göndərən Subkontragent
- 💰 ƏDV, Əsas və Yekun məbləğlər

### 📁 Qovluq Strukturu:
[ƏSAS/ana qovluq (aşağıdakılar bu qovluq içində olacaq) ]
|
├── yep.py            # Əsas Python skripti
└── pdf/              # PDF e-qaimələri yerləşdirəcəyiniz qovluq

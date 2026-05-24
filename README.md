# Turing Makinesi ile Araç Plaka Formatı Tanıyıcı

**Final Ödev 2** — Format: `NNLLNNN` (2 rakam + 2 büyük harf + 3 rakam)

## Çalıştırma

```bash
python turing_plaka.py
```

| Komut | Açıklama |
|-------|----------|
| `55AB123` | Plakayı simüle et |
| `t` | 5 geçerli + 6 geçersiz otomatik test |
| *(boş)* | Çıkış |

## Teslim dosyaları

- `turing_plaka.py` — kaynak kod
- `GECIS_TABLOSU.md` — geçiş tablosu
- `RAPOR.md` — proje raporu ve durum diyagramı (Mermaid)

## Örnek çıktı

```
Girdi bandı: '55AB123'
Adım  0 | Durum: q0       | Okunan: 5      | Hareket: R    | Bant: □[5]5AB123□
...
>>> KABUL <<<
```

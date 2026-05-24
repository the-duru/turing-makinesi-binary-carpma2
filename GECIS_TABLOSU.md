# Turing Makinesi Geçiş Tablosu — NNLLNNN Plaka Tanıyıcı

**Bant sembolü (boş):** `_` (gösterimde `□`)

**Sembol sınıfları:** `DIGIT` (0–9), `UPPER` (A–Z), `BLANK` (`_`), `OTHER` (diğer tümü, küçük harf dahil)

**Yazma:** Bu tanıyıcıda bant salt okunur; geçişlerde yazma yapılmaz (ε).

**Hareket:** `R` = sağa, `S` = dur

| Mevcut durum | Okunan sembol | Yeni durum | Hareket | Açıklama |
|--------------|---------------|------------|---------|----------|
| q0 | DIGIT | q1 | R | İlk rakam okundu |
| q0 | UPPER | q_red | R | Rakam bekleniyordu |
| q0 | OTHER | q_red | R | Geçersiz sembol |
| q0 | BLANK | q_red | R | Eksik girdi |
| q1 | DIGIT | q2 | R | İkinci rakam okundu |
| q1 | UPPER | q_red | R | Rakam bekleniyordu |
| q1 | OTHER | q_red | R | Geçersiz sembol |
| q1 | BLANK | q_red | R | Eksik girdi |
| q2 | UPPER | q3 | R | İlk büyük harf okundu |
| q2 | DIGIT | q_red | R | Harf bekleniyordu |
| q2 | OTHER | q_red | R | Küçük harf / geçersiz |
| q2 | BLANK | q_red | R | Eksik girdi |
| q3 | UPPER | q4 | R | İkinci büyük harf okundu |
| q3 | DIGIT | q_red | R | Harf bekleniyordu |
| q3 | OTHER | q_red | R | Geçersiz sembol |
| q3 | BLANK | q_red | R | Eksik girdi |
| q4 | DIGIT | q5 | R | Üçüncü blok — 1. rakam |
| q4 | UPPER | q_red | R | Rakam bekleniyordu |
| q4 | OTHER | q_red | R | Geçersiz sembol |
| q4 | BLANK | q_red | R | Eksik girdi |
| q5 | DIGIT | q6 | R | 2. rakam |
| q5 | UPPER | q_red | R | Rakam bekleniyordu |
| q5 | OTHER | q_red | R | Geçersiz sembol |
| q5 | BLANK | q_red | R | Eksik girdi |
| q6 | DIGIT | q7 | R | 3. rakam |
| q6 | UPPER | q_red | R | Rakam bekleniyordu |
| q6 | OTHER | q_red | R | Geçersiz sembol |
| q6 | BLANK | q_red | R | Eksik girdi |
| q7 | BLANK | q_accept | S | Tam 7 karakter sonrası kabul |
| q7 | DIGIT | q_red | R | Fazladan karakter |
| q7 | UPPER | q_red | R | Fazladan karakter |
| q7 | OTHER | q_red | R | Fazladan / geçersiz karakter |

**Kabul durumu:** `q_accept` → çıktı: `KABUL`  
**Red durumu:** `q_red` → çıktı: `RED`  
**Başlangıç durumu:** `q0`

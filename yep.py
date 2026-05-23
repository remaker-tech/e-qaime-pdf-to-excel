import pdfplumber
import re
import pandas as pd
import os

PDF_QOVLUQ = "./pdf"
EXCEL_ADI = "qaime_reyestri.xlsx"

data = []

for file in os.listdir(PDF_QOVLUQ):

    if not file.lower().endswith(".pdf"):
        continue

    path = os.path.join(PDF_QOVLUQ, file)

    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

    # ---------------- QAIME NO ----------------
    qaime_no = ""
    qaime_match = re.search(r'(MT\d{4})\s*(\d{6,})', text)

    if qaime_match:
        qaime_no = qaime_match.group(1) + qaime_match.group(2)

    # ---------------- TARIX ----------------
    tarix = ""
    tarix_match = re.search(r'Tarix:\s*(\d{2}\.\d{2}\.\d{4})', text)

    if tarix_match:
        tarix = tarix_match.group(1)

    # ======================================================
    # 🔥 GÖNDƏRƏN BLOK (FIXED MULTI-LINE)
    # ======================================================
    sender_block = []
    capture = False

    for line in text.split("\n"):

        if "Göndərən" in line:
            capture = True

        if capture:
            sender_block.append(line)

        if "Qəbul edən" in line:
            break

    sender_text = " ".join(sender_block)

    # ---------------- VOEN ----------------
    voen = ""
    voen_match = re.search(r'\b\d(?:\s*\d){9}\b', sender_text)

    if voen_match:
        voen = re.sub(r"\s+", "", voen_match.group())

    # ---------------- SUBKONTRAGENT ----------------
    subkontragent = ""
    name_match = re.search(
        r'"([^"]+)"\s*(MƏHDUD MƏSULİYYƏTLİ CƏMİYYƏTİ)?',
        sender_text
    )

    if name_match:
        subkontragent = name_match.group(1)

    # ======================================================
    # 🔥 CƏMİ SƏTRİ (STABLE VERSION)
    # ======================================================
    cem_line = ""

    for line in text.split("\n"):

        temiz = line.strip()

        if re.search(r'\bCəmi\b', temiz):

            nums = re.findall(r'\d+(?:[\.,]\d+)?', temiz)

            if len(nums) >= 3 and "Yekun" not in temiz:
                cem_line = temiz

    # ---------------- RƏQƏMLƏR ----------------
    esas = yekun = edv = 0.0

    if cem_line:

        nums = re.findall(r'\d+(?:[\.,]\d+)?', cem_line)
        nums = [float(x.replace(",", ".")) for x in nums]

        print("\nFILE:", file)
        print("CEM LINE:", cem_line)
        print("NUMS:", nums)

        esas = nums[0]
        yekun = nums[-1]
        edv = round(yekun - esas, 2)

    # ---------------- FALLBACK ----------------
    if yekun == 0:

        yekun_match = re.search(r'Yekun məbləğ\s*([\d\.,]+)', text)

        if yekun_match:
            yekun = float(yekun_match.group(1).replace(",", "."))

    if esas == 0 and yekun > 0:
        esas = round(yekun - edv, 2)

    # ---------------- ROUND ----------------
    esas = round(esas, 2)
    yekun = round(yekun, 2)
    edv = round(edv, 2)

    # ---------------- DATA ----------------
    data.append([
        qaime_no,
        voen,
        subkontragent,
        tarix,
        yekun,
        edv,
        esas
    ])

# ---------------- EXCEL ----------------
df = pd.DataFrame(data, columns=[
    "qaime no",
    "VOEN",
    "subkontragent adı",
    "tarix",
    "yekun cəm",
    "ƏDV",
    "əsas məbləğ"
])

df.to_excel(EXCEL_ADI, index=False)

print("\nHazırdır:", EXCEL_ADI)
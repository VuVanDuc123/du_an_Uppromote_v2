# Script ghép dữ liệu vào app-v3.js
# Đọc data.txt, khớp theo myshopify_domain, cập nhật dự án đã có
# và TỰ THÊM dự án hoàn toàn mới (domain chưa từng có trong allData)
import json

with open('app-v3.js', encoding='utf-8') as f:
    first_line = f.readline()
    rest = f.read()

start = first_line.index('[')
end = first_line.rindex(']') + 1
prefix = first_line[:start]
data = json.loads(first_line[start:end])

existing_domains = {it.get('myshopify_domain') for it in data}
max_id = max(it['id'] for it in data)

with open('data.txt', encoding='utf-8') as f:
    content = f.read()

decoder = json.JSONDecoder()
pos = 0
blocks = []
while pos < len(content):
    while pos < len(content) and content[pos] in ' \t\n\r':
        pos += 1
    if pos >= len(content):
        break
    obj, end2 = decoder.raw_decode(content, pos)
    blocks.append(obj)
    pos = end2

print('So khoi JSON trong data.txt:', len(blocks))
items = []
for b in blocks:
    items.extend(b['data']['data'])

merged = {}
raw_new_items = {}
for it in items:
    domain = it.get('myshopify_domain')
    if not domain:
        continue
    m = merged.setdefault(domain, {})
    m['is_recommended'] = True
    if it.get('recommend_score') is not None:
        m['recommend_score'] = round(it['recommend_score'], 2)
    if it.get('offer_score') is not None:
        m['offer_score'] = round(it['offer_score'], 2)
    if it.get('total_order_last_seven_day') is not None:
        m['total_order_last_seven_day'] = it['total_order_last_seven_day']
    if it.get('approval_rate') is not None:
        m['approval_rate'] = round(it['approval_rate'], 2)
    if it.get('enable_coupon') is not None:
        m['enable_coupon'] = bool(it['enable_coupon'])
    raw_new_items[domain] = it

print('So du an trong data.txt:', len(merged))

matched = 0
new_matched = 0
for item in data:
    domain = item.get('myshopify_domain')
    if domain in merged:
        was_new = 'recommend_score' not in item
        item.update(merged[domain])
        matched += 1
        if was_new:
            new_matched += 1
        del merged[domain]

print('Da cap nhat du an co san:', matched)
print('Trong do la du an moi co du lieu:', new_matched)

added = 0
for domain, extra in merged.items():
    raw = raw_new_items[domain]
    max_id += 1
    new_item = {
        'id': max_id,
        'name': raw.get('name', ''),
        'logo': raw.get('logo'),
        'myshopify_domain': domain,
        'payout_rate': raw.get('payout_rate', ''),
        'currency': raw.get('currency', ''),
        'symbol_currency': raw.get('symbol_currency', ''),
        'commission': raw.get('commission', ''),
        'cookie': raw.get('cookie', 0),
        'payout_period': raw.get('payout_period'),
        'application_review': raw.get('application_review', ''),
        'apply_url': raw.get('apply_url', ''),
        'target_audience_locations': raw.get('target_audience_locations', []),
        'target_audience_genders': raw.get('target_audience_genders', []),
        'status': 1,
        'payment_method_check': 1,
    }
    new_item.update(extra)
    data.append(new_item)
    added += 1

print('Du an HOAN TOAN MOI duoc them:', added)

new_array = json.dumps(data, ensure_ascii=False)
new_first_line = prefix + new_array + ';\n'

with open('app-v3.js', 'w', encoding='utf-8', newline='') as f:
    f.write(new_first_line)
    f.write(rest)
print('Done. Tong so du an:', len(data))

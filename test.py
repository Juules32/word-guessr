from vercel_kv import KV

kv = KV()
print(kv.has_auth())
print(kv.set("sss", "asasd"))
print(kv.get("sss"))
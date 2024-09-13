from vercel_kv import KV

kv = KV()
print(kv.set("test", "test local redis"))
print(kv.get("test"))

# Format pliku magazynu (data/magazyn.json)

```json
{
  "items": [
    {"id": "S-001", "name": "Śruba M8", "qty": 100, "unit": "szt", "location": "A1"},
    {"id": "F-010", "name": "Filtr",   "qty": 2,   "unit": "szt", "location": "B2"}
  ]
}
```

- `id` (string, wymagane, unikalne)
- `name` (string, wymagane)
- `qty` (number >= 0, wymagane)
- `unit` (string, wymagane)
- `location` (string, opcjonalne)

Uprawnienia: zapisu dokonują role **admin/magazynier**. Rola **brygadzista** nie ma dostępu do zapisu.

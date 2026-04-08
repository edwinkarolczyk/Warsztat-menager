# Indeks narzędzi

Moduł *Narzędzia* może korzystać z pliku indeksowego:

- `data/narzedzia/narzedzia.json` – pełny indeks (pole `"narzedzia": [...]`),
- `data/tools_index.json` – indeks skrócony (opcjonalny).

Importer z Excela tworzy pliki `data/narzedzia/*.json`. Jeśli UI nadal czyta
tylko indeks – uruchom:

```
tools\importers\run_build_tools_index.bat
```

Plik `narzedzia.json` ma strukturę:
```json
{
  "narzedzia": [ { ... }, { ... } ]
}
```

To ułatwia przejściowy okres, gdy część funkcji oczekuje jednego pliku,
a część czyta pliki jednostkowe.

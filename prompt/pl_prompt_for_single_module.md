# Prompt Template for Generating Polarion API Module Classes

## How to use this template:
Replace `[MODULE_NAME]` with the desired module name (e.g., "Projects", "Test Runs", "Documents", etc.)

---

## PROMPT:

```
Potrzebuję utworzyć klasę Pythona dla modułu **[MODULE_NAME]** w Polarion REST API, zgodnie z tą samą strukturą i wzorcem, który został użyty dla modułu "Work Items".

### Kontekst:
- Mam plik openapi.json w lokalizacji: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/data/openapi.json`
- Istnieje klasa bazowa PolarionBase w: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/modules/base.py`
- Główna klasa PolarionRestApi w: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/polarion_api.py`
- Wzorcowa klasa WorkItems w: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/modules/work_items.py`

### Zadania do wykonania:

1. **Analiza openapi.json**:
   - Znajdź wszystkie endpointy związane z kategorią **[MODULE_NAME]** w pliku openapi.json
   - Zidentyfikuj ich tagowanie (pole "tags" w każdym endpoincie)
   - Policz liczbę endpointów dla tej kategorii (podzielonych na DELETE, GET, PATCH, POST)

2. **Utworzenie nowej klasy**:
   - Utwórz nowy plik: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/modules/[module_name_snake_case].py`
   - Nazwa klasy: `[ModuleNamePascalCase]`
   - Klasa musi dziedziczyć po `PolarionBase`

3. **Struktura klasy**:
   - Dodaj docstring opisujący moduł i jego funkcjonalność
   - Zorganizuj metody według typu HTTP w kolejności: DELETE, GET, PATCH, POST (zgodnie ze Swaggerem)
   - Każda sekcja powinna być oddzielona komentarzem: `# ========== [METHOD] methods ==========`

4. **Wymagania dla metod**:
   - Każda metoda musi odpowiadać konkretnemu endpointowi z openapi.json
   - Nazwa metody powinna być w formacie snake_case i opisywać operację (np. `get_project`, `create_project`, `delete_project`)
   - Parametry metody muszą odpowiadać parametrom z openapi.json (path parameters, query parameters, request body)
   - Wszystkie parametry opcjonalne powinny mieć `Optional[]` type hint i wartość domyślną `None`
   - Request body powinien być typu `Dict[str, Any]`
   - Każda metoda powinna zwracać `requests.Response`
   - Dodaj docstring z opisem, argumentami (Args:) i zwracaną wartością (Returns:)

5. **Implementacja metod**:
   - Użyj metod z klasy bazowej: `self._get()`, `self._post()`, `self._patch()`, `self._delete()`
   - Dla DELETE z body użyj helpera `self._delete_with_body()` (lub stwórz go jeśli nie istnieje)
   - Parametry query przekazuj jako dict w `params=`
   - Request body przekazuj jako dict w `json=`
   - Zbuduj poprawną ścieżkę endpoint używając f-stringów dla path parameters

6. **Weryfikacja**:
   - Sprawdź, czy liczba metod w klasie odpowiada liczbie endpointów w openapi.json dla tej kategorii
   - Sprawdź, czy kolejność metod odpowiada kolejności w dokumentacji Swagger
   - Upewnij się, że wszystkie parametry z openapi.json są uwzględnione

7. **Integracja z PolarionRestApi**:
   - Upewnij się, że nowa klasa zostanie automatycznie załadowana przez `PolarionRestApi.load_modules()`
   - Nie trzeba modyfikować polarion_api.py - powinno działać automatycznie

### Format odpowiedzi:
1. Najpierw przeanalizuj openapi.json i wypisz znalezione endpointy dla **[MODULE_NAME]**
2. Pokaż podsumowanie: ile endpointów każdego typu (DELETE, GET, PATCH, POST)
3. Stwórz plik z klasą
4. Zweryfikuj poprawność (liczba metod vs liczba endpointów)

### Ważne zasady:
- Wszystkie ścieżki endpointów z openapi.json są względne do base_url (usuń początkowy `/api` jeśli występuje)
- Zachowaj spójność nazewnictwa z innymi modułami
- Kod musi być czytelny, z odpowiednimi type hints i docstrings
- Metody powinny być w dokładnie tej samej kolejności co w dokumentacji Swagger
```

---

## Example usage:

### For "Projects" module:
Replace `[MODULE_NAME]` with **"Projects"**

### For "Test Runs" module:
Replace `[MODULE_NAME]` with **"Test Runs"**

### For "Documents" module:
Replace `[MODULE_NAME]` with **"Documents"**

---

## Quick Reference - Available Modules in openapi.json:
To check available modules/categories, look for unique values in the "tags" field across all endpoints in openapi.json.

Common categories might include:
- Projects
- Test Runs
- Documents
- Plans
- Users
- Baselines
- Revisions
- etc.

Use semantic search or grep to find: `"tags"` in openapi.json to see all available categories.

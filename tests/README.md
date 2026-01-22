# Testovi za LLM Client

Ovaj direktorijum sadrži testove za LLM klijent.

## Struktura Testova

- `test_response.py` - Testovi za data klase (TextDelta, EventType, TokenUsage, StreamEvent)
- `test_client.py` - Testovi za LLMClient klasu i njene metode

## Pokretanje Testova

### Instalacija zavisnosti

```bash
pip install pytest pytest-asyncio pytest-cov
```

ili koristeći pyproject.toml:

```bash
pip install -e ".[test]"
```

### Pokretanje svih testova

```bash
pytest tests/
```

### Pokretanje sa detaljnim izlazom

```bash
pytest tests/ -v
```

### Pokretanje sa pokrićem koda (coverage)

```bash
pytest tests/ --cov=client --cov-report=html
```

Ovo će generisati HTML izveštaj u `htmlcov/` direktorijumu.

## Test Klase

### TestLLMClient
Testira osnovnu funkcionalnost LLMClient klase:
- Inicijalizaciju
- Kreiranje klijenta (singleton pattern)
- Prosleđivanje parametara
- Zatvaranje klijenta

### TestChatCompletion
Testira `chat_completition` metod:
- Non-streaming mod
- Prosleđivanje parametara API-u
- Handler za prazan content
- Handler za nedostajući usage

### TestNonStreamResponse
Testira `_non_stream_response` metod:
- Vraćanje ispravnog StreamEvent objekta

### TestTextDelta
Testira TextDelta klasu:
- Kreiranje objekta
- String reprezentaciju

### TestEventType
Testira EventType enum:
- Vrednosti enum-a

### TestTokenUsage
Testira TokenUsage klasu:
- Kreiranje objekta
- Default vrednosti
- Sabiranje objekata

### TestStreamEvent
Testira StreamEvent klasu:
- Kreiranje objekta
- Kreiranje sa svim poljima
- Error scenario

## Mockovanje

Testovi koriste `unittest.mock` biblioteku za mockovanje:
- `AsyncMock` - za asinhrone funkcije
- `MagicMock` - za obične objekte
- `patch` - za zamenjivanje modula

## Pokrivenost koda

Trenutna pokrivenost: ~100% za core funkcionalnost

Da biste videli detaljnu pokrivenost:

```bash
pytest tests/ --cov=client --cov-report=term-missing

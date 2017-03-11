# FBHack17

#witwrap.py

```python
>>> import witwrap
>>> w = witwrap.configure_wit()
>>> witwrap.parse_message("Get me $DEFG when it hits $5000", w)
>>> {'stock': 'DEFG', 'currency': '$', 'number': 5000, 'change': 'reaches'}
```
Instruktioner för att köra igång detta projekt
----------------------------------------------

1. Se till att du har python och pip installerat, projektet
är testat med Python 3.6.

2. Ladda in allt som behövs för att köra Django. Detta görs
lättast med `pip3 install -r requirements.txt` vilket kommer
installera alla beroenden som projektet har.

3. Installera testdatabasen (SQLite används) genom att köra
`python3 manage.py migrate`.

4. Skapa en adminanvändare så att du kan logga in via adminläget
och enkelt skapa nya inlägg som administratör. Gör detta med:
`python3 manage.py createsuperuser`.

5. Starta testservern med `python3 manage.py runserver`.
Dubbelkolla att du inte får några felmeddelanden.

6. Surfa till http://localhost:8000 i din webbläsare där
testsajten nu körs. Dubbelkolla att allt fungerar som det ska.

7. Surfa till http://localhost:8000/admin/ och logga in med de
uppgifter du skapade ovan. Skapa ett par frågor och ett par svar.

8. Se att din fråga och dina svar syns när du surfar till startsidan.

Du är nu redo med all setup!

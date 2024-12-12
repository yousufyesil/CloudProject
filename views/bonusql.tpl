<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bibliotheksverwaltung</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;3
            display: flex;
            flex-direction: column;
            background-color: #f5f5f5;
        }

        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            text-align: center;
        }

        main {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            padding: 2rem;
        }

        .button {
            padding: 2rem 3rem;
            font-size: 1.5rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }

        .button:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .add-button {
            background-color: #27ae60;
            color: white;
        }

        .search-button {
            background-color: #2980b9;
            color: white;
        }

        .icon {
            font-size: 2.5rem;
        }

        footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 1rem;
            margin-top: auto;
        }
    </style>
</head>
<body>
    <header>
        <h1>Bibliotheksverwaltung</h1>
    </header>

    <main>
        <a href="/add" class="button add-button">
            <span class="icon">+</span>
            <span>Item hinzufügen</span>
        </a>
        <a href="/search" class="button search-button">
            <span class="icon">🔍</span>
            <span>Item suchen</span>
        </a>
    </main>

    <footer>
        <p>&copy; 2024 Bibliotheksverwaltung</p>
    </footer>
</body>
</html>
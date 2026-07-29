import requests

# Запрос к API Shikimori для получения списка аниме
url = "https://shikimori.one/api/animes?limit=24&order=popularity"
headers = {'User-Agent': 'MyAnimeSiteApp'}

response = requests.get(url, headers=headers)
anime_list = response.json()

# Шаблон HTML-страницы
html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мой Аниме Сайт</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #141414; color: #fff; margin: 0; padding: 0; }
        header { display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: #1f1f1f; border-bottom: 2px solid #2c2c2c; }
        .logo { font-size: 24px; font-weight: bold; color: #ff7f50; }
        header input { padding: 8px 15px; width: 250px; border-radius: 4px; border: 1px solid #444; background-color: #2a2a2a; color: #fff; }
        main { padding: 30px; }
        .anime-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; margin-top: 20px; }
        .anime-card { background-color: #1f1f1f; border-radius: 8px; overflow: hidden; cursor: pointer; transition: transform 0.2s; }
        .anime-card:hover { transform: scale(1.05); }
        .anime-card img { width: 100%; height: 260px; object-fit: cover; }
        .anime-card h3 { font-size: 14px; padding: 10px; margin: 0; text-align: center; }
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8); }
        .modal-content { background-color: #1f1f1f; margin: 5% auto; padding: 20px; width: 80%; max-width: 900px; border-radius: 8px; position: relative; }
        .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close:hover { color: #fff; }
        .video-container { position: relative; padding-bottom: 56.25%; height: 0; margin-top: 15px; }
        .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 4px; }
    </style>
</head>
<body>

    <header>
        <div class="logo">🎬 MyAnime</div>
        <input type="text" id="search" placeholder="Поиск аниме..." onkeyup="searchAnime()">
    </header>

    <main>
        <h1>Популярное аниме</h1>
        <div class="anime-grid" id="anime-container">
"""

# Генерируем карточки аниме на основе данных от API
for anime in anime_list:
    title = anime.get('russian') or anime.get('name')
    # Используем официальный домен картинок Shikimori
    image_url = "https://shikimori.one" + anime['image']['original']
    
    # В качестве примера плеера используем плеер Kodik по ID аниме (или можно оставлять заглушку)
    # Для полноценного просмотра без рекламы сюда можно подставлять нужные ссылки на видеоплееры
    player_url = f"https://kodik.info/find-by-shikimori/{anime['id']}"

    html_content += f"""
            <div class="anime-card" onclick="openPlayer('{player_url}', '{title}')">
                <img src="{image_url}" alt="{title}">
                <h3>{title}</h3>
            </div>
    """

html_content += """
        </div>
    </main>

    <div id="player-modal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closePlayer()">&times;</span>
            <h2 id="modal-title">Просмотр</h2>
            <div class="video-container">
                <iframe id="anime-player" src="" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
    </div>

    <script>
        function openPlayer(url, title) {
            document.getElementById('modal-title').innerText = title;
            document.getElementById('anime-player').src = url;
            document.getElementById('player-modal').style.display = 'block';
        }

        function closePlayer() {
            document.getElementById('modal-title').innerText = 'Просмотр';
            document.getElementById('anime-player').src = '';
            document.getElementById('player-modal').style.display = 'none';
        }

        function searchAnime() {
            let input = document.getElementById('search').value.toLowerCase();
            let cards = document.getElementsByClassName('anime-card');
            for (let i = 0; i < cards.length; i++) {
                let title = cards[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
                cards[i].style.display = title.includes(input) ? '' : 'none';
            }
        }
    </script>
</body>
</html>
"""

# Сохраняем результат в файл index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Файл index.html успешно сгенерирован!")
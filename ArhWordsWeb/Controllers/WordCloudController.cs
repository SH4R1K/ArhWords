using ArhWordsWeb.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using System.Text;
using System.Text.Json;

namespace ArhWordsWeb.Controllers
{
    public class WordCloudController : Controller
    {
        private readonly IHttpClientFactory _httpClientFactory;

        public WordCloudController(IHttpClientFactory httpClientFactory)
        {
            _httpClientFactory = httpClientFactory;
        }

        public async Task<IActionResult> GenerateImage()
        {
            var themes = new List<SelectListItem>
        {
            new SelectListItem { Value = "black", Text = "Темная" },
            new SelectListItem { Value = "white", Text = "Светлая" }
        };

            var colorMaps = new List<SelectListItem>
        {
            new SelectListItem { Value = "Wisteria", Text = "Вистерия" },
            new SelectListItem { Value = "Reds", Text = "Красные" },
            new SelectListItem { Value = "afmhot", Text = "Теплый" },
            new SelectListItem { Value = "Purples", Text = "Пурпурные" },
            new SelectListItem { Value = "RdPu", Text = "Розовые" },
            new SelectListItem { Value = "gnuplot", Text = "График" },
            new SelectListItem { Value = "PRGn", Text = "Пурпурно-зеленый" },
            new SelectListItem { Value = "Greens", Text = "Зеленые" },
            new SelectListItem { Value = "Blues", Text = "Синие" },
            new SelectListItem { Value = "RdBu", Text = "Красно-синие" },
            new SelectListItem { Value = "Greys", Text = "Серые" },
            new SelectListItem { Value = "cool", Text = "Прохладный" },
            new SelectListItem { Value = "Dark2", Text = "Темный 2" },
            new SelectListItem { Value = "brg", Text = "BRG" },
            new SelectListItem { Value = "winter", Text = "Зима" },
            new SelectListItem { Value = "spring", Text = "Весна" },
            new SelectListItem { Value = "plasma", Text = "Плазма" },
            new SelectListItem { Value = "magma", Text = "Магма" },
            new SelectListItem { Value = "hot", Text = "Горячий" }
        };

            ViewBag.Themes = themes;
            ViewBag.ColorMaps = colorMaps;
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> GenerateImage([Bind("MaxWords,MinFontSize,MaxFontSize,Theme, ColorMap, Text")] WordCloud wordCloud)
        {
            var themes = new List<SelectListItem>
        {
            new SelectListItem { Value = "black", Text = "Темная" },
            new SelectListItem { Value = "white", Text = "Светлая" }
        };

            var colorMaps = new List<SelectListItem>
        {
            new SelectListItem { Value = "Wisteria", Text = "Вистерия" },
            new SelectListItem { Value = "Reds", Text = "Красные" },
            new SelectListItem { Value = "afmhot", Text = "Теплый" },
            new SelectListItem { Value = "Purples", Text = "Пурпурные" },
            new SelectListItem { Value = "RdPu", Text = "Розовые" },
            new SelectListItem { Value = "gnuplot", Text = "График" },
            new SelectListItem { Value = "PRGn", Text = "Пурпурно-зеленый" },
            new SelectListItem { Value = "Greens", Text = "Зеленые" },
            new SelectListItem { Value = "Blues", Text = "Синие" },
            new SelectListItem { Value = "RdBu", Text = "Красно-синие" },
            new SelectListItem { Value = "Greys", Text = "Серые" },
            new SelectListItem { Value = "cool", Text = "Прохладный" },
            new SelectListItem { Value = "Dark2", Text = "Темный 2" },
            new SelectListItem { Value = "brg", Text = "BRG" },
            new SelectListItem { Value = "winter", Text = "Зима" },
            new SelectListItem { Value = "spring", Text = "Весна" },
            new SelectListItem { Value = "plasma", Text = "Плазма" },
            new SelectListItem { Value = "magma", Text = "Магма" },
            new SelectListItem { Value = "hot", Text = "Горячий" }
        };

            ViewBag.Themes = themes;
            ViewBag.ColorMaps = colorMaps;
            using (var httpClient = _httpClientFactory.CreateClient())
            {
                // Создаем объект с параметрами
                var requestBody = new
                {
                    max_words = wordCloud.MaxWords,
                    colormap = wordCloud.ColorMap,
                    text = wordCloud.Text, // Используем переданный текст
                    min_font_size = wordCloud.MinFontSize,
                    max_font_size = wordCloud.MaxFontSize,
                    theme = wordCloud.Theme
                };

                // Сериализуем объект в JSON
                var json = JsonSerializer.Serialize(requestBody);

                var httpRequestMessage = new HttpRequestMessage(HttpMethod.Post, "http://127.0.0.1:3000/wordCloud")
                {
                    Content = new StringContent(json, Encoding.UTF8, "application/json") // Указываем тип контента
                };

                var response = await httpClient.SendAsync(httpRequestMessage);

                if (response.IsSuccessStatusCode)
                {
                    var imageBytes = await response.Content.ReadAsByteArrayAsync();
                    var base64Image = Convert.ToBase64String(imageBytes);
                    var imageDataUrl = $"data:image/png;base64,{base64Image}"; // Предполагаем, что изображение в формате PNG

                    ViewBag.ImageDataUrl = imageDataUrl; // Передаем URL изображения в ViewBag
                }
                else
                {
                    // Обработка ошибок
                    ViewBag.ErrorMessage = "Ошибка при получении изображения.";
                }
            }

            return View();
        }
    }
}

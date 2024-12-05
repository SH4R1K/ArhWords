namespace ArhWordsWeb.Models
{
    public class WordCloud
    {
        public int MaxWords { get; set; } = 100;
        public int MinFontSize { get; set; } = 4;
        public int? MaxFontSize { get; set; } = null;
        public string Theme { get; set; } = "black";
        public string? ColorMap { get; set; }
        public required string Text { get; set; }
    }
}

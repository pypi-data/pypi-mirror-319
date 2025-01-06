# Markdown İmporter 📝

Bu araç, markdown dosyalarınızı modüler bir şekilde yönetmenizi sağlar. Markdown dosyalarınızı parçalara ayırıp, ana dosyanızda import edebilirsiniz.

## 🚀 Özellikler

- Markdown dosyalarını modüler hale getirme
- Çoklu dil desteği (Türkçe/İngilizce)
- Eksik dosya kontrolü ve bildirimi
- Esnek import sözdizimi
- Otomatik senkronizasyon

## 🛠️ Kullanım

1. Import etmek istediğiniz dosyayı belirtin:
```markdown
<!-- @import "docs/api/auth/readme.md" -->
```

2. Scripti çalıştırın:
```bash
python _markdown_sync.py
```

3. Script otomatik olarak:
   - İmport edilen dosyaları bulur
   - İçerikleri ana dosyaya ekler
   - Eksik dosyaları bildirir
   - Sonuç dosyasını oluşturur

## ⚙️ Yapılandırma

```python
markdown_sync = MarkdownSync(
    editor_file="README.editor.md",    # Kaynak dosya
    github_file="README.github.md",    # Hedef dosya
    base_dir=".",                      # Temel dizin
    language=Language.TURKISH          # Dil seçeneği
)
```

## 🌍 Dil Desteği

- 🇹🇷 Türkçe (`Language.TURKISH`)
- 🇬🇧 İngilizce (`Language.ENGLISH`)

## ⚠️ Hata Yönetimi

- Eksik dosyalar `[Missing File]` olarak işaretlenir
- Her hata detaylı olarak raporlanır
- İşlem sonucu özeti sunulur

---

# Markdown Importer 📝

This tool allows you to manage your markdown files in a modular way. You can split your markdown files into pieces and import them into your main file.

## 🚀 Features

- Modular markdown file management
- Multi-language support (Turkish/English)
- Missing file checks and notifications
- Flexible import syntax
- Automatic synchronization

## 🛠️ Usage

1. Specify the file you want to import:
```markdown
<!-- @import "docs/api/auth/readme.md" -->
```

2. Run the script:
```bash
python _markdown_sync.py
```

3. The script automatically:
   - Finds imported files
   - Adds contents to main file
   - Reports missing files
   - Creates result file

## ⚙️ Configuration

```python
markdown_sync = MarkdownSync(
    editor_file="README.editor.md",    # Source file
    github_file="README.github.md",    # Target file
    base_dir=".",                      # Base directory
    language=Language.ENGLISH          # Language option
)
```

## 🌍 Language Support

- 🇹🇷 Turkish (`Language.TURKISH`)
- 🇬🇧 English (`Language.ENGLISH`)

## ⚠️ Error Handling

- Missing files are marked as `[Missing File]`
- Each error is reported in detail
- Summary of process result is provided

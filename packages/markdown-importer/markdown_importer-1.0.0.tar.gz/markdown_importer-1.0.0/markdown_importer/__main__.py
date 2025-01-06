import re
import os
import sys
import argparse
from typing import Tuple, List, Optional, Dict
from enum import Enum

class Language(Enum):
    """
    Desteklenen diller için enum sınıfı
    """
    TURKISH = "tr"
    ENGLISH = "en"

class LanguageManager:
    """
    Çoklu dil desteği için mesaj yöneticisi
    """
    
    MESSAGES: Dict[Language, Dict[str, str]] = {
        Language.TURKISH: {
            "source_read_error": "❌ Kaynak dosya okuma hatası: {error}",
            "target_write_error": "❌ Hedef dosya yazma hatası: {error}",
            "import_read_error": "❌ Import dosyası okuma hatası: {error}",
            "missing_file_warning": "⚠️ Uyarı: {file} dosyası bulunamadı! Import satırı [Missing File] olarak işaretlendi.",
            "process_completed_with_missing": "\n⚠️ İşlem tamamlandı ancak bazı dosyalar bulunamadı:",
            "missing_file_list_item": "  - {file}",
            "process_completed_success": "✅ {file} dosyasındaki tüm içerikler başarıyla aktarıldı.",
            "general_error": "❌ Hata oluştu: {error}",
            "imported_file_success": "✅ {file} dosyası başarıyla aktarıldı."
        },
        Language.ENGLISH: {
            "source_read_error": "❌ Source file read error: {error}",
            "target_write_error": "❌ Target file write error: {error}",
            "import_read_error": "❌ Import file read error: {error}",
            "missing_file_warning": "⚠️ Warning: File {file} not found! Import line marked as [Missing File].",
            "process_completed_with_missing": "\n⚠️ Process completed but some files were not found:",
            "missing_file_list_item": "  - {file}",
            "process_completed_success": "✅ All contents from {file} were successfully transferred.",
            "general_error": "❌ Error occurred: {error}",
            "imported_file_success": "✅ {file} was successfully transferred."
        }
    }
    
    def __init__(self, language: Language = Language.TURKISH):
        """
        Dil yöneticisi yapıcı metodu
        
        Args:
            language (Language): Kullanılacak dil
        """
        self.language = language
        
    def getMessage(self, key: str, **kwargs) -> str:
        """
        Belirtilen anahtara ait mesajı döndürür
        
        Args:
            key (str): Mesaj anahtarı
            **kwargs: Format parametreleri
            
        Returns:
            str: Formatlanmış mesaj
        """
        message = self.MESSAGES[self.language].get(key, "")
        return message.format(**kwargs) if message else ""

class MarkdownSync:
    """
    Markdown dosyalarını senkronize eden ve import direktiflerini işleyen sınıf
    """
    
    def __init__(self, editor_file: str = "README.editor.md", 
                 github_file: str = "README.github.md",
                 base_dir: str = ".",
                 language: Language = Language.TURKISH):
        """
        MarkdownSync sınıfının yapıcı metodu
        
        Args:
            editor_file (str): Kaynak markdown dosyası
            github_file (str): Hedef markdown dosyası
            base_dir (str): Temel dizin yolu
            language (Language): Kullanılacak dil
        """
        self.editor_file = editor_file
        self.github_file = github_file
        self.base_dir = base_dir
        self.import_pattern = r'<!--\s+@import\s+"(.*?)"\s*(?!\s*\[Missing File\])\s*-->'
        self.lang_manager = LanguageManager(language)
        
    def readSourceFile(self) -> str:
        """
        Kaynak markdown dosyasını okur
        
        Returns:
            str: Dosya içeriği
        """
        try:
            with open(self.editor_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(self.lang_manager.getMessage("source_read_error", error=str(e)))
            raise
            
    def writeTargetFile(self, content: str) -> None:
        """
        Hedef markdown dosyasını yazar
        
        Args:
            content (str): Yazılacak içerik
        """
        try:
            with open(self.github_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(self.lang_manager.getMessage("target_write_error", error=str(e)))
            raise
            
    def hasImports(self, content: str) -> bool:
        """
        İçerikte import direktifi olup olmadığını kontrol eder
        
        Args:
            content (str): Kontrol edilecek içerik
            
        Returns:
            bool: Import direktifi varsa True
        """
        return bool(re.search(self.import_pattern, content))
        
    def readImportedFile(self, file_path: str, base_dir: str) -> Tuple[str, bool]:
        """
        Import edilecek dosyayı okur
        
        Args:
            file_path (str): Dosya yolu
            base_dir (str): Temel dizin
            
        Returns:
            Tuple[str, bool]: Dosya içeriği ve başarı durumu
        """
        abs_path = os.path.join(base_dir, file_path)
        try:
            if os.path.exists(abs_path):
                with open(abs_path, 'r', encoding='utf-8') as f:
                    return f.read(), True
            return "", False
        except Exception as e:
            print(self.lang_manager.getMessage("import_read_error", error=str(e)))
            return "", False
            
    def handleMissingFile(self, file_path: str) -> str:
        """
        Bulunamayan dosya için import satırını düzenler
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            str: Düzenlenmiş import satırı
        """
        print(self.lang_manager.getMessage("missing_file_warning", file=file_path))
        return f'<!-- @import "{file_path}" [Missing File] -->'
        
    def processImports(self, content: str, base_dir: str) -> Tuple[str, List[str]]:
        """
        Markdown içeriğindeki import direktifelerini işler
        
        Args:
            content (str): İşlenecek markdown içeriği
            base_dir (str): Proje kök dizini
            
        Returns:
            Tuple[str, List[str]]: İşlenmiş içerik ve bulunamayan dosyalar listesi
        """
        missing_files = []
        
        if not self.hasImports(content):
            return content, missing_files
            
        for match in re.finditer(self.import_pattern, content):
            file_path = match.group(1)
            imported_content, success = self.readImportedFile(file_path, base_dir)
            
            if success:
                print(self.lang_manager.getMessage("imported_file_success", file=file_path))
                content = content.replace(match.group(0), imported_content)
            else:
                new_import = self.handleMissingFile(file_path)
                content = content.replace(match.group(0), new_import)
                missing_files.append(file_path)
        
        return content, missing_files
        
    def printResults(self, missing_files: List[str]) -> None:
        """
        İşlem sonuçlarını ekrana yazdırır
        
        Args:
            missing_files (List[str]): Bulunamayan dosyalar listesi
        """
        if missing_files:
            print(self.lang_manager.getMessage("process_completed_with_missing"))
            for file in missing_files:
                print(self.lang_manager.getMessage("missing_file_list_item", file=file))
        else:
            print(self.lang_manager.getMessage("process_completed_success", file=self.editor_file))
        
    def syncMarkdownFiles(self, base_dir: Optional[str] = None) -> bool:
        """
        README.editor.md dosyasındaki import direktifelerini işleyerek README.md oluşturur
        
        Algoritma Akışı:
        1. Kaynak dosyayı oku
        2. Import direktiflerini işle
           2.1. Import edilecek dosyaları bul
           2.2. Dosyaları oku ve içeriği yerleştir
           2.3. Bulunamayan dosyaları işaretle
        3. Sonuç dosyasını oluştur
        4. Sonuçları raporla
        
        Args:
            base_dir (Optional[str]): Temel dizin yolu. None ise mevcut dizin kullanılır.
            
        Returns:
            bool: İşlemin başarılı olup olmadığı
        """
        try:
            if base_dir is None:
                base_dir = self.base_dir
            
            content = self.readSourceFile()
            
            all_missing_files = []
            has_more_imports = True
            
            while has_more_imports:
                content, missing_files = self.processImports(content, base_dir)
                all_missing_files.extend(missing_files)
                has_more_imports = self.hasImports(content)
            
            self.writeTargetFile(content)
            self.printResults(all_missing_files)
            
            return True
            
        except Exception as e:
            print(self.lang_manager.getMessage("general_error", error=str(e)))
            return False

def main():
    """
    Ana çalıştırma fonksiyonu
    """
    # CMD'den çalıştırılıp çalıştırılmadığını kontrol et
    is_cmd = len(sys.argv) > 1
    
    if is_cmd:
        # CMD'den çalıştırılmışsa argümanları işle
        parser = argparse.ArgumentParser(
            description="Markdown dosyalarını modüler bir şekilde yönetmenizi sağlayan araç",
            formatter_class=argparse.RawTextHelpFormatter
        )
        
        parser.add_argument(
            "-e", "--editor-file",
            default="README.editor.md",
            help="Kaynak markdown dosyası (varsayılan: README.editor.md)"
        )
        
        parser.add_argument(
            "-g", "--github-file",
            default="README.github.md",
            help="Hedef markdown dosyası (varsayılan: README.github.md)"
        )
        
        parser.add_argument(
            "-b", "--base-dir",
            default=".",
            help="Temel dizin yolu (varsayılan: .)"
        )
        
        parser.add_argument(
            "-l", "--language",
            choices=["tr", "en"],
            default="tr",
            help="Kullanılacak dil (tr: Türkçe, en: İngilizce) (varsayılan: tr)"
        )
        
        args = parser.parse_args()
        
        # Dil seçeneğini belirle
        language = Language.TURKISH if args.language == "tr" else Language.ENGLISH
        
        # MarkdownSync nesnesini oluştur
        markdown_sync = MarkdownSync(
            editor_file=args.editor_file,
            github_file=args.github_file,
            base_dir=args.base_dir,
            language=language
        )
    else:
        # Doğrudan çalıştırılmışsa varsayılan değerleri kullan
        editor_file = "README.editor.md"
        github_file = "README.github.md"
        base_dir = "."
        language = Language.TURKISH
        
        markdown_sync = MarkdownSync(
            editor_file=editor_file,
            github_file=github_file,
            base_dir=base_dir,
            language=language
        )
    
    # İşlemi başlat
    success = markdown_sync.syncMarkdownFiles()
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 